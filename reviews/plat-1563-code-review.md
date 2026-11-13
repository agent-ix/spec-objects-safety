---
id: SR-058
title: "Code review of PLAT-1563/1565/1568 residual-risk object types (spec-objects-safety#39)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, typespec/main.tsp, spec_objects_safety/schemas/, spec_objects_safety/skeletons/, tests/, tests_integration/test_risk_chain_edges.py (git diff origin/main...23a713c)"
review_set: subset
---
# Code review of PLAT-1563/1565/1568 residual-risk object types (spec-objects-safety#39)

## Summary

Tickets: PLAT-1563, PLAT-1565, PLAT-1568. PR `agent-ix/spec-objects-safety#39`,
head `23a713c`, one commit. The PR adds four object types
(`acceptability_policy`, `residual_risk`, `benefit_risk`,
`overall_residual_risk_evaluation`), their TypeSpec models and 19 emitted
schemas, four skeletons, seven negative fixtures,
`tests/test_residual_risk.py` and edge tests in
`tests_integration/test_risk_chain_edges.py`. There is no Rust, so
rust-review does not apply.

Run evidence: after `make semantic-install`,
`pytest tests/test_residual_risk.py tests/test_skeletons_semantic.py tests/test_manifest.py tests/test_risk_chain.py`
gives 148 passed, and `pytest -m integration tests_integration/test_risk_chain_edges.py`
gives 29 passed (quire 0.44.0, engine 0.59.1; quoin 0.30.1). The reviewer also
ran probes through `validate_document` from a scratchpad script. The repository
was not edited.

- A filled `residual_risk` with `accepted` and an empty `Decided by` validates.
- A filled `residual_risk` with `undecided` and a named decider validates.
- The same two cases validate for `benefit_risk` and the evaluation.
- An `undecided` record with an empty rationale fails.
- A policy that repeats a severity level, drops a cell, or names an unlisted
  region validates.

A scratch copy of the package added the `record-sections` mapping token and
renamed the section to `## Determination`. With it, the engine refuses the
`determination` key: "has a schema shape record-sections cannot read", because
the key is an `anyOf` union. With the key pointed at the plain
`DecidedDetermination` object, the same document is extracted and validated:
an empty decider fails with `determination.decided_by: "decided_by" is a required property`.

## Verdict

Changes requested. PR #38's lessons hold:

- No `mappings.yaml`.
- No `spec/tests.md` rows.
- No hash, pin or file-count test.

FR-104 and NFR-100 hold for what this PR ships:

- Every new model is sealed.
- No score, region, ratio, total or date member exists on a decision record.
- No schema declares `default`.
- `outside_acceptable` is a required boolean with no default. A blank flag
  fails at the document, through `column_choices`.
- All four skeletons fail as shipped, and filled copies validate.
- The decision unions refuse `decided_by` on `undecided`, and require a
  non-blank rationale and `decided_by` when decided.

On `references`: reusing it for the policy link, the benefit-risk "covers" link
and the evaluation's "considers" link is acceptable. The iso verb is loose, but
`allowed_links` types each end, and the integration tests show
`disallowed-edge-target` naming the wrong type. No closer iso verb exists: iso
`covers` means a test covers a requirement.

