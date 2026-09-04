# SignalLab — Technical Review Notes

These notes sit behind the public demo. The UI intentionally stays simple for non-technical reviewers; this document keeps the deeper engineering reasoning inspectable.

## 1. Why PSI?

PSI is used here as a simple, model-independent early-warning signal for distribution change. It is easy to explain and works without labels. A PSI value indicates that a distribution changed; it does not establish why. In production I would combine it with schema checks, missingness monitoring and, depending on the data type, measures such as Wasserstein or Jensen-Shannon distance.

## 2. How were the thresholds chosen?

They are explicit demo operating rules, not claimed universal optima. A signal requires practical minimum change, sufficient sample size and an uncertainty check together. In production I would backtest thresholds on historical data and calibrate them against the operational costs of false alerts and missed changes.

## 3. Why a 95% confidence interval?

The point is not only to say that something changed, but to expose how large the change plausibly is. The interval around the difference in means makes uncertainty visible. For strongly skewed distributions or outliers I would evaluate robust or bootstrap intervals instead of treating this approximation as universally appropriate.

## 4. What happens with small samples?

The system should become more conservative. Below the minimum sample size I would not emit a strong operational signal; the UI should say “insufficient evidence”. Depending on the use case, options include wider time windows, defensible aggregation, bootstrap methods or Bayesian estimates.

## 5. How would real data sources be connected?

Through separate, preferably read-only source adapters: APIs, databases, files or event streams → validation → canonical schema → lineage/metadata → quality gates. Personally identifiable data should be minimised, access should be role-based and raw data should not be copied into downstream analysis or GenAI layers unless necessary.

## 6. What would the SQL / ETL layer look like?

**Raw → Staging → Core → Analytics Mart.**

- Raw: source-faithful, append-only where possible, with ingestion metadata.
- Staging: typing, parsing, schema validation and basic quality checks.
- Core: stable business keys, common dimensions and versioned domain logic.
- Analytics: narrow monitoring tables optimised for reproducible metrics and dashboards.

Transformations should be versioned, incremental where useful and covered by data-quality tests.

## 7. What is different about synthetic data?

Here the injected changes and the data-generating process are known. Real data introduces schema changes, delayed values, selection bias, missing labels, permissions, privacy constraints and feedback loops. Therefore the prototype demonstrates the method and engineering approach; it does not claim production performance on DRV data.

## 8. How would data or model drift be monitored?

For data: schema, missingness, feature distributions and important slices over time. For models: performance with delayed ground truth, calibration, residuals, slice metrics and backtests. Alerts should account for persistence so one outlier does not automatically trigger retraining or operational action.

## 9. Where should GenAI be used — and where not?

Useful for audience-specific summaries, analyst notes, document-grounded Q&A and explanation drafts, ideally grounded with sources. Not for core calculations, thresholds, data-quality logic or benefit decisions. The factual layer should remain deterministic; GenAI may explain and propose.

---

**Design principle:** compute first, explain second, human decides.
