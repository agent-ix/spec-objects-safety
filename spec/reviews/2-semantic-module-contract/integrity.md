---
id: SR-002
title: "Integrity review of the issue #2 semantic-module-contract specification"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/tests.md, spec/log.md, spec/stakeholder/StR-001-safety-object-types.md, spec/usecase/US-001-declare-safety-objects-against-semantic-core.md, spec/functional/FR-001-safety-object-types.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-type-distinct-safety-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-cross-module-references.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-quoin-module-install.md"
review_set: all
---
# SR-002: Integrity review of the issue #2 semantic-module-contract specification

## Summary

Integrity gate — completeness (US → FR → StR → verification), consistency and
conflict, atomicity and testability, plus the hidden-assumption probes and the
failure-domain check — over the thirteen artifacts that deliver
`agent-ix/spec-objects-safety#2`, grounded against the shipped
`spec_objects_safety/manifest.yaml` (0.3.0), the sixteen files under
`spec_objects_safety/schemas/`, `typespec/main.tsp`, `tests/conftest.py`, and
the merged `agent-ix/spec-objects-business` migration as the model.

This review deliberately adds to `base.md` rather than restating it. The base
set found the coverage-bookkeeping and enumeration defects; several have since
been closed on the branch (`spec/log.md` now carries the 2026-09-04 entry that
base FND-011 asked for, FR-004 Inputs now fixes the six ordinal vocabularies
that base FND-002 found nowhere in `spec/` and FR-004-AC-12/TC-071 assert them,
FR-001-CON-1 is now traced by TC-046, and NFR-001-AC-5 now has its metric row).
What follows is what an integrity pass sees underneath that.

Two highs. The first is the one that matters for a safety module: the module's
headline property — an unassessed axis says so, and never reads as the safe end
— is stated over records that the authoring path cannot produce. Three of the
five scored axes, and the `status`/`provenance` pair that carries risk
acceptance, have no column, no locator and no lint rule, so FR-004's own claim
that "the document form can express everything the schema admits" is false as
written, and the safety-critical rule FR-004-AC-8 is unreachable from any
document at 0.3.0. The second is structural: every shipped schema `$ref`s five
semantic-core documents that nothing this module ships carries, and no
requirement states how a consumer resolves them — the tests resolve them only
from a developer machine's `node_modules`.

Nine mediums (identity never made unique or linkable; two of issue #2's three
merge-gate items unallocated; an NFR the FRs it measures do not reference; an
emitted model with a real constraint and no owning requirement; an unspecified
wrong-engine-version path; an unstated duplicate-module tie-break; an
integration test that mutates global developer state with no failure-path
obligation; declared `Inspection` methods discharged by automated tests; and
FR-002 carrying three separable obligations) and seven lows follow.

## Verdict

**CONDITIONAL — not ready for `spec-to-plan`.** FND-101 and FND-102 need a
disposition before FR-004 and FR-002 are tasked: FND-101 is a scope decision
(state the consequence, or bring the axes into the document form once
`agent-ix/quoin#335` lands), FND-102 is a missing requirement about the
consumer-side resolution of `$ref`s the module already emits. The mediums are
new AC/CON/TC rows or one-line edits. No spec artifact was edited by this
review.

## Traceability Matrix

Completeness deliverable: US → FR → StR → verification. "(via US)" means the
only StR link is transitive through US-001.

