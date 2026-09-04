---
id: SR-001
title: "Base review of the issue #2 semantic-module-contract specification"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/tests.md, spec/stakeholder/StR-001, spec/usecase/US-001, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001, spec/integration/IT-001"
review_set: base
---
# Base review of the issue #2 semantic-module-contract specification

## Summary

Checklist review (id formats and sequence, story and requirement quality, the
six coverage rules, cross-references) of the specification authored on
`2-semantic-module-contract` for `agent-ix/spec-objects-safety#2`, measured
against the already-merged `agent-ix/spec-objects-business` migration as the
model. Structurally the bundle is sound: `quire validate --scope . "spec/**/*.md"`
exits zero with no errors, every FR links its US or StR, every index lists its
artifacts, ids are well-formed (`StR-001`, `US-001`, `FR-001..FR-006`,
`NFR-001`, `IT-001`, `TM-001`, `TC-001..TC-070`), and the requirement bodies are
unusually well-reasoned about the safety-specific distinctions they exist to
protect.

Two high findings sit under that surface. First, the Test Matrix marks 70 of 70
test cases `✅` while only 11 distinct `TC-` ids carry a real
`@pytest.mark.trace` tag in `tests/`; `quire coverage --scope .` reports
**1/123 rows backed (0%)**, against a matrix whose own Overview defines
completeness as "backed by a real `@pytest.mark.trace` tag" and whose Coverage
Gaps section records only three exceptions. Second, the safety scales the whole
specification turns on — `Severity`, `Likelihood`, `Exposure`, `Controllability`,
`Detection`, `LifecycleStatus` — are enumerated nowhere in `spec/`; they exist
only in `typespec/main.tsp`, so `FR-004-AC-6` and matrix rule 5 cannot be
evaluated from the specification, and only `EpistemicState` is actually fixed by
a requirement.

Nine mediums and eight lows follow, mostly coverage bookkeeping (an untested
constraint, four mistraced rows, stakeholder criteria that no test case names,
an ungrounded NFR criterion) plus one genuine consistency defect between
`FR-002`'s `make lint` obligation and `FR-002-CON-4`.

## Verdict

