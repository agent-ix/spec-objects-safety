---
id: SR-010
title: "Code review of the semantic-module-contract migration on spec/2-semantic-module-contract"
type: SpecReview
analysis: code-review
scope: "typespec/main.tsp, scripts/, spec_objects_safety/, tests/, tests_integration/, spec/tests.md, spec/functional/, pyproject.toml, Makefile, package.json, .github/workflows/"
review_set: subset
---
# Code review of the semantic-module-contract migration on spec/2-semantic-module-contract

## Summary

Full code review of `agent-ix/spec-objects-safety#2` (branch
`spec/2-semantic-module-contract`, worktree
`.worktrees/2-semantic-module-contract`) against `origin/main` and against the
already-merged sibling migration `agent-ix/spec-objects-business#4` (`567e5c4`).
Every gate was run rather than assumed: `make lint` green (ruff, black,
`generate-schemas.mjs --check` — 15 schemas match), `poetry run pytest tests/ -q
--no-cov` 69 passed / 2 xfailed, `node scripts/generate-schemas.mjs --check`
green, `quire validate --scope . "spec/**/*.md"` error-free (25 EARS grammar
warnings), and `quire coverage --scope .` reports 125/125 matrix rows backed
with 70/70 python evidence symbols bound.

The engineering is strong and, on the central question asked of a safety
module, clean: **no schema constraint, gate or test was weakened to get green.**
Verified positively rather than assumed — the vendored FR-035 module-manifest
schema under `tests/fixtures/` is *byte-identical* to
`agent-ix/spec-artifacts-iso` at the pinned revision `6686f11` (fetched from
GitHub and diffed), so the gate substitution TC-034 guards is honest; the two
`@pytest.mark.xfail(strict=True)` rows each name a real, open upstream defect
whose GitHub title matches the stated behaviour (`quire-rs#391` for the
legacy-form error, `quire-rs#221` + `quire-rs#394` for the unnamed refusal), so
neither hides a local bug; the widened `lint_rules` allow-lists only *add* the
three `EpistemicState` tokens and TC-069 asserts nothing was dropped; and the
uncommitted working tree strengthens the schemas further (dual sealing with
`additionalProperties: false`, `accepted` requiring the scored record).

Three problems sit under that. The strengthening is uncommitted, so the branch
as pushed is not the branch that passes these gates; the strengthened
acceptance rule now contradicts the requirement and the acceptance criterion it
traces to, while the Test Matrix still reports that row green; and a
free-floating TypeSpec doc comment silently attached itself to `IdentityField`,
shipping a description that states the opposite of that model's intent.

## Verdict

**FAIL** — two high findings: a shipped safety rule that contradicts its own
requirement, AC and Test Matrix row (FND-001), and 24 files of unpublished work
including that rule (FND-002). Both are small edits; nothing found requires
rework of the design.

## What was checked

- Every file in `git diff origin/main...HEAD`, plus the 16 modified and 8
  untracked files in the worktree that are *not* in that range.
- Gates run locally: `make lint`, `pytest tests/`, `generate-schemas.mjs
  --check`, `quire validate`, `quire coverage`.
- Trace-tag binding: no `@pytest.mark.trace` is formatter-wrapped (no
  `pytest.mark.trace(` at end of line anywhere), no requirement id sits in a
  comment or a non-binding docstring ahead of another symbol, and `quire
  coverage` reconciles at 70/70 bound.
- `scripts/generate-schemas.mjs` and `scripts/stage-npm.mjs` diffed against the
  merged `spec-objects-business` copies: identical modulo the module name, the
  package directory and the issue URL. No local divergence.
- Repo idiom honoured: plain pytest functions with `@pytest.mark.trace(...)`,
  no test classes, no `mocker`. Not reported as findings.

## Findings

