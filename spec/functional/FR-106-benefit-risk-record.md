---
id: FR-106
title: "A benefit-risk record links the risks, states the benefit and names the decider"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
---
# FR-106: A benefit-risk record links the risks, states the benefit and names the decider

## Description

Tracked by Linear PLAT-1523. Where a residual risk falls outside the acceptable
region (FR-101), the project can only accept it by weighing a benefit against
it. The module SHALL declare a `benefit_risk` object type recording that
weighing: the residual risks it covers, the benefit stated in the author's
words, a decision, a rationale, and the person who decided. As with FR-103,
who and when come from version-control history, not typed fields.

## Behavior

- The `benefit_risk` type SHALL require one or more references to `residual_risk` documents, a non-empty benefit statement, a `decision` of `undecided`, `accepted` or `not_accepted`, and a rationale.
- If `decision` is `accepted` or `not_accepted`, then the schema SHALL require a non-empty `decided_by`.
- If `decision` is `undecided`, then the schema SHALL reject `decided_by`.
- If a reference resolves to no loaded document, then validation SHALL fail naming the reference.
- If a reference resolves to a document of a type other than `residual_risk`, then validation SHALL fail naming the reference and the type.
- The schema SHALL NOT declare a computed ratio, a score, a date or a default decision.
- Whether a covered residual risk needs a benefit-risk record is reported by FR-105; the schema SHALL NOT require one.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-106-AC-1 | A fixture `benefit_risk` with two `residual_risk` references, a benefit, an `accepted` decision, a rationale and `decided_by` validates. | Test |
| FR-106-AC-2 | An empty references list, or an empty benefit statement, fails validation naming the field. | Test |
| FR-106-AC-3 | A decided record without `decided_by` fails; an `undecided` record with `decided_by` fails. | Test |
| FR-106-AC-4 | A reference to an id no loaded document declares fails validation naming that id. | Test |
| FR-106-AC-5 | The emitted schema declares no ratio, score, date or default decision property. | Inspection |
| FR-106-AC-6 | A reference that resolves to a `hazard` fails validation naming the reference and `hazard`. | Test |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md)
- **Downstream**: [FR-105](./FR-105-decision-policy-discrepancy-report.md), [FR-107](./FR-107-overall-residual-risk-evaluation.md)
