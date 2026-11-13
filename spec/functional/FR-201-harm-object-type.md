---
id: FR-201
title: "The module declares harm as an object type"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: "depends_on"
---
# FR-201: The module declares harm as an object type

## Description

PLAT-1409. `harm` is today only a lexicon term. The module declares it as a
third object type, with a body contract, an emitted schema and an authoring
skeleton, so that a harm is named once and referenced by every hazardous
situation that can lead to it.

A `harm` is the thing that happens to a person, property or the environment.
It is not a hazard (a state) and not a hazardous situation (FR-202). It carries
no severity of its own: severity belongs to an estimate (FR-203, FR-204),
because the same harm is more or less severe depending on the situation and the
controls in place. It carries no `status` either: `LifecycleStatus` includes
`accepted`, and an acceptance of a harm means nothing, since acceptance is
recorded only on the residual-risk decision (PLAT-1523, FR-103).

## Inputs

- The semantic-core declaration grammar and the declaration style of FR-001 and FR-004.

## Outputs

- A `harm` object type in `manifest.yaml`, `Harm.json`, and a `harm` skeleton.

## Behavior

- The manifest SHALL declare an object type `harm`.
- The manifest SHALL export `harm` in `semantic.exports`.
- The harm schema SHALL require an identity field, a title and a description of what is harmed.
- The harm schema SHALL forbid the keys `severity`, `probability`, `score`, `status` and `acceptance`.
- The harm schema SHALL admit an optional `provenance`.
- The existing `harm` lexicon entry SHALL remain the definition the schema description cites.
- The module SHALL leave existing `hazard` and `failure_mode` documents valid with no change and no migration.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-201-AC-1 | The manifest lists `harm` under `object_types` and `semantic.exports`, and the TypeSpec build emits `Harm.json`. | Test |
| FR-201-AC-2 | The shipped `harm` skeleton validates; the same skeleton with the description removed fails validation. | Test |
| FR-201-AC-3 | A `harm` fixture carrying any of `severity`, `probability`, `score`, `status` or `acceptance` fails validation, one fixture per key, including `status: accepted`. | Test |
| FR-201-AC-4 | A `harm` fixture with a `provenance` naming a person validates. | Test |
| FR-201-AC-5 | Every pre-existing `hazard` and `failure_mode` fixture validates unchanged against the new schemas. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-safety-object-types.md), [FR-004](./FR-004-type-distinct-safety-schemas.md)
- **Downstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md)
