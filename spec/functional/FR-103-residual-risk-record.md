---
id: FR-103
title: "A residual-risk record references the post-control estimate and holds the decision, a rationale and the decider"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
    type: "depends_on"
---
# FR-103: A residual-risk record references the post-control estimate and holds the decision, a rationale and the decider

## Description

Tracked by Linear PLAT-1523. The module SHALL declare a `residual_risk` object
type, one record per risk, holding the decision about what remains after
controls. The post-control severity and probability are not copied into it:
the record references the post-control `risk_estimate` (FR-204, PLAT-1409),
which is their one home, so two records cannot disagree about the same
judgement. The record adds a reference to the `acceptability_policy`, a
decision (`accepted` or `not_accepted`), a rationale and the person who
decided. Until a person decides, the record carries `undecided`, which is
distinct from both decisions.

When and by whom the decision was made comes from the version-control history
of the record's file (the commit author, and the signature where the
repository signs commits). The record SHALL NOT carry typed history, a
decision date, or a revision log.

### One acceptance record

The `residual_risk` decision is the record of acceptance for a residual risk.
The `status` and `provenance` that FR-004 lets a hazard carry are the hazard's
own lifecycle and are not a second acceptance of its residual risk. The
tooling reads no residual-risk meaning from a hazard's `status`, and a hazard
whose `status` is `accepted` does not make any residual risk accepted.

## Inputs

- A document of type `residual_risk` referencing one post-control `risk_estimate`, one `acceptability_policy` and the person's decision.

## Outputs

- A validated record, or a failure naming the missing field.

## Behavior

- The type SHALL require an `estimate` reference, a `policy` reference, a `decision` of `undecided`, `accepted` or `not_accepted`, and a rationale.
- The `estimate` reference SHALL resolve to a `risk_estimate` whose `phase` is `post_control`; a reference to any other type or phase SHALL fail validation naming the reference.
- The schema SHALL NOT carry severity or probability on the record.
- If `decision` is `accepted` or `not_accepted`, then the schema SHALL require a non-empty rationale.
- If `decision` is `accepted` or `not_accepted`, then the schema SHALL require a non-empty `decided_by`.
- If `decision` is `undecided`, then the schema SHALL reject `decided_by`.
- The schema SHALL NOT declare a decision timestamp, an author-history list, a computed region field, or a default for `decision`.
- A record that omits `decision` SHALL fail validation.
- The tooling SHALL NOT read a hazard's `status` as a residual-risk decision.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-103-AC-1 | A fixture `residual_risk` referencing a `post_control` estimate and a policy, with `decision: accepted`, a rationale and `decided_by`, validates. | Test |
| FR-103-AC-2 | The same fixture without `decided_by`, or with an empty rationale, fails validation naming the field. | Test |
| FR-103-AC-3 | A fixture with `decision: not_accepted`, rationale and `decided_by` validates; one with `decision: undecided` and no `decided_by` validates; `undecided` with a `decided_by` fails. | Test |
| FR-103-AC-4 | A fixture whose `estimate` references a `pre_control` estimate, or a document of another type, fails validation naming the reference. | Test |
| FR-103-AC-5 | A fixture omitting `decision` fails validation and no code path supplies a default value. | Test |
| FR-103-AC-6 | The emitted schema contains no property for severity, probability, a decision date, a history list, or a region. | Inspection |
| FR-103-AC-7 | Over a bundle with a hazard at `status: accepted` and a `residual_risk` at `undecided`, the tooling reports `residual-risk-undecided` (FR-105) and no accepted state for the risk. | Test |

## Dependencies

- **Upstream**: [FR-101](./FR-101-acceptability-policy.md), [FR-004](./FR-004-type-distinct-safety-schemas.md); FR-204 post-control risk estimate (PLAT-1409).
- **Downstream**: [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-104](./FR-104-no-computed-verdicts.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md), [FR-106](./FR-106-benefit-risk-record.md), [FR-107](./FR-107-overall-residual-risk-evaluation.md)