**CONDITIONAL** — two highs must be dispositioned before planning. Findings are
reported only; no spec artifact was edited by this review.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | The Test Matrix marks all 70 `TC-` rows `✅`, but only 11 distinct ids are tagged in `tests/` (TC-001..TC-007, TC-010, TC-011, TC-034, TC-057). `quire coverage --scope .` reports `Coverage: 1/123 rows backed (0%)` and `has no backing symbol` for 59 rows, including every FR-002, FR-004, FR-005, FR-006, NFR-001 and IT-001 row. The matrix Overview defines coverage as complete only when each row is "backed by a real `@pytest.mark.trace` tag", and Coverage Gaps records three exceptions — the measurement says fifty-nine. Either the status column is aspirational and must read `🚧` until the tests land, or the tags are missing. Escape cause: correct-requirement-no-evidence. | spec/tests.md Test Case Summary, Coverage Gaps |
| FND-002 | high | The ordinal safety scales are never enumerated in `spec/`. `Severity`, `Likelihood`, `Exposure`, `Controllability`, `Detection` and `LifecycleStatus` are named as models in FR-002-AC-1 and constrained as axes in FR-004, but their members exist only in `typespec/main.tsp`. FR-004-AC-6 ("accepts every member of its own scale ... rejects a member of another scale") and matrix rule 5 therefore cannot be evaluated from the specification, and the module's headline property — `not_assessed` never reads as the safe end — is asserted over vocabularies no requirement fixes. Only `EpistemicState` is enumerated (FR-004 Behavior); `negligible`, `none`, `accepted` and `identified` appear solely as incidental examples inside criteria. A future edit to `main.tsp` could add or drop a scale member with no requirement changing. Escape cause: missing-requirement. | FR-004 Behavior, FR-004-AC-5/AC-6/AC-8/AC-11, spec.md Scope, typespec/main.tsp:49-133 |
| FND-003 | medium | FR-001-AC-1 requires each object type to declare "a `data_schema` and at least one role", while FR-001's own body concludes "No role is declared either ... the `safety-relevant` capability tag this module first reached for turned out to be unnecessary", and TC-002 asserts `data_schema` and `allowed_links` instead. The criterion and the requirement that owns it contradict each other. The matrix self-discloses this and defers it to `agent-ix/spec-objects-safety#3`; recorded here because the contradiction is inside the bundle under review and FR-001 is in scope for the reader of this branch. Escape cause: wrong-requirement. | FR-001-AC-1, FR-001 "No new verbs", spec/tests.md TC-002 and Coverage Gaps §1 |
| FND-004 | medium | FR-001-CON-1 ("Hazard identification and scoring are authored judgement. Nothing in this module computes, infers, or defaults either", validation `Inspection`) appears in the FR-001 coverage row's criterion list but in no `Traces To` cell of the Test Case Summary. Coverage rule 1 (every named constraint has ≥ 1 test case) is unmet for it. The nearest row, TC-046, traces FR-004-CON-2 only. Escape cause: correct-requirement-no-evidence. | FR-001-CON-1, spec/tests.md |
| FND-005 | medium | Four rows trace criteria they do not assert. TC-006 (the pack exposes `MANIFEST_PATH`/`PACK_ROOT`), TC-010 (bidirectional coverage is manifest data) and TC-011 (every relation names a declared type and an iso verb) all trace `FR-001-AC-4`, which is about skeleton headings supplying the contract; TC-070 (Quoin install roundtrip) traces `FR-003-AC-5`, the byte-for-byte traceability-model criterion, which its six-step procedure never exercises (that criterion is already covered by TC-031). The traced criteria are covered elsewhere, so this inflates apparent coverage rather than losing it. Escape cause: wrong-requirement. | spec/tests.md TC-006, TC-010, TC-011, TC-070 |
| FND-006 | medium | StR-001-VC-1 and StR-001-VC-2 appear in no `Traces To` cell (`grep 'StR-001-VC' spec/tests.md` → 0 hits). The Stakeholder Requirement Coverage row cites TC-003, TC-048 and TC-063, each of which traces FR criteria only, so the stakeholder validation criteria are covered by a narrative roll-up rather than by traced evidence. VC-2 is additionally `Inspection`-verified with no inspection artifact anywhere in the bundle. Escape cause: correct-requirement-no-evidence. | StR-001 Validation Criteria, spec/tests.md Stakeholder Requirement Coverage |
| FND-007 | medium | Two tests carry a trace id that matches nothing: `quire coverage` reports `test_no_verb_outside_the_declared_iso_vocabulary` and `test_tc011_the_relation_vocabulary_is_the_declared_one` in `tests/test_manifest.py` tracing to `FR-041-AC-2`, "which matches no declared row". The id is a prose reference to `spec-artifacts-iso` FR-041 inside a comment (lines 106 and 275) that the `python-comment-id` trace form mints as a real tag. A cross-repo requirement id written in a comment silently becomes a dangling trace. Escape cause: correct-requirement-no-evidence. | tests/test_manifest.py:106,275; `quire coverage --scope .` |
| FND-008 | medium | FR-002 Behavior requires "`make lint` SHALL run `make schemas-check`, so a `typespec/` edit that was never regenerated fails before push", and `schemas-check` runs the generator, which compiles `typespec/` and exits non-zero when the compiler is absent. FR-002-CON-4 states that `@agent-ix/semantic-core` "resolves from npm.ix through the user-level npm config ... so `make schemas` runs on a developer machine rather than in the GitHub workflow". The two obligations collide wherever `make lint` runs without the npm.ix toolchain, and no criterion or matrix row covers that path — TC-023/TC-024 check the pins, not the gate's behaviour when the toolchain is unavailable. Escape cause: missing-requirement. | FR-002 Behavior, FR-002-CON-4, pyproject.toml `[tool.poe.tasks.lint]` |
| FND-009 | medium | All four NFR-001 Measurement methods are uncatalogued: `quire coverage` reports `uncatalogued-verification-method` for "Baseline diff against `tests/fixtures/baseline-0.2.0`", "Manifest inspection in test", "Structural comparison against the 0.2.0 model" and "Validation of the checked-in 0.2.0 skeletons" — none is a catalog method id or a declared class, so nothing can say what discharging them means. This is the same class of defect the business review raised as FND-003 for FR-001's Verification cells. Escape cause: wrong-requirement. | NFR-001 Measurement and Evaluation |
| FND-010 | medium | NFR-001-AC-5 ("Widening the three advisory lint allow-lists refuses no value they admitted at 0.2.0") is ungrounded: neither the Statement, the Scope, the Rationale nor the four Measurement metrics mention lint allow-lists, and no artifact in the bundle names the three lists or says what was widened. The criterion is untestable as written from the spec alone, and its supporting metric row is missing. Escape cause: missing-requirement. | NFR-001-AC-5, NFR-001 Statement/Scope/Measurement |
| FND-011 | medium | `spec/log.md` has no entry for this change: its newest entry is the 2026-08-18 module minting, while the branch adds US-001, FR-002..FR-006, NFR-001, IT-001 and converts `tests.md` to a `TestMatrix`. The merged business migration recorded exactly this in two dated entries (`spec-objects-business/spec/log.md:11-12`), and the log archetype's own description is "Chronological log of structural changes to this bundle". Escape cause: correct-requirement-no-evidence. | spec/log.md |
| FND-012 | low | The `TC-` sequence skips TC-008 and TC-009: the matrix runs TC-001..TC-007 then TC-010. Neither id exists on `main` either, so the gap is an allocation artifact rather than a deletion, but the checklist's "ids are sequential" item is unmet. Escape cause: wrong-requirement. | spec/tests.md Test Case Summary |
| FND-013 | low | US-001 carries illustrative examples (US-001-EX-1..3) rather than Given/When/Then acceptance criteria, so the checklist's "≥ 2 acceptance criteria" item is satisfied by examples plus the FR criteria they lead to. This follows the `spec-artifacts-iso` US skeleton and matches the merged business precedent exactly. No change recommended. | US-001 |
| FND-014 | low | `quire coverage` reports `status-column-matches-nothing`: the `functional-coverage` declaration reads a `Status` column, and the coverage tables authored here use `Coverage Status`, so status classification is skipped and complete-but-unbacked rows go unchecked — which is part of why FND-001 was invisible to the gate. Pre-existing and byte-identical in `spec-objects-business/spec/tests.md`, so it is an ecosystem-level header/declaration mismatch, not a defect this branch introduced. Escape cause: wrong-requirement. | spec/tests.md coverage tables |
| FND-015 | low | No error condition anywhere in the bundle carries a diagnostic code. FR-002, FR-003 and FR-005 enumerate failure paths carefully in prose ("SHALL exit non-zero naming each such file", "refused naming `foo`") but nothing gives a consumer a stable identifier to assert on, and the criteria assert prose fragments instead. Acceptable for a Markdown-and-JSON module; recorded against the checklist item. Escape cause: missing-requirement. | FR-002 Behavior, FR-003 Behavior, FR-005 Behavior |
| FND-016 | low | `quire validate` emits 29 grammar warnings on the new artifacts — 22 `ears:non-singular` (one statement, several `shall`) and 7 `quality:agentless-passive` (`shall be required`, `shall be reached`, `shall be refused`, `shall be minted`, `shall be relaxed`, `shall be edited`), concentrated in FR-004..FR-006. Zero errors. Belongs to an `ears-conformance` analysis, which this `base` set did not run. Escape cause: wrong-requirement. | FR-002:71,74; FR-003:52,61; FR-004:35-46,42,55; FR-005:48-56,49,64; FR-006:38-50; NFR-001:14 |
| FND-017 | low | `spec.md` frontmatter declares `depends_on: []` while its `relationships` block declares four `depends_on` edges (filament-core-service FR-035, filament-core-data FR-031, quoin FR-070, quire-rs FR-069). The empty list is at best redundant and at worst read by a consumer as "no dependencies". Escape cause: wrong-requirement. | spec/spec.md frontmatter |
| FND-018 | low | FR-003 Behavior restates IT-001's procedure ("The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic, and `quoin module` SHALL then list `spec-objects-safety`"), duplicating the integration allocation in a functional requirement. IT-001 already owns that boundary and FR-003 has no criterion for it — the obligation is stated twice and traced once. Escape cause: wrong-requirement. | FR-003 Behavior, IT-001 Test Procedure |
| FND-019 | low | No `SuiteRegistry` document declares a producer for the `Unit`, `Integration`, `Static` and `Property` evidence kinds, and no `Inspections` document exists for the five `Static` rows; `quire coverage` reports `archetype-matches-nothing` for both declarations. Self-recorded at the end of the matrix and deferred to the plan; repeated here so the deferral is visible in the review record. Escape cause: correct-requirement-no-evidence. | spec/tests.md Coverage Gaps, `quire coverage --scope .` |

