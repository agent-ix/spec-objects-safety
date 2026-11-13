---
id: negative-27
title: "residual_risk-decided-without-decider"
type: residual_risk
object: residual_risk
expect: "determination.decided_by"
because: "an accepted or not_accepted decision names a decider"
---
# [negative-27] residual_risk-decided-without-decider

## Determination

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| accepted | Within the policy. |  |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| residual_risk_id | UUID | 1..1 | identity |

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
