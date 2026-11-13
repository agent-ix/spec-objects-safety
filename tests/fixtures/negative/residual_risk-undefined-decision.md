---
id: negative-22
title: "residual_risk-undefined-decision"
type: residual_risk
object: residual_risk
expect: "Decision"
because: "decision is exactly undecided, accepted or not_accepted and has no default"
---
# [negative-22] residual_risk-undefined-decision

## Determination

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| approved | Within the policy. | A. Person |

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
