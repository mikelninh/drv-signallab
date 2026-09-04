from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {
    "case_id",
    "received_at",
    "region",
    "process_type",
    "channel",
    "processing_days",
    "is_complete",
    "within_sla",
    "age_band",
    "source_system",
}


def generate_cases(n: int = 50_000, seed: int = 42) -> pd.DataFrame:
    """Generate deterministic synthetic administrative cases with two injected shifts.

    The data is deliberately fictional. The recent period contains:
    1) an operational processing-time increase for Kontenklaerung in Berlin/Brandenburg;
    2) a source-system/channel shift that increases missingness and digital share.
    """
    rng = np.random.default_rng(seed)
    months = pd.period_range("2024-09", "2026-08", freq="M")
    month_idx = rng.integers(0, len(months), size=n)
    received = pd.to_datetime([months[i].start_time for i in month_idx]) + pd.to_timedelta(
        rng.integers(0, 27, size=n), unit="D"
    )

    region = rng.choice(
        ["Berlin", "Brandenburg", "Hamburg", "Nordrhein-Westfalen"],
        size=n,
        p=[0.30, 0.20, 0.16, 0.34],
    )
    process = rng.choice(
        ["Rentenantrag", "Reha", "Kontenklaerung", "Betriebspruefung"],
        size=n,
        p=[0.38, 0.22, 0.25, 0.15],
    )
    age_band = rng.choice(["under_35", "35_49", "50_64", "65_plus"], size=n, p=[0.16, 0.26, 0.38, 0.20])

    recent = received >= pd.Timestamp("2026-06-01")
    source_system = np.where(recent & (rng.random(n) < 0.43), "source_c", rng.choice(["source_a", "source_b"], n, p=[0.65, 0.35]))

    digital_prob = np.where(recent, 0.61, 0.44)
    draw = rng.random(n)
    channel = np.where(draw < digital_prob, "digital", np.where(draw < digital_prob + 0.24, "postal", "service_center"))

    base_days = {
        "Rentenantrag": 29.0,
        "Reha": 21.0,
        "Kontenklaerung": 24.0,
        "Betriebspruefung": 32.0,
    }
    processing = np.array([base_days[p] for p in process]) + rng.normal(0, 6.0, n)

    operational_shift = recent & (process == "Kontenklaerung") & np.isin(region, ["Berlin", "Brandenburg"])
    processing += np.where(operational_shift, 9.0, 0.0)
    processing = np.clip(processing, 2.0, None)

    completeness_prob = np.full(n, 0.982)
    completeness_prob -= np.where(source_system == "source_c", 0.055, 0.0)
    completeness_prob -= np.where((recent) & (age_band == "under_35"), 0.018, 0.0)
    is_complete = rng.random(n) < completeness_prob

    # A missing-value shift is injected only into source_c records in the recent period.
    missing_mask = recent & (source_system == "source_c") & (rng.random(n) < 0.08)
    processing[missing_mask] = np.nan

    sla_days = np.array([36 if p == "Betriebspruefung" else 30 for p in process], dtype=float)
    within_sla = processing <= sla_days

    frame = pd.DataFrame(
        {
            "case_id": [f"SYN-{i:06d}" for i in range(n)],
            "received_at": received,
            "region": region,
            "process_type": process,
            "channel": channel,
            "processing_days": processing,
            "is_complete": is_complete,
            "within_sla": within_sla,
            "age_band": age_band,
            "source_system": source_system,
        }
    )
    return frame.sort_values("received_at").reset_index(drop=True)
