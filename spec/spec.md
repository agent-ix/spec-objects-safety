---
type: master-requirements
name: spec-objects-safety
org: agent-ix
component_type: filament-module
implementation_language: python
tags:
  - filament-module
  - safety
  - object-types
depends_on: []
standards_alignment:
  - iso-iec-ieee-29148
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quire-rs/FR-069"
    type: "depends_on"
    cardinality: "1:1"
security_critical: false
---
# Master Requirements Specification

## Purpose

Declare the **safety** object types — `hazard` and `failure_mode` — so safety
analysis is recorded as validated, linkable specification objects rather than
as prose nothing can check, and declare them in the same semantic contract the
rest of the module ecosystem uses so a reader, a generator, or another module
sees the contract that was authored instead of guessing at it.

## Scope

### In Scope

- The Module manifest (`spec_objects_safety/manifest.yaml`), the two safety
  object types it contributes, their body contracts, their authoring skeletons,
  and the domain lexicon.
- The semantic-module contract (issue #2): a TypeSpec source importing
  `@agent-ix/semantic-core` 0.1.0, the emitted JSON Schema per declared model
  shipped under `spec_objects_safety/schemas/`, the manifest `semantic` block
  with reference-form `data_schema`, and the skeletons rewritten as executable
  typed fixtures with negative counterparts.
- The safety vocabulary the schemas fix: severity, likelihood, exposure,
  controllability, detection, lifecycle status, provenance, and the epistemic
  states (`unknown`, `not_assessed`, `not_applicable`) that keep an unexamined
  axis distinct from a safe one.

### Out of Scope

- Automated hazard identification, which does not exist. Identification and
  scoring are authored judgement; nothing in this module computes, infers, or
  defaults either, and schema validity is never a safety claim.
- Declaring a `control`, `risk`, `asset`, `incident`, `interface` or
  evidence-record type. Those belong to `agent-ix/spec-objects-security`,
  `agent-ix/spec-objects-architecture`, `agent-ix/spec-objects-operational` and
  `agent-ix/engineering-assurance`; this module references them and never
  redeclares them (FR-006).
- Populating `semantic.imports`. The map pins imported semantic **packages** at
  exact versions, and none of the four neighbours above has published a
  semantic contract yet: `agent-ix/spec-objects-security#13`,
  `agent-ix/spec-objects-architecture#8` and
  `agent-ix/spec-objects-operational#6` are the open migration tickets. Pinning
  a version a neighbour does not declare would be a false claim, so the map
  stays `{}` and FR-006 records the obligation to fill it.
- Extraction of the module-specific record keys (`assessment`, `context`,
  `analysis`, `status`, `provenance`, `evidence`) from Markdown. The published
  mapping covers `Properties`, `Invariants` and `Operations` only
  (`agent-ix/quoin#335`, quoin FR-071/FR-072); until a mapping for the
  `Assessment` and `Analysis` tables is published and an extractor lands in
  `agent-ix/quire-rs`, those keys are declared optional and are verified
  against hand-built records rather than extracted ones. The tests that do so
  say which they are.
- Widening the `Assessment` table with `Exposure` and `Controllability`
  columns. The 0.2.0 contract asserts the columns exactly, so adding one would
  not be additive (NFR-001); the two axes are typed in `HazardAssessment` and
  wait on the same mapping.
- Generated-language fixtures (Rust, TypeScript, Python) for the safety types:
  produced by `agent-ix/filament-core-data#21`, `#22` and `#23` and published
  only behind the promotion gate `agent-ix/quoin#290`; the semantic-core
  language packages are `agent-ix/filament-core-data#11`. None is produced or
  faked here, so issue #2's "generated packages preserve traceability and
  evidence references" is carried by those tickets, not discharged here.
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown
  manifest key empties the model silently) and `agent-ix/quire-rs#394` (a
  `data_schema` digest mismatch drops the object type with no diagnostic).
  FR-003-AC-6's "naming the key or the path" half is blocked on them and is
  carried as an explicit expected failure.
- Treating a legacy prose `## Properties` block as a warning rather than an
  error: `agent-ix/quire-rs#391` (the engine validates an `unavailable` record
  as `{}`, so a legacy form errors even under `legacy_forms: warning`).
  NFR-001-AC-3 is carried as an explicit expected failure beside it rather than
  worked around by relaxing a schema. NFR-001-AC-2 itself holds — every
  checked-in 0.2.0 skeleton validates under 0.3.0.
