# DRV SignalLab

**Trustworthy data & AI monitoring for public administration.**

SignalLab is a small, application-specific portfolio proof built around the kind of work described for a Junior Data Scientist in a public-sector AI lab: Python analytics, multi-source data, anomaly detection, data quality, distribution drift, group-level outcome monitoring, dashboards and clear human-reviewable explanations.

> **Independent portfolio project. Synthetic data only. Not affiliated with Deutsche Rentenversicherung Bund.**

## The question

> **Where is our case workload changing — and can we trust the data enough to act on the signal?**

Instead of an LLM making decisions, SignalLab computes evidence deterministically and makes every warning inspectable:

`synthetic admin events → quality checks → drift → signals → group outcomes → explanation → human review`

The model may eventually summarise these facts, but it never owns the underlying calculation or decision authority.

## What the demo shows

### 1. Operations overview
- 50,000 deterministic synthetic administrative cases
- current workload and processing-time indicators
- data trust score
- prioritised warnings

### 2. Signal Explorer
Detects material changes by process and region. Each signal includes:
- baseline and recent value
- percentage change
- sample sizes
- trigger rule
- interpretation boundary
- recommended human follow-up

### 3. Data Trust
Checks:
- completeness
- duplicate IDs
- schema integrity
- missing-value drift
- distribution drift via Population Stability Index (PSI)

### 4. Group Outcome Monitor
Compares synthetic age bands on a service-level outcome. It is intentionally descriptive:

**A disparity is a review signal, not a finding of discrimination or causality.**

## Golden cases

**A — Operational shift**  
A synthetic process develops a sustained processing-time increase in recent months. SignalLab identifies where the change is concentrated and shows the exact calculation behind the warning.

**B — Data / model-input shift**  
A synthetic source-system change increases missing values and changes the channel distribution. SignalLab raises drift warnings and recommends investigation rather than automatic retraining or policy action.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn signallab.api:app --reload
```

Open `http://127.0.0.1:8000`.

## Test

```bash
pytest -q
```

## API

- `GET /health`
- `GET /api/summary`
- `GET /api/signals`
- `GET /api/drift`
- `GET /api/groups`

## Why this is trustworthy by design

1. **Synthetic data only** — the proof cannot expose citizen data.
2. **Deterministic analytics** — thresholds and formulas are inspectable Python.
3. **Evidence before narrative** — explanations point back to metrics and sample sizes.
4. **No causal overclaiming** — drift and disparities are labelled as review signals.
5. **Human authority** — consequential follow-up is always a recommendation, never an autonomous action.
6. **Regression tests** — the injected golden cases must remain detectable.

## Stack

Python · FastAPI · pandas · NumPy · pytest · vanilla HTML/CSS/JS

The intentionally small stack keeps the proof easy to audit and easy to run.

## Role-fit map

| Capability | SignalLab proof |
|---|---|
| Python | deterministic analytics engine |
| data consolidation | multi-source synthetic case generator |
| large datasets | 50k-case default dataset |
| pattern detection | process/region signal detection |
| bias awareness | group-level outcome monitor |
| data drift | PSI + missing-value drift |
| dashboards | operational web UI |
| GenAI readiness | computed evidence contract ready for bounded summarisation |
| communication | plain-language `Why?` explanations |
| responsible public-sector AI | explicit uncertainty + human review boundary |

## Design principle

> **Compute first. Explain second. Human decides.**
