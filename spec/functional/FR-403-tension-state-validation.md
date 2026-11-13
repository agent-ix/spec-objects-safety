---
id: FR-403
title: "Validation rejects a tension whose state lacks what that state requires"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-401"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
---
# FR-403: Validation rejects a tension whose state lacks what that state requires

## Description

Tracked by Linear PLAT-1480. The `tension` schema SHALL reject a record that claims a person's
acceptance without that person's name. It reuses the person-acceptance contract of FR-103: a
non-empty `decided_by`, with who and when taken from version-control history, and no second copy of
either. In particular an accepted tension without a named person never validates.

## Inputs

- A `tension` record: its `status` and its `decided_by`.

## Outputs

- A schema rejection, naming the missing field, for a record that claims a state it does not support.

## Behavior

- If `status` is `accepted-by-person`, then the schema SHALL require a non-empty `decided_by`.
- If `status` is `open` or `resolved-by-design`, then the schema SHALL reject `decided_by`.
- If `status` is `open`, then the schema SHALL reject any `resolved_by` relation entry, in the same relations array that FR-402 counts `conflicts_with` in.
- The schema SHALL NOT declare an acceptance date or a default for `status` or `decided_by`.
- The module SHALL NOT derive `decided_by` or `accepted-by-person` from other records.
- Agreement between `status: resolved-by-design` and a `resolved_by` edge is checked by the
  manifest relations of FR-404, not by this schema.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-403-CON-1 | Acceptance is a human act: nothing in this module sets `decided_by` or `status: accepted-by-person` on any record. | Safety | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-403-AC-1 | A record with `status: accepted-by-person` and no `decided_by` fails validation, naming `decided_by`. | Test |
| FR-403-AC-2 | A record with `status: accepted-by-person` and an empty `decided_by` fails validation. | Test |
| FR-403-AC-3 | A record with `status: accepted-by-person` and a named person in `decided_by` validates. | Test |
| FR-403-AC-4 | A record with `status: open` or `status: resolved-by-design` and a `decided_by` fails validation. | Test |
| FR-403-AC-5 | A record with `status: open` and a `resolved_by` relation entry fails validation. | Test |
| FR-403-AC-6 | The emitted `Tension.json` has no acceptance-date property and no default for `status` or `decided_by`. | Inspection |

## Dependencies

- **Upstream**: [FR-401](./FR-401-tension-object-type.md), [FR-103](./FR-103-residual-risk-record.md)
- **Downstream**: [FR-404](./FR-404-tension-completeness-rule.md)
