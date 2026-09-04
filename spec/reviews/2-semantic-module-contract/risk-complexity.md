---
id: SR-008
title: "Risk and complexity analysis of the issue #2 semantic-module-contract specification"
type: SpecReview
analysis: risk-complexity
scope: "spec/spec.md, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001, spec/integration/IT-001, spec/tests.md; typespec/main.tsp and spec_objects_safety/manifest.yaml for context"
review_set: subset
---
# Risk and complexity analysis of the issue #2 semantic-module-contract specification

## Summary

Technical-risk and volatility scoring of every stakeholder, user-story,
functional, non-functional and integration requirement on
`2-semantic-module-contract` (`agent-ix/spec-objects-safety#2`, Track A wave 4
of `agent-ix/quoin#286`), before `spec-to-plan` decomposes tasks.

The bundle's safety semantics are the stable part. `Severity`, `Likelihood`,
`Exposure`, `Controllability`, `Detection` and the `EpistemicState` triple come
from IEC 61508 / ISO 26262 / FMEA and will not move; the reasoning that keeps
`hazard` and `failure_mode` apart will not move either. Essentially all the
risk in this branch sits in the **delivery machinery** the migration bolted
onto a Markdown-and-YAML module: a pinned TypeSpec toolchain reached only
through npm.ix, a version-embedded `$id` and a digest chain, a vendored copy of
an unreleased upstream schema, an unpublished engine wheel, three open engine
defects, and a manifest block frozen for a neighbouring repository's benefit.

Six requirements score High on at least one axis. The single dominant hazard is
that **no hosted runner can obtain the two inputs the evidence base needs** —
`@agent-ix/semantic-core` 0.1.0 from npm.ix and the Quire 0.46.0 wheel — while
CI is manual-only, so every green result in `tests.md` is a claim about one
developer machine and the branch has no reproducible verification environment.
That is a risk statement, not a coverage statement: the base review's FND-001
is about rows without tags; this is about tagged rows that only one machine can
run.

## Verdict

**CONDITIONAL** — FND-101 through FND-104 should be dispositioned into the plan
as explicit tasks or accepted risks before decomposition. No requirement is
unsound; four are under-hedged. No spec artifact was edited by this review.

## Relationship to the base review

`base.md` (SR-001) checked ids, requirement quality, the six coverage rules and
cross-references, and reported nineteen findings led by unbacked matrix rows
(FND-001) and unenumerated safety scales (FND-002; since answered by the
`FR-004` Inputs vocabulary table). None of those is restated here. Two base
findings are re-used only as inputs to a risk score and are cited as such:
FND-008 (the `make lint` / `FR-002-CON-4` collision) feeds FND-104, and FND-001
feeds FND-101. Everything else below is new and is framed as exposure and
mitigation rather than as a defect.

## Risk Register