| ID      | Severity | Summary                                                                                                      | Refs                                                                                 | Escape Cause                        |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----------------------------------- |
| FND-001 | high     | `status: accepted` now also requires the scored record, contradicting FR-004, FR-004-AC-8 and TC-042, all still green | typespec/main.tsp:278, typespec/main.tsp:312, spec/functional/FR-004-type-distinct-safety-schemas.md:59, spec/functional/FR-004-type-distinct-safety-schemas.md:86, spec/tests.md:131 | wrong-requirement                   |
| FND-002 | high     | 16 modified and 8 untracked files are uncommitted; the pushed branch lacks the dual seal, the acceptance rule, the engine pin and 8 review artifacts | spec_objects_safety/manifest.yaml:110, tests/conftest.py:207, spec/reviews/2-semantic-module-contract/ | correct-requirement-no-evidence     |
| FND-003 | medium   | A free-floating `/** ... */` doc comment binds to `IdentityField` and concatenates into its emitted description, which now claims the model is sealed when it is deliberately open | typespec/main.tsp:34, spec_objects_safety/schemas/IdentityField.json:14              | implementation-bug-despite-evidence |
| FND-004 | medium   | Four of IT-001's six success criteria bind nothing: the range form mints only the endpoints        | spec/tests.md:145, tests_integration/test_quoin_install_roundtrip.py:47              | correct-requirement-no-evidence     |
| FND-005 | medium   | Four constraints were flipped Inspection to Test but the matrix still types their rows `Static` and Coverage Gaps still claims no `Inspections` document covers them | spec/functional/FR-002-emitted-json-schemas.md:80, spec/tests.md:120, spec/tests.md:210 | wrong-requirement                   |
| FND-006 | low      | `traceability.status.column` is `Status` and the authored header is `Coverage Status`, so status classification is skipped and the branch's new `🚧` rows are never gate-checked | spec/tests.md:66                                                                     | correct-requirement-no-evidence     |
| FND-007 | low      | TC-049's clause assertion is `A == B or [ids] == [ids]`; the first disjunct can never hold, so only `clauseId` is compared | tests/test_skeletons_semantic.py:99                                                  | correct-requirement-no-evidence     |
| FND-008 | low      | The CI job runs bare `poetry run pytest` with no `make dev-quire` and no `npm ci`, so a manual dispatch cannot pass the new suite | .github/workflows/ci.yml:22, pyproject.toml:80                                       | correct-requirement-no-evidence     |
| FND-009 | low      | TC-057's skip-token scan and TC-025's version-literal scan walk `tests/` only, leaving `tests_integration/` unpoliced | tests/test_skeletons_semantic.py:283, tests/test_schema_emission.py:355              | correct-requirement-no-evidence     |
| FND-010 | low      | Six of the eight untracked spec review artifacts share `id: SR-002`, and `quire validate` does not catch it | spec/reviews/2-semantic-module-contract/dependency.md:3                              | correct-requirement-no-evidence     |
| FND-011 | low      | 25 EARS grammar warnings on the new FR/NFR bodies (non-singular `shall`, agentless passive)         | spec/functional/FR-005-executable-skeletons.md:48                                    | wrong-requirement                   |
| FND-012 | low      | `# pragma: no cover` marks the two missing-engine branches, which TC-057 does exercise; the merged business model carries none | tests/conftest.py:196, tests/conftest.py:199                                          | correct-requirement-no-evidence     |

## Finding detail

### FND-001 — the shipped acceptance rule contradicts its own requirement

`typespec/main.tsp` now emits, on both record models:

```json
"then": { "required": ["provenance", "assessment"] }
```

(`analysis` for `FailureMode`). `tests/test_record_schemas.py` was updated to
match and asserts, for the exact record FR-004-AC-8 says must validate:

```python
assert not valid(validator, dict(base, status="accepted", provenance=PROVENANCE)), \
    f"{model}: accepted with nothing scored to accept passed"
```

FR-004's own statement (line 59) still says *"If `status` is `accepted`, then
`provenance` SHALL be required"* and nothing more; FR-004-AC-8 still says *"the
same record with a `provenance` naming `assertedBy` and `assertedAt`
validates"*; `spec/tests.md` TC-042 repeats that sentence and carries `✅`. The
implementation is the stricter and better rule — a hazard `accepted` with no
severity ever assigned is this module's central failure wearing a lifecycle
state — but as authored, the second clause of AC-8 is refuted by the shipped
schema while the matrix reports the criterion fully backed. This is the one
place in the branch where a criterion and the code disagree and the disagreement
is not recorded: TC-032 and TC-067 handle exactly this situation honestly, with
a strict xfail and a named issue. Fix the requirement, the AC and the TC title;
do not relax the schema.

### FND-002 — the branch that passes these gates is not the branch that was pushed

`git status` in the worktree shows 16 modified tracked files and 8 untracked
files that appear in no commit. The uncommitted delta is substantive and is all
improvement:

- `@extension("additionalProperties", false)` on all six sealed models, because
  `unevaluatedProperties` is 2020-12-only and a draft-07 consumer would silently
  accept a `Hazard` carrying `analysis`;
- the `accepted` rule of FND-001;
- `quire>=0.46.0` tightened to `quire==0.46.0` in `make dev-quire`, plus a new
  `QUIRE_VERSION` guard in `require_quire()` so the two strict xfails cannot be
  judged against an engine they were not reasoned against;
- the README's "What this module ships" section;
- eight `spec/reviews/2-semantic-module-contract/*.md` review artifacts.

Every gate reported in this review was run against that working tree. A reviewer
reading the PR, and CI, see `77a976e` instead — without the dual seal, without
the acceptance rule, with a floating `>=` engine constraint. Commit it.

### FND-003 — a doc comment landed on the wrong model

The explanation of the dual seal was written as a `/** ... */` doc comment
placed on its own under the `// Support models` banner at `typespec/main.tsp:34`.
TypeSpec attaches it to the next declaration, `IdentityField`, and the emitter
concatenates the two blocks with no separator. `IdentityField.json` now ships:

