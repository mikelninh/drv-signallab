import math

from signallab.data import REQUIRED_COLUMNS, generate_cases
from signallab.metrics import detect_signals, drift_report, group_outcome_report, population_stability_index, quality_report, summary


def test_generator_is_deterministic_and_well_shaped():
    a = generate_cases(2_000, seed=7)
    b = generate_cases(2_000, seed=7)
    assert a.equals(b)
    assert REQUIRED_COLUMNS.issubset(a.columns)
    assert a.case_id.is_unique


def test_psi_zero_for_identical_distribution():
    assert math.isclose(population_stability_index([50, 50], [50, 50]), 0.0, abs_tol=1e-10)


def test_quality_schema_passes():
    report = quality_report(generate_cases(5_000))
    assert report["schema_integrity"] == "PASS"
    assert report["duplicate_pct"] == 0.0
    assert report["completeness_pct"] > 99.0


def test_injected_channel_drift_is_visible():
    report = drift_report(generate_cases())
    assert report["channel_psi"] >= 0.10
    assert report["recent_missing_pct"] > report["baseline_missing_pct"]


def test_injected_operational_shift_is_detected():
    signals = detect_signals(generate_cases())
    keys = {(s["process_type"], s["region"]) for s in signals}
    assert ("Kontenklaerung", "Berlin") in keys
    assert ("Kontenklaerung", "Brandenburg") in keys


def test_group_monitor_never_claims_causality():
    report = group_outcome_report(generate_cases())
    text = report["interpretation"].lower()
    assert "not a finding" in text
    assert "causality" in text


def test_summary_has_explicit_synthetic_boundary():
    report = summary(generate_cases(10_000))
    assert report["dataset"]["synthetic"] is True
    assert 0 <= report["trust_score"] <= 100
