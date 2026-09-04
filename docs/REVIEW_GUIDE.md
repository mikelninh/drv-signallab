# SignalLab reviewer / interview guide

## One-sentence pitch

**SignalLab detects operational and data-quality changes in synthetic administrative cases, quantifies the evidence, exposes uncertainty and stops at a human review boundary.**

## 60-second walkthrough

### 0–10s — Lagebild

Start at the top.

The page should answer immediately:

- human review required?
- strongest signal?
- is the data usable?
- what is explicitly *not* automated?

### 10–25s — Golden Case 01

Show the monthly trend for `Kontenklaerung · Berlin + Brandenburg`.

Then inspect one signal:

- baseline vs recent mean,
- +% change,
- mean difference,
- approximate 95% CI,
- Cohen's d,
- sample sizes.

Key sentence:

> "I did not want a dashboard that merely says red or green. I wanted the reviewer to see exactly why the signal exists and how uncertain it is."

### 25–40s — Golden Case 02

Show channel PSI and missingness drift.

Key sentence:

> "Before changing a model or process, I first want to know whether the input itself changed."

### 40–50s — Group monitor

Point to the explicit distinction between:

- observed disparity,
- discrimination finding,
- causality.

Key sentence:

> "The system can surface a review signal; it does not promote a descriptive difference into a consequential conclusion."

### 50–60s — Human authority

Finish with the boundary:

> "The analytics can compute and explain. Intervention, retraining and any individual administrative decision remain outside the system."

## Likely technical questions

### Why PSI?

It is a simple, inspectable way to demonstrate distribution change across a categorical input. It is not presented as a universal drift metric.

### Why not use p-values?

For this work sample the operational signal combines a practical effect threshold with an approximate confidence interval for the mean difference and an effect size. The goal is to show magnitude and uncertainty, not to turn one hypothesis test into an automatic decision rule.

### Why an approximate 95% CI?

The synthetic sample sizes are large and the implementation stays dependency-light and auditable. In a production study I would validate the distributional assumptions and consider robust / bootstrap alternatives.

### Why is the trust score heuristic?

It is an operational demo indicator to summarise quality/drift review state. It is explicitly **not** a model-performance score, certification or probability of correctness.

### What would you add next?

1. real, approved public-data connectors,
2. metric lineage / run IDs,
3. persisted monitoring snapshots,
4. reviewer annotations,
5. alert precision / false-positive evaluation,
6. robust drift metrics for continuous variables,
7. bounded evidence-grounded narrative generation.

The important point: add those only after the monitoring contract is clear and testable.
