---
id: SR-006
title: "Evidence and verification-method review of the issue #2 semantic-module-contract specification"
type: SpecReview
analysis: evidence
scope: "spec/stakeholder/StR-001, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001, spec/integration/IT-001, spec/tests.md"
review_set: subset
---
# Evidence and verification-method review of the issue #2 semantic-module-contract specification

## Summary

Verification-method review of the `2-semantic-module-contract` bundle for
`agent-ix/spec-objects-safety#2`. Every declared obligation's authored method
was checked against the `verification_catalog` in
`/home/peter/.ix/filament/modules/spec-artifacts-process/manifest.yaml` (33
methods across the classes `Test`, `Analysis`, `Inspection`, `Demonstration`),
and every Test Matrix `Type` value against
`traceability.vocabularies.test_type`, which is the same vocabulary the
catalog's `evidence_kind` is drawn from.

`quoin advise` was run first, as the deterministic half. It reports **59
obligations: 5 mismatch, 0 uncatalogued, 0 inconclusive**. That headline is
weaker than it reads, and the two findings that lead this review are the two
reasons why.

First, 54 of those 59 obligations authored the bare string `Test`. `Test` is an
IADT **class**, not one of the catalog's 33 method ids, so the mismatch check
over them cannot fire: a class contains whichever method the advisor
recommends. The only cells carrying real method ids are NFR-001's five
Measurement rows — and those are the only five mismatches reported. The
mismatch count is therefore a count of the rows that were specific enough to
disagree, not a measure of method conformance.

Second, the advisor's obligation set is the acceptance criteria plus the NFR
metric rows. The bundle's **18 named constraints, 2 stakeholder validation
criteria and 6 integration success criteria carry declared verification methods
that `quoin advise` never evaluated** — 26 obligations, and every one of the six
`Inspection` claims in the bundle lives among them. Those six are the substantive
defect here: each is discharged by an automated, tagged test, which is not what
`Inspection` means in the catalog and is not what the engine does with it.

The evidence side is otherwise in good order. `quire coverage --scope .` reports
125/125 rows backed; all four Test Matrix `Type` values in use (`Unit`,
`Integration`, `Static`, `Property`) are declared vocabulary members; and the
five metric methods that were uncatalogued at base review now carry real catalog
ids. Three of the five advisory recommendations this review rejects are
false positives whose trigger is checkable and worth carrying upstream.

## Verdict