| US | FR/NFR/IT | StR | Verification (AC/CON → TC) | Gap |
|---|---|---|---|---|
| — | FR-001 | StR-001 (direct, `satisfies`) | AC-1..7 → TC-001..TC-007; CON-1 → TC-046; CON-2 → TC-007 | AC-1 contradicts its own body (base FND-003) |
| US-001 | FR-002 | StR-001 (via US) | AC-1..9 → TC-012..TC-020; CON-1..5 → TC-021..TC-025 | not atomic (FND-111); AC-1 self-referential (FND-113) |
| US-001 | FR-003 | StR-001 (via US) | AC-1..7 → TC-026..TC-034; CON-1 → TC-026; CON-2 → TC-029; CON-3 → TC-034 | AC-4 names an empty manifest key (FND-114); one unobservable Behavior bullet (FND-116) |
| US-001 | FR-004 | StR-001 (via US) | AC-1..12 → TC-035..TC-045, TC-071; CON-1 → TC-044; CON-2 → TC-046; CON-3 → TC-047 | guarantee unreachable from documents (FND-101); `HazardContext` unspecified (FND-106) |
| US-001 | FR-005 | StR-001 (via US) | AC-1..10 → TC-048..TC-057; CON-1 → TC-059; CON-2 → TC-049, TC-058; CON-3 → TC-057 | wrong-version path unspecified (FND-107) |
| US-001 | FR-006 | StR-001 (via US) | AC-1..4 → TC-060..TC-063; CON-1 → TC-064; CON-2 → TC-062 | — |
| — | NFR-001 (`constrains` FR-003 only) | — | AC-1..5 → TC-065..TC-069; 5 metrics → same rows | measures FR-001/FR-004/FR-005 without referencing them (FND-105); AC-3 has no metric (FND-115) |
| — | IT-001 (`verifies` FR-003) | — | SC-01..06 → TC-070 | mutates global state, no failure-path SC (FND-109) |
| — | StR-001-VC-1, VC-2 | — | named by no `Traces To` cell (base FND-006) | VC-2 declared `Inspection`, credited to a Unit row (FND-110) |
| US-001-EX-1..3 | — | — | illustrative only; no TC names them by id | FND-118 |

Every FR maps to at least one verification method and at least one matrix row.
No FR other than FR-001 carries a direct StR relationship; the chain is
transitive through US-001 and `spec.md` §Requirements Architecture states it,
which matches the merged business precedent. Above the FR layer, no artifact
has evidence traced by id.

## Hidden Assumption Probes

| FR | Pattern | Result |
|---|---|---|
| FR-002 | Delegates to external CLIs (`node`, `tsp compile`) | Covered. Inputs pin `@typespec/compiler` 1.15.0 and Node 20, and Behavior states the failure ("exit non-zero naming the required Node version or the missing package"). |
| FR-002 | Depends on a registry-scoped package (`@agent-ix/semantic-core` on npm.ix) | Partly covered by FR-002-CON-4 for the *build*. The *consumer* side is unstated and is FND-102: the emitted `$ref`s point at semantic-core documents nothing ships. |
| FR-002 | Generation command | Both modes specified (`make schemas`, `--check`); no interactive mode needed. OK. |
| FR-002 | Emitted artifact consumed by a downstream generator | The `$id` version discipline is unusually well specified (AC-2, AC-8, CON-5, TC-025). OK. |
| FR-003 | Lookup over multiple sources (worktree copy vs installed catalog copy) | **No tie-break stated** (FND-108). `quire validate` already reports `DuplicateModuleName ... 2 path(s)` in this worktree. |
| FR-003 | Depends on an unreleased upstream schema (`spec-artifacts-iso` CR-012) | Covered, and well: FR-003-CON-3 forbids the skip, TC-034 proves the pinned copy is the release plus exactly the CR-012 pointers and fails when a release makes the pin unnecessary. |
| FR-005 | Depends on a package version not on any index the repo may pin (Quire 0.46.0) | Absence covered (AC-10, CON-3, TC-057 — no skip, which is right). **Wrong version present is not** (FND-107). |
| FR-005 / FR-004 | Record keys no extractor populates (`assessment`, `context`, `status`, `provenance`, `evidence`) | Disclosed in `spec.md` §Out of Scope and in the matrix's Test Environment. The *consequence* — the safety guarantees hold only over hand-built records — is stated by no requirement (FND-101). |
| IT-001 | Drives an authenticated/stateful external CLI against user-global state | Restore is a step, not an obligation; the isolation clause is conditional and unresolved (FND-109). The precondition is an unordered git sha (FND-107). |
| FR-001 / FR-006 | Reuses another repository's closed vocabulary rather than minting one | Covered, and it is the strongest reasoning in the bundle: TC-007/TC-063 fail if a future edit reaches for a verb the iso vocabulary lacks. |

## Failure Domain Check

- **Extension failures.** The record models are sealed (`...Record<never>` in
  `typespec/main.tsp`; FR-004 "SHALL forbid every other key"), and FR-004 lists
  the forward-compatible optional keys explicitly, so a future extractor key
  fails loudly rather than silently. Good. The two engine-side silent-drop
  paths (`agent-ix/quire-rs#221`, `#394`) are carried as strict expected
  failures rather than worked around — the correct disposition.
