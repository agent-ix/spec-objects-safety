---
id: FR-405
title: "The tension record is optional input that a planning workflow can emit and a design gate can read"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-404"
    type: "depends_on"
---
# FR-405: The tension record is optional input that a planning workflow can emit and a design gate can read

## Description

Tracked by Linear PLAT-1480. This module offers the `tension` record as an output contract for
planning workflows to emit and for a design-gate loop to read as optional input. The workflows
and the loop are owned by other modules; this FR binds only what this module's record and rules
do with whatever they produce.

## Inputs

- `tension` records in the corpus, from any author.

## Outputs

- No output of its own.

## Behavior

- The module SHALL treat a corpus with no `tension` record as complete input and raise no tension
  finding of any kind.
- The module SHALL validate an emitted `tension` with `status: open` and two `conflicts_with`
  entries, and report it under `trace:open-tension`.
- The module SHALL declare no workflow definition and no gate behaviour.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-405-CON-1 | No workflow definition SHALL live in this module's object-type vocabulary. | Architecture | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-405-AC-1 | A corpus with no `tension` records raises no tension finding of any kind. | Test |
| FR-405-AC-2 | An emitted `tension` with `status: open` and two `conflicts_with` entries validates and is reported by FR-404-AC-1. | Test |

## Dependencies

- **Upstream**: [FR-404](./FR-404-tension-completeness-rule.md)
- **Downstream**: planning workflows and the design-gate loop, owned by other modules.