| Req | Tech Risk | Volatility | Drivers | Mitigation |
|---|---|---|---|---|
| StR-001 | Low | Low | Need is standards-derived (IEC 61508 / ISO 26262); the question "which hazards have nothing addressing them" does not shift. | None required. |
| US-001 | Low | Medium | Rests on `@agent-ix/semantic-core` 0.1.0, a pre-1.0 grammar published only to npm.ix (`filament-core-data#11`). | Treat the grammar version as a plan input; re-emit and re-digest on any semantic-core bump as one task. |
| FR-001 | Low | Low | The 0.2.0 object-type model is carried forward unchanged; no new verb, no new type. Lowest-risk requirement in the bundle. | None required. Schedule first so the rest lands on a stable base. |
| FR-002 | **High** | **High** | Exact pins on `@typespec/compiler` / `@typespec/json-schema` 1.15.0 plus an emitter-behaviour compensation step (`$id`/`$ref` normalization with an `applied` flag); a digest chain over emitted bytes; the `$id` base embedding the manifest `version`; the only enforcing gate (`make schemas-check` via `make lint`) runnable solely where npm.ix is routed. | FND-104, FND-105. Spike the coordinated-bump path (FR-002-AC-8) before any other FR-002 task; keep `toolchain.json`'s normalization record as the emitter-drift tripwire and assert `applied` in a test. |
| FR-003 | **High** | **High** | Conforms to an FR-035 module-manifest schema that exists only at an unreleased commit (`spec-artifacts-iso` CR-012, `6686f11`) and to quoin FR-070's `contract_version: 1.0.0`, itself pre-release; AC-6 half-blocked on two engine defects; AC-5 freezes a block another repository reads. | FND-103, FND-102, FND-106. Keep TC-034's self-retiring drift gate; add the release of `spec-artifacts-iso#36` as a tracked plan exit item rather than an ambient wait. |
| FR-004 | Medium | **High** | Vocabulary is stable, but the record keys the schema types (`assessment`, `context`, `analysis`, `status`, `provenance`, `evidence`) have no published Markdown mapping (`quoin#335`), so their shapes are validated only against hand-built records; `Exposure` and `Controllability` are typed but unauthorable without a non-additive change to the `Assessment` columns. | FND-106. Slice the mapping-dependent criteria (AC-2..AC-5, AC-8, AC-11) so they can be re-pointed at extracted records without re-deriving the schema; do not widen the `Assessment` table on this branch. |
| FR-005 | **High** | **High** | Every extraction criterion runs against a Quire wheel that is on no index this repo may depend on (`quire-rs#392`), provisioned by `make dev-quire` as an unbounded `quire>=0.46.0` from a rolling dev index; two strict xfails are measured against exactly 0.46.0; `legacy_forms`, typed-table and clause mappings (quoin FR-071/FR-072) are themselves pre-release. | FND-101, FND-102. Assert the engine version in `conftest.py` and version-gate both xfail reasons; keep the fail-never-skip policy (FR-005-CON-3) — it is what makes the exposure visible. |
| FR-006 | Low | **High** | `semantic.imports` stays `{}` until three neighbouring migrations land (`spec-objects-security#13`, `spec-objects-architecture#8`, `spec-objects-operational#6`); each will force an edit here, and each is out of this repo's control. | Keep the map empty and the prose reason in the manifest (already done); slice each future pin as its own one-line change coupled to the first fixture that names the neighbour's type, exactly as the requirement states. |
| NFR-001 | Medium | **High** | AC-3 is a strict expected failure on `quire-rs#391`; AC-4 freezes the `traceability` model for `spec-objects-security`'s benefit with no enforcement on the other side; AC-5's allow-list widening is asserted against a baseline this branch also authors. | FND-102, FND-103. Keep `tests/fixtures/baseline-0.2.0/` immutable for the life of the 0.3.x line and say so in the plan. |
| IT-001 | Medium | **High** | Drives the real `quoin` CLI against the user-level catalog at `~/.ix/filament/modules`, mutating global developer state and restoring it; the pinned Quoin build (`3e842ce` or later) is a commit, not a release, and the installed CLI is currently broken (TC-070 is `🚧`). | FND-101. Keep the test in `tests_integration/` so `make test` cannot report green over a broken CLI; add "TC-070 passes against a whole CLI" as a plan exit criterion rather than a matrix footnote. |

Every requirement is scored on both axes; every High carries a named
mitigation.

## Top hazards

1. **FND-101 — the evidence base runs on one machine.** Both inputs the tagged
   tests need are unobtainable in hosted CI: `@agent-ix/semantic-core` 0.1.0
   resolves only through a user-level npm config pointing at npm.ix
   (FR-002-CON-4), and Quire 0.46.0 is on no index this repository may commit
   against (FR-005 Inputs, `quire-rs#392`). `tests/conftest.py` needs the first
   for `$ref` resolution and the second for every extraction row, `ci.yml` is
   `workflow_dispatch` only, and the FR-035 drift gate additionally compares
   against whichever `spec-artifacts-iso` happens to be *installed*. The
   consequence is that FR-002, FR-003, FR-004, FR-005, NFR-001 and IT-001 are
   all verified in exactly one environment, and nothing reproduces it.
   **Mitigation:** make the environment an artifact of the plan — a documented
   `make dev-*` bootstrap plus a recorded environment fingerprint
   (semantic-core version, quire version, installed `spec-artifacts-iso`
   version) emitted by the suite — so a later reader can tell which machine a
   green run describes. Do not weaken FR-005-CON-3 to reach a green suite
   elsewhere.
2. **FND-102 — strict xfails over an unpinned engine.** TC-032
   (`quire-rs#221`, `#394`) and TC-067 (`quire-rs#391`) are
   `@pytest.mark.xfail(strict=True)` reasoned explicitly against "quire
   0.46.0", but `make dev-quire` installs `quire>=0.46.0` from the rolling
   `pypi.ix root/dev` index and no test asserts the engine version. When any of
   those three defects is fixed upstream, the next `make dev-quire` turns both
   rows XPASS and the suite goes red on somebody else's fix, with no
   requirement having changed — and a developer who reads the failure as local
   breakage may relax the assertion, which is precisely what FR-004-CON-3 and
   FR-005-CON-3 forbid. **Mitigation:** assert the resolved engine version in
   `conftest.py`, gate each xfail on it, and record "flip TC-032/TC-067 when
   `quire-rs#221`/`#394`/`#391` close" as tracked plan items so the red run is
   an expected event with a named owner.
