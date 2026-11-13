---
id: negative-23
title: "residual_risk-empty-rationale"
type: residual_risk
object: residual_risk
expect: "Rationale"
because: "a decision without a stated rationale is refused"
---
# [negative-23] residual_risk-empty-rationale

## Determination

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| accepted |  | A. Person |

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
