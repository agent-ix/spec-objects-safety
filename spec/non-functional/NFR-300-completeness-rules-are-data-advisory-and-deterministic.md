---
id: NFR-300
title: "Completeness relations are manifest data, advisory and deterministic"
type: NFR
quality_attribute: maintainability
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-301"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-302"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-303"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-304"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-305"
    type: "constrains"
---
# NFR-300: Completeness relations are manifest data, advisory and deterministic

## Statement

Each completeness relation declared by FR-301, FR-302 and FR-303 and the cycle
entry of FR-304 SHALL be a `traceability` entry in the module manifest, advisory
by default, with its own `trace:<check>` key and no other relation sharing that
key; the same bundle SHALL yield identical findings on every run.

## Scope

- Applies to: the relations and `acyclic_edges` entries of the safety manifest, and their findings.
- Out of scope: the rules FR-303 assigns to the FR-103 schema and the FR-105 report, the engine (`agent-ix/quire-rs`), and the output of FR-305, whose determinism FR-305 states.

## Rationale

A rule written as engine code names a chain in the engine and forks with every
module. A rule that errors by default turns an unfilled analysis into a blocked
build. Findings that vary between runs cannot be reviewed.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Completeness rules implemented as engine code naming a safety archetype or verb | 0 | 0 | Inspection |
| Relations whose default severity is error | 0 | 0 | Manifest scan |
| `check` tokens declared by more than one relation | 0 | 0 | Manifest scan |
| Differences between two runs over one bundle | 0 | 0 | Repeat-run test |

## Verification

A manifest scan lists every relation with its `check` token and default
severity. A repeat-run test compares findings byte for byte. An inspection of
the engine confirms it holds no safety archetype or verb.
