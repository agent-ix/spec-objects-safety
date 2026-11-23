---
id: RMR-001
title: "ProjectRiskManagementReview"
type: risk_management_review
object: risk_management_review
---
<!-- risk_management_review authoring skeleton (spec-objects-safety).
     THIS SKELETON FAILS VALIDATION AS SHIPPED, ON PURPOSE: every cell is a
     placeholder that a person replaces. This module ships no review, and no tool
     fills one in or derives one from the records it references.
     Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: risk_management_review,
       object: risk_management_review.
     - "## Review" (H2) is REQUIRED: a table with headers exactly
       `Reviewer | Plan executed | Post-production readiness | Statement` and
       exactly one data row. `Reviewer` is the named person who reviewed.
       `Plan executed` is exactly `yes`, `partly` or `no`.
       `Post-production readiness` is exactly `ready` or `not_ready`. There is
       no default for either. `Statement` is the reviewer's own words.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     THE PLAN AND THE OVERALL EVALUATION ARE REFERENCED, NOT WRITTEN HERE. Link
     the review to the risk management plan that was executed and to the overall
     residual-risk evaluation people decided, a `reviews` relationship to the
     plan and a `references` relationship to the evaluation:

       relationships:
         - target: RMP-001
           type: reviews
         - target: ORE-001
           type: references

     People accept risk. No score, class, acceptability or approval is recorded
     in this review, and no tool computes or defaults one. -->
# [RMR-001] ProjectRiskManagementReview

## Review

| Reviewer | Plan executed | Post-production readiness | Statement |
| -------- | ------------- | ------------------------- | --------- |
| <person who reviewed> | <yes, partly or no> | <ready or not_ready> | <the reviewer's statement> |

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
