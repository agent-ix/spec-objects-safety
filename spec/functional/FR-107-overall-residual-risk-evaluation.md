---
id: FR-107
title: "An overall residual-risk evaluation for the product is decided by a named person"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-106"
    type: "depends_on"
---
# FR-107: An overall residual-risk evaluation for the product is decided by a named person

## Description

Tracked by Linear PLAT-1523. Beyond each individual risk, a product needs one
recorded judgement of whether the residual risk taken together is acceptable.
The module SHALL declare an `overall_residual_risk_evaluation` object type:
the product it concerns, the residual risks and benefit-risk records it
considers, a decision, a rationale, and the person who decided. The tooling
does not aggregate the individual risks into the verdict.

The product is named by the evaluation's `product` field, a non-empty string.
The bundle being validated is the product: every `residual_risk` document
loaded in that bundle belongs to the product. The evaluation's list is what
the person considered; the bundle is what exists.

## Behavior

- The type SHALL require a `product` string, a decision of `undecided`, `accepted` or `not_accepted`, a rationale, and a list of considered `residual_risk` and `benefit_risk` references.
- If `decision` is `accepted` or `not_accepted`, then the schema SHALL require a non-empty `decided_by`.
- If `decision` is `undecided`, then the schema SHALL reject `decided_by`.
- If a `residual_risk` document in the bundle is not in the considered list, then the tooling SHALL report `residual-risk-not-considered` naming it, as a warning.
- If the evaluation is `accepted` and a considered residual risk is `undecided` or `not_accepted`, then the tooling SHALL report `evaluation-accepted-with-open-risk` naming those risks, as a warning.
- The tooling SHALL NOT derive the evaluation decision from the considered records.
- The schema SHALL NOT declare a computed total, score or date.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-107-AC-1 | A fixture evaluation with product, considered records, `accepted`, rationale and `decided_by` validates. | Test |
| FR-107-AC-2 | A decided evaluation without `decided_by` fails; an `undecided` one with `decided_by` fails. | Test |
| FR-107-AC-3 | A fixture bundle with a `residual_risk` missing from the considered list yields one `residual-risk-not-considered` warning naming it. | Test |
| FR-107-AC-4 | An `accepted` evaluation over a considered `not_accepted` risk yields `evaluation-accepted-with-open-risk` naming that risk. | Test |
| FR-107-AC-5 | Given only decided-accepted considered records and no evaluation document, the tooling creates no evaluation and reports no accepted state. | Test |
| FR-107-AC-6 | The emitted schema declares no total, score or date property. | Inspection |
| FR-107-AC-7 | An `accepted` evaluation over a considered `undecided` risk yields `evaluation-accepted-with-open-risk` naming that risk. | Test |
| FR-107-AC-8 | An evaluation with an empty `product` string fails validation naming the field. | Test |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md), [FR-106](./FR-106-benefit-risk-record.md)
