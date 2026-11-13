---
id: negative-28
title: "residual_risk-undecided-with-decider"
type: residual_risk
object: residual_risk
expect: "is not allowed for"
because: "an undecided record refuses a decider"
---
# [negative-28] residual_risk-undecided-with-decider

## Determination

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| undecided | Within the policy. | A. Person |

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