**CONDITIONAL** — FND-001 and FND-002 change what the `Verification` and
`Validation` cells say, and those cells *are* the obligations' methods
(quire-rs FR-053), so they should be settled before the plan allocates suites.
Findings are reported only; no spec artifact was edited by this review.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | All 54 acceptance criteria authored a class, not a method. `quire properties --json` reports `obligation.method: "Test"` for 54 of 54 criteria; `Test` is one of the catalog's four `class` values, not one of its 33 method ids, so `quoin advise` can never report a mismatch on any of them and reports none. The five real mismatches it does report are exactly the five cells (NFR-001's metrics) that named a method. A `Test`-class cell cannot say whether the obligation is discharged by `unit-testing`, `property-based-testing`, `golden-approval-testing` or `negative-abuse-testing` — and the matrix already distinguishes them by `Type` (37 `Unit`, 26 `Integration`, 1 `Property`, 5 `Static`), so the information exists and is simply not in the cell that carries the obligation. Recommend narrowing each cell to the method id the matrix row already implies. | FR-001..FR-006 Acceptance Criteria; NFR-001 Acceptance Criteria; `quoin advise` |
| FND-002 | high | Six obligations declare `Inspection` and every one is discharged by an automated test. FR-001-CON-1, FR-002-CON-1, FR-002-CON-2, FR-002-CON-4, FR-004-CON-3 and StR-001-VC-2 carry `Inspection` in their `Validation` cell. The catalog's `inspection` method is `class: Inspection`, `evidence_kind: Manual`, `tooling: [inspections registry]`, defined as "a person reads the artifact against the requirement and records a verdict … discharged through the inspections registry rather than by a tagged test". Each is in fact backed by a tagged test — TC-046 (`Integration`), TC-022 (`Static`), TC-023 (`Static`), TC-024 (`Unit`), TC-047 (`Static`), TC-063 (`Unit`) — and the matrix says so outright in its own Coverage Gaps: "no `Inspections` document exists for the `Static` rows … each of which is nonetheless discharged by an automated test here rather than by a human procedure." No matrix row anywhere carries `Type: Manual`, `Inspection` or `Analysis`. The evidence is right and the method is wrong. It is not cosmetic: `traceability.vocabularies.no_source_symbol` lists `Inspection`, so an obligation declared that way is exempted from the backing accusation — if these tests were deleted the declared method would say nothing was expected to bind. Recommend `architecture-conformance` (Analysis/`Static`) for FR-002-CON-1 and FR-004-CON-3, `sca-sbom` (Analysis/`Static`) for FR-002-CON-2 and FR-002-CON-4, `integration-testing` for FR-001-CON-1 and `unit-testing` for StR-001-VC-2 — each of which is the method the existing test actually is. | FR-001-CON-1, FR-002-CON-1/2/4, FR-004-CON-3, StR-001-VC-2; spec/tests.md TC-022, TC-023, TC-024, TC-046, TC-047, TC-063, Coverage Gaps |
| FND-003 | medium | 26 of the bundle's 85 declared obligations are invisible to the deterministic advisor. `quoin advise` reports 59 obligations — 54 acceptance criteria plus 5 NFR metrics. The 18 named constraints across FR-001..FR-006 never reach it (`quire properties --json` mints no criterion for a `Constraints` table row at all), the 2 StR-001 validation criteria reach it as criteria whose `obligation` is `null` — so their authored `Test` and `Inspection` values are read by nothing — and IT-001's 6 success criteria have no method-bearing column to read. This is the mechanism behind FND-002: the six wrong `Inspection` claims sit precisely where nothing automated looks. Reported as a tooling gap against `quoin advise`/`quire properties` rather than against this bundle, which authored its cells in the shape the templates provide. | FR-001..FR-006 Constraints tables; StR-001 Validation Criteria; IT-001 Test Procedure; `quire properties --json` |
| FND-004 | medium | All five NFR-001 mismatches are false positives; confirm the authored methods. `quoin advise` flags NFR-001-M-1..M-5 (`unit-testing` ×4, `integration-testing` ×1) against a recommendation of `performance-benchmarking`, matched on the single characteristic `quantified-threshold`. Judgement, not a verdict: reject the recommendation. `performance-benchmarking` is defined as measuring "a quantified metric against its declared target and threshold" with `criterion`, `pytest-benchmark`, `hyperfine` — instruments for latency and throughput. NFR-001's metrics are conformance **counts** (`0.2.0 locators changed`, `Added locators that are required: true`, `traceability facts changed`) whose target and threshold are both `0`; no benchmark harness can discharge "zero locators changed", and the tests that do (TC-065, TC-066, TC-068, TC-069) are a baseline diff and a validation run. The trigger is over-broad rather than the authoring wrong: `quantified-threshold` matches any Measurement row stating a number, which is every well-formed NFR metric table in the corpus, so this method is elicited from every one of them regardless of quality attribute. Worth filing against `spec-artifacts-process` to co-key `performance-benchmarking` on `latency`/`throughput`. Note the base review's FND-009 is discharged: these cells now carry catalog method ids rather than prose. | NFR-001 Measurement and Evaluation; `quoin advise --mismatch-only` |
| FND-005 | medium | `model-checking` is recommended for eight criteria on a homonym; reject it. FR-001-AC-1, FR-001-AC-2, FR-002-AC-1, FR-004-AC-1, FR-004-AC-2, FR-004-AC-4, FR-004-AC-9 and FR-006-AC-1 each draw `model-checking (safety)`. The catalog's `safety` characteristic sits alongside `temporal`, `liveness` and `state-machine` under a method defined as exhaustively checking a temporal property against a state model and returning a counterexample trace (`Kind2`, `nuXmv`, `TLA+`) — the temporal-logic sense of "safety property", not the domain. The eight criteria are structural assertions about JSON Schema files and manifest keys; there is no state model and no temporal property among them. The trigger is checkable: those eight are exactly the criteria whose statement contains the word *hazard* in prose, and the only other criterion mentioning it (NFR-001-AC-5) mentions it solely inside code spans and draws no such recommendation. A safety-domain module is where this will fire hardest, so it is worth carrying upstream. `property_shapes` for the same eight is `example`/`universal` and the authored evidence (`Unit`, `Integration`) is right. | FR-001-AC-1/2, FR-002-AC-1, FR-004-AC-1/2/4/9, FR-006-AC-1; `verification_catalog.model-checking` |
| FND-006 | medium | `criticality` is null on all 54 obligations, so the safety escalations can never fire. `quire properties --json` reports `obligation.criticality: null` for every criterion in the bundle. Two catalog methods key on `high-criticality` — `mutation-testing` and `concolic-execution` — and the latter's entry names ISO 26262 ASIL D and IEC 62304 Class C as the case it exists for. In the ecosystem's safety module, nothing can ever elicit either, and the advisor's "0 inconclusive" is partly a consequence: an axis with no values recorded produces no recommendations rather than an unmatched obligation. Recommend deciding whether this bundle declares criticality at all — a module that only *declares* the hazard vocabulary may legitimately not, but that should be a recorded decision rather than an absent field. | `quire properties --json`; `verification_catalog.mutation-testing`, `.concolic-execution` |
| FND-007 | low | IT-001's six success criteria declare no verification method anywhere. `IT-001-SC-01..SC-06` are stated inline under Test Procedure with no `Verification` or `Validation` column, and the nearest statement of method is `Automation: Automated` in the Metadata block, which is neither a catalog method id nor a `test_type` value. The matrix covers all six with one row, TC-070, typed `Integration` — which is the right evidence kind for `integration-testing`, so the method is correct in effect and undeclared in fact. | IT-001 Test Procedure and Metadata; spec/tests.md TC-070 |
| FND-008 | low | `dast` and `iast` are recommended for FR-005-AC-3 and FR-005-AC-5 on `security`; reject both. Both methods probe a running, network-exposed system from outside or from inside (`ZAP`, `Burp`, `Contrast`), and both are additionally keyed `object_types: [attack_surface]`, which this module does not declare. FR-005-AC-3 is about extraction diagnostics under a bundle index and FR-005-AC-5 about negative fixtures failing with a declared `expect` token; the module ships JSON Schema files and Markdown skeletons and exposes no network surface. `negative-abuse-testing`, recommended alongside for AC-5 and for FR-005-AC-1, is right in substance for the wrong reason — those criteria do exercise refusal paths — and its `evidence_kind: Integration` already matches the authored `Type` of TC-050 and TC-052. Recommend `negative-abuse-testing` for FR-005-AC-5 and rejecting the two dynamic security methods. | FR-005-AC-3, FR-005-AC-5; spec/tests.md TC-050, TC-052 |
| FND-009 | low | The catalog's `fault-injection` rule names this module's own object types and elicits nothing from it. The entry is keyed `object_types: [hazard, failure_mode]`, added — per its own comment — because "a declared failure mode names a failure the system can suffer, and a hazard names a state that failure can reach". Across all 59 advised obligations it was recommended zero times. Judgement: that is correct, not a gap. This bundle's requirements are about the *declaration* of the hazard and failure-mode types — their schemas, locators and skeletons — and not about a system that suffers them, so no obligation here has a failure to induce. The rule will fire in consumer repositories authoring hazard documents. Recorded so a later reader does not read the silence as an unverified reliability obligation. | `verification_catalog.fault-injection`; FR-001, FR-004 |
| FND-010 | low | The matrix's NFR method cell and NFR-001's own metric cells now disagree in kind. `spec/tests.md` Non-Functional Requirement Coverage carries `Test (locator baseline diff, 0.2.0 skeleton validation, traceability comparison, lint allow-list widening)` — a class plus prose — while NFR-001's Measurement table now names `unit-testing` and `integration-testing`. Two statements of the same obligations' methods in two granularities; the requirement's own cell is the one quire-rs FR-053 reads. Same class of defect as FND-001, recorded separately because it is one cell and a one-line fix. | spec/tests.md Non-Functional Requirement Coverage; NFR-001 Measurement and Evaluation |
| FND-011 | low | Two adjacent packaging checks are typed inconsistently. TC-023 (no `.npmrc`, no `file:`/`link:` dependency, exact pins) is `Static` and TC-024 (`package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core`) is `Unit`, though both read a checked-in manifest file for a supply-chain property and both discharge an `Inspection`-declared constraint (FND-002). Under the recommendation there, both are `sca-sbom`, whose `evidence_kind` is `Static`. | spec/tests.md TC-023, TC-024 |

