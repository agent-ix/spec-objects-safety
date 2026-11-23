---
id: FR-109
title: "A risk management review names its reviewer, states plan execution and post-production readiness, and references the overall residual-risk evaluation"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-107"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-108"
    type: "depends_on"
---
# FR-109: A risk management review names its reviewer, states plan execution and post-production readiness, and references the overall residual-risk evaluation

## Description

Tracked by Linear EA-140. Before release, the people responsible review the
risk management work: was the plan carried out, is the overall residual risk
evaluated, and are the production and post-production methods in place. The
module SHALL declare a `risk_management_review` object type that records that
review as the reviewer's own statement.

The review holds a reference to the overall evaluation, never the evaluation.
The evaluation is the `overall_residual_risk_evaluation`
([FR-107](./FR-107-overall-residual-risk-evaluation.md)) that people decided;
the review names it with a `references` relationship. The plan that was
executed is the `risk_management_plan` ([FR-108](./FR-108-risk-management-plan.md)),
which the review names with a `reviews` relationship. People accept risk. The review records no score, class,
acceptability or approval of its own, and the module ships no review.

## Inputs

- A document of type `risk_management_review` authored by a person.
- The module manifest and the emitted schema for the type.

## Outputs

- A validated review document, or a validation failure naming the offending table and, for a cell, its column.
- A warning, `review-without-plan`, naming a review that has no `reviews` edge to a `risk_management_plan`.
- A warning, `review-without-overall-evaluation`, naming a review that has no `references` edge to an `overall_residual_risk_evaluation`.

## Behavior

- The `risk_management_review` type SHALL require a Review table with exactly one data row and the columns `Reviewer`, `Plan executed`, `Post-production readiness` and `Statement`.
- The `Reviewer` cell SHALL be the name of a person, non-empty and not a placeholder.
- The `Plan executed` cell SHALL be exactly `yes`, `partly` or `no`, with no default.
- The `Post-production readiness` cell SHALL be exactly `ready` or `not_ready`, with no default.
- The `Statement` cell SHALL be non-empty and not a placeholder.
- If a Review cell is empty or an unfilled placeholder, then validation SHALL fail naming the table and the column.
- The type SHALL allow `reviews` edges to `risk_management_plan` documents and `references` edges to `overall_residual_risk_evaluation` documents, and no other target type for these two edges.
- If a review has no `reviews` edge to a `risk_management_plan`, then the tooling SHALL report `review-without-plan` naming the review, as a warning.
- If a review has no `references` edge to an `overall_residual_risk_evaluation`, then the tooling SHALL report `review-without-overall-evaluation` naming the review, as a warning.
- The tooling SHALL NOT derive `Plan executed`, `Post-production readiness` or the review's outcome from the referenced records.
- The schema SHALL NOT declare a score, class, acceptability or approval property.
- The module SHALL NOT ship a review document.
- The skeleton SHALL carry a placeholder in every review cell.
- The skeleton SHALL fail validation until a person fills every review cell.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-109-AC-1 | The emitted manifest declares a `risk_management_review` type whose required `review` locator asserts the four columns and exactly one row, and whose allowed edges are `reviews` to `risk_management_plan` and `references` to `overall_residual_risk_evaluation`. | Test |
| FR-109-AC-2 | The skeleton with every placeholder filled validates, and the skeleton as shipped fails validation. | Test |
| FR-109-AC-3 | For each of the four cells, a fixture with that cell left as a placeholder fails validation naming the `review` table and that column. | Test |
| FR-109-AC-4 | A `Plan executed` value outside `yes`, `partly`, `no` and a `Post-production readiness` value outside `ready`, `not_ready` each fail validation naming the column. | Test |
| FR-109-AC-5 | A review with a `reviews` edge to a `risk_management_plan` and a `references` edge to an `overall_residual_risk_evaluation` validates without either warning; a review lacking the first yields `review-without-plan` once and one lacking the second yields `review-without-overall-evaluation` once, each naming the review. | Test |
| FR-109-AC-6 | A `references` or `reviews` edge from a review to a `hazard` document is disallowed, naming the type. | Test |
| FR-109-AC-7 | Neither the emitted schema, the manifest's review locator and columns, nor the skeleton's headings and table headers declare a score, class, acceptability or approval, and the package contains no document of type `risk_management_review` other than the unfilled skeleton. | Test |
| FR-109-AC-8 | A review that says `yes` and `ready` and references an evaluation that is `not_accepted` yields no finding about the evaluation's decision, and a review that says `no` yields no finding about the evaluation. | Test |

## Dependencies

- **Upstream**: [FR-107](./FR-107-overall-residual-risk-evaluation.md), [FR-108](./FR-108-risk-management-plan.md)
- **Downstream**: engineering-assurance FR-048 (the release decision presents this record).
