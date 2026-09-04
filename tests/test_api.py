from fastapi.testclient import TestClient

from signallab.api import app


client = TestClient(app)


def test_health_boundary_is_explicit():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["synthetic_data"] is True


def test_summary_endpoint_returns_evidence_shape():
    response = client.get("/api/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["dataset"]["cases"] == 50_000
    assert body["dataset"]["synthetic"] is True
    assert body["signal_count"] >= 2


def test_signals_include_human_review_boundaries():
    response = client.get("/api/signals")
    signals = response.json()["signals"]
    assert signals
    assert all(signal["boundary"] for signal in signals)
    assert all(signal["next_step"] for signal in signals)