## Automated Checks

| Check | Result |
|---|---|
| `quire validate --scope . "spec/**/*.md"` | Exit 0. Zero errors. 29 grammar warnings (FND-016). Registry advisories are environmental (`DuplicateModuleName: 'spec-objects-safety' declared at 2 path(s)` — the worktree plus the installed catalog copy; `DuplicateArchetype` for `spec-artifacts-process`; `DuplicateInverseEdge part_of`). |
| Id format | ✅ `StR-001`, `US-001`, `FR-001..FR-006`, `NFR-001`, `IT-001`, `TM-001`, `TC-001..TC-070`, `{PARENT}-AC-N`, `{PARENT}-CON-N`, `{PARENT}-VC-N`, `{PARENT}-SC-NN`, `US-001-EX-N` all well-formed. |
| Duplicate ids | ✅ none. |
| Id sequence | ❌ TC-008 and TC-009 unallocated (FND-012). All other classes contiguous. |
| Link integrity | ✅ every relative link resolves; every `ix://` target is a declared external requirement; every directory index lists its artifacts. |
| Trace backing | ❌ `quire coverage --scope .` → 1/123 rows backed (0%); 11 TC ids tagged; 2 dangling `FR-041-AC-2` traces (FND-001, FND-007). |

## Coverage Rules