## Automated Checks

| Check | Result |
|---|---|
| `quoin advise` | 59 obligations; 5 mismatch (NFR-001-M-1..M-5), 0 uncatalogued, 0 inconclusive. All five mismatches rejected as false positives (FND-004). |
| Authored method granularity | ❌ 54/54 acceptance criteria authored the class `Test` rather than a catalog method id (FND-001). |
| Obligations reaching the advisor | ❌ 59 of 85 declared obligations; 18 constraints, 2 StR validation criteria and 6 IT success criteria unevaluated (FND-003). |
| Uncatalogued methods | ✅ `quire coverage` reports no `uncatalogued-verification-method`. NFR-001's five Measurement methods are catalog ids (`unit-testing`, `integration-testing`); base FND-009 discharged. |
| Test Matrix `Type` vocabulary | ✅ all values in use — `Unit` (37), `Integration` (26), `Static` (5), `Property` (1) — are members of `traceability.vocabularies.test_type`. No invalid token. |
| Method/evidence-kind agreement | ❌ six `Inspection`-declared obligations (`evidence_kind: Manual`) are backed by rows typed `Static`, `Unit` and `Integration` (FND-002). No row anywhere is typed `Manual`, `Inspection`, `Analysis`, `Eval` or `Demonstration`. |
| Trace backing | ✅ `quire coverage --scope .` → `Coverage: 125/125 rows backed (100%)`; python 70/70/72 bound/tagged/candidates. |
| Obligation criticality | ❌ null on all 54; `high-criticality` methods unreachable (FND-006). |

