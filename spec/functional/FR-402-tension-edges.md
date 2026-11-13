---
id: FR-402
title: "A tension names the clauses in conflict and what resolved it through authorable edges"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-401"
    type: "depends_on"
---
# FR-402: A tension names the clauses in conflict and what resolved it through authorable edges

## Description

Tracked by Linear PLAT-1480. A `tension` SHALL state the clauses in conflict and the design
element or decision that resolved it as edges the corpus graph can read, so that the completeness
rule of FR-404 is manifest data over existing engine mechanisms.

## Inputs

- The `allowed_links` of the `tension` object type and the `spec-artifacts-iso` edge vocabulary.

## Outputs

- Two verbs authorable from a `tension`: `conflicts_with` and `resolved_by`.

## Behavior

- The `tension` object type SHALL declare `allowed_links` for exactly `conflicts_with` and
  `resolved_by`, and no other verb, `references` included.
- A `tension` SHALL declare `conflicts_with` to any requirement or clause document.
- The `tension` record schema SHALL require at least two `conflicts_with` relation entries,
  expressed as a `contains` constraint with `minContains: 2`.
- A `tension` SHALL declare `resolved_by` to a design element or decision document.
- An author SHALL write each verb from the `tension` end only, so that a conflict is written once.
- The accepted person is not an edge: it is the `decided_by` field of FR-403.
- The `spec-artifacts-iso` edge vocabulary lacks both verbs; Linear PLAT-1675 adds them. Neither
  has a near-synonym there: `relates_to` and `peer` are too loose, `blocks` means something else,
  `remediates` is runbook-to-incident and `satisfied_by` is stakeholder-requirement only.
- The module SHALL NOT change the direction or meaning of any existing verb.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-402-CON-1 | Every verb in `allowed_links` for `tension` SHALL exist in the `spec-artifacts-iso` edge vocabulary once PLAT-1675 lands (FR-006-AC-4 continues to hold). | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-402-AC-1 | A `tension` record with two `conflicts_with` relation entries validates; one with a single entry fails schema validation. | Test |
| FR-402-AC-2 | A `tension` that authors `references` or any other verb outside `conflicts_with` and `resolved_by` draws an undeclared-link diagnostic naming the tension. | Test |
| FR-402-AC-3 | A `tension` authoring `resolved_by` to a design element document resolves and passes the edge check. | Test |
| FR-402-AC-4 | The `tension` schema declares no property naming a person other than `decided_by`, and the manifest declares no person object type. | Test |
| FR-402-AC-5 | Once PLAT-1675 lands, every verb in the `tension` `allowed_links` exists in the iso edge vocabulary as a forward key or declared inverse. | Test |

## Dependencies

- **Upstream**: [FR-401](./FR-401-tension-object-type.md), [FR-006](./FR-006-cross-module-references.md); Linear PLAT-1675 (iso edge verbs)
- **Downstream**: [FR-404](./FR-404-tension-completeness-rule.md)
