---
id: FR-405
title: "Planning workflows may emit tensions; the design-gate loop consumes them as optional input"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-404"
    type: "depends_on"
---
# FR-405: Planning workflows may emit tensions; the design-gate loop consumes them as optional input

## Description

A planning workflow that notices conflicting clauses MAY emit `tension` records, and the
design-gate loop MAY read them. Neither side depends on the other existing. Source: PLAT-1480.

## Inputs

- `tension` records in the corpus.

## Outputs

- No output of its own: this FR constrains the contract between producer and consumer.

## Behavior

- A planning workflow MAY emit a `tension` with `status: open` and its `conflicts_with` edges.
- A workflow SHALL NOT emit `resolved-by-design` or `accepted-by-person`: resolution links a
  design element a person or the design loop supplies, and acceptance is a person's act (FR-403).
- The design-gate loop SHALL accept a corpus with no `tension` records as complete input;
  tensions are optional input and their absence is not a finding.
- When tensions are present, the design-gate loop SHALL read their status and edges and
  SHALL report every `open` tension to the person running the gate.
- The design-gate loop SHALL NOT mark a tension resolved or accepted on a person's behalf.
- The module SHALL declare only the record and the rule; the workflow modules own the
  definitions that emit and consume tensions.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-405-CON-1 | No workflow definition SHALL live in this module's object-type vocabulary. | Architecture | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-405-AC-1 | A corpus with no `tension` records raises no tension finding of any kind. | Test |
| FR-405-AC-2 | The `tension` schema rejects an `accepted-by-person` record with no accepter name, so an emitted acceptance without a person fails validation. | Test |
| FR-405-AC-3 | An emitted `tension` with `status: open` and two `conflicts_with` edges validates and is reported by FR-404-AC-1. | Test |

## Dependencies

- **Upstream**: [FR-404](./FR-404-tension-completeness-rule.md)
- **Downstream**: the design-gate loop and planning workflows, owned elsewhere.
