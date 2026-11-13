---
id: FR-103
title: "A residual-risk record holds the post-control estimate, the decision, a rationale and the named decider"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: "depends_on"
---
# FR-103: A residual-risk record holds the post-control estimate, the decision, a rationale and the named decider

## Description

Tracked by Linear PLAT-1523. The module SHALL declare a `residual_risk` object
type, one record per risk, holding what remains after controls: the
post-control estimate, a decision (`accepted` or `not_accepted`), a rationale,
and the named person who decided. Until a person decides, the record carries
`undecided`, which is distinct from both decisions.

When and by whom the decision was made comes from the version-control history
of the record's file (the commit author, and the signature where the repository
signs commits). The record SHALL NOT carry typed history, a decision date, or a
revision log.

## Inputs

- A document of type `residual_risk` referencing the risk it concerns, an `acceptability_policy`, and the controls applied.

## Outputs

- A validated record, or a failure naming the missing field.

## Behavior

- The type SHALL require a reference to the risk, a reference to the policy, the post-control severity and probability levels (each possibly a not-assessed marker), a `decision` from `undecided`, `accepted`, `not_accepted`, and a rationale.
- If `decision` is `accepted` or `not_accepted`, then the schema SHALL require a non-empty rationale and a `decided_by` naming a person, and SHALL reject a value naming a role, team, or tool.
- If `decision` is `undecided`, then the schema SHALL forbid `decided_by`.
- The schema SHALL NOT declare a decision timestamp, an author-history list, a computed region field, or a default for `decision`.
- A record that omits `decision` SHALL fail validation; there is no implied acceptance.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-103-AC-1 | A fixture `residual_risk` with `decision: accepted`, a rationale and a person in `decided_by` validates. | Test |
| FR-103-AC-2 | The same fixture without `decided_by`, or with an empty rationale, fails validation naming the field. | Test |
| FR-103-AC-3 | A fixture with `decision: not_accepted`, rationale and person validates; one with `decision: undecided` and no `decided_by` validates; `undecided` with a `decided_by` fails. | Test |
| FR-103-AC-4 | A fixture with `decided_by` set to a team name or tool name from a configured non-person list fails validation. | Test |
| FR-103-AC-5 | A fixture omitting `decision` fails validation and no code path supplies a default value. | Test |
| FR-103-AC-6 | The emitted schema contains no property for a decision date, a history list, or a region. | Inspection |

## Dependencies

- **Upstream**: [FR-101](./FR-101-acceptability-policy.md), [FR-004](./FR-004-type-distinct-safety-schemas.md); the risk-estimate objects (specified separately).
- **Downstream**: [FR-104](./FR-104-no-computed-verdicts.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md), [FR-106](./FR-106-benefit-risk-record.md), [FR-107](./FR-107-overall-residual-risk-evaluation.md)
