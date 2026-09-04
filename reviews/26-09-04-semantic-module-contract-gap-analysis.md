---
id: SR-011
title: "Gap analysis — Plan-001 semantic module contract (issue #2)"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-semantic-module-contract/, spec/tests.md, spec/spec.md, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001, spec/integration/IT-001, spec_objects_safety/, typespec/, scripts/, tests/, tests_integration/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/Plan-001"
    type: reviews
  - target: "ix://agent-ix/spec-objects-safety/TM-001"
    type: references
---
# Gap analysis — Plan-001 semantic module contract (issue #2)

## Summary

Post-implementation verification of `plan/Plan-001-semantic-module-contract/`
against `agent-ix/spec-objects-safety#2` on `spec/2-semantic-module-contract`,
anchored at HEAD `77a976e` and diffed against `origin/main`. All eleven tasks
are `status: done`, `quire coverage --scope .` reports **125/125 rows backed
(100%)**, `quire validate` over `spec/**/*.md` and `plan/**/*.md` exits zero
with grammar warnings only, and the safety content the module exists for is
real: `EpistemicState` (`unknown`, `not_assessed`, `not_applicable`) shares no
member with `Severity`, `Likelihood`, `Exposure`, `Controllability`,
`Detection` or `LifecycleStatus`; every scored axis is an `anyOf` of its own
scale and those three; no schema declares a `default` anywhere; and
`status: accepted` is gated on a `Provenance` requiring `assertedBy` and
`assertedAt`. The headline claim holds at the schema level and is verified
exhaustively over the finite domain by TC-040.

The 125/125 is a **binding** census, not a pass census, and it is not an
artifact of tags on non-binding symbols: all 70 bound symbols are
`@pytest.mark.trace`-decorated `test_` functions, the 125 rows are 69 `TC-`
rows from `spec/tests.md` plus 56 acceptance-criterion rows minted from the
requirement documents, and the census carries no unbacked row and no status
lie. Three qualifications sit under it, and they are the substance of this
review: the engine **skipped status classification entirely**
(`[status-column-matches-nothing]`, so complete-but-unbacked rows were never
checked); four of IT-001's six success criteria are not declared rows at all
and are reported as untracked; and the branch's own pass census is wrong —
`make test` runs `tests_integration/` and produced 70 passed + 2 xfailed, not
the 69 + 2 the plan log, the matrix and the commit message record.

Against the ticket, the two deliverables the branch does **not** discharge are
recorded honestly. "Generated-language fixtures" is an explicit Out of Scope
entry in `spec/spec.md` naming `filament-core-data#21/#22/#23`, `#11` and the
`quoin#290` promotion gate, and it says in terms that issue #2's "generated
packages preserve traceability and evidence references" is carried by those
tickets. The imports deliverable is recorded for three of its four neighbours
only: `engineering-assurance` is named as an owner of evidence records in
FR-006, `spec/spec.md` and the manifest, but no migration issue is recorded
for it, and FR-006-AC-3 / TC-062 bake "the three open migration issues" into
the assertion.

Finally, the working tree was **being edited by another agent throughout this
review**: at the time of writing it carries uncommitted changes to
`typespec/main.tsp`, nine emitted schemas, the manifest digests,
`tests/test_record_schemas.py`, `tests/conftest.py`, two FR documents, and
eight untracked `spec/reviews/` artifacts. Those changes alter the safety
contract (`additionalProperties: false` on every model, and
`then.required: [provenance, assessment|analysis]` in place of
`[provenance]`). Every finding below is anchored at HEAD; the dynamic runs are
flagged where a moving tree could have influenced them.

## Verdict

