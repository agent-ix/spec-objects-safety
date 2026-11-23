---
id: negative-30
title: "risk_management_review-placeholder-reviewer"
type: risk_management_review
object: risk_management_review
expect: "Reviewer"
because: "a review no named person wrote is refused"
---
# [negative-30] risk_management_review-placeholder-reviewer

## Review

| Reviewer | Plan executed | Post-production readiness | Statement |
| -------- | ------------- | ------------------------- | --------- |
| <person who reviewed> | yes | ready | The plan was carried out. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| review_id | UUID | 1..1 | identity |

## Invariants

The clauses this risk-management-review declaration enforces. Each clause owns
one `ocl` fence under its own `### <clauseId>` heading; the fence text is
carried verbatim and never evaluated here.

### ReviewCarriesNoScore

```ocl
context RiskManagementReview
inv ReviewCarriesNoScore:
  self.score->isEmpty()
```