3. **FND-103 — the manifest conforms to contracts nobody has released.** The
   FR-035 module-manifest schema carrying the `semantic` block and the
   reference-form `data_schema` exists only at `spec-artifacts-iso` `6686f11`
   on `main` (`spec-artifacts-iso#36` open, `v0.18.0` predates it), vendored
   into this repo as `tests/fixtures/module-manifest.schema.json`; quoin
   FR-070's `contract_version: 1.0.0` is the same class of pre-release
   contract. The nine admitted `semantic` keys, their value domains, and the
   `{schema, digest}` shape can all still move before release, and every one of
   them is asserted exactly (FR-003-AC-1, FR-003-AC-2, FR-003-CON-1). The
   design already handles this well — TC-034 retires its own pin by failing
   when a release carries the key — but the residual exposure is that this
   module may ship a manifest that the eventual release refuses.
   **Mitigation:** treat `spec-artifacts-iso#36` and the quoin FR-070 release
   as plan-level gates on *tagging* 0.3.0, not on landing it; re-run TC-033 and
   TC-034 as the first step after either releases.
4. **FND-104 — the emission invariants have no enforcing gate off the author's
   machine.** `make lint` runs `make schemas-check`, which compiles TypeSpec;
   `FR-002-CON-4` concedes the GitHub workflow does not run it. So the
   `$id`-matches-version rule, the digest-equals-bytes rule, the no-stale-file
   rule and the deterministic-emission rule (FR-002-AC-2/AC-4/AC-8/AC-9,
   FR-002-CON-3/CON-5) are protected only by a developer remembering to run
   `make lint` before pushing. The base review's FND-008 records the
   contradiction; the risk is the unguarded invariant, and it is the invariant
   a stale digest silently violates — with `quire-rs#394` open, a digest
   mismatch drops the object type with **no diagnostic at all**, so the failure
   mode of this gap is a silently empty module rather than an error.
   **Mitigation:** add a pre-push hook or a self-hosted lint job as a plan
   task, and — cheaply and independently of npm.ix — add a pure-Python test
   that re-hashes both shipped schema files and compares them to the manifest
   digests, so the highest-consequence half of the gate runs wherever `pytest`
   runs.
5. **FND-106 — the module ships a contract for keys nothing can author yet.**
   `assessment`, `context`, `analysis`, `status`, `provenance` and `evidence`
   are typed in the schemas and exercised only against hand-built records,
   because the published Markdown mapping covers `Properties`, `Invariants` and
   `Operations` only (`quoin#335`, quoin FR-071/FR-072). Two consequences
   compound. First, when the `Assessment`/`Analysis` mapping is published its
   key shapes may not match what this branch guessed (`assertedBy` /
   `assertedAt` casing, `rationale` versus the `Rationale` column,
   single-record versus per-row), so FR-004-AC-2..AC-5, AC-8 and AC-11 are
   rework candidates rather than settled evidence. Second, `Exposure` and
   `Controllability` are typed as optional axes that **no document form can
   carry**: `FR-001-AC-2` asserts the `Assessment` columns exactly and
   `spec.md` correctly rules that widening them would break NFR-001. Two of the
   five scored axes are therefore unreachable from Markdown for the life of
   0.3.x. **Mitigation:** keep the "schema evidence, not extraction evidence"
   labelling the matrix already carries, and file the axis-authoring question
   against `quoin#335` now so the mapping is designed knowing two typed axes
   are waiting on it — rather than discovering after publication that reaching
   them needs a 0.4.0.

## Findings