## Recommended Methods

Per obligation class, the method this review would confirm. Rows the advisor and
the authoring already agree on at method level are omitted.

| Obligation | Authored | Recommended | Basis |
|---|---|---|---|
| FR-001-AC-1..AC-3, AC-5; FR-002-AC-1, AC-4, AC-6, AC-7, AC-9; FR-003-AC-1, AC-2, AC-4, AC-5, AC-7; FR-004-AC-1; FR-005-AC-2, AC-4, AC-8, AC-10; FR-006-AC-1, AC-3; NFR-001-AC-4, AC-5 | `Test` | `unit-testing` | catalog, `property_shapes: example` |
| FR-001-AC-4, AC-7; FR-002-AC-2, AC-3, AC-5, AC-8; FR-003-AC-3, AC-6; FR-004-AC-2..AC-12; FR-005-AC-6, AC-7, AC-9; FR-006-AC-2, AC-4; NFR-001-AC-1..AC-3 | `Test` | `property-based-testing` | catalog, `property_shapes: universal` |
| FR-005-AC-1, AC-5 | `Test` | `negative-abuse-testing` | catalog, `characteristics: input-validation`; `security` trigger rejected (FND-008) |
| FR-002-AC-4, AC-8, AC-9 | `Test` | `integration-testing` | judgement — the row drives `make schemas-check` across the generator boundary; matches the authored `Type: Integration` |
| FR-001-CON-1 | `Inspection` | `integration-testing` | FND-002 |
| FR-002-CON-1; FR-004-CON-3 | `Inspection` | `architecture-conformance` | FND-002 |
| FR-002-CON-2; FR-002-CON-4 | `Inspection` | `sca-sbom` | FND-002 |
| StR-001-VC-2 | `Inspection` | `unit-testing` | FND-002 |
| IT-001-SC-01..SC-06 | (none) | `integration-testing` | FND-007 |
| NFR-001-M-1..M-5 | `unit-testing`, `integration-testing` | confirm as authored | FND-004; `performance-benchmarking` rejected |

## Suite Plan

A method implies an evidence kind; a suite produces it. Under the
recommendations above the bundle needs producers for four kinds — `Unit`,
`Integration`, `Property` and `Static` — which is the same set the matrix
already declares and the same gap it already records: no `SuiteRegistry`
document exists, and `quire coverage` reports `archetype-matches-nothing` for
both the `suite` and `inspection` declarations. FND-002 changes what the second
of those means. With the `Inspection` methods corrected, **no obligation in this
bundle requires an `Inspections` document at all** — every one is discharged by
executable evidence — so the absent inspections registry stops being a gap and
becomes a thing this module does not need. The absent `SuiteRegistry` remains a
gap in the plan, not in the spec.

## Notes

- Nothing in this bundle warrants `concolic-execution`. It is recommended
  nowhere, and correctly so: the escalation is reached after cheaper search has
  stalled, and nothing here has stalled — 125/125 rows are backed by tests that
  run. The `fault-detection-unmeasured` characteristic that would elicit it is
  also unproducible, since no mutation or fault-detection measurement exists for
  this suite. That absence is worth naming as an option rather than a defect: if
  the safety module's schemas are later treated as high-criticality (FND-006),
  `mutation-testing` is the cheap first step and the one that says whether any
  escalation is warranted.
- Three of the five rejected or corrected recommendations (FND-004, FND-005,
  FND-008) are catalog-keying issues rather than authoring defects, and all
  three are reproducible from a single `quoin advise` run in this worktree. They
  belong upstream in `agent-ix/spec-artifacts-process` rather than in this
  branch's disposition.
- The base review (`base.md`) is not restated here. Where it overlaps —
  its FND-009 on uncatalogued Measurement methods — the state has changed and
  the change is recorded in the Automated Checks table above.
- No spec artifact was edited by this review.
