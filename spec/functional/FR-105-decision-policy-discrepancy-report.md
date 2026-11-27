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
  - target: "ix://agent-ix/spec-objects-safety/FR-106"
    type: "depends_on"
---
# FR-105: The tooling reports where a recorded decision disagrees with the policy

## Description

Tracked by Linear PLAT-1523. The tooling SHALL report, as advisory findings,
each place where a recorded residual-risk decision disagrees with the
region the policy lists for its levels. A finding is information for the
decider; it changes no record and settles no question.

"Outside the acceptable region" is as defined in FR-101: the policy region
carries `outside_acceptable: true`. The region is the one FR-102 resolves.

A benefit-risk record "covers" a residual risk when it lists that risk
(FR-106). A residual risk outside the acceptable region is covered
acceptably when at least one covering benefit-risk record is `accepted`.

## Behavior

- If a residual risk is `accepted` or `not_accepted` and FR-102 resolves no region for it, then the tooling SHALL report `decision-without-region`.
- If a residual risk is `accepted`, its region has `outside_acceptable: true` and no benefit-risk record covers it, then the tooling SHALL report `accepted-outside-acceptable-region`.
- If a residual risk is `accepted`, its region has `outside_acceptable: true`, covering records exist and none is `accepted` and at least one is `undecided`, then the tooling SHALL report `benefit-risk-undecided`.
- If a residual risk is `accepted`, its region has `outside_acceptable: true`, covering records exist and all are `not_accepted`, then the tooling SHALL report `benefit-risk-not-accepted`.
- If a residual risk is `not_accepted` and its region has `outside_acceptable: false`, then the tooling SHALL report `not-accepted-inside-acceptable-region`.
- If a residual risk is `undecided`, then the tooling SHALL report `residual-risk-undecided`.
- If a residual risk's decision agrees with the policy, then the tooling SHALL report no discrepancy for it.
- The tooling SHALL report each finding as a warning naming the residual-risk document, the decision, the policy region and the policy.
- The tooling SHALL turn the warnings into errors only when the author passes a promote flag.
- The tooling SHALL produce identical findings for identical inputs.

## Acceptance Criteria

Quoin owns and tests the report findings under FR-155. The module specifies
the source record contract; see
[Quoin FR-155](https://github.com/agent-ix/quoin/blob/main/spec/functional/FR-155-risk-discrepancy-findings.md).

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-105-AC-7 | All findings exit 0 by default as warnings; with `--strict` the run exits non-zero. | Test |

## Dependencies

- **Upstream**: [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-103](./FR-103-residual-risk-record.md), [FR-104](./FR-104-no-computed-verdicts.md), [FR-106](./FR-106-benefit-risk-record.md)