Ranked by severity. FND-101..FND-104 and FND-106 are the top hazards narrated
above; the rest are recorded here only. Ids start at 101 so they cannot be
confused with the base review's FND-001..FND-019.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-101 | high | The evidence base runs on exactly one machine: `@agent-ix/semantic-core` 0.1.0 (npm.ix only) and Quire 0.46.0 (on no index this repo may depend on) are both unobtainable in hosted CI, and `ci.yml` is `workflow_dispatch` only. FR-002..FR-005, NFR-001 and IT-001 are all verified in one unreproducible environment. See Top hazards 1 for the mitigation. | FR-002-CON-4, FR-005 Inputs, `tests/conftest.py`, `.github/workflows/ci.yml` |
| FND-102 | high | Two `strict=True` xfails are reasoned against "quire 0.46.0" while `make dev-quire` installs an unbounded `quire>=0.46.0` from the rolling `pypi.ix root/dev` index and no test asserts the engine version. An upstream fix to `quire-rs#221`/`#394`/`#391` turns both rows XPASS and reds the suite with no requirement change. See Top hazards 2. | TC-032, TC-067, `pyproject.toml` `dev-quire`, `tests/test_manifest_semantic.py:177`, `tests/test_additive_compatibility.py:70` |
| FND-103 | high | The manifest conforms to contracts nobody has released: the FR-035 schema exists only at `spec-artifacts-iso` `6686f11` (vendored as `tests/fixtures/module-manifest.schema.json`), and quoin FR-070's `contract_version: 1.0.0` is likewise pre-release. The nine admitted `semantic` keys and the `{schema, digest}` shape are asserted exactly and can still move. See Top hazards 3. | FR-003 Inputs, FR-003-AC-1/AC-2/AC-7, FR-003-CON-1/CON-3 |
| FND-104 | high | The emission invariants have no enforcing gate off the author's machine — `make lint` runs `make schemas-check`, which needs the npm.ix toolchain the workflow does not have. With `quire-rs#394` open, a stale digest drops the object type with no diagnostic, so the failure mode of this gap is a silently empty module. See Top hazards 4; base FND-008 records the underlying contradiction. | FR-002 Behavior, FR-002-CON-4, FR-003 Behavior |
| FND-106 | high | The module ships a contract for keys nothing can author: six module-specific record keys are validated only against hand-built records (`quoin#335`), and `Exposure`/`Controllability` are typed axes no document form can carry, since widening the `Assessment` columns would break NFR-001. See Top hazards 5. | FR-004 Behavior, FR-004-AC-2..AC-5/AC-8/AC-11, FR-001-AC-2, spec.md Out of Scope |
| FND-105 | medium | **Version-coupling amplifies churn.** The `$id` base embeds the *manifest* `version`, so the schema URL version and the module version are one number. Any manifest-only edit that warrants a bump — a lexicon entry, an added `required: false` locator, a lint allow-list value — re-versions all fifteen schema URLs, re-digests both object types and rewrites `toolchain.json`, in a five-artifact atomic commit (FR-002 Behavior, FR-002-CON-5). The immutable-URL property is worth having, but the coupling means schema consumers see a breaking URL change for reasons that have nothing to do with the schemas. Consider recording the trade explicitly, or decoupling a `schema_version` from `version`, before 0.3.0 is tagged and the pattern becomes precedent across the module family. | FR-002 Behavior, FR-002-CON-5, manifest `version` |
| FND-107 | medium | **The `traceability` freeze is a cross-repo contract with enforcement on one side only.** FR-003-AC-5 and NFR-001-AC-4 freeze the block byte-for-byte because `spec-objects-security`'s hazard-coverage work (`#5`) reads it across repositories, and FR-006 forbids changing any edge's direction, verb or type. Nothing in `spec-objects-security` pins this side, no shared fixture exists, and that repo has its own semantic migration open (`#13`) which will rewrite its manifest. So the coupling is real, undocumented outside prose, and asymmetric: this repo is frozen, the neighbour is not. It also means any future safety-chain evolution — a third required relation, a `causes` edge should the iso vocabulary ever gain one — is a coordinated two-repo change from day one. Mitigation: state the contract in `spec-objects-security#5` explicitly, or promote the `traceability` shape to a shared fixture both repos assert against. | FR-003-AC-5, NFR-001-AC-4, FR-006 Behavior |
| FND-108 | medium | **Emitter-behaviour compensation is load-bearing and only weakly observed.** The generator keeps a normalization step that rewrites relative `$id`/`$ref` values to absolute ones and records `applied: true/false` in `toolchain.json` — that is, the pipeline already knows the pinned emitter's output shape is not stable across versions. Nothing in the criteria asserts what `applied` currently is, so a toolchain bump that changes emitter relativity would flip the flag, change every emitted byte, change both digests, and be visible only as a large diff. FR-002-AC-1 records compiler and emitter versions; it does not record the normalization state. Mitigation: assert the expected `applied` value in TC-012 so an emitter behaviour change is named as such rather than read as ordinary churn. | FR-002 Behavior, FR-002 Outputs, `toolchain.json` |
| FND-109 | medium | **IT-001 mutates global developer state.** The procedure installs into the user-level catalog at `~/.ix/filament/modules` and restores it in step 6, "running against a temporary config root when one can be given". If the run aborts between steps 2 and 6 — and the CLI is currently known to exit non-zero mid-procedure — a developer's catalog is left holding this branch's module. The restore is a step, not a fixture teardown, so its execution depends on the earlier steps passing. Mitigation: make the restore a `finally`/fixture-scoped teardown in the test rather than a numbered step, and make the temporary config root the default rather than the fallback. | IT-001 Preconditions, IT-001 Test Procedure steps 1 and 6, `tests_integration/` |
| FND-110 | low | **Complexity concentration.** FR-002 carries 9 acceptance criteria, 5 constraints and roughly twenty-five Behavior clauses spanning a Node generator, an npm staging script, a `.gitattributes` rule, wheel packaging and npm packing — several times the surface of any other requirement here, and the only one whose subject is a build pipeline rather than a safety concept. It is the natural first slice and the natural place for a plan to over-estimate progress: partial completion is invisible because nothing fails until the check runs end to end. Mitigation: decompose FR-002 by criterion in the plan rather than as one task, and land AC-4 (the check itself) before the criteria it is the gate for. | FR-002 |
| FND-111 | low | **Fail-never-skip makes red the default state.** FR-005-CON-3 is correct — a skipped row is not coverage — but combined with an engine no index serves, the suite's out-of-the-box condition for any new contributor is a wall of failures rather than a skip summary. Over time that erodes the signal FR-005-CON-3 exists to protect. Mitigation: keep the policy; make TC-057's failure message the first thing a contributor sees (it already names `make dev-quire` and `quire-rs#392`) and reference it from the README bootstrap section. | FR-005-CON-3, FR-005-AC-10, `tests/conftest.py` |
| FND-112 | low | **`package.json` routes `@agent-ix` at public npm for publish while the build's own `@agent-ix` dependency is npm.ix-only.** `publishConfig` targets `registry.npmjs.org` with `access: public`, and the shared release workflow rewrites `$HOME/.npmrc` to point `@agent-ix` at public npm. The publish itself is safe — it runs `prepack` (Node built-ins only) and never installs `devDependencies` — so this is recorded as a boundary to watch rather than a defect: any future release step that adds `npm ci` would fail on `@agent-ix/semantic-core` 0.1.0, which public npm does not carry. | `package.json`, `.github/workflows/release-npm.yml` |

