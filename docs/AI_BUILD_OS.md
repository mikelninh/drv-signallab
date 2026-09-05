# AI Build OS — DRV SignalLab

SignalLab uses a lightweight agentic engineering loop. The goal is not maximum automation. The goal is to make the path from problem definition to accepted evidence explicit and reproducible.

## 01 — SHAPE
**Problem → user → constraints → architecture**

- problem: operational data can drift or change in ways that deserve investigation before anyone acts;
- reviewer/user: public-sector AI/data teams that need an inspectable Lagebild, not a black-box prediction;
- constraints: synthetic data only, no real DRV policy or citizen decisions, causal claims prohibited;
- architecture: deterministic analytics API + transparent web brief + human review boundary.

Outputs: `README.md`, `docs/ARCHITECTURE.md`.

## 02 — SPECIFY
**Requirements → boundaries → acceptance criteria**

The golden reviewer path and thresholds are documented in `README.md`. The regression contract lives in `tests/`.

Core acceptance conditions:
- the seeded dataset is reproducible;
- Golden Case 01 surfaces the injected processing-time shift only when explicit evidence thresholds are met;
- Golden Case 02 surfaces source/input drift and recommends investigation before retraining/action;
- uncertainty, effect size and sample sizes remain inspectable;
- group differences remain descriptive review signals, never causal or discrimination findings;
- public metrics/charts stay consistent with the analytics engine.

## 03 — DELEGATE
**Agents execute within explicit autonomy limits**

`AGENTS.md` defines A0–A4 action classes.

Coding agents may implement, test, critique and document the proof. They may not reinterpret synthetic thresholds as policy, connect real citizen data without authority, or automate consequential decisions.

## 04 — PROVE
**Tests → evals → benchmarks → adversarial cases**

Current gate:

```bash
pytest -q
```

The proof is intentionally deterministic. Regression coverage includes data quality, PSI, missingness drift, injected signals, confidence/effect evidence, boundaries, API contracts and presentation drift.

Useful future eval extensions:
- threshold sensitivity and false-alert analysis across more synthetic regimes;
- adversarial missing-data patterns;
- delayed/source-specific drift;
- robustness to small samples and distribution skew;
- explanation consistency against the computed evidence contract;
- reviewer task-completion time and correction rate.

These should be measured before any production-quality claim is made.

## 05 — SHIP
**CI → deployment gates → production**

CI should run the full deterministic regression suite before merge/deploy.

A passing work sample is not production readiness. A real deployment would additionally require real data contracts, governance, access controls, operational thresholds, monitoring ownership and domain validation.

## 06 — WATCH
**Traces → logs → regressions → feedback**

For this work sample, the primary watch layer is regression/presentation drift: the numbers displayed to a reviewer must continue to come from the same analytics engine that tests validate.

A production monitoring layer should additionally watch:
- source/schema changes,
- missingness/completeness trends,
- alert volume and false-alert feedback,
- latency/errors,
- threshold changes,
- reviewer overrides/corrections,
- data access and operational incidents.

Monitoring findings should feed back into tests and acceptance criteria.

## Build principle

> Compute first. Explain second. Human decides. Agents accelerate the build; evidence decides whether the build is accepted.
