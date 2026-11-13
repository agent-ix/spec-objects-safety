---
id: ORE-001
title: "OverallResidualRiskOfProduct"
type: overall_residual_risk_evaluation
object: overall_residual_risk_evaluation
---
<!-- overall_residual_risk_evaluation authoring skeleton (spec-objects-safety).
     THIS SKELETON FAILS VALIDATION AS SHIPPED, ON PURPOSE: the product,
     decision and rationale are placeholders that a person replaces. Contract
     (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type:
       overall_residual_risk_evaluation, object:
       overall_residual_risk_evaluation.
     - "## Decision" (H2) is REQUIRED: a table with headers exactly
       `Product | Decision | Rationale | Decided by` and exactly one data row. `Decision` is exactly
       `undecided`, `accepted` or `not_accepted`; there is no default.
       `Rationale` is stated. `Decided by` is the named person who decided;
       leave it empty while the decision is `undecided`, and never leave it
       empty or a placeholder once it is `accepted` or `not_accepted`.
       `Product` names the product this evaluation concerns.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     WHO AND WHEN COME FROM VERSION CONTROL (the commit author and signature of
     this file), not from a field. No score, region, ratio, total or date is
     recorded here, and no tool computes or defaults a decision. Acceptance is a
     human decision: a passing validation is not one.

     No tool aggregates the individual risks into this decision. LINK THE
     RECORD to every residual risk and benefit-risk record you considered, one
     `references` relationship each:

       relationships:
         - target: RR-001
           type: references
         - target: BR-001
           type: references -->
# [ORE-001] OverallResidualRiskOfProduct

## Decision

| Product | Decision | Rationale | Decided by |
| ------- | -------- | --------- | ---------- |
| <product> | <undecided, accepted or not_accepted> | <why the person decided so> | <person who decided, empty while undecided> |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| evaluation_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

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
