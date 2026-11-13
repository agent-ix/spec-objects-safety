---
id: negative-24
title: "residual_risk-placeholder-decider"
type: residual_risk
object: residual_risk
expect: "Decided by"
because: "a placeholder is not a named decider"
---
# [negative-24] residual_risk-placeholder-decider

## Decision

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| accepted | Within the policy. | <person> |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| residual_risk_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

## Invariants

The clauses this residual-risk declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### ResidualRiskCarriesNoVerdict

```ocl
context ResidualRisk
inv ResidualRiskCarriesNoVerdict:
  self.score->isEmpty()
```