> `... and is redundant only where the consumer is already on 2020-12.Open
> marker: a `FieldDecl` flagged as identity ... it is deliberately open ...`

`IdentityField` is the one model that intentionally has no seal, so its
published description now opens by asserting the opposite of its own second
paragraph. `make schemas-check` cannot catch this — the committed bytes match
the source exactly. Change the block to `//` line comments and re-run `make
schemas`.

### FND-004 — IT-001-SC-02..SC-05 bind nothing

`quire coverage --scope .` reports, four times:

> `test_quoin_installs_the_module_and_quire_loads_it_from_the_catalog ... traces
> to IT-001-SC-02, which matches no declared row`

The test's two stacked `@pytest.mark.trace` marks name all six criteria
explicitly and are read correctly. The gap is on the matrix side:
`spec/tests.md:145` writes the success criteria as the range
`IT-001-SC-01..IT-001-SC-06`, and only the two literal endpoints mint rows. Four
of the six steps of the only integration test in the branch are therefore
unbacked in the census while the row reads as covered. Enumerate them.

### FND-005 — Static rows for constraints that are now Test

The uncommitted spec edits flip FR-002-CON-1, FR-002-CON-2, FR-002-CON-4 and
FR-004-CON-3 from `Inspection` to `Test`, correctly: each is discharged by an
automated test. But `spec/tests.md` still types TC-022, TC-023, TC-025 and
TC-047 as `Static`, and the Coverage Gaps section still records that "no
`Inspections` document exists for the `Static` rows (TC-022, TC-023, TC-025,
TC-059)". After the flip, three of those four are no longer Static and the
recorded evidence-plan gap is smaller than stated.

### FND-006 — the status column the matrix declares is not the one it has

`quire coverage` reports `[status-column-matches-nothing]`: the
`functional-coverage` declaration reads a `Status` column, the authored header is
`Coverage Status`, and "status classification was skipped, so complete-but-unbacked
rows could not be checked". This is pre-existing — the same diagnostic appears on
`origin/main` — but it matters more now, because this branch is the first to
introduce `🚧` rows (FR-001, IT-001) whose whole purpose is to be
distinguishable from `✅`, and nothing checks them.

### FND-007 — TC-049 compares clause ids only

FR-005-AC-2 requires the table and `sysml` skeletons to extract to identical
normalized fields. `fields` is compared strictly and passes. `clauses` is not:

```python
assert table["clauses"] == fence["clauses"] or [
    c["clauseId"] for c in table["clauses"]
] == [c["clauseId"] for c in fence["clauses"]], name
```

Executing both extractions confirms the first disjunct can never be true — each
clause carries a `sourceSpan` whose `path` and line numbers necessarily differ
between two files — so the assertion reduces to a comparison of `clauseId`
lists. `language`, and any future clause facet, are unasserted. Compare the
clauses with `sourceSpan` stripped instead, and the assertion says what the
criterion says.

### FND-008 — CI cannot run the suite it now owns

`ci.yml` delegates to `python-service-actions/.github/workflows/lib-ci.yml`,
whose test job is `poetry run pytest` after `poetry install`. The new suite
needs `quire` 0.46.0 (deliberately not a declared dependency —
`agent-ix/quire-rs#392`), `node_modules/@agent-ix/semantic-core` for `$ref`
resolution, a Node toolchain for `npm pack` (TC-018), and `poetry build`
(TC-017). None is provisioned. The failure is loud rather than silent, the
workflow is `workflow_dispatch`-only by repo policy, and the merged
`spec-objects-business` migration has the same shape — so this is recorded, not
charged against the branch.

## Not findings

Checked and deliberately not reported:

- **No test classes, no `mocker`.** Documented repo idiom; the merged sibling is
  the same.
- **The widened `lint_rules` allow-lists.** Advisory table-column lints gaining
  `unknown` / `not_assessed` / `not_applicable`. TC-069 asserts no 0.2.0 value
  was dropped and no rule added or removed; the emitted schemas keep the
  epistemic states disjoint from every ordinal scale (TC-040, TC-071). Widening
  an advisory to admit "nobody looked" is not a relaxation — refusing the honest
  token was the defect.
- **The vendored `module-manifest.schema.json`.** Byte-identical to
  `spec-artifacts-iso@6686f11`; TC-034 additionally diffs it against the
  installed release and fails on the first assertion once a release carries the
  `semantic` key.
- **Both strict xfails.** `quire-rs#391`, `#221` and `#394` are all open and
  their titles state exactly the behaviour the reasons describe.
- **`--cov-fail-under=100`.** Vacuous, since `spec_objects_safety` is one
  13-line `__init__.py` — but unchanged from `main` and from the merged sibling.
- **TC-018 staging files at the repository root.** It cleans up in a `finally`
  and asserts `postpack` ran; the hazard it guards against is real and stated.