## Failure-domain cross-reference

No `spec-failure-domain-analysis` deliverable exists for this bundle; the
`reviews/2-semantic-module-contract/` set holds `base.md` and this document
only. The extension, identity, purity and topology questions that analysis
would ask are therefore **open**, and three of them are visible from here and
should be carried into it rather than assumed handled:

- **Identity** — `IdentityField` is an open marker used as a `@contains`
  predicate; FR-004 requires "at least one" identity field but states no
  uniqueness or stability rule for the identity value itself, and nothing says
  what two hazards sharing an identity field mean.
- **Purity** — FR-004's no-`default` rule is asserted over the shipped schemas
  (FR-004-AC-7), but the same guarantee is not stated for the *extractor*: a
  future Markdown mapping that supplies a column default would reintroduce the
  exact collapse this module exists to prevent, one layer below the schema.
- **Topology** — `acyclic_edges: [arises_from]` is declared and frozen, but no
  criterion in this bundle exercises a cycle; the check belongs to the engine
  (quire-rs FR-058) and this module verifies only that the declaration is
  present and unchanged.

Recommend running `spec-failure-domain-analysis` over FR-004 and FR-005 before
plan generation; the risk scores above assume its findings are additive to,
not overlapping with, FND-101..FND-112.

## Notes

- The Out of Scope section of `spec.md` is where most of this analysis came
  from: fourteen exclusions, each naming the issue that owns it. That is
  unusually honest scoping and it is what made the volatility scoring possible
  at all — the risks below are documented, not discovered. Nothing here should
  be read as an argument to widen the branch.
- No requirement was found whose risk is a reason not to build it. Every High
  score is an argument for sequencing and hedging, not for deferral.
- No spec artifact was edited by this review.
