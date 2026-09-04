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
- The declared safety vocabulary, fixed here rather than only in the emitted
  schemas, because the epistemic property below is a claim about these exact
  member sets:

| Vocabulary | Members | Lineage |
|---|---|---|
| `Severity` | `negligible`, `marginal`, `critical`, `catastrophic` | IEC 61508 / MIL-STD-882 four-band harm severity. **Not** ISO 26262 `S0..S3`, so no ASIL is derivable from these members and none is claimed. |
| `Likelihood` | `incredible`, `improbable`, `remote`, `occasional`, `probable`, `frequent` | IEC 61508 frequency bands |
| `Exposure` | `E0`, `E1`, `E2`, `E3`, `E4` | ISO 26262 exposure. Typed only: no authored column carries it at 0.3.0. |
| `Controllability` | `C0`, `C1`, `C2`, `C3` | ISO 26262 controllability. Typed only: no authored column carries it at 0.3.0. |
| `Detection` | `none`, `indirect`, `direct`, `automatic` | FMEA detectability |
| `LifecycleStatus` | `identified`, `analysed`, `mitigated`, `accepted`, `transferred`, `closed` | Authored disposition |
| `EpistemicState` | `unknown`, `not_assessed`, `not_applicable` | Not a scale; what an axis says instead of a scale value |

- The three advisory lint allow-lists the manifest declares over the authored
  tables — `hazard-severity` (`Assessment.Severity`), `hazard-likelihood`
  (`Assessment.Likelihood`) and `failure-mode-detection` (`Analysis.Detection`).

## Outputs

- `Hazard.json`, `FailureMode.json` and the support-model schemas of FR-002.

## Behavior