- Publishing the Quire 0.46.0 wheel to an index a repository may commit
  against: `agent-ix/quire-rs#392`. `internal-pypi` serves 0.33.0 at most, so
  this module provisions the wheel with a documented `make dev-quire` target
  and its semantic tests fail rather than skip when the engine is absent
  (FR-005-CON-3). Declaring `quire` as a committed dev dependency waits on that
  issue.
- Publishing a `spec-artifacts-iso` release whose FR-035 module-manifest schema
  carries the `semantic` block and the `data_schema` reference form: the schema
  landed on `main` at `6686f11` (CR-012) and no tag carries it, `v0.18.0`
  included; `agent-ix/spec-artifacts-iso#36` is the blocking issue. FR-003-AC-7 therefore runs the gate against the pinned CR-012
  revision and proves it differs from the installed release only at the CR-012
  pointers; the gate still never skips.
- Resolving a reference-form `data_schema` into a stored snapshot at
  activation: `agent-ix/filament-core-service#23`. Until it lands the service
  stores the reference verbatim.
- Bidirectional hazard↔requirement coverage checking, which is declared
  `traceability.required_relations` against quire-rs FR-058 rather than code in
  this module (`agent-ix/spec-objects-security#5`). The 0.2.0 model is kept
  unchanged here on purpose (NFR-001-AC-4).
- Editing any corpus repository or vendored fixture; the corpus sweep is
  `agent-ix/quoin#291` and promotion is `agent-ix/quoin#290`.

## System Overview

### System Description

A Filament Module, activated by `filament-core-service` and reached through
`cloudmanager-local-sync`. It ships `manifest.yaml`, one authoring skeleton per
object type with a `sysml` alternate, and the JSON Schemas emitted from
`typespec/main.tsp`, and contributes its object types, `allowed_links`,
`traceability` model and lexicon to the merged registry that `quire validate`
reads.

Its lineage is IEC 61508 / ISO 26262 / FMEA / STPA. That is a different
regulatory domain from the STRIDE, identity and crypto types in
`spec-objects-security`, which is why the two are separate modules: merged,
one module's applicability signals would answer for both.

### Intended Users

The Filament platform (which activates and serves the contributed ObjectTypes),
safety engineers and spec authors (who record hazards and failure modes with
them), reviewers asking which hazards have nothing addressing them, and the
generators that will produce typed readers from the shipped schemas.

## Requirements Architecture

The requirement classes trace from the stakeholder need for safety analysis as
validated, linkable objects (`stakeholder/`) through the maintainer's story of
declaring those types against semantic-core (`usecase/`) to the functional
requirements (`functional/`): FR-001 declares the two object types and why they
are two; FR-002 emits the schemas; FR-003 declares the semantic contract in the
manifest; FR-004 fixes each type's schema and the epistemic distinctions the
safety domain needs; FR-005 makes the skeletons executable fixtures; FR-006
keeps the cross-module types referenced rather than copied. NFR-001 bounds the
change to additive compatibility. `integration/` carries the Quoin install
boundary; the Quire engine boundary has no IT artifact of its own — the FR-003
and FR-005 test harness is this module's Quire contract test, and the wheel
version is pinned once in FR-005 Inputs. The Test Matrix in `tests.md` records
every criterion's test case.

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- IEC 61508 — functional safety of electrical/electronic systems.
- ISO 26262 — road-vehicle functional safety; the source of the exposure and
  controllability axes.
- FMEA — failure mode and effects analysis (the effect/cause/detection triple).
- STPA — systems-theoretic process analysis, the reason a hazard is not
  derivable from a set of failure modes.
- `spec-artifacts-iso` FR-004 — the edge-type and role vocabulary the
  safety-chain verbs join; and its `module-manifest.schema.json` (FR-035,
  CR-012), the schema this manifest conforms to.
- `agent-ix/filament-core-data` FR-031..FR-034 (semantic-core grammar, scalars,
  JSON Schema projection, lowering) and ADR-0005 (TypeSpec source).
- `agent-ix/quoin` FR-070..FR-075 (semantic-module contract, mappings,
  `data_schema` by digest, legacy forms, package exports).
- `agent-ix/quire-rs` FR-069..FR-072 (contract at load, typed Properties,
  clauses and operations, extraction surface) and FR-058 (upward-trace
  completeness).
