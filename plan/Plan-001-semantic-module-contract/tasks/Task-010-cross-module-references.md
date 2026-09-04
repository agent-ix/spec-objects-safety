---
id: Task-010
title: "FR-006 — reference the neighbours, redeclare none of them"
type: Task
status: done
track: B
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-006
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-060
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-061
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-062
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-063
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-064
    type: verifies
---
# Task-010: FR-006 — reference the neighbours, redeclare none of them

## Scope

Hold the line at the module boundary: two object types, no neighbour's type
redeclared, no safety-only synonym minted, and an `imports` map that is empty for a
stated reason rather than aspirational.

## Subtasks

- [x] **Two types.** `hazard` and `failure_mode`, and nothing `spec-objects-security`, `-architecture` or `-operational` owns.
- [x] **Reference shape.** Every cross-module reference is a `SemanticId`; no `controls` or `mitigations` key.
- [x] **Imports.** `{}`, with the three open migration issues named in the manifest.
- [x] **Vocabulary.** Every `allowed_links` and `traceability` verb exists in the iso vocabulary, and neither `causes` nor `contributes_to` reappears.

## Deliverables

- `tests/test_cross_module_references.py`
- The `semantic.imports` comment in the manifest

## Notes

- The module was founded on the finding that `arises_from` already said what `causes` would. This task is what keeps that true through a migration that touched every other part of the manifest.