1. **Coverage** — every AC and named CON has ≥ 1 matrix row except **FR-001-CON-1** (FND-004); StR-001-VC-1/VC-2 have none by id (FND-006). Per requirement: FR-001 7 AC + 2 CON, FR-002 9 AC + 5 CON, FR-003 7 AC + 3 CON, FR-004 11 AC + 3 CON, FR-005 10 AC + 3 CON, FR-006 4 AC + 2 CON, NFR-001 5 AC + 4 metrics, IT-001 6 SC. Rows exist; tagged evidence does not (FND-001).
2. **Option permutation** — both Properties forms (typed table, `sysml` fence) × both object types are covered by TC-049 and TC-058; both `data_schema` forms (reference vs inline) by TC-027 and FR-003's prohibition; both engine-present and engine-absent paths by TC-057.
3. **Constraint boundary** — zero versus one identity field (TC-036, TC-037), forbidden key present versus absent (TC-037, TC-038), digest matching versus mutated (TC-015, TC-027, TC-032), version pair bumped together versus half (TC-019). Boundaries on the ordinal scales themselves cannot be checked because the scales are unenumerated (FND-002).
4. **Error path** — digest mismatch, unknown `semantic` key, both Properties forms, missing `Assessment` table, clause heading with no fence, non-`Identifier` token, `Analysis` missing `Detection`, stale committed schema: all seven named refusals have a negative fixture and a row (TC-020, TC-032, TC-052, TC-058). ✅
5. **State transition** — availability states per kind (`fields: available`, `clauses: available`, `operations: not_applicable`) in TC-051; the `LifecycleStatus` transitions themselves are neither enumerated nor tested, and only the `accepted`-requires-`provenance` edge is asserted (TC-042). Partial, on FND-002.
6. **Edge case** — hazard with no `relations` (the STPA case, TC-043), `not_assessed` ≠ `negligible` (TC-039), `detection: none` ≠ `not_assessed` (TC-045), legacy prose Properties block (TC-067), 0.2.0 skeletons under 0.3.0 (TC-066). ✅ — the safety-specific edges are the strongest part of the matrix.
7. **TC field completeness** — every row carries Type, Priority, Traces To and Status. ✅

## Notes

- Two rows are declared expected failures rather than passes, each naming the
  engine defect that owns it: TC-032 (`agent-ix/quire-rs#221`, `#394` — the
  refusal does not name the offending key or path) and TC-067
  (`agent-ix/quire-rs#391` — a legacy prose Properties block errors even under
  `legacy_forms: warning`). Both run and neither skips. This is the right
  disposition and is called out so a later reader does not mistake either for
  FND-001's unbacked-row class.
- The Out of Scope section of `spec.md` is unusually complete: fourteen
  exclusions, every one naming the issue that owns it. Nothing in it reads as a
  gate invented to avoid work — each is a published dependency or an open
  upstream defect.
- No spec artifact was edited by this review. Findings are reported for
  disposition by the branch author.
