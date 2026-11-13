---
id: FR-102
title: "A residual risk's estimate levels are checked against the policy's declared levels"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
---
# FR-102: A residual risk's estimate levels are checked against the policy's declared levels

## Description

Tracked by Linear PLAT-1523. A residual risk (FR-103) references a
post-control risk estimate. The tooling SHALL check that the severity and
probability recorded on that estimate are members of the referenced policy's
level lists, and SHALL report the region the policy names for that pairing as
a lookup. A lookup reads a cell a person wrote; it is not a computation and
yields no score.

## Inputs

- A residual-risk record (FR-103), its referenced post-control risk estimate, and its referenced `acceptability_policy`.

## Outputs

- A finding when a level is not a policy member or is an epistemic marker; otherwise the policy's own region label for the pairing, presented as "the policy says".

## Behavior

- If the estimate's severity or probability is not in the policy's level lists, then the check SHALL report a finding `level-not-in-policy` naming the level and the policy.
- If the estimate's severity or probability is `unknown`, `not_assessed` or `not_applicable` (FR-004), then the check SHALL report a finding `level-not-assessed` naming the marker.
- If either finding is reported, then the check SHALL report no region for that residual risk.
- The check SHALL NOT substitute a level for an epistemic marker.
- The check SHALL NOT combine, rank, weight or average levels.
- The check SHALL NOT produce a number.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-102-AC-1 | For a fixture whose estimate levels exist in the referenced policy, the report shows exactly the region label written in that policy cell. | Test |
| FR-102-AC-2 | For a fixture whose severity is not in the policy's list, the report contains a `level-not-in-policy` finding naming that level and the policy, and no region. | Test |
| FR-102-AC-3 | For a fixture whose probability is `not_assessed`, the report contains one `level-not-assessed` finding naming `not_assessed`, no region, and no substituted level. | Test |
| FR-102-AC-4 | The same holds for `unknown` and for `not_applicable`, each yielding a `level-not-assessed` finding. | Test |
| FR-102-AC-5 | Over every fixture, no report field holds a computed numeric value; the report schema declares none. | Inspection |

## Dependencies

- **Upstream**: [FR-101](./FR-101-acceptability-policy.md), [FR-103](./FR-103-residual-risk-record.md), [FR-004](./FR-004-type-distinct-safety-schemas.md)
- **Downstream**: [FR-105](./FR-105-decision-policy-discrepancy-report.md)