**FAIL** — no task is incomplete and no matrix row is unbacked, but two `high`
findings stand: the test-isolation mechanism the branch relies on to justify
TC-070's `🚧` does not exist, so the recorded pass census is false; and the
branch's safety contract is being changed in an uncommitted working tree that
HEAD's own tests contradict.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | `make test` DOES run `tests_integration/`: `pyproject.toml` declares no `testpaths` and `poe test` is a bare `pytest`, so the whole tree is collected. The isolation is asserted in four places — `spec/tests.md` Coverage Gaps 1, `plan.md` Test Plan, `tests_integration/conftest.py:3-6`, commit `77a976e` — and is implemented in none. The observed run is 70 passed + 2 xfailed including TC-070, not the recorded 69 + 2, and on a machine with no working `quoin` the suite `pytest.fail`s by design rather than isolating the row. | pyproject.toml, tests.md, Plan-001/plan.md, TC-070 | correct-requirement-no-evidence |
| FND-002 | high | The working tree is mid-edit by a concurrent agent and has diverged from HEAD on the safety contract: nine schemas gain `additionalProperties: false`, both records change `then.required` from `[provenance]` to `[provenance, assessment]` / `[provenance, analysis]`, `typespec/main.tsp` and the manifest digests follow, and `tests/test_record_schemas.py` is edited to match. HEAD's TC-047 asserts `rule["then"]["required"] == ["provenance"]`, so HEAD and the tree now disagree about what FR-004-AC-8 means, and `IdentityField.json`'s description in the tree is a mangled concatenation of two doc comments. None of it is committed. | Hazard.json, FailureMode.json, typespec/main.tsp, TC-047, FR-004-AC-8 | implementation-bug-despite-evidence |
| FND-003 | medium | `quire coverage`'s 125/125 was computed with **status classification skipped**: `[status-column-matches-nothing]` — `traceability.status.column` is `Status`, the Functional Requirement Coverage table's header is `Coverage Status`, "so complete-but-unbacked rows could not be checked". The caveat is in commit `77a976e` and filed as `spec-artifacts-process#82`, but `spec/tests.md` presents 125/125 with no mention of it. | spec/tests.md, TM-001 | correct-requirement-no-evidence |
| FND-004 | medium | IT-001's success criteria are not matrix rows. `spec/integration/` mints nothing, and the only cell naming them is the range string `IT-001-SC-01..IT-001-SC-06`, which the binder resolves by substring — SC-01 and SC-06 bind, SC-02 through SC-05 are reported "matches no declared row". Four of the six criteria sit outside the 125 denominator entirely. | IT-001, TC-070, spec/tests.md | correct-requirement-no-evidence |
| FND-005 | medium | The ticket deliverable "define imports to architecture, operational, security, **and assurance** types" is discharged for three neighbours only. `engineering-assurance` is named as the owner of evidence records in FR-006 Inputs, `spec/spec.md` Out of Scope and the manifest comment, but no migration issue is recorded for it, and FR-006-AC-3 / TC-062 assert "the three open migration issues", making the omission part of the test. | FR-006-AC-3, TC-062, spec/spec.md, manifest.yaml | missing-requirement |
| FND-006 | medium | Declared verification method `Inspection` is discharged by an automated test with no `Inspections` artifact and no owning issue. FR-002-CON-1/CON-2/CON-4 and FR-004-CON-3 read `Inspection` at HEAD; the matrix types their rows `Static`/`Unit`; its own Coverage Gaps admits no `Inspections` and no `SuiteRegistry` document exists; the engine confirms both with `[archetype-matches-nothing]`. | FR-002-CON-1, FR-002-CON-2, FR-002-CON-4, FR-004-CON-3, TC-022, TC-047 | wrong-requirement |
| FND-007 | medium | TC-022 (FR-002-CON-1, "the official emitter only; no hand-edited emitted file") is largely tautological. Three of its five assertions grep the generator's own source text and `scripts/*.mjs` filenames, and a fourth compares `record["emitter"]["name"]` to the literal the generator hard-codes at `scripts/generate-schemas.mjs:185`. The only load-bearing line is a verbatim duplicate of TC-015's drift assertion, so CON-1 has no evidence of its own. | TC-022, FR-002-CON-1 | correct-requirement-no-evidence |
| FND-008 | medium | Both skeletons declare `ocl` invariants that nothing evaluates, and one of them is a safety rule with no other home. `AcceptedHazardCarriesProvenance` restates the schema's `allOf`, but `UnassessedSeverityIsNotClosed` — a hazard whose severity is `not_assessed` may not be `closed` — exists only as a verbatim string. No requirement, test or owning issue records that no evaluator exists. | FR-005-AC, hazard.md, failure_mode.md | missing-requirement |
| FND-009 | medium | The ticket's merge gate "Safety/security analysis is required before release" has no committed artifact on this branch: `spec/reviews/` at HEAD holds `base.md` alone. A `security.md` and a `failure-domain.md` exist only as untracked files in the moving working tree, alongside six more. | spec/reviews/, issue #2 gate | correct-requirement-no-evidence |
| FND-010 | medium | TC-025 (FR-002-CON-5, no hard-coded `$id` version) greps only `tests/**/*.py` for one literal form. CON-5's scope is "acceptance criterion, test, **or fixture**", so `tests/fixtures/` and `spec/` are never scanned and a version written any other way passes. TC-017 (FR-002-AC-6) is narrower than its criterion too: it checks the wheel for the 2 record models, not the 15 emitted schemas. | TC-025, TC-017, FR-002-CON-5, FR-002-AC-6 | correct-requirement-no-evidence |
| FND-011 | medium | Code with no owning requirement. `scripts/stage-npm.mjs`'s `GITHUB_REF_NAME` version-stamping and `package.json`'s `publishConfig` (public `registry.npmjs.org`, `access: public`, for an `@agent-ix` package) are unowned — FR-002-AC-7 covers only the prepack/postpack staging. `coverage.implements` is 0 over 69 production symbols: no production symbol carries an `implements` marker. | scripts/stage-npm.mjs, package.json, FR-002-AC-7 | missing-requirement |
| FND-012 | medium | Five FR-002 Behavior clauses have no test at all: the `make schemas` / `make lint` → `schemas-check` wiring (every generator test shells `node scripts/generate-schemas.mjs` directly), the `.gitattributes eol=lf` rule, the Node-older-than-20 refusal, the `normalization.applied: false` path, and the `tsp compile` failure path. | FR-002, Makefile, scripts/generate-schemas.mjs | correct-requirement-no-evidence |
| FND-013 | medium | FR-003-AC-6's digest half is untested in either direction. TC-032's live half asserts the refusal only as *silence* (`archetype_names() == []`) closed by an unqualified `pytest.raises(Exception)`, which is the opposite of "refused **naming** the key or the path"; and the strict-xfail body that does assert naming (`test_the_refusal_names_the_offending_key_and_path`) never touches the altered-digest copy despite its name, so it isolates `quire-rs#221` only and leaves `quire-rs#394` unevidenced. | TC-032, FR-003-AC-6 | correct-requirement-no-evidence |
| FND-014 | medium | Two FR-005 obligations are asserted vacuously or not at all. AC-3's "zero unresolved type tokens" is asserted against documents that cannot produce one — every skeleton field target is a kernel scalar, so the `ix://` resolution loop body never runs and the bundle index is never load-bearing. And the Behavior clause "the extracted `clauses` SHALL carry a source span" has no test anywhere: no `sourceSpan` / `source_span` assertion exists in `tests/`. | TC-050, FR-005-AC-3, FR-005 | correct-requirement-no-evidence |
| FND-015 | low | TC-070 / IT-001 carry `🚧` on the stated ground that the ambient `quoin` CLI cannot run the test, but the test passed in this environment as part of the observed suite run. The row and its Coverage Gaps entry under-report, and `plan.md`'s Requirements Summary leaves `- [ ] IT-001` unchecked while `Task-009` is `status: done`. | TC-070, IT-001, Task-009, Plan-001/plan.md | correct-requirement-no-evidence |
| FND-016 | low | TC-039's closing assertion, `unassessed != dict(ASSESSMENT, severity="negligible")`, compares two dicts that differ by construction and can never fail; the criterion's real content ("`not_assessed` is not a scale member") is carried by TC-040 instead. TC-014 likewise checks only the semantic-core URL **prefix**, never that the referenced model exists in the installed package. | TC-039, TC-014, FR-004-AC-5, FR-002-AC-3 | correct-requirement-no-evidence |
| FND-017 | low | The Markdown contract and the record contract disagree about whether a hazard may be unscored: the `assessment` locator is `required: true`, but `assessment` is optional in `Hazard.json`. The asymmetry is a consequence of the `quoin#335` extraction gap `spec/spec.md` records, but it is not itself recorded, so only the advisory half of "a hazard cannot be recorded unscored" is live. | manifest.yaml, Hazard.json, FR-001-AC-2 | missing-requirement |
| FND-018 | low | Three more assertions are weaker than the criterion they carry. TC-052's "detail beyond the `expect` token" guard is `len(hit) > len(expect)`, satisfied by one extra character, and the two identity fixtures assert only the generic `semantic.record-invalid` token without asserting that identity is what was refused. TC-059 (FR-005-CON-1) matches path prefixes this repository has never contained, and a diff of this repository structurally cannot show an edit to a sibling module. TC-064 covers FR-006-CON-1's verb half only — a safety-only *type* synonym would pass it and TC-060 both. | TC-052, TC-059, TC-064, FR-005-CON-1, FR-006-CON-1 | correct-requirement-no-evidence |
| FND-019 | low | Matrix bookkeeping: `TC-008` and `TC-009` do not exist and the Test Case Summary jumps `TC-007` → `TC-010`; and `coverage.self_named_binding.python` is 0/3 with a `[hollow-denominator]` diagnostic — three test names carry an id in their own name that no declared form reads, e.g. `test_zero_020_locators_changed`. | spec/tests.md, tests/test_additive_compatibility.py | wrong-requirement |