- **Identity keys.** Weakest axis. `identity: true` is required to be present
  at least once and is otherwise unconstrained: no uniqueness, no relation to
  the document `id`/`title` the locators yield, no composite-key semantics
  (FND-103).
- **Evaluation purity.** Strong. No `default` anywhere (FR-004, TC-041), no
  computed or inferred score (FR-001-CON-1, TC-046), deterministic emission
  (FR-002-CON-3, TC-021), advisory lint widened rather than a schema relaxed.
  The one impurity is FND-101: absence is a fourth epistemic state whose
  meaning no requirement fixes, and for `exposure`/`controllability`/`status`
  it is the only state an authored document can reach.
- **Topological robustness.** `acyclic_edges: [arises_from]` can never fire
  under the declared `allowed_links` (FND-112), and the STPA edge case — a
  hazard arising from no failure mode — is explicitly required to validate
  (FR-004 Behavior, AC-9, TC-043), which is right.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-101 | high | The module's headline safety property is stated over records the authoring path cannot produce: `exposure`, `controllability` and `status`/`provenance` have no column, no locator and no lint rule, so FR-004's "the document form can express everything the schema admits" is false, and FR-004-AC-8 (risk acceptance requires provenance) is unreachable from any document at 0.3.0 | FR-004:52,57, FR-004-AC-8; FR-001-AC-2; spec.md §Out of Scope; manifest `lint_rules`, `body_extraction` | missing-requirement |
