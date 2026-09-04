---
id: Task-002
title: "FR-004 — the two record models and the thirteen support models"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-035
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-036
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-037
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-038
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-039
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-041
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-043
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-044
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-045
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-046
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-047
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-071
    type: verifies
---
# Task-002: FR-004 — the two record models and the thirteen support models

## Scope

Declare `Hazard` and `FailureMode` as type-distinct sealed records, and the safety
vocabularies that carry the module's central property: an axis nobody scored can never
be read as a safe one.

## Subtasks

- [x] **Type distinction.** Each record requires `fields` with at least one identity item; `Hazard` admits `assessment`/`context` and forbids `analysis`; `FailureMode` admits `analysis` and forbids `assessment`/`context`; both forbid `operations` and every other key through the seal.
- [x] **Scales.** `Severity`, `Likelihood`, `Exposure`, `Controllability`, `Detection` and `LifecycleStatus` as closed enums with exactly the members FR-004's Inputs table states.
- [x] **Epistemic states.** `EpistemicState` = `unknown` | `not_assessed` | `not_applicable`, admitted on every scored axis and sharing no member with any scale.
- [x] **No inferred judgement.** No `default` anywhere; `status: accepted` requires a `provenance` naming `assertedBy` and `assertedAt`.
- [x] **No cause required.** `Hazard.relations` carries no minimum and no `contains`: the STPA case is a hazard with no failure mode behind it.
- [x] **References, not copies.** `EvidenceRef.target` is a `SemanticId` and `kind` stays an open string; no `controls` or `mitigations` key exists.

## Deliverables

- The safety models in `typespec/main.tsp`
- The fifteen emitted schemas under `spec_objects_safety/schemas/`

## Notes

- Every grammar item is a `$ref` to semantic-core; nothing here redeclares `FieldDecl`, `TypeRef`, `ConstraintDecl`, `RelationDecl` or `ClauseRef`.
- This is the task where a constraint would most easily be relaxed to make a stubborn fixture pass. The required/forbidden facts of every model are asserted as a table so a relaxation shows up as a diff.
- Unblocks: Task-003, Task-005.