## Coverage

- Reconciliation: `quire coverage --scope .` (quire 0.31.0, cli `4f6ed024`, engine 0.46.0 `ca7362d4`), run both against the live worktree and against a clean `git archive` of HEAD `77a976e` — identical result, so the number is not an artifact of the concurrent edits.
- Tasks done: 11 / 11 (`Task-001`..`Task-011`, every one `status: done`).
- Rows backed by a tagged test: 125 / 125 (100%) — 69 `TC-` rows from `spec/tests.md` plus 56 acceptance-criterion rows minted from 8 requirement documents. `unbacked_rows`: 0. `status_lies`: 0. Status classification was **skipped** (FND-003), so this is a binding census only.
- Binding census: python 70 bound / 70 tagged / 72 candidates; every bound symbol is a `@pytest.mark.trace`-decorated `test_` function, so the rollup is not carried by non-binding symbols. The 2 untagged candidates are the two `xfail` halves of TC-032 and TC-067, each of which shares its tag with the passing half.
- Untracked symbols: 4 (`IT-001-SC-02`..`SC-05`, FND-004).
- Shared trace ids: 2 (`TC-002`, `TC-005` each split across two test functions) — legitimate, not double counting.
- Pass census, observed: `make test` → 70 passed, 2 xfailed (the branch records 69 + 2; FND-001). Taken against a moving tree, and not reproducible at HEAD because HEAD's `tests/test_record_schemas.py` contradicts the tree's schemas (FND-002).
- `quire validate --scope . "spec/**/*.md"` and `"plan/**/*.md"`: exit 0, grammar warnings only (`ears:non-singular`, `quality:agentless-passive`).
- Untraced behaviors / unowned code: 3 (FND-011, FND-012).
- Semantic review: ran, over FR-001..FR-006 and NFR-001. The module's headline claim holds — `EpistemicState`'s three members are disjoint from all six enums, every scored axis is an `anyOf` of its scale and `EpistemicState`, TC-040 verifies this exhaustively over the finite domain against member lists authored independently in `tests/conftest.py` rather than read back from the schemas, and TC-046 shows a validating record gains no status, score or acceptance. No schema declares a `default`. Schema validity implies no safety claim.
