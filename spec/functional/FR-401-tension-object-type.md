---
id: FR-401
title: "The module declares tension as an object type for conflicting requirements"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "depends_on"
---
# FR-401: The module declares tension as an object type for conflicting requirements

## Description

The module SHALL declare a `tension` object type: a record that two or more clauses or
requirements are in conflict, with a status, a link to what closed it, and, when a person
chose to live with it, that person's name. Source: PLAT-1480.

## Inputs

- The `semantic` block and `object_types` list of the manifest (FR-003).
- The shared status and provenance models of FR-004 (`Provenance`).

## Outputs

- A `tension` entry in `object_types` and in `semantic.exports`, an emitted `Tension.json`
  schema, and an executable skeleton, under FR-002 and FR-005.

## Behavior

- The module SHALL declare `tension` as a third object type beside `hazard` and `failure_mode`.
- The `tension` schema, skeleton and vocabulary SHALL use no term taken from a particular
  standard, regulator or product line.
- A `tension` record SHALL carry a required `status` whose members are exactly `open`,
  `resolved-by-design` and `accepted-by-person`.
- A `tension` record SHALL NOT reuse `LifecycleStatus`; its three members describe a
  disposition of a conflict, not the life of a safety judgement.
- A `tension` record SHALL carry a required prose `Conflict` section stating, in a sentence
  each, the reading each party demands and why they cannot both hold.
- A `tension` record SHALL carry `Provenance` (FR-004) naming who recorded it and when.
- The `tension` type SHALL NOT carry a severity, a likelihood or any other score. A tension
  is a conflict between statements; it is not a risk estimate.
- A newly authored `tension` SHALL default to nothing: an author who omits `status` is
  rejected, so that "open" is always a statement and never an accident.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-401-CON-1 | The module SHALL declare the type with the existing manifest object-type grammar and add no new engine mechanism. | Architecture | Inspection |
| FR-401-CON-2 | The type SHALL NOT quote or name text from a paywalled standard. | Licensing | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-401-AC-1 | The manifest declares `tension` as an object type and exports it, and a `Tension.json` schema is emitted for it. | Test |
| FR-401-AC-2 | A `tension` record validates with `status` set to each of `open`, `resolved-by-design` and `accepted-by-person` (given each state's other required fields), and is rejected with any other `status` value. | Test |
| FR-401-AC-3 | A `tension` record with no `status` is rejected. | Test |
| FR-401-AC-4 | A `tension` record carrying a severity or likelihood key is rejected by the schema seal. | Test |
| FR-401-AC-5 | The `tension` skeleton validates, and an edited copy with its `Conflict` section removed is rejected. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-type-distinct-safety-schemas.md)
- **Downstream**: [FR-402](./FR-402-tension-edges.md), [FR-403](./FR-403-tension-state-validation.md), [FR-404](./FR-404-tension-completeness-rule.md)
