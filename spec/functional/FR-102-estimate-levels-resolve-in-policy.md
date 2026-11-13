---
id: FR-102
title: "A risk estimate's levels are checked against the policy's declared levels"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "depends_on"
---
# FR-102: A risk estimate's levels are checked against the policy's declared levels

## Description

Tracked by Linear PLAT-1523. A residual risk records a post-control estimate.
The tooling SHALL check that the severity and probability levels recorded in
that estimate are members of the referenced policy's level lists, and SHALL
report the one cell and region the pairing names in the policy as a lookup.
A lookup reads a cell a person wrote; it is not a computation and yields no
score.

## Inputs

- A residual-risk record (FR-103) referencing an `acceptability_policy`.
- The referenced policy.

## Outputs

- A finding when a level is not a policy member; otherwise the policy's own region label for the pairing, presented as "the policy says".

## Behavior

- If the estimate's severity or probability is not in the policy's level lists, then the check SHALL report a finding naming the level and the policy, and SHALL report no region.
- If the estimate's severity or probability is an unassessed or unknown marker (FR-004), then the check SHALL report no region and SHALL NOT substitute any level.
- The check SHALL NOT combine, rank, weight, or average levels and SHALL NOT produce a number.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-102-AC-1 | For a fixture residual risk whose levels exist in the referenced policy, the report shows exactly the region label written in that policy cell. | Test |
| FR-102-AC-2 | For a fixture whose severity is not in the policy's list, the report contains a finding naming that level and the policy, and no region. | Test |
| FR-102-AC-3 | For a fixture whose probability is the not-assessed marker, the report contains no region and the finding does not name any substituted level. | Test |
| FR-102-AC-4 | Over every fixture, no report field holds a computed numeric value; the report schema declares none. | Inspection |

## Dependencies

- **Upstream**: [FR-101](./FR-101-acceptability-policy.md), [FR-103](./FR-103-residual-risk-record.md)
