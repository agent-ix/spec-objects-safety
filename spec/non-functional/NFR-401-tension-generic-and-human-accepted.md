---
id: NFR-401
title: "The tension type is generic and acceptance is always a person's"
type: NFR
quality_attribute: safety
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-401"
    type: "constrains"
---
# NFR-401: The tension type is generic and acceptance is always a person's

## Statement

The `tension` type SHALL use generic terms only and SHALL take every acceptance from a person's
written name. Source: PLAT-1480.

## Rationale

The module ships publicly, so it cannot quote a paywalled standard. A conflict accepted by a
rule or a default would be a risk nobody owns.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Schema defaults for `accepter` or `status` | 0 | 0 | Test |
| Paywalled-standard names or quotations in the `tension` schema, skeleton and manifest entry | 0 | 0 | Inspection |
| Source files that branch on the name `tension` | 0 | 0 | Test |

## Verification

A test reads the emitted `Tension.json` and asserts it declares no default for `accepter` or
`status`, and a scan of the package source asserts nothing branches on the name `tension`. An
inspection of the schema, skeleton and manifest entry confirms no paywalled text.

## Dependencies

- **Upstream**: [FR-401](../functional/FR-401-tension-object-type.md), [FR-403](../functional/FR-403-tension-state-validation.md)
