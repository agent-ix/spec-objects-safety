---
id: TM-001
title: "spec-objects-safety Test Matrix"
type: TestMatrix
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/US-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-002"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-005"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/FR-006"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/NFR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-safety/IT-001"
    type: covers
---
# Test Matrix

## Overview

The verification contract for the module: the 0.2.0 object-type declaration
(FR-001) and the issue #2 semantic-module migration (US-001, FR-002..FR-006,
NFR-001, IT-001). Coverage is complete when every acceptance criterion, named
constraint, and NFR metric maps to at least one test case backed by a real
`@pytest.mark.trace` tag.

Two rows carry an explicit expected failure rather than a pass, each naming the
engine defect that owns it (TC-032, TC-067). Neither is skipped: both run, both
assert what the engine does today, and both name the issue that will let them
assert what the requirement says.

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and both object types are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero versus one identity field, a forbidden key present versus absent).
4. Every named refusal (digest mismatch, unknown key, both forms, missing table, clause without a fence, non-`Identifier` token) has a failing fixture.
5. Every scored axis is tested at each member of its own scale, at each `EpistemicState` member, and at a member of a foreign scale.
6. The safety-specific edges are tested as their own rows: `not_assessed` is not `negligible`, `detection: none` is not `detection: not_assessed`, and `status: accepted` without provenance is refused.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-006 | StR-001-VC-1 by TC-003, StR-001-VC-2 by TC-063 | ✅ |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-006 | TC-036, TC-039, TC-061 | ✅ |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1..7, FR-001-CON-1..2 | TC-001..TC-007, TC-046 | 🚧 AC-1's "at least one role" half is unbacked; see Coverage Gaps |
| FR-002 | FR-002-AC-1..9, FR-002-CON-1..5 | TC-012..TC-025 | ✅ |
| FR-003 | FR-003-AC-1..7, FR-003-CON-1..3 | TC-026..TC-034 | ✅ AC-6's naming half is an expected failure |
| FR-004 | FR-004-AC-1..12, FR-004-CON-1..3 | TC-035..TC-047, TC-071 | ✅ |
| FR-005 | FR-005-AC-1..10, FR-005-CON-1..3 | TC-048..TC-059 | ✅ |
| FR-006 | FR-006-AC-1..4, FR-006-CON-1..2 | TC-060..TC-064 | ✅ |

### Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test (locator baseline diff, 0.2.0 skeleton validation, traceability comparison, lint allow-list widening) | TC-065..TC-069 | ✅ AC-3 is an expected failure on quire-rs#391 |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| IT-001 | IT-001-SC-01..06 | TC-070 | 🚧 the row is backed by a tagged test; the CLI it drives is broken in this environment |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | The manifest validates against the FR-035 module-manifest schema, imported rather than copied — no skip and no escape hatch | Unit | P0 | FR-001-AC-5 | ✅ |
| TC-002 | The manifest declares exactly `hazard` and `failure_mode`, each with a `data_schema` and `allowed_links` | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-003 | `hazard` requires Condition plus an Assessment table; `failure_mode` requires Description plus an Analysis table, and the two shapes differ | Unit | P0 | FR-001-AC-2, FR-001-AC-3 | ✅ |
| TC-004 | Every lexicon entry is exactly `{definition: <text>}`, asserted structurally | Unit | P0 | FR-001-AC-6 | ✅ |
| TC-005 | Each object type ships a skeleton supplying every heading its contract requires | Unit | P0 | FR-001-AC-4 | ✅ |
| TC-006 | The pack exposes `MANIFEST_PATH` / `PACK_ROOT` as importable resource data | Unit | P1 | FR-001-AC-4 | ✅ |
| TC-007 | Every `allowed_links` verb exists in the iso edge vocabulary as a forward key or a declared inverse label | Unit | P0 | FR-001-AC-7, FR-001-CON-2 | ✅ |
| TC-010 | Bidirectional hazard coverage is manifest data: two independently tunable relations, `direction: incoming`, `arises_from` acyclic | Unit | P0 | FR-003-AC-5 | ✅ |
| TC-011 | Every relation names an object type this module declares and a verb the iso vocabulary carries | Unit | P0 | FR-006-AC-4 | ✅ |
| TC-012 | The emitted set equals the fifteen models `toolchain.json` lists, with compiler and emitter 1.15.0 recorded | Unit | P0 | FR-002-AC-1 | ✅ |
| TC-013 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name, with the version read from the manifest | Unit | P0 | FR-002-AC-2 | ✅ |
| TC-014 | Every `$ref` resolves to a shipped sibling or to semantic-core 0.1.0 | Unit | P0 | FR-002-AC-3 | ✅ |
| TC-015 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest | Integration | P1 | FR-002-AC-4 | ✅ |
| TC-016 | A `@jsonSchema` base version differing from the manifest version fails the generator naming both | Integration | P1 | FR-002-AC-5 | ✅ |
| TC-017 | The built wheel contains every emitted schema file | Integration | P1 | FR-002-AC-6 | ✅ |
| TC-018 | The packed npm tarball carries `manifest.yaml` and a sibling `schemas/<Model>.json`, and `postpack` leaves no staged copy at the repository root | Integration | P1 | FR-002-AC-7 | ✅ |
| TC-019 | A coordinated version bump re-emits every `$id`/`$ref` with matching digests; bumping one half of the pair fails the check | Integration | P1 | FR-002-AC-8, FR-002-CON-5 | ✅ |
| TC-020 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | ✅ |
| TC-021 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | ✅ |
| TC-022 | The build uses the official emitter only and no emitted file is hand-edited | Static | P2 | FR-002-CON-1 | ✅ |
| TC-023 | No `.npmrc`, no `file:`/`link:` dependency, exact toolchain pins in `package.json` | Static | P2 | FR-002-CON-2 | ✅ |
| TC-024 | `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core` | Unit | P2 | FR-002-CON-4 | ✅ |
| TC-025 | No test or fixture hard-codes the `$id` version segment; each reads it from the manifest `version` | Static | P2 | FR-002-CON-5 | ✅ |
| TC-026 | The `semantic` block equals the nine admitted keys and `exports` equals the two types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | ✅ |
| TC-027 | Every exported type's `data_schema` is the reference form whose file hashes to the recorded digest | Unit | P0 | FR-003-AC-2 | ✅ |
| TC-028 | Every 0.2.0 locator is unchanged against the checked-in baseline | Unit | P0 | FR-003-AC-3 | ✅ |
| TC-029 | Every locator added after 0.2.0 is `required: false` | Unit | P1 | FR-003-AC-3, FR-003-CON-2 | ✅ |
| TC-030 | Quire's registry loader lists both archetypes and `validate_document` reports no `semantic.*` load failure on any skeleton | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-031 | The `traceability` model is fact-for-fact the 0.2.0 model | Unit | P0 | FR-003-AC-5 | ✅ |
| TC-032 | An unknown `semantic` key and an altered digest are each refused by the loader; the refusal naming the key or path is an expected failure | Integration | P1 | FR-003-AC-6 | ✅ refusal verified; the naming half is an expected failure on quire-rs#221 and quire-rs#394 |
| TC-033 | The manifest validates against the FR-035 module-manifest schema at CR-012 | Unit | P0 | FR-003-AC-7 | ✅ |
| TC-034 | The CR-012 schema differs from the installed `spec-artifacts-iso` release only at the pointers CR-012 introduces, and the gate never skips | Unit | P0 | FR-003-AC-7, FR-003-CON-3 | ✅ |
| TC-035 | `Hazard.json` and `FailureMode.json` differ in a required key, a forbidden key or an item rule; neither is `type: object` only | Unit | P0 | FR-004-AC-1 | ✅ |
| TC-036 | Hazard: an identity record validates; the identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | ✅ |
| TC-037 | Failure mode: an identity record validates; `assessment`, `context` or `operations` each fail | Integration | P0 | FR-004-AC-3 | ✅ |
| TC-038 | Hazard: a record carrying `analysis` fails and one carrying `operations` fails | Integration | P0 | FR-004-AC-4 | ✅ |
| TC-039 | Assessment: a missing `severity`, a missing `likelihood` or an empty `rationale` fails; `severity: not_assessed` validates and is not `negligible` | Integration | P0 | FR-004-AC-5 | ✅ |
| TC-040 | Every scored axis accepts each member of its own scale and each `EpistemicState` member, rejects a foreign scale's member, and shares no member with `EpistemicState` | Property | P0 | FR-004-AC-6 | ✅ |
| TC-041 | No shipped schema declares a `default`, a `controls` key or a `mitigations` key | Unit | P0 | FR-004-AC-7 | ✅ |
| TC-042 | `status: accepted` without `provenance` fails; with `assertedBy` and `assertedAt` it validates; `status: identified` without provenance validates | Integration | P0 | FR-004-AC-8 | ✅ |
| TC-043 | A hazard record with no `relations` validates, and one with an `arises_from` relation validates | Integration | P1 | FR-004-AC-9 | ✅ |
| TC-044 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-AC-10, FR-004-CON-1 | ✅ |
| TC-045 | `detection: none` and `detection: not_assessed` are both accepted and are distinct values | Integration | P0 | FR-004-AC-11 | ✅ |
| TC-046 | A record that validates carries no status, no score and no acceptance the document did not state | Integration | P0 | FR-004-CON-2, FR-001-CON-1 | ✅ |
| TC-047 | No schema constraint was relaxed to make a fixture or skeleton pass | Static | P1 | FR-004-CON-3 | ✅ |
| TC-048 | All four skeletons validate with no error | Integration | P0 | FR-005-AC-1 | ✅ |
| TC-049 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | ✅ |
| TC-050 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | ✅ |
| TC-051 | Availability per skeleton is `fields: available`, `clauses: available`, `operations: not_applicable` | Integration | P1 | FR-005-AC-4 | ✅ |
| TC-052 | Every negative fixture fails with its `expect` token and carries detail beyond it; all seven named cases exist | Integration | P0 | FR-005-AC-5 | ✅ |
| TC-053 | Every skeleton H2 is a heading a locator names, and every required heading is present | Unit | P1 | FR-005-AC-6 | ✅ |
| TC-054 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | ✅ |
| TC-055 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` | Unit | P1 | FR-005-AC-8 | ✅ |
| TC-056 | No `## Properties` row names a column of the same type's `Assessment` or `Analysis` table | Unit | P1 | FR-005-AC-9 | ✅ |
| TC-057 | With the engine absent the semantic helper fails naming `make dev-quire` and quire-rs#392, and no test skips | Unit | P0 | FR-005-AC-10, FR-005-CON-3 | ✅ |
| TC-058 | A Properties section holding both forms is refused at the second form | Integration | P1 | FR-005-CON-2 | ✅ |
| TC-059 | The branch edits no corpus repository or vendored fixture | Static | P2 | FR-005-CON-1 | ✅ |
| TC-060 | The manifest declares exactly two object types and none a neighbouring module owns | Unit | P0 | FR-006-AC-1 | ✅ |
| TC-061 | No schema declares `controls` or `mitigations`, and every cross-module reference is a `SemanticId` | Unit | P0 | FR-006-AC-2 | ✅ |
| TC-062 | `semantic.imports` is `{}` and the manifest names the three open migration issues that keep it empty | Unit | P1 | FR-006-AC-3, FR-006-CON-2 | ✅ |
| TC-063 | Every `allowed_links` and `traceability` verb exists in the iso edge vocabulary | Unit | P0 | FR-006-AC-4 | ✅ |
| TC-064 | No safety-only synonym is minted for a verb or a type another module declares | Unit | P1 | FR-006-CON-1 | ✅ |
| TC-065 | Zero 0.2.0 locators changed against the baseline | Unit | P0 | NFR-001-AC-1 | ✅ |
| TC-066 | Every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors | Integration | P0 | NFR-001-AC-2 | ✅ |
| TC-067 | A legacy prose `## Properties` block warns rather than errors under `legacy_forms: warning` | Integration | P1 | NFR-001-AC-3 | ✅ the warning is emitted; the "not an error" half is an expected failure on quire-rs#391 |
| TC-068 | The `traceability` model is unchanged from 0.2.0 | Unit | P0 | NFR-001-AC-4 | ✅ |
| TC-069 | The widened lint allow-lists still admit every value they admitted at 0.2.0 | Unit | P1 | NFR-001-AC-5 | ✅ |
| TC-070 | Quoin install roundtrip: install, list, load through Quire, validate a skeleton, restore the catalog | Integration | P1 | IT-001-SC-01..IT-001-SC-06 | 🚧 the installed quoin CLI cannot read its own packaged schemas |
| TC-071 | Each ordinal scale's emitted enum equals the stated member list, and each advisory lint allow-list is its scale plus the three epistemic states | Unit | P0 | FR-004-AC-12 | ✅ |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins (0.46.0), provisioned by `make dev-quire`. That wheel is not on any
index this repository may commit a dependency against (`internal-pypi` serves
0.33.0 at most); `agent-ix/quire-rs#392` is the blocking issue. The suite
**fails** rather than skips when `extract_semantic` is absent, so no row here
can be reported green without the engine under test — TC-057 is the test of
that policy.