| FND-102 | high | Every shipped schema `$ref`s five semantic-core documents that nothing this module ships, and no requirement states how a consumer resolves them; the tests resolve them only from a developer machine's `node_modules` | FR-004-CON-1, FR-002-AC-3/AC-6/AC-7, FR-002 Inputs, FR-003 Description, IT-001-SC-05, tests/conftest.py:44-52,255-283 | missing-requirement |
| FND-103 | medium | Identity is required to exist and is otherwise unconstrained: no uniqueness across records, no stated relation to the document `id`, no composite-key semantics when several fields are flagged — while StR-001 needs hazards countable and linkable | FR-004 Behavior, FR-004-AC-2/AC-3, StR-001, manifest `traceability` | missing-requirement |
| FND-104 | medium | Two of issue #2's three merge-gate items are unallocated: "advisory-only until promotion" appears only in US-001's explicitly non-normative Constraints section and an NFR-001 scope note, and "safety/security analysis is required before release" appears nowhere; `spec.md` declares `security_critical: false` | issue #2 §Safety / merge gate; US-001 §Constraints (Contextual); NFR-001 §Scope; spec.md frontmatter | missing-requirement |
| FND-105 | medium | NFR-001 measures the manifest locators and `traceability` (FR-001, FR-003), the 0.2.0 skeletons (FR-005) and the three lint allow-lists (declared in FR-004 Inputs), but its only relationship is `constrains FR-003`; FR-001, FR-004 and FR-005 reference it nowhere | NFR-001 frontmatter/§Scope, FR-001, FR-004, FR-005 | correct-requirement-no-evidence |
| FND-106 | medium | `HazardContext` is emitted (FR-002-AC-1) and admitted as an optional Hazard key (FR-004), and no requirement states what it contains, while the source imposes a real constraint the spec never states; `IdentityField` and `EvidenceRef`'s shape are in the same position | FR-002-AC-1, FR-004 Behavior, typespec/main.tsp:39-41,183-190 | missing-requirement |
| FND-107 | medium | Only the *absent*-engine path is specified. A Quire wheel present at the wrong version (internal-pypi serves 0.33.0, which has no `extract_semantic`; anything after 0.46.0 is unpinned) has no stated detection or failure, and IT-001's precondition is an unordered git sha rather than a checkable predicate | FR-005 Inputs, FR-005-AC-10, FR-005-CON-3, IT-001 §Preconditions, tests.md §Test Environment | missing-requirement |
| FND-108 | medium | Two criteria load "through Quire's registry loader" over two different copies of this module (worktree, `~/.ix/filament/modules`) with no tie-break stated; `quire validate` already reports `DuplicateModuleName ... 2 path(s)` here | FR-003-AC-4, IT-001-SC-04, base.md §Automated Checks | missing-requirement |
| FND-109 | medium | IT-001 mutates the user-global module catalog; isolation is conditional ("when one can be given") and unresolved, restore is a numbered step rather than an obligation, and no success criterion covers restore after an earlier step fails — which the matrix records as today's actual path | IT-001 §Preconditions, §Test Procedure steps 1/6, tests.md §Coverage Gaps ¶1 | missing-requirement |
| FND-110 | medium | Six obligations declare `Inspection` as their verification method and are all discharged by automated `Static`/`Unit` rows, which `tests.md` states outright; the declared method and the credited evidence disagree | FR-001-CON-1, FR-002-CON-1/CON-2/CON-4, FR-004-CON-3, StR-001-VC-2; tests.md TC-022..TC-024, TC-046, TC-047, TC-063, §Coverage Gaps | wrong-requirement |
| FND-111 | medium | FR-002 carries three separable obligations under one id — emission, the regeneration gate, and packaging (wheel contents, `npm pack` staging, `postpack` cleanup, `.gitattributes`) — 25 SHALL bullets and 9 AC; the packaging half (AC-6, AC-7) traces to no stakeholder or story obligation | FR-002 §Behavior, FR-002-AC-6/AC-7, US-001 | wrong-requirement |
| FND-112 | low | `acyclic_edges: [arises_from]` can never fire: `arises_from` is declared on `hazard` targeting `failure_mode` only and FR-001 states `failure_mode` declares no outgoing safety verb, so no path returns to a hazard — yet FR-003-AC-5 and NFR-001-AC-4 freeze it as a load-bearing compatibility fact | manifest:269-271, FR-001 "No new verbs", FR-003-AC-5, NFR-001-AC-4 | wrong-requirement |
| FND-113 | low | FR-002-AC-1 says the schemas directory "holds exactly the files `toolchain.json` lists", but the directory also holds `toolchain.json`, which is not one of the fifteen it lists; read with AC-9 it is itself the extra file with no emitted counterpart | FR-002-AC-1, FR-002-AC-9, FR-002 §Outputs | wrong-requirement |
| FND-114 | low | FR-003-AC-4 asserts the loader "lists both archetypes" while the manifest declares `archetypes: []` and puts both types under `object_types:`; nothing in the bundle says an object type registers as an archetype | FR-003-AC-4, manifest:40, tests/test_manifest_semantic.py:111-115 | wrong-requirement |
| FND-115 | low | NFR-001-AC-3 (legacy prose Properties block warns, not errors) has no row in the Measurement and Evaluation table; the five metrics cover AC-1, AC-2, AC-4 and AC-5 only | NFR-001 §Measurement and Evaluation, NFR-001-AC-3 | correct-requirement-no-evidence |
| FND-116 | low | Two normative statements are obligations on future authorial conduct rather than on an artifact, so nothing can observe them: FR-003's "SHALL correct its own manifest ... rather than relax the contract keys" and FR-004-CON-3's "No constraint ... SHALL be relaxed to make a fixture ... pass" (credited to a `Static` row, TC-047) | FR-003:53, FR-004-CON-3, tests.md TC-047 | wrong-requirement |
| FND-117 | low | The lexicon defines `severity`, `likelihood` and `detection` but nothing for `exposure`, `controllability`, `provenance` or the three epistemic tokens — precisely the vocabulary 0.3.0 adds and the choice an author has to make; FR-001-AC-6 asserts entry *shape* only, so nothing notices | manifest `lexicon`, FR-004 §Inputs, FR-001-AC-6 | missing-requirement |
| FND-118 | low | No artifact above the FR layer has evidence traced by id: US-001 has only illustrative examples, and (base FND-006) StR-001-VC-1/VC-2 appear in no `Traces To` cell, so both the US and StR matrix rows are narrative roll-ups of FR rows | US-001 §Acceptance Examples, tests.md §Stakeholder/User Story Coverage | correct-requirement-no-evidence |

## Finding Details

### FND-101 (high) — the epistemic guarantee is stated over records nothing authors

Evidence. FR-004 Behavior:52 admits `exposure` and `controllability` as
optional on `HazardAssessment`, and :57 requires the three advisory lint
allow-lists to admit their scale plus the three `EpistemicState` members "**so
the document form can express everything the schema admits**". The manifest
carries exactly three `lint_rules` — `hazard-severity` (`Assessment.Severity`),
`hazard-likelihood` (`Assessment.Likelihood`), `failure-mode-detection`
(`Analysis.Detection`) — and the `assessment` locator asserts columns exactly
`Severity | Likelihood | Rationale` (FR-001-AC-2). `spec.md` §Out of Scope then
refuses to widen that table, correctly, because widening it would not be
additive under NFR-001.

