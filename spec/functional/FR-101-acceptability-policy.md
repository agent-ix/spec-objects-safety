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
severity levels, probability levels, and for every severity and probability
pairing the region the pairing belongs to (for example acceptable, further
control required, unacceptable). The policy is data. The module ships no
policy, no default levels, no default regions and no example values that a
tool could fall back to.

The severity and probability levels are those the project chooses; the policy
names them. Severity and probability as estimated on a risk are produced by the
risk-estimate objects, which are specified elsewhere and are referenced here
only as "the risk estimate".

## Inputs

- A document of type `acceptability_policy` authored by a person.
- The module manifest and the emitted schema for the type.

## Outputs

- A validated policy document, or a validation failure naming the offending row or column.

## Behavior

- The `acceptability_policy` type SHALL require a severity level list, a probability level list, a region list, and a cell table.
- The cell table SHALL carry one row per severity and probability pairing, each naming exactly one region from the region list.
- The module SHALL NOT ship a policy document, a default region assignment, or a region fallback for a missing cell.
- If a policy omits a pairing, repeats a pairing, or names a region absent from the region list, then validation SHALL fail naming that pairing.
- If a policy repeats a level name within a list, then validation SHALL fail naming the level.
- The skeleton SHALL contain placeholders only and SHALL fail validation until a person fills every cell.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-101-AC-1 | The emitted manifest declares an `acceptability_policy` type whose schema requires severity levels, probability levels, regions and cells. | Test |
| FR-101-AC-2 | A fixture policy with 3 severity levels, 3 probability levels and 9 cells, each naming a listed region, validates. | Test |
| FR-101-AC-3 | The same fixture with one cell removed fails validation and the diagnostic names the missing severity and probability pairing. | Test |
| FR-101-AC-4 | A fixture with a duplicated pairing, or a cell naming a region not in the region list, fails validation naming the pairing. | Test |
| FR-101-AC-5 | A fixture repeating a level name in one list fails validation naming the level. | Test |
| FR-101-AC-6 | The package contains no document of type `acceptability_policy` other than the unfilled skeleton, and the unfilled skeleton fails validation. | Inspection |

## Dependencies

- **Upstream**: [FR-004](./FR-004-type-distinct-safety-schemas.md); the risk-estimate objects (specified separately), referenced only as the source of the estimated levels.
- **Downstream**: [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md)
