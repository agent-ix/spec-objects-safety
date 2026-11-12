---
id: FR-007
title: "A mitigating document can declare a mitigates edge to a hazard or failure_mode"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/quire-cli/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-038"
    type: "depends_on"
---
# FR-007: A mitigating document can declare a mitigates edge to a hazard or failure_mode

## Description

The `hazard-has-mitigation` and `failure-mode-has-mitigation` relations demand
an **incoming** `mitigates` edge. That edge SHALL be authorable, by a document
that mitigates a safety object, with no advisory diagnostic.

### Which end authors it

The control end authors it. A `control` (owned by `agent-ix/spec-objects-security`)
declares `mitigates` and gains `hazard` and `failure_mode` among its targets. The
direction stays `incoming` on the safety side: a hazard never lists its own
mitigations, which would duplicate the fact and let the two drift.

The requirement-end alternative (`FR`/`NFR` archetypes in `spec-artifacts-iso`
gaining `mitigates`) is outside this module and `spec-objects-security`; this
module's relations accept whatever document declares the edge, because
`to: []` is unchanged.

### No relaxation

Widening the target set of `control.mitigates` adds two targets. It removes no
constraint, changes no verb and changes no direction, so this module's
`traceability` block (the two hazard-end relations) is untouched and its `compatibility_posture: additive`
holds. The `to: []` of both relations is not narrowed.

## Inputs

- A document of type `control` carrying a `mitigates` relationship whose target is a `hazard` or `failure_mode`.
- The `spec-objects-security` and `spec-objects-safety` manifests loaded together.

## Outputs

- No `disallowed-edge-target` and no `DisallowedEdgeType` diagnostic for that edge.
- A resolved incoming `mitigates` edge on the target.

## Behavior

- Quire SHALL accept a `control` document's `mitigates` edge to a `hazard` without a `disallowed-edge-target` diagnostic.
- Quire SHALL accept a `control` document's `mitigates` edge to a `failure_mode` without a `disallowed-edge-target` diagnostic.
- The manifest SHALL declare no outgoing `mitigates` on `hazard` or `failure_mode`, and no field listing their own mitigations.
- When a `mitigates` edge targets a bare id or an id under this repository's own authority that no loaded document declares, `quire validate --okf --strict` SHALL exit non-zero with a diagnostic naming the source document's path, the edge type and the missing target id (`agent-ix/quire-cli` FR-014-AC-11, `agent-ix/quire-rs` FR-038-AC-11). A target under a foreign authority is skipped, as those requirements state.
- If the target resolves to an object type outside the declared target set, then Quire SHALL report `disallowed-edge-target` naming the target's type.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | A fixture `control` with a `mitigates` frontmatter relationship to a fixture `hazard`, validated with both manifests loaded, produces no `disallowed-edge-target` and no `DisallowedEdgeType` diagnostic. | Test |
| FR-007-AC-2 | The same holds for a fixture `control` that mitigates a fixture `failure_mode`. | Test |
| FR-007-AC-3 | Running `quire validate --okf --strict` over a fixture bundle whose `control` has a `mitigates` relationship to an undeclared bare id exits non-zero, and stderr contains the control's file path, `mitigates` and the missing id. The behavior itself is specified upstream in `agent-ix/quire-cli` FR-014-AC-11; this criterion is this module's fixture evidence for it. | Test |
| FR-007-AC-4 | A fixture `control` that declares `mitigates` to a type outside the target set is still reported `disallowed-edge-target`, naming that type, so the widening admits exactly `hazard` and `failure_mode` and nothing else. | Test |

## Dependencies

- **Upstream**: [FR-006](./FR-006-cross-module-references.md); `agent-ix/spec-objects-security` FR-007, which must land first or together (the `control` target set); `agent-ix/quire-cli` FR-014-AC-11 and `agent-ix/quire-rs` FR-038-AC-11 (dangling-target failure). The fixture tests load the `spec-objects-security` module from its own checkout or git dependency; no file is copied.
- **Downstream**: [FR-008](./FR-008-mitigation-coverage-findings.md)
