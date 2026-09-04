# DRV SignalLab

**Trustworthy data & AI monitoring for public administration.**

SignalLab is an independent, application-specific work sample for public-sector AI-lab / data-science roles. It turns 50,000 deterministic synthetic administrative cases into an inspectable operational brief:

`data → quality → drift → signal → uncertainty → explanation → human review`

> **Synthetic data only. Independent portfolio project. Not affiliated with Deutsche Rentenversicherung Bund.**

## The 60-second reviewer path

1. **Read the Lagebild.** The system says what changed and whether human review is required.
2. **Inspect Golden Case 01.** A sustained processing-time shift appears in `Kontenklaerung` for Berlin / Brandenburg.
3. **Check the evidence.** Each signal exposes baseline/recent means, sample sizes, the mean difference, an approximate 95% confidence interval and Cohen's *d*.
4. **Inspect Golden Case 02.** A synthetic source-system migration changes channel distribution and missingness.
5. **Check the boundary.** No cause, discrimination finding or individual benefit/enforcement decision is inferred automatically.

The core design principle is:

> **Compute first. Explain second. Human decides.**

## Why I built it this way

A public-sector AI lab does not only need a model that can spot patterns. It needs an evidence trail that lets people answer:

- What changed?
- Is the data trustworthy enough to inspect the signal?
- How large is the effect?
- How uncertain is the estimate?
- Which threshold fired?
- What *cannot* be concluded from the signal?
- What should a human inspect next?

SignalLab is deliberately small enough that every important rule can be read and tested.

## Golden cases

### 01 — Operational level shift

The synthetic recent window injects a +9 day processing-time shift into `Kontenklaerung` for Berlin and Brandenburg.

A signal is only surfaced when it clears:

- at least **+15%** mean increase,
- at least **80 observations** in baseline and recent windows,
- and an approximate **95% CI for the mean difference above zero**.

The UI then exposes effect size, CI, sample sizes and the interpretation boundary.

### 02 — Input / source-system drift

A fictional `source_c` enters the recent window and changes:

- channel distribution,
- processing-time missingness,
- completeness.

SignalLab calculates Population Stability Index (PSI), missingness drift and data-quality checks, then recommends investigation **before** retraining or operational action.

## Responsible group monitoring

The recent synthetic data is also compared across age bands.

A configured completion-rate gap can trigger `REVIEW`, but the system explicitly states:

> A group difference is a review signal. It is **not** a finding of discrimination and does not establish causality.

## What is deterministic

The demo does **not** need an LLM to produce its core findings.

- data generation is seeded,
- signal thresholds are explicit,
- PSI is calculated in Python,
- confidence intervals and effect sizes are calculated in Python,
- review boundaries are encoded,
- golden cases are regression-tested,
- the deployed hero metrics and chart are rendered from the same analytics engine and checked for presentation drift.

A future LLM could summarise the computed evidence contract, but it would not own the calculation or decision authority.

## API

- `GET /health`
- `GET /api/summary`
- `GET /api/brief`
- `GET /api/signals`
- `GET /api/trend`
- `GET /api/drift`
- `GET /api/groups`
- `GET /api/methodology`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e . --no-deps
uvicorn signallab.api:app --reload
```

Open `http://127.0.0.1:8000`.

## Test

```bash
pytest -q
```

The regression suite verifies the data generator, data quality, PSI, the two injected operational signals, statistical support, the sustained trend, decision boundaries, methodology exposure, API contracts and the public presentation values.

## Role-fit map

| Public-sector data / AI capability | SignalLab proof |
|---|---|
| Python | deterministic analytics engine |
| source-system variation | 50k synthetic records across simulated source systems and channels |
| pattern detection | process × region monitoring |
| statistical reasoning | practical threshold + 95% CI + Cohen's *d* |
| data quality | completeness, duplicates, schema integrity |
| data drift | PSI + missingness shift |
| bias awareness | descriptive group-outcome monitor |
| dashboards | German operational Lagebild |
| explainability | `Why?` evidence + threshold + boundary |
| responsible AI | no consequential autonomous action |
| communication | decision brief + recommended next investigation |
| engineering quality | FastAPI, packaging, CI, regression tests |

## Scope boundary

SignalLab is a portfolio proof, not a simulation of actual DRV systems or decision rules.

It uses:

- no real citizen data,
- no real DRV schema,
- no real operational thresholds,
- no automated pension / benefit / fraud / enforcement decision.

Real multi-source ingestion, production ETL and operational data contracts are intentionally out of scope for this work sample. The synthetic generator models source-system variation so the monitoring logic can be inspected without claiming a production integration that does not exist.

The thresholds exist to make the work sample inspectable and testable, not to claim domain policy.

## Stack

Python · FastAPI · pandas · NumPy · pytest · vanilla HTML/CSS/JS

The intentionally small stack keeps the proof easy to run, audit and discuss in an interview.

See [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md) for the short interview walkthrough.
