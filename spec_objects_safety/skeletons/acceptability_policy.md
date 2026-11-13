---
id: POL-001
title: "ProjectAcceptabilityPolicy"
type: acceptability_policy
object: acceptability_policy
---
<!-- acceptability_policy authoring skeleton (spec-objects-safety). THIS
     SKELETON FAILS VALIDATION AS SHIPPED, ON PURPOSE: every level, region,
     flag and cell is a placeholder that your project's people replace. This
     module ships no policy, no default levels, no default regions and no
     default flag, and no tool fills one in. Contract (manifest body_extraction
     asserts):
     - Frontmatter MUST carry id, title, type: acceptability_policy,
       object: acceptability_policy.
     - "## Severity levels" (H2) is REQUIRED: header exactly `Severity level`,
       one row per level, at least one row.
     - "## Probability levels" (H2) is REQUIRED: header exactly
       `Probability level`, one row per level, at least one row.
     - "## Regions" (H2) is REQUIRED: header exactly
       `Region | Outside acceptable`, one row per region. `Outside acceptable`
       is exactly `true` or `false`, set by your people for each region.
       "The acceptable region" means the regions flagged `false`; any number
       of regions may be flagged `true`.
     - "## Cells" (H2) is REQUIRED: header exactly
       `Severity | Probability | Region`, one row for every severity and
       probability pairing, each naming exactly one listed region.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     The risk estimates' severity and probability values are matched against
     the level names written here; the policy only names the levels. -->
# [POL-001] ProjectAcceptabilityPolicy

## Severity levels

| Severity level |
| -------------- |
| <severity level> |

## Probability levels

| Probability level |
| ----------------- |
| <probability level> |

## Regions

| Region | Outside acceptable |
| ------ | ------------------ |
| <region> | <true or false> |

## Cells

| Severity | Probability | Region |
| -------- | ----------- | ------ |
| <severity level> | <probability level> | <region> |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| policy_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

## Invariants

The clauses this acceptability-policy declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### PolicyCarriesNoScore

```ocl
context AcceptabilityPolicy
inv PolicyCarriesNoScore:
  self.score->isEmpty()
```
