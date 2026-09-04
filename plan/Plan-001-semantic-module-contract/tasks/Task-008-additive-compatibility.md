---
id: Task-008
title: "NFR-001 — additive compatibility and the widened advisory lists"
type: Task
status: done
track: B
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-065
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-066
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-067
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-068
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-069
    type: verifies
---
# Task-008: NFR-001 — additive compatibility and the widened advisory lists

## Scope

Prove nothing a 0.2.0 author wrote stopped working, and that widening the three
advisory lint allow-lists took nothing away.

## Subtasks

- [x] **Locators.** Zero 0.2.0 locators changed; every added one optional.
- [x] **Documents.** Every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors.
- [x] **Legacy form.** A prose `## Properties` block warns; the half that requires it not to also error is a strict expected failure on quire-rs#391.
- [x] **Traceability.** The model is unchanged fact for fact.
- [x] **Lint lists.** Each still admits every 0.2.0 value and now also admits the three epistemic tokens.

## Deliverables

- `tests/test_additive_compatibility.py`

## Notes

- Widening an advisory allow-list to admit `not_assessed` is not a relaxation: at 0.2.0 the only way past the advisory was to write a scale value, which is the collapse the module exists to prevent.
