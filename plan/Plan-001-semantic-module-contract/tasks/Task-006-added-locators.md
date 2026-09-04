---
id: Task-006
title: "FR-003 — required:false locators for the sections the skeletons introduced"
type: Task
status: done
track: B
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-029
    type: verifies
---
# Task-006: FR-003 — required:false locators for the sections the skeletons introduced

## Scope

Add the `properties` and `invariants` section locators to both object types, both
`required: false`, so a 0.2.0 document with neither section stays valid.

## Subtasks

- [x] **Both types.** `properties` and `invariants` as `section_body` locators after their headings.
- [x] **Optional.** Both `required: false`, asserted against the baseline as *added* rather than changed.

## Deliverables

- The added locators in `spec_objects_safety/manifest.yaml`

## Notes

- This task is the only writer of the added locators; Task-004 is the only writer of the `semantic` block, the version and the `data_schema` values.
