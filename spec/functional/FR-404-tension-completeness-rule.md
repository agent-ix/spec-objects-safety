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

Tracked by Linear PLAT-1480. The module SHALL state the tension completeness rule as
`traceability` manifest data, using the engine's `required_relations` with the `where` selector
(quire-rs FR-058), so that a corpus with an open tension fails the check and a closed one passes.
Nothing here needs a new engine mechanism.

## Inputs

- The manifest `traceability` block, which already declares `hazard-has-mitigation`,
  `failure-mode-has-mitigation` and `safety-nfr-has-mitigation-target` (which uses `where`).

## Outputs

- Two added `required_relations` entries.

## Behavior

- The manifest SHALL add a relation `resolved-tension-has-link` with `from: tension`,
  `where: {field: status, values: [resolved-by-design]}`, `edges: [resolved_by]`, `to: []`,
  `direction: outgoing` and `check: resolved-tension-without-link`.
- The manifest SHALL add a relation `tension-is-not-open` with `from: tension`,
  `where: {field: status, values: [open]}`, `edges: [resolved_by]`, `to: []`,
  `direction: outgoing` and `check: open-tension`.
- An open tension is reported because it has no `resolved_by` edge, and the record schema
  rejects a `resolved_by` entry on an open tension (FR-403), so an open tension cannot clear the
  relation by gaining an edge without also changing `status`. An incoming edge of any verb, from
  another tension or any document, does not satisfy an outgoing relation and so does not clear it.
- A tension closes by changing `status`: to `resolved-by-design` with a `resolved_by` edge, or to
  `accepted-by-person` with a named `decided_by` (FR-403), which the schema enforces and no
  relation needs.
- `to: []` on `resolved-tension-has-link` is accepted at its cost: a mistyped or dangling
  `resolved_by` target satisfies the relation, and only the dangling-reference check reports it.
  A constrained `to` would reject a design element owned by another repository.
- The rule SHALL be data only: the engine names no archetype, verb or direction of this chain
  (quire-rs FR-058-CON-2).
- The release gate of a repository SHALL fail the completeness rule when it maps
  `trace:open-tension` and `trace:resolved-tension-without-link` to `error`; this module leaves
  the advisory default of FR-058 unchanged.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-404-CON-1 | The engine SHALL contain no tension-specific code; the rule is two manifest entries. | Architecture | Inspection |
| FR-404-CON-2 | The rule SHALL NOT compare, count or weigh tensions against each other; each is closed or not. | Design | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-404-AC-1 | A corpus containing a `tension` with `status: open` is reported under `trace:open-tension`, naming that tension, and fails when the key is mapped to `error`. | Test |
| FR-404-AC-2 | A `tension` with `status: open` that is the target of an incoming `conflicts_with` edge, or of an edge from a dangling or other document, is still reported under `trace:open-tension`. | Test |
| FR-404-AC-3 | Setting `status: resolved-by-design` with a `resolved_by` edge to a design element clears the finding; the corpus passes. | Test |
| FR-404-AC-4 | A `tension` with `status: resolved-by-design` and no `resolved_by` edge is reported under `trace:resolved-tension-without-link`. | Test |
| FR-404-AC-5 | A `tension` with `status: accepted-by-person` and a named `decided_by` passes both relations; the same record with no `decided_by` still fails schema validation (FR-403-AC-1). | Test |
| FR-404-AC-6 | The manifest `traceability` block loads with the two new relations and the existing relations unchanged, and a corpus with no `tension` produces output identical to one before this FR. | Test |

## Dependencies

- **Upstream**: [FR-402](./FR-402-tension-edges.md), [FR-403](./FR-403-tension-state-validation.md), quire-rs FR-058
- **Downstream**: [FR-405](./FR-405-tension-intake.md)
