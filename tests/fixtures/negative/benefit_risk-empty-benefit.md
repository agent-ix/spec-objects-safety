---
id: negative-25
title: "benefit_risk-empty-benefit"
type: benefit_risk
object: benefit_risk
expect: "Benefit"
because: "the benefit statement is required"
---
# [negative-25] benefit_risk-empty-benefit

## Determination

| Benefit | Decision | Rationale | Decided by |
| ------- | -------- | --------- | ---------- |
|  | accepted | Within the policy. | A. Person |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| benefit_risk_id | UUID | 1..1 | identity |

## Invariants

The clauses this benefit-risk declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### BenefitRiskCarriesNoRatio

```ocl
context BenefitRisk
inv BenefitRiskCarriesNoRatio:
  self.score->isEmpty()
```