The FR-035 gate (TC-033, TC-034) runs against the module-manifest schema at
`agent-ix/spec-artifacts-iso` CR-012 (`6686f11`), because no released
distribution carries it (`agent-ix/spec-artifacts-iso#36`). TC-034 proves the pinned copy differs from the
installed release only at the pointers CR-012 introduces, so the copy cannot
drift into a weaker gate; when a release carries the `semantic` key, TC-034
fails and tells the maintainer to delete the pinned copy.

Rows over the record keys the extractor does not populate (`assessment`,
`context`, `analysis`, `status`, `provenance`, `evidence`) are verified against
hand-built records, not extracted ones — TC-036 through TC-046 in particular —
and their tests say so; they are schema evidence, not extraction evidence. The
mapping that would populate them is `agent-ix/quoin#335`.

## Coverage Gaps

Every acceptance criterion, constraint, and metric above has a row backed by a
tagged test, with three recorded exceptions:

1. **TC-070** is backed by a tagged, real test that drives the Quoin CLI, and
   that test does not pass on the machine this branch was written on: the
   globally installed `quoin` is a symlink into a live worktree whose `dist/`
   is mid-build and missing `dist/schemas/module-manifest.schema.json`, so
   `quoin module install` exits non-zero before reaching anything this module
   owns. The row is `🚧` rather than `✅`, the test lives in
   `tests_integration/` so `make test` does not report a green suite over a
   broken CLI, and `make test-integrations` runs it once the CLI is whole.
2. **FR-001-AC-1** reads "each with a `data_schema` and at least one role", but
   FR-001's own body decided against declaring a role
   (*"the `safety-relevant` capability tag this module first reached for turned
   out to be unnecessary"*), and neither the 0.2.0 tests nor TC-002 check for
   one. The criterion and the requirement that owns it disagree; the row stays
   `🚧` and `agent-ix/spec-objects-safety#3` carries the correction, because
   FR-001 belongs to the ticket that authored it rather than to this one.
3. **FR-003-AC-6** (TC-032) — the refusal is verified; the half that requires
   the refusal to *name* the offending key or path is an expected failure while
   `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` are open.
4. **NFR-001-AC-3** (TC-067) — the legacy-form warning is emitted; the half that
   requires it not to be accompanied by an error is an expected failure while
   `agent-ix/quire-rs#391` is open.

Two evidence-plan artifacts are absent and are carried by the plan rather than
by this matrix: no `SuiteRegistry` document declares a producer for the `Unit`,
`Integration`, `Static` and `Property` evidence kinds, and no `Inspections`
document exists for the `Static` rows (TC-022, TC-023, TC-025, TC-047, TC-059),
each of which is nonetheless discharged by an automated test here rather than by
a human procedure.
