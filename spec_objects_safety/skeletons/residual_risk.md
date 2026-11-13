---
id: RR-001
title: "ResidualRiskOfDecelerationSituation"
type: residual_risk
object: residual_risk
---
<!-- residual_risk authoring skeleton (spec-objects-safety). THIS SKELETON FAILS
     VALIDATION AS SHIPPED, ON PURPOSE: the decision and rationale are
     placeholders that a person replaces. Contract (manifest body_extraction
     asserts):
     - Frontmatter MUST carry id, title, type: residual_risk,
       object: residual_risk.
     - "## Determination" (H2) is REQUIRED: a table with headers exactly
       `Decision | Rationale | Decided by` and exactly one data row. `Decision` is exactly
       `undecided`, `accepted` or `not_accepted`; there is no default.
       `Rationale` is stated. `Decided by` is the named person who decided;
       leave it empty while the decision is `undecided`, and never leave it
       empty or a placeholder once it is `accepted` or `not_accepted`.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     THE POST-CONTROL SEVERITY AND PROBABILITY ARE NOT COPIED HERE. They live on
     the post_control risk_estimate this record names; the record holds the
     decision about what remains. A hazard's own `status` is not an acceptance
     of its residual risk.

     WHO AND WHEN COME FROM VERSION CONTROL (the commit author and signature of
     this file), not from a field. No score, region, ratio, total or date is
     recorded here, and no tool computes or defaults a decision. Acceptance is a
     human decision: a passing validation is not one.

     LINK THE RECORD with relationships in the frontmatter. `estimate` names
     the one post-control risk estimate; `references` names the acceptability
     policy the decision is read against:

       relationships:
         - target: EST-002
           type: estimate
         - target: POL-001
           type: references -->
# [RR-001] ResidualRiskOfDecelerationSituation

## Determination

| Decision | Rationale | Decided by |
| -------- | --------- | ---------- |
| <undecided, accepted or not_accepted> | <why the person decided so> | <person who decided, empty while undecided> |

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
