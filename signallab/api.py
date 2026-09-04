from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .data import generate_cases
from .metrics import (
    decision_brief,
    detect_signals,
    drift_report,
    group_outcome_report,
    methodology_report,
    summary,
    trend_report,
)

app = FastAPI(
    title="DRV SignalLab",
    description="Trustworthy monitoring over synthetic public-administration data.",
    version="0.2.0",
)


@lru_cache(maxsize=1)
def dataset():
    return generate_cases()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "synthetic_data": True, "version": "0.2.0"}


@app.get("/api/summary")
def get_summary() -> dict:
    return summary(dataset())


@app.get("/api/brief")
def get_brief() -> dict:
    return decision_brief(dataset())


@app.get("/api/signals")
def get_signals() -> dict:
    return {"signals": detect_signals(dataset())}


@app.get("/api/trend")
def get_trend() -> dict:
    return trend_report(dataset())


@app.get("/api/drift")
def get_drift() -> dict:
    return drift_report(dataset())


@app.get("/api/groups")
def get_groups() -> dict:
    return group_outcome_report(dataset())


@app.get("/api/methodology")
def get_methodology() -> dict:
    return methodology_report()


@app.get("/", include_in_schema=False)
def demo() -> FileResponse:
    return FileResponse(Path(__file__).parent.parent / "web" / "index.html")