The main defect is FND-001. Real documents never reach the decision unions,
so a document can record an `accepted` decision with nobody named, and it
validates. FND-003 to FND-005 are in-PR fixes.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | At the document level, an `accepted` or `not_accepted` residual_risk, benefit_risk or evaluation with an empty `Decided by` validates, and an `undecided` one with a named decider validates. The `Decided by` pattern `^[^<>]*$` admits blank. The `Determination` unions are never reached from a document, because Quire populates only fields, clauses, operations and relations. The decider tests run over hand-built records only. | spec_objects_safety/manifest.yaml:480-487, spec_objects_safety/manifest.yaml:523-530, spec_objects_safety/manifest.yaml:567-574, tests/test_residual_risk.py:290-320 |
| FND-002 | medium | The `rationale` member is optional (`rationale?`) on `UndecidedDetermination`, `UndecidedBenefitDetermination` and `UndecidedEvaluation`. FR-103, FR-106 and FR-107 Behavior 1 say the type SHALL require a rationale; only non-emptiness depends on the decision. The document layer goes the other way: it requires a non-blank rationale even when `undecided`. So the two layers disagree with each other and with the spec. | typespec/main.tsp:563-566, typespec/main.tsp:612, typespec/main.tsp:654, spec_objects_safety/manifest.yaml:486 |
| FND-003 | medium | No required relation is declared for the references FR-103, FR-106 and FR-107 require: an `estimate` and a policy reference on `residual_risk`, one or more `residual_risk` references on `benefit_risk`, and the considered references on the evaluation. A `residual_risk` with no edges validates silently. FR-058 `required_relations` can state each one today, declared once each and promotable through `trace:<check>`. | spec_objects_safety/manifest.yaml:595-665 |
| FND-004 | medium | `estimate` is a new verb that PLAT-1676 does not list (it lists `estimates` and `assumes`). Adding it to `PENDING_ISO_VERBS`, whose expiry is "when PLAT-1676 lands", means that expiry can never clear the set. The verb is also a near-synonym of the pending `estimates`, and the module's own rule is "NO NEW VERBS". `references` restricted to `[risk_estimate, acceptability_policy]` plus typed required relations would distinguish the two ends without a verb. | tests/conftest.py:65, spec_objects_safety/manifest.yaml:461-463 |
| FND-005 | medium | The `residual_risk`, `benefit_risk` and evaluation skeletons, and the negative fixtures copied from them, declare `reviewed_at Timestamp 0..1` in `## Properties`. FR-103 says the record SHALL NOT carry typed history or a decision date, and FR-106 and FR-107 forbid a date. The banned-property test checks top-level schema keys only, not the FieldDecls a document declares, so it misses this. | spec_objects_safety/skeletons/residual_risk.md:58, spec_objects_safety/skeletons/benefit_risk.md:52, spec_objects_safety/skeletons/overall_residual_risk_evaluation.md:55 |
| FND-006 | medium | `test_each_reference_is_allowed_to_exactly_its_target_type` asserts that the manifest's `allowed_links` equal a literal copy of themselves. It is a self-copy test. The integration tests already cover FR-103-AC-4 and FR-106-AC-6 by behaviour (`disallowed-edge-target` naming the type). | tests/test_residual_risk.py:492-507 |
| FND-007 | medium | `assert {p.name for p in fixtures} == NAMED_NEGATIVE_CASES` is a file-inventory equality. The diff extends it with seven fixture names. Each fixture's own failure is already asserted per file. | tests/test_skeletons_semantic.py:47-71, tests/test_skeletons_semantic.py:192 |
| FND-008 | low | `SUPPORT_MODELS` in conftest has no reader in `tests/` or `scripts/`. The diff adds 15 names to a dead inventory. | tests/conftest.py:91-124 |
| FND-009 | low | `test_a_blank_policy_cell_fails_at_the_document` is tagged `FR-101-AC-2`, but AC-2 is the positive case (the 3x3 fixture validates). The test asserts that an unfilled cell fails, which belongs to FR-101's "fail until a person fills every cell" (FR-101-AC-6). | tests/test_residual_risk.py:244-252 |

## Finding detail

- FND-001: this is an engine limit, but not the one the PR body names. The
  engine already has record-sections extraction (quire-rs FR-081, quoin FR-121,
  present since v0.55.0). The probe shows it would enforce the decider rule
  through the emitted schema, except that it refuses an `anyOf` record key. A
  narrow quire-rs ticket is warranted: record-sections should read a record key
  whose schema is an `anyOf` of object `$ref`s. Until it lands, either file that
  ticket and record the deferral, or take the decider-half tags off the
  schema-only tests. Today those tags claim FR-103-AC-2, FR-103-AC-3,
  FR-106-AC-3 and FR-107-AC-2 for an assertion no document can reach.
- FND-002: make `rationale` a required `string` (may be empty) on the three
  undecided models. Either relax the document `Rationale` pattern, or state
  in the manifest comment that the document layer is deliberately stricter.
- FND-003: four relations, each declared once:
  - `residual-risk-has-estimate`: `edges: [estimate]` (or `references`), `to: [risk_estimate]`.
  - `residual-risk-has-policy`: `to: [acceptability_policy]`.
  - `benefit-risk-covers-risk`: `to: [residual_risk]`.
  - `evaluation-considers`: `to: [residual_risk, benefit_risk]`.

  All are outgoing. Each needs a one-warning test and an edge-clears-it test,
  as `estimate-has-situation` has.
- FND-004: either switch to `references`, or add `estimate` to PLAT-1676's
  scope explicitly. Do not leave it in an allowance whose expiry cannot fire.
