---
id: FR-004
title: "Type-distinct safety schemas that keep unknown, not-assessed and not-applicable apart"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Type-distinct safety schemas that keep unknown, not-assessed and not-applicable apart

## Description

Each declared object type SHALL have its own emitted schema that differs from
the other in a required key, a forbidden key, or an item rule, and the scored
axes SHALL keep "unknown", "not assessed" and "not applicable" distinct from
every scale value, so that no consumer can read an unexamined hazard as a safe
one.

## Inputs

- The semantic-core declaration grammar 0.1.0.
- The declared safety vocabulary: severity, likelihood, exposure,
  controllability, detection, lifecycle status.

## Outputs

- `Hazard.json`, `FailureMode.json` and the support-model schemas of FR-002.

## Behavior

- `Hazard` SHALL require `fields` with at least one item and at least one item flagged `identity`.
- `FailureMode` SHALL require `fields` with at least one item and at least one item flagged `identity`.
- `Hazard` SHALL admit `assessment`, `context`, `status`, `provenance`, `evidence`, `relations` and `clauses` as optional keys and SHALL forbid every other key, `analysis` and `operations` included.
- `FailureMode` SHALL admit `analysis`, `status`, `provenance`, `evidence`, `relations` and `clauses` as optional keys and SHALL forbid every other key, `assessment`, `context` and `operations` included.
- `HazardAssessment` SHALL require `severity`, `likelihood` and a non-empty `rationale`, and SHALL admit `exposure` and `controllability` as optional.
- `FailureAnalysis` SHALL require a non-empty `effect`, a non-empty `cause` and a `detection`.
- Each of `severity`, `likelihood`, `exposure`, `controllability` and `detection` SHALL admit either a value of its own ordinal scale or a value of `EpistemicState`.
- `EpistemicState` SHALL be exactly `unknown`, `not_assessed`, `not_applicable`, and SHALL share no member with any ordinal scale.
- No schema SHALL declare a `default` for any scored axis or for `status`, so an absent value is never filled in as a safe one.
- If `status` is `accepted`, then `provenance` SHALL be required, so risk acceptance always carries the name of whoever accepted it.
- `Provenance` SHALL require a non-empty `assertedBy` and an `assertedAt` timestamp.
- `Hazard.relations` SHALL NOT carry a minimum-item or `contains` rule, because a hazard that arises from no declared failure mode is a valid record — the STPA case this module exists for.
- No schema SHALL declare a `controls` or `mitigations` key: the mitigation edge is authored from the requirement's end and is checked by the manifest `traceability` model.
- No schema SHALL redeclare a semantic-core model; every grammar item SHALL be a `$ref` to `@agent-ix/semantic-core` 0.1.0.
- No schema SHALL declare a safety-domain type that another module already owns; a control, risk, asset, interface, incident or evidence record is named by `SemanticId`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | Every grammar item SHALL be a `$ref` to semantic-core; no module schema redeclares `FieldDecl`, `TypeRef`, `ConstraintDecl`, `RelationDecl` or `ClauseRef`. | Architecture | Test |
| FR-004-CON-2 | Schema validity SHALL NOT constitute a safety claim. No status, no risk acceptance and no score is reached by a document merely validating. | Safety | Test |
| FR-004-CON-3 | No constraint in these schemas SHALL be relaxed to make a fixture, a skeleton or a corpus document pass. | Safety | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | `Hazard.json` and `FailureMode.json` differ in a required key, a forbidden key or an item rule, and neither is `type: object` only. | Test |
| FR-004-AC-2 | A hazard record with one identity field validates; the same record with the identity flag removed fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A failure-mode record with one identity field validates; a record carrying `assessment` or `context` fails; a record carrying `operations` fails. | Test |
| FR-004-AC-4 | A hazard record carrying `analysis` fails, and one carrying `operations` fails. | Test |
| FR-004-AC-5 | An assessment missing `severity`, missing `likelihood` or carrying an empty `rationale` fails; one scoring `severity: not_assessed` validates and is not equal to `severity: negligible`. | Test |
| FR-004-AC-6 | Each of the five scored axes accepts every member of its own scale and every member of `EpistemicState`, and rejects a member of another scale; no scale shares a member with `EpistemicState`. | Test |
| FR-004-AC-7 | No shipped schema declares a `default` anywhere, and none declares a `controls` or `mitigations` key. | Test |
| FR-004-AC-8 | A record with `status: accepted` and no `provenance` fails; the same record with a `provenance` naming `assertedBy` and `assertedAt` validates; a record with `status: identified` and no `provenance` validates. | Test |
| FR-004-AC-9 | A hazard record with no `relations` validates, and a hazard record with one `arises_from` relation validates. | Test |
| FR-004-AC-10 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core 0.1.0. | Test |
| FR-004-AC-11 | An analysis whose `detection` is `none` and one whose `detection` is `not_assessed` are both accepted and are distinct values. | Test |

## Dependencies

- **Upstream**: [US-001](../usecase/US-001-declare-safety-objects-against-semantic-core.md); semantic-core FR-031
- **Downstream**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models; [FR-005](./FR-005-executable-skeletons.md) exercises them