- `Hazard` SHALL require `fields` with at least one item and at least one item flagged `identity`.
- `FailureMode` SHALL require `fields` with at least one item and at least one item flagged `identity`.
- `Hazard` SHALL admit `assessment`, `context`, `status`, `provenance`, `evidence`, `relations` and `clauses` as optional keys.
- `Hazard` SHALL forbid every other key, `analysis` and `operations` included.
- `FailureMode` SHALL admit `analysis`, `status`, `provenance`, `evidence`, `relations` and `clauses` as optional keys.
- `FailureMode` SHALL forbid every other key, `assessment`, `context` and `operations` included.
- `HazardAssessment` SHALL require `severity`, `likelihood` and a non-empty `rationale`.
- `HazardAssessment` SHALL admit `exposure` and `controllability` as optional.
- `FailureAnalysis` SHALL require a non-empty `effect`, a non-empty `cause` and a `detection`.
- Each of `severity`, `likelihood`, `exposure`, `controllability` and `detection` SHALL admit either a value of its own ordinal scale or a value of `EpistemicState`.
- `EpistemicState` SHALL be exactly `unknown`, `not_assessed`, `not_applicable`.
- `EpistemicState` SHALL share no member with any ordinal scale.
- Each ordinal scale SHALL hold exactly the members its row of the Inputs table names, so a consumer reading a scale reads a closed, stated set.
- Each of the three advisory lint allow-lists SHALL admit its own scale's members and the three `EpistemicState` members, so the document form can express everything the schema admits and an unscored axis is never nudged towards a scale's safe end.
- No schema SHALL declare a `default` for any scored axis or for `status`, so an absent value is never filled in as a safe one.
- An absent `assessment`, `analysis` or `status` SHALL mean "the document does not carry this", which is distinct from every `EpistemicState` member and from every scale value. A consumer counting the unanalysed backlog therefore reads both the absent case and `not_assessed`; this specification claims no equivalence between them.
- The emitted schemas SHALL type `Exposure` and `Controllability` while no authored form carries them at 0.3.0, because the `Assessment` table's columns are fixed by the 0.2.0 contract and widening them would not be additive; `agent-ix/quoin#342` owns the mapping that makes them authorable.
- No schema SHALL derive, name or imply an ASIL, a SIL or any other integrity level, because `Severity` is a four-band harm scale rather than ISO 26262 `S0..S3` and no determination table is declared here.
- If `status` is `accepted`, then the record schema SHALL require `provenance` together with `assessment` on a hazard, or with `analysis` on a failure mode, so an acceptance names both a person and the thing being accepted.
- Each record and value schema SHALL seal its key set with `unevaluatedProperties` and with `additionalProperties`, because the first is a 2020-12 keyword a consumer on an older dialect ignores, which would admit a forbidden key while `required` and `enum` still fail closed.
- `Provenance` SHALL require a non-empty `assertedBy` and an `assertedAt` timestamp.
- `Hazard.relations` SHALL NOT carry a minimum-item or `contains` rule, because a hazard that arises from no declared failure mode is a valid record — the STPA case this module exists for.
- No schema SHALL declare a `controls` or `mitigations` key: the mitigation edge is authored from the requirement's end and is checked by the manifest `traceability` model.
- No schema SHALL redeclare a semantic-core model.
- Every grammar item in a shipped schema SHALL be a `$ref` to `@agent-ix/semantic-core` 0.1.0.
- No schema SHALL declare a safety-domain type that another module already owns; a control, risk, asset, interface, incident or evidence record is named by `SemanticId`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | Every grammar item SHALL be a `$ref` to semantic-core; no module schema redeclares `FieldDecl`, `TypeRef`, `ConstraintDecl`, `RelationDecl` or `ClauseRef`. | Architecture | Test |
| FR-004-CON-2 | Schema validity SHALL NOT constitute a safety claim. No status, no risk acceptance and no score is reached by a document merely validating. | Safety | Test |
| FR-004-CON-3 | No author SHALL relax a constraint in these schemas to make a fixture, a skeleton or a corpus document pass. | Safety | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | `Hazard.json` and `FailureMode.json` differ in a required key, a forbidden key or an item rule, and neither is `type: object` only. | Test |
| FR-004-AC-2 | A hazard record with one identity field validates; the same record with the identity flag removed fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A failure-mode record with one identity field validates; a record carrying `assessment` or `context` fails; a record carrying `operations` fails. | Test |
| FR-004-AC-4 | A hazard record carrying `analysis` fails, and one carrying `operations` fails. | Test |
| FR-004-AC-5 | An assessment missing `severity`, missing `likelihood` or carrying an empty `rationale` fails; one scoring `severity: not_assessed` validates and is not equal to `severity: negligible`. | Test |
| FR-004-AC-6 | Each of the five scored axes accepts every member of its own scale and every member of `EpistemicState`, and rejects a member of another scale; no scale shares a member with `EpistemicState`. | Test |
| FR-004-AC-12 | Each ordinal scale's emitted `enum` equals the member list the Inputs table states, and each advisory lint allow-list is its scale's members plus the three `EpistemicState` members. | Test |
| FR-004-AC-7 | No shipped schema declares a `default` anywhere, and none declares a `controls` or `mitigations` key. | Test |
| FR-004-AC-8 | A record with `status: accepted` fails when `provenance` is absent, fails when the accepted `assessment`/`analysis` is absent, and validates only with both; a record with `status: identified` and neither validates. | Test |
| FR-004-AC-13 | Every record and value schema declares both `unevaluatedProperties` and `additionalProperties: false`, so a forbidden key is refused on a pre-2020-12 validator as well. | Test |
| FR-004-AC-14 | No shipped schema names an ASIL, a SIL or any other integrity level, and `Severity` is the four-band harm scale rather than `S0..S3`. | Test |
| FR-004-AC-9 | A hazard record with no `relations` validates, and a hazard record with one `arises_from` relation validates. | Test |
| FR-004-AC-10 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core 0.1.0. | Test |
| FR-004-AC-11 | An analysis whose `detection` is `none` and one whose `detection` is `not_assessed` are both accepted and are distinct values. | Test |

## Dependencies

- **Upstream**: [US-001](../usecase/US-001-declare-safety-objects-against-semantic-core.md); semantic-core FR-031
- **Downstream**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models; [FR-005](./FR-005-executable-skeletons.md) exercises them
