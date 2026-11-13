---
id: FR-104
title: "The module's tooling computes, stores and defaults no score, region verdict or acceptance"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
---
# FR-104: The module's tooling computes, stores and defaults no score, region verdict or acceptance

## Description

Tracked by Linear PLAT-1523. Acceptance of residual risk is a human decision.
The tooling this module ships (its validation, extraction and reports) SHALL
leave the score, the region assignment and the acceptance to the people who
authored them. It may read what a person wrote and report disagreement
(FR-105); it SHALL NOT originate a verdict.

## Inputs

- Any authored `acceptability_policy`, `residual_risk`, `benefit_risk` and `overall_residual_risk_evaluation` document.

## Outputs

- Validation results and reports only; no changed document.

## Behavior

- The module's tooling SHALL NOT write or change a `decision`, `decided_by`, rationale or region field in any document.
- The module's tooling SHALL NOT derive a numeric score from severity and probability levels.
- The module's tooling SHALL NOT assign a region to a pairing the policy does not list.
- The module's tooling SHALL NOT set, infer or default an acceptance from a validation pass, a green check or the absence of findings.
- The module's report output SHALL state that region labels come from the project's policy and that decisions come from the named person.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-104-AC-1 | Running validation and the discrepancy report over fixtures leaves the bytes of every fixture file unchanged. | Test |
| FR-104-AC-2 | With a fixture `residual_risk` that has `decision: undecided` and an all-acceptable policy, the report contains no accepted state for that risk. | Test |
| FR-104-AC-3 | No emitted schema and no report schema of the module declares a numeric score, weight or total property, and the shipped package contains no `acceptability_policy` document other than the unfilled skeleton. | Inspection |
| FR-104-AC-4 | The report output for a fixture contains the attribution statement naming the policy as the source of regions and the named person as the source of decisions. | Test |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md)
