from fastapi.testclient import TestClient

from signallab.api import app


client = TestClient(app)


def test_health_boundary_is_explicit():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["synthetic_data"] is True
    assert response.json()["version"] == "0.2.0"


def test_summary_endpoint_returns_evidence_shape():
    response = client.get("/api/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["dataset"]["cases"] == 50_000
    assert body["dataset"]["synthetic"] is True
    assert body["signal_count"] >= 2


def test_signals_include_statistical_and_human_review_boundaries():
    response = client.get("/api/signals")
    signals = response.json()["signals"]
    assert signals
    assert all(signal["ci_95_low_days"] > 0 for signal in signals)
    assert all(signal["statistical_note"] for signal in signals)
    assert all(signal["boundary"] for signal in signals)
    assert all(signal["next_step"] for signal in signals)


def test_decision_brief_never_executes_action():
    body = client.get("/api/brief").json()
    assert body["status"] == "HUMAN_REVIEW_REQUIRED"
    assert body["autonomous_action"] is False
    assert body["recommendation"]


def test_trend_and_methodology_are_inspectable():
    trend = client.get("/api/trend")
    methods = client.get("/api/methodology")
    assert trend.status_code == 200
    assert methods.status_code == 200
    assert len(trend.json()["series"]) == 24
    assert methods.json()["thresholds"]["processing_signal"]
