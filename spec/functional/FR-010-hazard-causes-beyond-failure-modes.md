---
id: FR-010
title: "A hazard can arise from SOUP, threat, vulnerability and control causes, and a failure mode can name its part"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-006"
    type: "depends_on"
---
# FR-010: A hazard can arise from SOUP, threat, vulnerability and control causes, and a failure mode can name its part

## Description

Tracked by Linear PLAT-1833. A hazard is reached by more than a failing
component. A defect or known anomaly in third-party software (a SOUP record), an
adversary action (a threat), a weakness (a vulnerability) and a risk control that
itself introduces a new hazard are all recognised causes in software and
medical-device risk management. Admitting only `failure_mode` as a cause forced
authors to wrap each of those in an invented failure mode, or to leave the
cause out of the chain.

The module SHALL admit `soup_record`, `threat`, `vulnerability` and `control`
as `arises_from` targets of a `hazard`, beside `failure_mode`. A failure mode
SHALL allow a reference to the `part` it sits in, so the chain reaches a
software item. The types are owned by other modules and are named by reference
only (FR-006); this module declares none of them and mints no verb.

People record the causal link. The module never scores, classifies or judges a
cause, and never decides acceptability.

## Inputs

- The manifest `object_types` entries for `hazard` and `failure_mode`.
- `soup_record`, `threat`, `vulnerability` and `control` from `agent-ix/spec-objects-security`; `part` (role `systems-part`) from `agent-ix/spec-objects-architecture`.

## Outputs

- `hazard.allowed_links.arises_from` listing the five cause types.
- `failure_mode.allowed_links.references` listing the `systems-part` role.

## Behavior

- The `hazard` type SHALL allow `arises_from` to each of `failure_mode`, `soup_record`, `threat`, `vulnerability` and `control`.
- When a hazard arises from a `control`, the module SHALL accept the edge authored on the hazard and SHALL leave the control's own `mitigates` edge unchanged.
- The `failure_mode` type SHALL allow `references` to the `systems-part` role, which `part` carries, in addition to its existing targets.
- The module SHALL use the existing `arises_from` and `references` verbs and add no verb.
- The module SHALL NOT make a cause required: a hazard with no `arises_from` edge stays valid.
- The module SHALL keep the direction and verb of every edge the `traceability` model declares, with `arises_from` acyclic.
- No schema key SHALL carry a severity, likelihood or acceptability for a cause.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | The `hazard` `arises_from` target list is exactly `failure_mode`, `soup_record`, `threat`, `vulnerability`, `control`. | Test |
| FR-010-AC-2 | The `failure_mode` `references` target list contains the `systems-part` role (the role of the `part` type), `failure_mode` and `hazard`. | Test |
| FR-010-AC-3 | The manifest declares no object type named `soup_record`, `threat`, `vulnerability`, `control` or `part`, and no new edge verb is added. | Test |
| FR-010-AC-4 | `failure_mode` still declares no `arises_from`, and `arises_from` is still the only acyclic edge. | Test |
| FR-010-AC-5 | A hazard document with one `arises_from` edge to each of the five cause types passes `quire validate` under the module without an edge-type diagnostic. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-safety-object-types.md), [FR-006](./FR-006-cross-module-references.md)
- **Downstream**: [FR-301](./FR-301-hazard-reaches-harm-through-situation.md)
