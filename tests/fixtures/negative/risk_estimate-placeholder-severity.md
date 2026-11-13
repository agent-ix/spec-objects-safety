---
id: negative-010
title: "EstimateWithPlaceholderSeverity"
type: risk_estimate
object: risk_estimate
phase: pre_control
expect: "column 'Severity' cell '<severity>'"
because: "an unfilled placeholder is not a level"
---
# [negative-010] EstimateWithPlaceholderSeverity

## Judgement

| Severity | Probability | Rationale |
| -------- | ----------- | --------- |
| <severity> | remote | because |

## Provenance

| Asserted by | Asserted at |
| ----------- | ----------- |
| Ann | 2026-11-12 |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| estimate_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

## Invariants

The clauses this risk-estimate declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### EstimateCarriesNoScore

```ocl
context RiskEstimate
inv EstimateCarriesNoScore:
  self.score->isEmpty()
```
