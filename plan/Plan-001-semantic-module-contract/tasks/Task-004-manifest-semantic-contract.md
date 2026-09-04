---
id: Task-004
title: "FR-003 — manifest 0.3.0, semantic block and reference-form data_schema"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-003
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-026
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-027
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-028
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-030
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-033
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-034
    type: verifies
---
# Task-004: FR-003 — manifest 0.3.0, semantic block and reference-form data_schema

## Scope

Turn `manifest.yaml` into a semantic module: version 0.3.0, the quoin FR-070
`semantic` block, and reference-form `data_schema` on both object types — without
changing a single 0.2.0 locator or one fact of the traceability model.

## Subtasks

- [x] **`semantic` block.** Exactly the nine admitted keys, `exports` naming both object types, `imports: {}` with the reason written in the file.
- [x] **Reference-form `data_schema`.** `{schema, digest}` per type, the digest written by the generator over the shipped bytes; no inline `data_schema` survives.
- [x] **Version.** `0.3.0`, bumped together with the `@jsonSchema` base in one commit.
- [x] **Locator preservation.** Every 0.2.0 locator keeps every facet, compared structurally against the Task-007 baseline.
- [x] **Traceability preservation.** The `traceability` model is compared fact for fact against the 0.2.0 bytes, because `spec-objects-security` reads it across the repository boundary.
- [x] **FR-035 gate.** Validate against the module-manifest schema at `spec-artifacts-iso` CR-012, with a drift test proving the pinned copy is the released schema plus exactly the CR-012 pointers.

## Deliverables

- `spec_objects_safety/manifest.yaml` at 0.3.0
- `tests/fixtures/module-manifest.schema.json` (pinned CR-012 copy)

## Notes

- An unknown `semantic` key drops every object type of the module and a wrong digest drops one type, both silently — measured, and carried as a strict expected failure on quire-rs#221 and #394.
- The pinned FR-035 copy exists only because no `spec-artifacts-iso` release carries CR-012 (#36). The drift test deletes the need for it the moment one does.
- Unblocks: Task-005, Task-006, Task-008, Task-009.
