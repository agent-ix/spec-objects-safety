---
id: EST-001
title: "PreControlEstimateOfDecelerationSituation"
type: risk_estimate
object: risk_estimate
phase: <pre_control | post_control>
---
<!-- risk_estimate authoring skeleton (spec-objects-safety). THIS SKELETON FAILS
     VALIDATION AS SHIPPED, ON PURPOSE: the phase, severity, probability,
     rationale and provenance are placeholders that a person replaces. No tool
     fills them, defaults them or derives them. Contract (manifest
     body_extraction asserts):
     - Frontmatter MUST carry id, title, type: risk_estimate,
       object: risk_estimate and `phase`, exactly `pre_control` or
       `post_control`. `phase` is a top-level frontmatter key so that required
       relations can select on it.
     - "## Estimate" (H2) is REQUIRED: a table with headers exactly
       Severity | Probability | Rationale and exactly one data row.
     - "## Provenance" (H2) is REQUIRED: a table with headers exactly
       Asserted by | Asserted at and exactly one data row. Asserted at is a
       date or UTC timestamp.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     AN ESTIMATE IS ONE PERSON'S JUDGEMENT of how bad (severity) and how likely
     (probability) the harm is for ONE hazardous situation. The levels are the
     words of your project's acceptability policy; this module fixes no list.
     Write `unknown`, `not_assessed` or `not_applicable` when you have not
     scored an axis. Never write the safe end of a scale instead.

     NO SCORE, REGION, LEVEL, ACCEPTABLE OR ACCEPTANCE is recorded here, and no
     tool computes one. Whether a risk is acceptable is decided on the
     residual-risk record by a named person.

     LINK THE ESTIMATE with relationships in the frontmatter. `estimates` names
     the hazardous situation; a `post_control` estimate also names each control
     it assumes with `assumes`:

       relationships:
         - target: SIT-001
           type: estimates
         - target: CTRL-001
           type: assumes -->
# [EST-001] PreControlEstimateOfDecelerationSituation

## Estimate

| Severity | Probability | Rationale |
| -------- | ----------- | --------- |
| <severity> | <probability> | <why this person judges it so> |

## Provenance

| Asserted by | Asserted at |
| ----------- | ----------- |
| <person> | <date or UTC timestamp> |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| estimate_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

## Invariants

The clauses this risk-estimate declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### EstimateCarriesNoScore

```ocl
context RiskEstimate
inv EstimateCarriesNoScore:
  self.score->isEmpty()
```
