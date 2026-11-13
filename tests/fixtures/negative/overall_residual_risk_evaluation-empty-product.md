---
id: negative-26
title: "overall_residual_risk_evaluation-empty-product"
type: overall_residual_risk_evaluation
object: overall_residual_risk_evaluation
expect: "Product"
because: "the product is named"
---
# [negative-26] overall_residual_risk_evaluation-empty-product

## Determination

| Product | Decision | Rationale | Decided by |
| ------- | -------- | --------- | ---------- |
|  | accepted | Within the policy. | A. Person |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| evaluation_id | UUID | 1..1 | identity |

## Invariants

The clauses this overall-residual-risk-evaluation declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### EvaluationCarriesNoTotal

```ocl
context OverallResidualRiskEvaluation
inv EvaluationCarriesNoTotal:
  self.score->isEmpty()
```
