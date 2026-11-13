---
id: BR-001
title: "BenefitWeighedAgainstDecelerationRisk"
type: benefit_risk
object: benefit_risk
---
<!-- benefit_risk authoring skeleton (spec-objects-safety). THIS SKELETON FAILS
     VALIDATION AS SHIPPED, ON PURPOSE: the benefit, decision and rationale are
     placeholders that a person replaces. Contract (manifest body_extraction
     asserts):
     - Frontmatter MUST carry id, title, type: benefit_risk,
       object: benefit_risk.
     - "## Decision" (H2) is REQUIRED: a table with headers exactly
       `Benefit | Decision | Rationale | Decided by` and exactly one data row. `Decision` is exactly
       `undecided`, `accepted` or `not_accepted`; there is no default.
       `Rationale` is stated. `Decided by` is the named person who decided;
       leave it empty while the decision is `undecided`, and never leave it
       empty or a placeholder once it is `accepted` or `not_accepted`.
       `Benefit` is the benefit that justifies the residual risks, in your own
       words.
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

     LINK THE RECORD to every residual risk it covers, one `references`
     relationship each, at least one:

       relationships:
         - target: RR-001
           type: references -->
# [BR-001] BenefitWeighedAgainstDecelerationRisk

## Decision

| Benefit | Decision | Rationale | Decided by |
| ------- | -------- | --------- | ---------- |
| <the benefit that justifies the residual risks> | <undecided, accepted or not_accepted> | <why the person decided so> | <person who decided, empty while undecided> |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| benefit_risk_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

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
