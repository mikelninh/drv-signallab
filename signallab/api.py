from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
from .presentation import render_demo_html

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


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def demo() -> HTMLResponse:
    root = Path(__file__).parent.parent
    source = (root / "web" / "index.html").read_text(encoding="utf-8")
    faq = (root / "web" / "faq-snippet.html").read_text(encoding="utf-8")
    return HTMLResponse(render_demo_html(source, faq))
