---
id: FR-104
title: "No tool computes, stores or defaults a score, a region verdict or an acceptance"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
---
# FR-104: No tool computes, stores or defaults a score, a region verdict or an acceptance

## Description

Tracked by Linear PLAT-1523. Acceptance of residual risk is a human decision.
Every tool built on these types SHALL leave the score, the region assignment
and the acceptance to the people who authored them. A tool may read what a
person wrote and report disagreement (FR-105); it SHALL NOT originate a
verdict.

## Behavior

- No tool SHALL write or change a `decision`, `decided_by`, rationale, or region field in any document.
- No tool SHALL derive a numeric score from severity and probability levels.
- No tool SHALL assign a region to a pairing the policy does not list.
- No tool SHALL set, infer or default an acceptance from a validation pass, a green check, or the absence of findings.
- The tooling's output SHALL state that region labels come from the project's policy and that decisions come from the named person.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-104-AC-1 | Running validation and the discrepancy report over fixtures leaves every fixture file byte-identical. | Test |
| FR-104-AC-2 | With a fixture `residual_risk` that has `decision: undecided` and an all-acceptable policy, the tooling's output contains no `accepted` state for that risk. | Test |
| FR-104-AC-3 | The module's source and emitted schemas contain no scoring function, no numeric weights table, and no default policy; a search of the package for such definitions returns none. | Inspection |
| FR-104-AC-4 | The report output for a fixture contains the attribution statement naming the policy as the source of regions and the named person as the source of decisions. | Test |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md)
