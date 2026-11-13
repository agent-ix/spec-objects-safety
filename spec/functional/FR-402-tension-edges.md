---
id: FR-402
title: "A tension names the clauses in conflict and what closed it through authorable edges"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-401"
    type: "depends_on"
---
# FR-402: A tension names the clauses in conflict and what closed it through authorable edges

## Description

A `tension` SHALL state the clauses in conflict, the design element or decision that resolved
it, and the person who accepted it, each as an edge the corpus graph can read, so that the
completeness rule of FR-404 is manifest data over existing engine mechanisms. Source: PLAT-1480.

## Inputs

- The `allowed_links` of the `tension` object type and the `spec-artifacts-iso` edge
  vocabulary (FR-006-AC-4 of this module).

## Outputs

- Three verbs authorable from a `tension`: `conflicts_with`, `resolved_by`, `accepted_by`.

## Behavior

- A `tension` SHALL declare `conflicts_with` to any requirement or clause document, and a
  well-formed `tension` SHALL carry at least two such edges.
- A `tension` SHALL declare `resolved_by` to any design element or decision document.
- A `tension` SHALL declare `accepted_by` to a person reference. A person reference is an
  `ix://` target naming a person record or roster entry owned by another repository; this
  module SHALL NOT declare a person type.
- The module SHALL NOT mint a verb that the `spec-artifacts-iso` edge vocabulary already
  carries under another word; `references` is too loose to distinguish the three roles, so
  the three verbs above are added there. Adding them is a coordinated change owned by the
  iso module, as FR-006 records for `mitigates`; this module SHALL NOT change the direction
  or meaning of any existing verb to make room.
- An author SHALL write each verb from the `tension` end only, so that a conflict is written once.
- The edge from a `tension` SHALL NOT change the statement of any clause it names; a clause
  in conflict is not edited by being named.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-402-CON-1 | Every verb declared in `allowed_links` for `tension` SHALL exist in the `spec-artifacts-iso` edge vocabulary (FR-006-AC-4 continues to hold). | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-402-AC-1 | A `tension` with two `conflicts_with` edges to two requirements passes the edge check; the same `tension` with one `conflicts_with` edge draws a finding naming the tension. | Test |
| FR-402-AC-2 | A `tension` authoring `resolved_by` to a design element resolves and passes; an edge from a `tension` using a verb outside the three declared and `references` is reported. | Test |
| FR-402-AC-3 | A `tension` authoring `accepted_by` to an `ix://` person reference passes without that target being loaded in the bundle. | Test |
| FR-402-AC-4 | The manifest declares no `person` object type. | Test |
| FR-402-AC-5 | Every verb in the `tension` `allowed_links` exists in the iso edge vocabulary as a forward key or declared inverse. | Test |

## Dependencies

- **Upstream**: [FR-401](./FR-401-tension-object-type.md), [FR-006](./FR-006-cross-module-references.md)
- **Downstream**: [FR-404](./FR-404-tension-completeness-rule.md)
