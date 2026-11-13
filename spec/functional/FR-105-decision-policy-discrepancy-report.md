---
id: FR-105
title: "The tooling reports where a recorded decision disagrees with the policy"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-102"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-104"
    type: "depends_on"
---
# FR-105: The tooling reports where a recorded decision disagrees with the policy

## Description

Tracked by Linear PLAT-1523. The tooling SHALL report, as advisory findings,
each place where a recorded residual-risk decision disagrees with the
region the policy lists for its levels. A finding is information for the
decider; it changes no record and settles no question.

The region that requires a benefit-risk record is declared in the policy by
the project (FR-101 region list). The policy marks which regions are
"outside the acceptable region"; the tooling reads that mark.

## Behavior

- If a residual risk is `accepted` and the policy region for its levels is marked outside the acceptable region and no benefit-risk record (FR-106) references that risk, then the tooling SHALL report `accepted-outside-acceptable-region`.
- If a residual risk is `accepted` and the region is outside the acceptable region and a benefit-risk record references it but that record is `undecided`, then the tooling SHALL report `benefit-risk-undecided`.
- If a residual risk is `not_accepted` and the region is marked acceptable, then the tooling SHALL report `not-accepted-inside-acceptable-region`.
- If a residual risk is `undecided`, then the tooling SHALL report `residual-risk-undecided`.
- If a residual risk's decision agrees with the policy, then the tooling SHALL report no discrepancy for it.
- Findings SHALL be warnings naming the residual-risk document, the decision, the policy region and the policy; a promote flag turns them into errors.
- Findings SHALL be deterministic for identical inputs.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-105-AC-1 | A fixture `accepted` residual risk in an outside-acceptable cell with no benefit-risk record yields exactly one `accepted-outside-acceptable-region` finding naming the document, `accepted`, the region and the policy. | Test |
| FR-105-AC-2 | Adding a decided benefit-risk record referencing that risk removes the finding. | Test |
| FR-105-AC-3 | A benefit-risk record with `decision: undecided` yields `benefit-risk-undecided` instead. | Test |
| FR-105-AC-4 | A `not_accepted` risk in an acceptable cell yields `not-accepted-inside-acceptable-region`. | Test |
| FR-105-AC-5 | An `undecided` risk yields `residual-risk-undecided` regardless of region. | Test |
| FR-105-AC-6 | An `accepted` risk in an acceptable cell yields no finding. | Test |
| FR-105-AC-7 | All findings exit 0 by default as warnings; with the promote flag the run exits non-zero. | Test |
| FR-105-AC-8 | Two runs over the same fixtures produce identical output. | Test |

## Dependencies

- **Upstream**: [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-103](./FR-103-residual-risk-record.md), [FR-104](./FR-104-no-computed-verdicts.md)
