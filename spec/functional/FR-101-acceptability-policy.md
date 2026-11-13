---
id: FR-101
title: "An acceptability policy is a project-authored table of levels and the region each cell belongs to"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: "depends_on"
---
# FR-101: An acceptability policy is a project-authored table of levels and the region each cell belongs to

## Description

Tracked by Linear PLAT-1523. The module SHALL declare an `acceptability_policy`
object type: a table, written by a person for one project, that lists
severity levels, probability levels (the members of the `Likelihood` scale or
project-named levels), and regions, and gives for every severity and
probability pairing the one region it belongs to. Each region carries a flag,
`outside_acceptable`, that the project's people set to say whether pairings in
that region fall outside the acceptable region. The policy is data. The module
ships no policy, no default levels, no default regions, no default flag value
and no example values that a tool could fall back to.

In this requirement set, "the acceptable region" means exactly the regions
whose `outside_acceptable` flag is `false`, and "outside the acceptable
region" means exactly the regions whose flag is `true`. A three-region policy
(acceptable, further control required, unacceptable) therefore has two regions
with the flag `true`. No requirement here reads the word as anything else.

Estimated severity and probability come from the risk-estimate objects
(FR-203, FR-204 of the harm and risk-estimate requirements, PLAT-1409); the
policy only names the levels they are matched against.

## Inputs

- A document of type `acceptability_policy` authored by a person.
- The module manifest and the emitted schema for the type.

## Outputs

- A validated policy document, or a validation failure naming the offending row, region or column.

## Behavior

- The `acceptability_policy` type SHALL require a severity level list, a probability level list, a region list, and a cell table.
- Each entry in the region list SHALL require a name and an `outside_acceptable` flag of `true` or `false`.
- The schema SHALL declare no default for `outside_acceptable`; an entry without it SHALL fail validation naming the region.
- The cell table SHALL carry one row per severity and probability pairing, each naming exactly one region from the region list.
- If a policy omits a pairing, repeats a pairing, or names a region absent from the region list, then validation SHALL fail naming that pairing.
- If a policy repeats a level name within a list, then validation SHALL fail naming the level.
- The module SHALL NOT ship a policy document, a default region assignment, or a region fallback for a missing cell.
- The skeleton SHALL contain placeholders only.
- The skeleton SHALL fail validation until a person fills every cell and every flag.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-101-AC-1 | The emitted manifest declares an `acceptability_policy` type whose schema requires severity levels, probability levels, regions with `outside_acceptable`, and cells. | Test |
| FR-101-AC-2 | A fixture policy with 3 severity levels, 3 probability levels, 3 regions each carrying an `outside_acceptable` flag, and 9 cells each naming a listed region, validates. | Test |
| FR-101-AC-3 | The same fixture with one cell removed fails validation and the diagnostic names the missing severity and probability pairing. | Test |
| FR-101-AC-4 | A fixture with a duplicated pairing, or a cell naming a region not in the region list, fails validation naming the pairing. | Test |
| FR-101-AC-5 | A fixture repeating a level name in one list fails validation naming the level. | Test |
| FR-101-AC-6 | The package contains no document of type `acceptability_policy` other than the unfilled skeleton, and the unfilled skeleton fails validation. | Inspection |
| FR-101-AC-7 | The fixture with one region's `outside_acceptable` removed fails validation naming that region, and the emitted schema declares no default for the property. | Test |
| FR-101-AC-8 | A fixture with 3 regions, two flagged `true` and one `false`, validates, so more than one region can lie outside the acceptable region. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-type-distinct-safety-schemas.md); the risk-estimate objects (PLAT-1409), referenced only as the source of the estimated levels.
- **Downstream**: [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-103](./FR-103-residual-risk-record.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md)
