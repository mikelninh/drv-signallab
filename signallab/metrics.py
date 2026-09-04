from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

import numpy as np
import pandas as pd

from .data import REQUIRED_COLUMNS

BASELINE_START = pd.Timestamp("2025-12-01")
BASELINE_END = pd.Timestamp("2026-05-31")
RECENT_START = pd.Timestamp("2026-06-01")


@dataclass
class Signal:
    id: str
    severity: str
    title: str
    process_type: str
    region: str
    baseline_days: float
    recent_days: float
    change_pct: float
    baseline_n: int
    recent_n: int
    why: str
    boundary: str
    next_step: str

    def as_dict(self) -> dict:
        return asdict(self)


def _periods(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    baseline = df[(df.received_at >= BASELINE_START) & (df.received_at <= BASELINE_END)]
    recent = df[df.received_at >= RECENT_START]
    return baseline, recent


def population_stability_index(expected: Iterable[float], actual: Iterable[float], epsilon: float = 1e-6) -> float:
    exp = np.asarray(list(expected), dtype=float)
    act = np.asarray(list(actual), dtype=float)
    exp = np.clip(exp / max(exp.sum(), epsilon), epsilon, None)
    act = np.clip(act / max(act.sum(), epsilon), epsilon, None)
    return float(np.sum((act - exp) * np.log(act / exp)))


def quality_report(df: pd.DataFrame) -> dict:
    missing = float(df.isna().mean().mean())
    duplicate_rate = float(df.case_id.duplicated().mean()) if "case_id" in df else 1.0
    schema_ok = REQUIRED_COLUMNS.issubset(set(df.columns))
    completeness = 1.0 - missing

    score = 100.0
    score -= min(45.0, missing * 500.0)
    score -= min(25.0, duplicate_rate * 500.0)
    if not schema_ok:
        score -= 30.0

    return {
        "completeness_pct": round(completeness * 100, 2),
        "missing_pct": round(missing * 100, 2),
        "duplicate_pct": round(duplicate_rate * 100, 3),
        "schema_integrity": "PASS" if schema_ok else "FAIL",
        "quality_score": round(max(0.0, score), 1),
    }


def drift_report(df: pd.DataFrame) -> dict:
    baseline, recent = _periods(df)
    categories = ["digital", "postal", "service_center"]
    base_channel = baseline.channel.value_counts(normalize=True).reindex(categories, fill_value=0.0)
    recent_channel = recent.channel.value_counts(normalize=True).reindex(categories, fill_value=0.0)
    channel_psi = population_stability_index(base_channel.values, recent_channel.values)

    base_missing = float(baseline.processing_days.isna().mean())
    recent_missing = float(recent.processing_days.isna().mean())
    missing_delta_pp = (recent_missing - base_missing) * 100.0

    return {
        "channel_psi": round(channel_psi, 3),
        "channel_status": "WARNING" if channel_psi >= 0.25 else "WATCH" if channel_psi >= 0.10 else "PASS",
        "baseline_missing_pct": round(base_missing * 100, 2),
        "recent_missing_pct": round(recent_missing * 100, 2),
        "missing_delta_pp": round(missing_delta_pp, 2),
        "missing_status": "WARNING" if missing_delta_pp >= 1.5 else "PASS",
        "interpretation": "PSI and missingness are change signals only; they do not identify a cause.",
        "next_step": "Inspect source-system and intake changes before retraining or operational action.",
    }


def detect_signals(df: pd.DataFrame) -> list[dict]:
    baseline, recent = _periods(df)
    signals: list[Signal] = []

    groups = df[["process_type", "region"]].drop_duplicates().itertuples(index=False, name=None)
    for process_type, region in groups:
        b = baseline[(baseline.process_type == process_type) & (baseline.region == region)].processing_days.dropna()
        r = recent[(recent.process_type == process_type) & (recent.region == region)].processing_days.dropna()
        if len(b) < 80 or len(r) < 80:
            continue
        b_mean = float(b.mean())
        r_mean = float(r.mean())
        change = ((r_mean - b_mean) / b_mean) * 100.0 if b_mean else 0.0
        if change < 15.0:
            continue
        severity = "high" if change >= 25.0 else "medium"
        signals.append(
            Signal(
                id=f"processing-{process_type.lower()}-{region.lower().replace(' ', '-')}",
                severity=severity,
                title="Processing-time shift",
                process_type=process_type,
                region=region,
                baseline_days=round(b_mean, 1),
                recent_days=round(r_mean, 1),
                change_pct=round(change, 1),
                baseline_n=len(b),
                recent_n=len(r),
                why=f"Mean processing time rose from {b_mean:.1f} to {r_mean:.1f} days across the defined baseline and recent windows.",
                boundary="This is a statistical change signal, not evidence of a cause, fault or service failure.",
                next_step="Review workload, staffing, intake mix and source-system changes with the responsible team.",
            )
        )
    return [s.as_dict() for s in sorted(signals, key=lambda x: x.change_pct, reverse=True)]


def group_outcome_report(df: pd.DataFrame) -> dict:
    _, recent = _periods(df)
    grouped = (
        recent.groupby("age_band", observed=True)
        .agg(cases=("case_id", "count"), complete_rate=("is_complete", "mean"), sla_rate=("within_sla", "mean"))
        .reset_index()
    )
    grouped["complete_rate_pct"] = grouped.complete_rate * 100
    grouped["sla_rate_pct"] = grouped.sla_rate * 100
    max_gap = float(grouped.complete_rate_pct.max() - grouped.complete_rate_pct.min())
    rows = [
        {
            "group": row.age_band,
            "cases": int(row.cases),
            "complete_rate_pct": round(float(row.complete_rate_pct), 1),
            "sla_rate_pct": round(float(row.sla_rate_pct), 1),
        }
        for row in grouped.itertuples()
    ]
    return {
        "groups": rows,
        "max_completion_gap_pp": round(max_gap, 1),
        "status": "REVIEW" if max_gap >= 2.0 else "PASS",
        "interpretation": "A group difference is a review signal. It is not a finding of discrimination and does not establish causality.",
        "next_step": "Check sample composition, missingness and process mix before drawing a substantive conclusion.",
    }


def summary(df: pd.DataFrame) -> dict:
    quality = quality_report(df)
    drift = drift_report(df)
    signals = detect_signals(df)
    groups = group_outcome_report(df)

    trust = quality["quality_score"]
    if drift["channel_status"] == "WARNING":
        trust -= 8
    elif drift["channel_status"] == "WATCH":
        trust -= 3
    if drift["missing_status"] == "WARNING":
        trust -= 8
    if groups["status"] == "REVIEW":
        trust -= 4

    recent = df[df.received_at >= RECENT_START]
    return {
        "dataset": {
            "cases": int(len(df)),
            "from": str(df.received_at.min().date()),
            "to": str(df.received_at.max().date()),
            "recent_cases": int(len(recent)),
            "synthetic": True,
        },
        "trust_score": round(max(0.0, trust), 1),
        "signal_count": len(signals),
        "quality": quality,
        "drift": drift,
        "group_status": groups["status"],
        "principle": "Compute first. Explain second. Human decides.",
    }
