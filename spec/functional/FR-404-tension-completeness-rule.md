---
id: FR-404
title: "Completeness rule as manifest data: no tension is open at release; accepted tensions name a person"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-401"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-402"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-403"
    type: "depends_on"
---
# FR-404: Completeness rule as manifest data: no tension is open at release; accepted tensions name a person

## Description

The module SHALL state the tension completeness rule as `traceability` manifest data, using the
engine's existing `required_relations` and `acyclic_edges` declarations (quire-rs FR-058),
so that a corpus with an open tension fails the check and a closed one passes. Source: PLAT-1480.

## Inputs

- The manifest `traceability` block, which already declares `hazard-has-mitigation`,
  `failure-mode-has-mitigation` and `acyclic_edges: [arises_from]`.

## Outputs

- One added `required_relations` entry and one `acyclic_edges` verb, with no engine change.

## Behavior

- The manifest SHALL add a relation `tension-is-closed` with `from: tension`,
  `edges: [resolved_by, accepted_by]`, `to: []`, `direction: outgoing` and
  `check: open-tension`.
- Any one of the two edges satisfies the relation (FR-058: any one of `edges`). A `tension`
  with neither is open, and is reported by name under `trace:open-tension`.
- `to: []` is deliberate: an `accepted_by` target is a person reference owned by another
  repository, and a dangling or cross-repository edge counts when `to` is empty.
- The manifest SHALL add `resolved_by` to `acyclic_edges`, because a decision that resolves
  a conflict by way of itself resolves nothing.
- The rule SHALL be data only: the engine names no archetype, verb or direction of this chain
  (quire-rs FR-058-CON-2).
- The release gate of a repository SHALL fail the completeness rule when it maps
  `trace:open-tension` to `error`; this module leaves the advisory default of FR-058 unchanged.
- The status-versus-evidence agreement of FR-403 is the record schema's job; the relation
  checks the edge, and the schema checks that an edge-closed record carries the matching
  status and the accepter's name. Each check stays in its own place.
- A `tension` whose `resolved_by` target is present in the bundle SHALL satisfy the rule
  whatever kind of document that target is; the module SHALL NOT restrict the target kind.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-404-CON-1 | The engine SHALL contain no tension-specific code; the rule is one manifest entry. | Architecture | Inspection |
| FR-404-CON-2 | The rule SHALL NOT compare, count or weigh tensions against each other; each is closed or not. | Design | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-404-AC-1 | A corpus containing a `tension` with `status: open` and neither edge is reported under `trace:open-tension`, naming that tension, and fails when the key is mapped to `error`. | Test |
| FR-404-AC-2 | Adding a `resolved_by` edge to a design element and setting `status: resolved-by-design` clears the finding; the corpus passes. | Test |
| FR-404-AC-3 | Adding an `accepted_by` edge to a person reference, with `status: accepted-by-person` and a named `accepter`, clears the finding; the corpus passes. | Test |
| FR-404-AC-4 | A `tension` carrying `accepted_by` but `status: accepted-by-person` with no `accepter` passes the relation check and is still rejected by schema validation (FR-403-AC-1). | Test |
| FR-404-AC-5 | A cycle over `resolved_by` is reported exactly once. | Test |
| FR-404-AC-6 | The manifest `traceability` block loads with the new relation and the existing relations unchanged, and a corpus with no `tension` produces output identical to one before this FR. | Test |

## Dependencies

- **Upstream**: [FR-402](./FR-402-tension-edges.md), [FR-403](./FR-403-tension-state-validation.md), quire-rs FR-058
- **Downstream**: [FR-405](./FR-405-tension-intake.md)
