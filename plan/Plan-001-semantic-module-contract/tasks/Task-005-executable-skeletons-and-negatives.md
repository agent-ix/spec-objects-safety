---
id: Task-005
title: "FR-005 — executable skeletons, sysml alternates and negative fixtures"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-048
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-049
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-050
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-051
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-052
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-053
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-054
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-055
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-056
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-058
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-059
    type: verifies
---
# Task-005: FR-005 — executable skeletons, sysml alternates and negative fixtures

## Scope

Rewrite both skeletons as documents the engine validates and extracts, add the `sysml`
alternates, and pin every named refusal with a fixture that fails for that reason.

## Subtasks

- [x] **Typed Properties.** One typed row per attribute with at least one `identity`, and a `sysml` fence alternate declaring exactly the same fields.
- [x] **Invariants.** One `### <clauseId>` per clause, each owning one `ocl` fence carrying a source span.
- [x] **One fact, one home.** No Properties row restates a column of the same type's `Assessment` or `Analysis` table.
- [x] **Negative fixtures.** Seven: no identity row on each type, both Properties forms, a non-`Identifier` type token, a hazard with no Assessment table, a clause heading with no fence, and an Analysis table missing `Detection`. Each declares `expect` and `because` and fails with detail beyond its token.
- [x] **Hygiene.** Placeholder-free, distinct `Identifier` titles outside the kernel scalars, `object` equal to `type`, every H2 a heading a locator names.

## Deliverables

- `spec_objects_safety/skeletons/{hazard,failure_mode}{,.sysml}.md`
- `tests/fixtures/negative/*.md` (7 files)

## Notes

- The typed-table Constraints cell grammar is comma-separated with `pattern: /re/` and `enumValues: a|b|c`; a `|` inside a Markdown cell must be escaped. Getting this wrong yields `semantic.unknown-constraint-keyword`, not a parse error.
- Unblocks: Task-006.
