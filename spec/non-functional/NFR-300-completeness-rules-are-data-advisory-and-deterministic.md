---
id: NFR-300
title: "Completeness rules are manifest data, advisory and deterministic"
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
# NFR-300: Completeness rules are manifest data, advisory and deterministic

## Statement

Each completeness rule of FR-301 to FR-304 SHALL be a `traceability` entry in
the module manifest, advisory by default, and tunable on its own `trace:<check>`
key; the same bundle SHALL yield identical findings and an identical risk
summary report on every run.

## Scope

- Applies to: the relations and `acyclic_edges` entries of the safety manifest, their findings, and the report of FR-305.
- Out of scope: the engine itself (`agent-ix/quire-rs`) and the scoping selector named in FR-302.

## Rationale

A rule written as engine code names a chain in the engine and forks with every
module. A rule that errors by default turns an unfilled analysis into a blocked
build. Findings that vary between runs cannot be reviewed.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Completeness rules implemented as engine code naming a safety archetype or verb | 0 | 0 | Inspection |
| Relations whose default severity is error | 0 | 0 | Manifest scan |
| Relations sharing a `check` token | 0 | 0 | Manifest scan |
| Differences between two runs over one bundle | 0 | 0 | Repeat-run test |

## Verification

A manifest scan lists every relation with its `check` token and default
severity. A repeat-run test compares findings and the report byte for byte. An
inspection of the engine confirms it holds no safety archetype or verb.
