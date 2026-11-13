---
id: negative-014
title: "EstimateWithUnparsableDate"
type: risk_estimate
object: risk_estimate
phase: pre_control
expect: "column 'Asserted at' cell 'yesterday'"
because: "assertedAt is a date"
---
# [negative-014] EstimateWithUnparsableDate

## Judgement

| Severity | Probability | Rationale |
| -------- | ----------- | --------- |
| critical | remote | because |

## Provenance

| Asserted by | Asserted at |
| ----------- | ----------- |
| Ann | yesterday |

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
