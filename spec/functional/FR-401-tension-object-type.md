---
id: FR-401
title: "The module declares tension as an object type for conflicting requirements"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/StR-401"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "depends_on"
---
# FR-401: The module declares tension as an object type for conflicting requirements

## Description

Tracked by Linear PLAT-1480. The module SHALL declare a `tension` object type: a record that
two or more clauses or requirements are in conflict, with a status, a link to what closed it,
and, when a person chose to live with it, that person's name. The module enumerates its object
types in the manifest; `tension` joins `hazard`, `failure_mode` and the types of the sibling
Risk Model requirements, and FR-001, FR-003 and FR-006 are amended to say so.

## Inputs

- The `semantic` block and `object_types` list of the manifest (FR-003).
- The person-acceptance contract of FR-103 (`decided_by`).

## Outputs

- A `tension` entry in `object_types` and in `semantic.exports`, an emitted `Tension.json`
  schema, and an executable skeleton, under FR-002 and FR-005.

## Behavior

- The module SHALL declare `tension` as an object type and export it.
- The `tension` schema, skeleton and vocabulary SHALL use no term taken from a particular
  standard, regulator or product line.
- A `tension` record SHALL carry a required `status` frontmatter field whose members are exactly
  `open`, `resolved-by-design` and `accepted-by-person`.
- A `tension` record SHALL NOT reuse `LifecycleStatus`; its three members describe the disposition
  of a conflict, not the life of a safety judgement.
- A `tension` record SHALL carry a required prose `Conflict` section stating, in a sentence
  each, the reading each party demands and why they cannot both hold.
- The `tension` schema SHALL NOT carry a date, a revision list or a copy of a person's identity
  beyond `decided_by`; who recorded it and when comes from the version-control history of its file.
- The `tension` schema SHALL NOT carry a severity, a likelihood or any other score.
- A `tension` record that omits `status` SHALL fail validation, so that "open" is always a
  statement and never an accident.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-401-CON-1 | The module SHALL declare the type with the existing manifest object-type grammar and add no new engine mechanism. | Architecture | Inspection |
| FR-401-CON-2 | The type SHALL NOT quote or name text from a paywalled standard. | Licensing | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-401-AC-1 | The manifest declares `tension` as an object type and exports it, and a `Tension.json` schema is emitted for it. | Test |
| FR-401-AC-2 | A `tension` record validates with `status` set to each of `open`, `resolved-by-design` and `accepted-by-person` (given each state's other required fields), and fails with any other `status` value. | Test |
| FR-401-AC-3 | A `tension` record with no `status` fails validation. | Test |
| FR-401-AC-4 | The emitted `Tension.json` has no property for severity, likelihood, a date or a history list. | Inspection |
| FR-401-AC-5 | The `tension` skeleton validates, and an edited copy with its `Conflict` section removed fails. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-103](./FR-103-residual-risk-record.md)
- **Downstream**: [FR-402](./FR-402-tension-edges.md), [FR-403](./FR-403-tension-state-validation.md), [FR-404](./FR-404-tension-completeness-rule.md)
