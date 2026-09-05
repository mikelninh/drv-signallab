# AGENTS.md — DRV SignalLab

## Mission
Build a small, inspectable public-sector monitoring proof that separates deterministic computation from explanation and keeps consequential interpretation with humans.

Core contract:

`data -> quality -> drift -> signal -> uncertainty -> explanation -> human review`

The project is an independent work sample using synthetic data. Do not imply affiliation with Deutsche Rentenversicherung Bund or claim real DRV thresholds, schemas or operations.

## Start here
1. Read `README.md`.
2. Read `docs/ARCHITECTURE.md`.
3. Read `docs/TECHNICAL_REVIEW.md` for known limitations and review notes.
4. Read `tests/` before changing analytics, thresholds or API behaviour.
5. Run the full test suite before claiming success.

## Source-of-truth map
- Product scope, claims and golden reviewer path: `README.md`
- Architecture: `docs/ARCHITECTURE.md`
- Technical limitations/review: `docs/TECHNICAL_REVIEW.md`
- Interview walkthrough: `docs/REVIEW_GUIDE.md`
- Deterministic analytics/runtime: `signallab/`
- Regression truth: `tests/`
- Public presentation: `web/`
- CI truth: `.github/workflows/`

## Build contract before substantial work
Define:
- problem and reviewer/user outcome,
- requirements and non-goals,
- data assumptions,
- autonomy class,
- acceptance criteria,
- evidence required to call the task done,
- interpretation boundaries,
- rollback or next action.

Do not optimise for an impressive dashboard at the expense of inspectable evidence.

## Autonomy boundaries
- **A0 Observe** — inspect code, data, tests, docs. Automatic.
- **A1 Local reversible** — implement calculations, fixtures, docs and tests; run locally. Automatic.
- **A2 Shared reversible** — branch, pull request, preview deployment. Logged and normally automatic.
- **A3 Consequential** — publish external claims, change live infrastructure or connect real operational data. Human approval required.
- **A4 High-impact** — real citizen data or any automated benefit, fraud, enforcement or other consequential decision. Out of scope for this proof and requires explicit authority plus independent review.

## Verification
Minimum gate:

```bash
pytest -q
```

Regression checks must continue to prove:
- deterministic seeded data generation,
- data-quality checks,
- PSI and missingness drift,
- both injected golden signals,
- statistical support and thresholds,
- decision/interpretation boundaries,
- API contracts,
- public presentation values do not drift from the analytics engine.

For UI-impacting changes, also run the reviewer path in `docs/REVIEW_GUIDE.md`.

Never claim a command, metric or deployment passed unless it was actually checked.

## Agent roles
Use distinct passes where useful:
- **Shaper** — defines the operational question and acceptable evidence.
- **Builder** — implements the smallest auditable solution.
- **Verifier** — independently checks tests, calculations and presentation consistency.
- **Critic** — challenges causal overreach, statistical misuse, data leakage and unnecessary complexity.

## Hard boundaries
- Compute first; explain second; human decides.
- A signal is not a causal explanation.
- A group difference is not a discrimination finding.
- Synthetic thresholds are not real policy.
- A future LLM may summarise the evidence contract but must not own core calculations or consequential authority.
- Do not fabricate production performance, model quality or operational impact.
- Prefer deterministic, reproducible evidence over opaque sophistication.

## Definition of done
A change is done only when:
- acceptance criteria are explicit,
- relevant tests pass,
- calculations remain reproducible,
- the public UI matches computed values,
- interpretation boundaries remain visible,
- scope and unknowns are not overstated.
