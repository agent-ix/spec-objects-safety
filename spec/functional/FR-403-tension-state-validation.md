---
id: FR-403
title: "Validation rejects a tension whose state lacks what that state requires"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-401"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-402"
    type: "depends_on"
---
# FR-403: Validation rejects a tension whose state lacks what that state requires

## Description

The `tension` schema SHALL reject a record that claims a status without the evidence that makes
it true. In particular an accepted tension without a named accepter never validates. Source: PLAT-1480.

## Inputs

- A `tension` record: its `status`, its `accepter`, its `relations` and its `Provenance`.

## Outputs

- A schema rejection, naming the missing field, for a record that claims a state it does not support.

## Behavior

- If `status` is `accepted-by-person`, then the record schema SHALL require an `accepter`
  carrying a non-empty `name` and an `acceptedAt` date, and a `relations` entry whose verb
  is `accepted_by`.
- The schema SHALL require `accepter.name` to be a person's name.
- The schema SHALL reject `unknown`, `not_assessed` and `not_applicable` as `accepter.name`.
- The module SHALL NOT derive `accepter` or `accepted-by-person` from other records. A person
  writes the name.
- If `status` is `resolved-by-design`, then the record schema SHALL require a `relations`
  entry whose verb is `resolved_by`.
- If `status` is `open`, then the record schema SHALL reject an `accepter`, so a half-finished
  acceptance is not left looking like an open conflict.
- The schema SHALL reject an `accepter` on a record whose `status` is `resolved-by-design`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-403-CON-1 | Acceptance is a human act: nothing in this module SHALL set `accepter` or `status: accepted-by-person` on any record. | Safety | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-403-AC-1 | A record with `status: accepted-by-person` and no `accepter` is rejected, naming `accepter`. | Test |
| FR-403-AC-2 | A record with `status: accepted-by-person` and an `accepter` whose `name` is empty is rejected. | Test |
| FR-403-AC-3 | A record with `status: accepted-by-person`, a named `accepter`, an `acceptedAt` and an `accepted_by` relation validates. | Test |
| FR-403-AC-4 | A record with `status: resolved-by-design` and no `resolved_by` relation is rejected; with the relation it validates. | Test |
| FR-403-AC-5 | A record with `status: open` and an `accepter` is rejected. | Test |
| FR-403-AC-6 | An `accepter` whose `name` is `unknown`, `not_assessed` or `not_applicable` is rejected. | Test |

## Dependencies

- **Upstream**: [FR-401](./FR-401-tension-object-type.md), [FR-402](./FR-402-tension-edges.md), [FR-004](./FR-004-type-distinct-safety-schemas.md)
- **Downstream**: [FR-404](./FR-404-tension-completeness-rule.md)
