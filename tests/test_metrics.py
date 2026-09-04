import math

from signallab.data import REQUIRED_COLUMNS, generate_cases
from signallab.metrics import (
    decision_brief,
    detect_signals,
    drift_report,
    group_outcome_report,
    methodology_report,
    population_stability_index,
    quality_report,
    summary,
    trend_report,
)


def test_generator_is_deterministic_and_well_shaped():
    a = generate_cases(2_000, seed=7)
    b = generate_cases(2_000, seed=7)
    assert a.equals(b)
    assert REQUIRED_COLUMNS.issubset(a.columns)
    assert a.case_id.is_unique


def test_psi_zero_for_identical_distribution():
    assert math.isclose(
        population_stability_index([50, 50], [50, 50]),
        0.0,
        abs_tol=1e-10,
    )


def test_quality_schema_passes():
    report = quality_report(generate_cases(5_000))
    assert report["schema_integrity"] == "PASS"
    assert report["duplicate_pct"] == 0.0
    assert report["completeness_pct"] > 99.0


def test_injected_channel_drift_is_visible():
    report = drift_report(generate_cases())
    assert report["channel_psi"] >= 0.10
    assert report["recent_missing_pct"] > report["baseline_missing_pct"]


def test_injected_operational_shift_is_detected_with_uncertainty_support():
    signals = detect_signals(generate_cases())
    by_key = {(s["process_type"], s["region"]): s for s in signals}
    for key in [("Kontenklaerung", "Berlin"), ("Kontenklaerung", "Brandenburg")]:
        assert key in by_key
        signal = by_key[key]
        assert signal["ci_95_low_days"] > 0
        assert signal["effect_size"] > 1.0
        assert signal["baseline_n"] >= 80
        assert signal["recent_n"] >= 80


def test_trend_exposes_sustained_recent_level_shift():
    report = trend_report(generate_cases())
    recent = [x["mean_days"] for x in report["series"] if x["recent"]]
    prior = [
        x["mean_days"]
        for x in report["series"]
        if "2025-12" <= x["month"] <= "2026-05"
    ]
    assert len(recent) == 3
    assert sum(recent) / len(recent) > (sum(prior) / len(prior)) + 7


def test_group_monitor_never_claims_causality():
    report = group_outcome_report(generate_cases())
    text = report["interpretation"].lower()
    assert "not a finding" in text
    assert "causality" in text


def test_decision_brief_preserves_human_authority():
    brief = decision_brief(generate_cases())
    assert brief["status"] == "HUMAN_REVIEW_REQUIRED"
    assert brief["autonomous_action"] is False
    assert brief["strongest_signal"]["ci_95_low_days"] > 0
    assert len(brief["excluded_conclusions"]) == 3


def test_methodology_exposes_thresholds():
    report = methodology_report()
    assert "95% CI" in report["thresholds"]["processing_signal"]
    assert report["principles"]


def test_summary_has_explicit_synthetic_boundary():
    report = summary(generate_cases(10_000))
    assert report["dataset"]["synthetic"] is True
    assert 0 <= report["trust_score"] <= 100
    assert "not a model-performance" in report["trust_score_note"]
