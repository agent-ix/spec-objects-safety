---
id: negative-013
title: "EstimateWithoutProvenance"
type: risk_estimate
object: risk_estimate
phase: pre_control
expect: "required 'provenance'"
because: "an estimate names who asserted it"
---
# [negative-013] EstimateWithoutProvenance

## Estimate

| Severity | Probability | Rationale |
| -------- | ----------- | --------- |
| critical | remote | because |

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