Consequences the bundle does not state:

1. `exposure` and `controllability` are typed, emitted (FR-002-AC-1), asserted
   member-by-member (FR-004-AC-6, AC-12, TC-040, TC-071) — and unreachable from
   any authored document. For those two axes, *absent* is the only state an
   author can produce, and no requirement says what absent means. The module's
   whole reason for existing is that "nobody looked" must not collapse into a
   scale value; a fourth, unlabelled state that is the only reachable one for
   two of the five axes is that same collapse in a different position.
2. `status` and `provenance` have no locator either, so FR-004-AC-8 — a record
   at `status: accepted` requires a `provenance` naming who accepted the risk —
   the single most safety-relevant rule in the bundle, cannot be reached by any
   document at 0.3.0. It is real schema evidence over hand-built records and
   nothing more, which `tests.md` §Test Environment says plainly for TC-036..046
   but no requirement, criterion or metric records.
3. FR-004's `so`-clause at :57 is therefore false as authored, not merely
   incomplete: for three of the five axes the document form expresses strictly
   less than the schema admits.

Recommendation. Not a code change. Either state the restriction in FR-004 (an
AC of the form "for each scored axis, either a lint allow-list and a column
exist or the axis is recorded as schema-only until `agent-ix/quoin#335`"), and
narrow the :57 clause to the three axes it is true of; or add an explicit AC
fixing the meaning of an absent axis so absence is not readable as a
non-judgement-free state. `spec.md` §Out of Scope already names the blocking
mapping ticket, so this is a statement gap, not a scope gap.

### FND-102 (high) — the shipped schemas cannot be resolved by a consumer

Evidence. Every module schema refers out to five semantic-core documents:

```
https://schemas.agent-ix.org/semantic-core/0.1.0/{FieldDecl,RelationDecl,ClauseRef,SemanticId,SourceLocus}.json
```

FR-004-CON-1 and AC-10 *require* exactly this ("every grammar item SHALL be a
`$ref` to `@agent-ix/semantic-core` 0.1.0"), and FR-002 Behavior requires the
generator to discard the re-emitted semantic-core files. Nothing this module
ships carries them: FR-002-AC-6 puts only `schemas/<Model>.json` in the wheel,
FR-002-AC-7 only `manifest.yaml` plus `schemas/` in the npm tarball, and FR-002
Inputs states of the three build inputs that "the published artifact is
Markdown and JSON, so none is a runtime dependency of a consumer". The tests
resolve only because `tests/conftest.py:44-52` reads
`node_modules/@agent-ix/semantic-core/generated/json-schema` and registers each
file under the `schemas.agent-ix.org` URI — an npm.ix devDependency that
FR-002-CON-4 explicitly scopes to a developer machine.

So no requirement states: whether the `$id` host publishes those five documents;
how Quire at load, Quoin at install, or a generated reader obtains them; or what
a consumer sees when a `$ref` does not resolve. FR-003's Description ("Quire
validates every declaration record against them") and IT-001-SC-05 ("the
referenced schema resolved from the installed location") both assume the answer.
This is also the gap FND-111's split would surface: it sits between FR-002's
emission half and its packaging half, and belongs to neither as authored.

Recommendation. One FR-002 or FR-006 obligation naming the resolution
mechanism — vendor the five semantic-core documents beside `schemas/` and
`$ref` them relatively, or state the published base URL and the offline
resolution contract — plus an AC that validates a shipped record from an
installed copy with no `node_modules` present. `agent-ix/filament-core-data#11`
(semantic-core language packages) is the neighbouring ticket to check first.

### FND-103 (medium) — identity is required to exist and nothing else

FR-004 requires "at least one item flagged `identity`" on both types (AC-2,
AC-3, TC-036, TC-037) and stops there. Nothing states that identity values are
unique across records, how a record's identity field relates to the document
`id`/`title` the manifest locators yield, or what a second `identity: true`
field means. Meanwhile StR-001's need is that a hazard be *countable* and
*linkable*, and the `traceability` model resolves incoming `mitigates` and
`arises_from` edges against something the spec never names. Two hazards can
declare the same identity value and every criterion in the bundle passes.

### FND-104 (medium) — the merge gate is not in the specification

Issue #2 states three gate items. "No automated risk acceptance or safety claim
is inferred from schema validity" is allocated well (FR-004-CON-2, TC-046).
"Advisory-only until promotion" appears twice, both times outside the normative
surface: US-001 §Constraints, a section the artifact itself labels
*(Contextual)*, and a bullet in NFR-001 §Scope. "Safety/security analysis is
required before release" appears in no artifact at all, and `spec.md`
frontmatter carries `security_critical: false`. For a safety module the release
gate is the one obligation that should be a requirement rather than a note.

### FND-107 (medium) — only the absent engine is specified

FR-005-CON-3 and AC-10 are right and are the strongest anti-skip policy in the
bundle. They cover one of two failure modes. `internal-pypi` serves Quire
0.33.0, which has no `extract_semantic`; FR-005 Inputs pins 0.46.0; nothing
asserts the installed version. Sixteen matrix rows measure engine behaviour, and
two of them (TC-032, TC-067) encode 0.46.0's *exact defect behaviour* as
expected failures — so a later wheel that fixes `agent-ix/quire-rs#391` or
`#221` turns a green expected-failure row red for the right reason with no
requirement explaining it, and an earlier wheel fails obscurely. IT-001's
"Quoin ... at build `3e842ce` or later" has the same shape and is worse: a git
sha carries no ordering a test can check.

## Automated Checks

| Check | Result |
|---|---|
| `quire validate --scope <worktree> "spec/**/*.md"` | Exit 0. Zero errors; 29 grammar warnings (base FND-016 — `ears:non-singular`, `quality:agentless-passive`), unchanged by this review. Review artifact included. |
| Requirement → verification method | ✅ every FR, NFR and IT names at least one method; 6 declare `Inspection` and are discharged by automated rows (FND-110). |
| NFR scoping and back-reference | ❌ NFR-001 is scoped, but no FR references it (FND-105). |
| US → FR → StR chain | ✅ complete; transitive through US-001 for FR-002..FR-006, stated in `spec.md` §Requirements Architecture and matching the merged business precedent. |
| Single-interpretation rule | ❌ FND-101 (:57 clause false for 3 of 5 axes), FND-113 (`toolchain.json` in or out of its own list), FND-114 (`archetypes` vs `object_types`). |
| Atomicity | ❌ FR-002 (FND-111). FR-001, FR-003..FR-006, NFR-001 and IT-001 each state one obligation class. |
| Externally observable | ❌ FR-003:53 and FR-004-CON-3 (FND-116). All other Behavior bullets are artifact-observable. |
| Spec ↔ shipped artifact agreement | Manifest 0.3.0, 16 files under `schemas/`, 15 emitted models, both digests match their files, `semantic` block carries exactly the nine keys FR-003 admits, `imports: {}` with the reason in a comment, `traceability` two relations + `acyclic_edges`, lexicon 8 entries all `{definition: ...}`. Agrees with the spec except as recorded in FND-101, FND-106, FND-112, FND-113, FND-114, FND-117. |

## Notes

- Several base findings are already closed on the branch and are not repeated
  as findings here: `spec/log.md` now carries the 2026-09-04 entry (base
  FND-011), FR-004 §Inputs now fixes all six ordinal vocabularies and
  FR-004-AC-12/TC-071 assert them (base FND-002), FR-001-CON-1 is now traced by
  TC-046 (base FND-004), and NFR-001-AC-5 now has its metric row (base FND-010).
  Base FND-001 (unbacked matrix rows), FND-012 (TC-008/TC-009 unallocated),
  FND-017 (`depends_on: []`) and FND-018 (FR-003 restating IT-001's procedure)
  still stand as written and are not restated.
- The parts of this bundle that are right are worth recording, because they are
  the parts a later reader is most likely to erode: the no-new-verbs reasoning
  and the test that enforces it (TC-007/TC-063), the no-skip policy and the test
  of the policy itself (TC-057), the two expected failures that name their
  engine defect instead of relaxing a schema, and the CR-012 drift test that
  fails the moment the pin becomes unnecessary. None of these should be
  simplified while dispositioning the findings above.
- No spec artifact was edited by this review. Findings are reported for
  disposition by the branch author.
