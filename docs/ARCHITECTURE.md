# Architecture

SignalLab intentionally separates **measurement** from **interpretation**.

```text
Synthetic data generator
        ↓
Schema + quality checks
        ↓
Deterministic metrics
  ├─ operational signals
  ├─ channel PSI
  ├─ missing-value drift
  └─ group outcomes
        ↓
Evidence-shaped API responses
        ↓
Human-readable dashboard
        ↓
Human investigation / decision
```

## Evidence contract

Every operational signal returns:

- metric name
- baseline value and period
- recent value and period
- baseline/recent sample counts
- threshold-derived severity
- plain-language reason
- interpretation boundary
- recommended human next step

A future LLM summariser may consume this contract, but it should not recompute metrics, invent causes or execute consequential actions.

## Threat / failure considerations

| Failure mode | Current control |
|---|---|
| fabricated demo facts | deterministic synthetic generator |
| causal overclaim | explicit interpretation boundaries |
| silent schema break | required-column validation |
| hidden missingness | missing-value metrics + drift |
| misleading distribution change | PSI shown with threshold and explanation |
| autonomous consequential action | no write/action endpoints |
| PII exposure | synthetic data only |
| regression of golden cases | CI tests injected shifts |

## What this proof deliberately does not claim

- that these fields or thresholds represent real DRV operations
- that a statistical disparity proves unfairness
- that drift proves model degradation
- that an alert identifies root cause
- that the system should make benefit, fraud, enforcement or eligibility decisions
