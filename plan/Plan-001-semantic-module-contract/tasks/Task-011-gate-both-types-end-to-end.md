---
id: Task-011
title: "Gate — both object types end to end, and the epistemic property"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-008
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-010
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-safety/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-039
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-045
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-048
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-049
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-050
    type: verifies
---
# Task-011: Gate — both object types end to end, and the epistemic property

## Scope

The quality gate: prove the whole chain works for both types before anything
downstream is built on it, and prove the property the module exists for.

## Subtasks

- [x] **Chain.** Skeleton → extraction → record → emitted schema, green for `hazard` and `failure_mode` in both Properties forms.
- [x] **Property.** Every scored axis admits its own scale and the three epistemic states, rejects a foreign scale's members, and shares no member with `EpistemicState`.
- [x] **Acceptance.** `status: accepted` without provenance is refused; `detection: none` and `detection: not_assessed` are distinct accepted values.
- [x] **Validation.** `quire validate` structurally clean over the bundle, and `quire coverage` reporting every matrix row backed.

## Deliverables

- A green `make test` and `make lint`
- `quire validate` exit 0, `quire coverage` 125/125

## Notes

- If this gate fails, the emitter recipe or the epistemic modelling is wrong and everything after it is wasted work. It passed on the first run.
