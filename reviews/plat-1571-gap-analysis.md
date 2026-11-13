---
id: SR-061
title: "Gap analysis of FR-301, FR-303, FR-304 and FR-205 against spec-objects-safety#40"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-301, FR-303, FR-304, FR-205 (on main), spec_objects_safety/manifest.yaml, tests/test_risk_chain.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...4d37731)"
review_set: subset
---
# Gap analysis of FR-301, FR-303, FR-304 and FR-205 against spec-objects-safety#40

## Summary

Tickets: PLAT-1571 (FR-301, FR-304), PLAT-1574 (FR-303), PLAT-1561 (FR-205).
Scope: the Behavior and Acceptance Criteria of FR-301, FR-303, FR-304 and
FR-205, as they stand on main, against PR head `4d37731`. Plan completion:
not assessed.

Method:

- Read each FR, the manifest and the tests.
- Ran `quoin matrix --json` (quoin 0.30.1) and `quire trace`.
- Ran the changed test files: 103 passed.
- Probed `quire validate` and `quire extract` (quire 0.44.0, engine 0.59.1)
  from a scratchpad script.

The computed matrix is not usable as evidence for this scope. It reports
every FR-2xx and FR-3xx criterion as `untagged`, on main as well as on this
branch. `quoin matrix` binds a `@pytest.mark.trace` tag only through a TC row
in `spec/tests.md`, and `quire trace` lists these tags as
`evidence_near_miss/line_heuristic` citations. That is a quoin tooling
limit, not a defect in this PR. The repository rule is not to hand-write
`spec/tests.md` rows, so the AC-to-test map below was built by reading the
`trace` tags directly.

## Verdict

Not mergeable as is.

Implemented and tested by behaviour:

- FR-301-AC-1 to AC-10. AC-7 is tagged on a test that runs a different case
  (SR-060 FND-003). A probe shows the AC-7 behaviour itself holds.
- FR-303-AC-1 to AC-4. AC-6 (Inspection) holds by inspection: the new
  relation carries no region, level, score or default decision.
- FR-304-AC-1 (asserted, but untagged; SR-060 FND-004), AC-2 and AC-3.
  AC-4 is only partly covered.
- FR-205-AC-4 and AC-5 from #38. AC-6 holds at this head: there is no
  relation from `control`.

PLAT-1561's claims, checked:

- "Authored edges and ACs done in #38." This holds for AC-4 and AC-5.
  AC-1 and AC-2 are tested through a proxy: a dangling-reference count drops
  from 2 to 0 when the control is added. That proxy can fail, which is the
  property FR-205 asks for. But the criteria as written cannot be met (FND-004).
- "FR-205-AC-3 needs a quire-rs library test with no owner." FND-005 gives
  the judgement on a ticket.
- "Resolved inverse edges wait on PLAT-1676." This is true for `arises_from`,
  `estimates`, `assumes` and `estimate`. It does not apply to FR-205:
  `satisfies` and `verifies` are iso verbs that already have inverses, so
  PLAT-1676 does not unblock FR-205-AC-1 or AC-2.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-303-AC-5 has no tagged test. FR-203-AC-6's test covers the skeleton half: the locator is `frontmatter_field` and the skeleton carries `phase`. Nothing checks the relation half: a fixture with `phase` only in the body should be unselected by `post-control-estimate-has-decision` (no finding) and invalid under validation. | tests/test_risk_chain.py:270-279, tests_integration/test_risk_chain_edges.py:702-727 |
| FND-002 | medium | The engine does not see `phase` as a declared frontmatter key of `risk_estimate`. FR-303 says the module SHALL declare it as one. `risk_estimate` has no `frontmatter_schema_ref`, and `RiskEstimate.json` has no top-level `phase`. In any bundle with no estimate, the new relation emits "selects on `where` field 'phase', which is not a property of 'risk_estimate' frontmatter ... matches nothing [undeclared-relation-vocabulary]". `post-control-assumes-control` already emitted the same false advisory; this PR adds a second. | spec_objects_safety/manifest.yaml:311-330, spec_objects_safety/manifest.yaml:687-693 |
| FND-003 | low | FR-304-AC-4 asks for an acyclic chain of failure mode, hazard, situation and harm. The `chain()` fixture has no failure mode, so the `failure_mode` to `hazard` `arises_from` hop is never in the acyclic case. A probe with FM-001 added gives no cycle finding, so the behaviour holds and only the test is short. | tests_integration/test_risk_chain_edges.py:609-612, tests_integration/test_risk_chain_edges.py:753-756 |
| FND-004 | medium | FR-205-AC-1 and AC-2 require `quire extract` to list the FR or IT as an incoming edge on the control. `quire extract` reads one document and emits only that document's outgoing edges. It does not accept a repeated `--module`, and run over the control with the iso module it fails with "archetype 'control' not registered". So no test can meet the criteria as written. The #38 tests use a proxy (the dangling-reference count drops from 2 to 0) and are tagged with both ACs. | spec/functional/FR-205-control-requirement-and-verification-links.md:91-92, tests_integration/test_risk_chain_edges.py:345-363 |
| FND-005 | medium | FR-205-AC-3 has no test. Its `evidence::qualify` half is behaviour of quire-rs FR-078 and belongs in quire-rs's own test suite. Its module half can be tested here today with `quire validate`: an FR `satisfies` a control that has no `verifies` edge, and no diagnostic about a missing verification is raised. | spec/functional/FR-205-control-requirement-and-verification-links.md:93 |

## Finding detail

- FND-001: add one integration test that uses the `risk_estimate-no-phase`
  negative fixture, or a post-control estimate with `phase` moved into the
  body. Assert there is no `post-control-estimate-without-decision` line and
  that validation reports the estimate as invalid. Tag it FR-303-AC-5.
- FND-002: declare `phase` where the engine reads frontmatter properties,
  for example a `frontmatter_schema_ref` for `risk_estimate` as iso does for
  `NFR` `quality_attribute`. Then FR-303's "SHALL declare `phase` as a
  top-level frontmatter key" holds for the engine too, and the false
  advisory goes away for both `where` relations.
- FND-004: reword FR-205-AC-1 and AC-2 to what can be observed:
  `quire validate --okf --strict` resolves the edge to the declared control,
  which the existing tests assert. The other option is to name the corpus
  command that does report incoming edges. Do not wait on PLAT-1676 for this.
- FND-005, on whether this deserves a ticket: no new ticket. The
  `evidence::qualify` half is quire-rs FR-078's own behaviour, so it should
  be cited, not re-tested from Python. Reword FR-205-AC-3 to the
  module-observable claim and add the `quire validate` test. This matters
  for PLAT-1573: its `control-has-verification` relation (commit `df09e8c`)
  will report exactly the missing-`verifies` diagnostic that FR-205 says the
  retained-evidence route SHALL NOT need. The PLAT-1573 review should check
  that conflict.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, eac2fb4: there are three FR-303-AC-5 tests. A unit test reads `phase` from the emitted frontmatter schema. A unit test shows a body-only `phase` estimate is invalid while the filled one validates. An integration test shows the relation stops reporting once `phase` moves to the body. |
| FND-002 | fixed | Round 1, eac2fb4: `risk_estimate` declares `frontmatter_schema_ref: schemas/RiskEstimateFrontmatter.json`, emitted from TypeSpec (`schemas-check`: 37 match). The reviewer compared stderr before and after on 13 bundles. Both false `phase` advisories are gone from every bundle with no estimate. Exit codes are unchanged everywhere. The only other change is one extra `[frontmatter]` error when `phase` is not one of the two values, which the body extraction already reports: a duplicate diagnostic, not a new failure. |
| FND-003 | fixed | Round 1, eac2fb4: the FR-304-AC-4 fixture is FM-001, then HAZ-001 `arises_from` FM-001, then SIT-001, then HARM-001, with no cycle finding asserted. |
| FND-004 | fixed | Round 1, eac2fb4: FR-205-AC-1 and AC-2 now ask for no `dangling-reference` for the edge under `--strict`, and for the same edge to dangle once the control is removed. The existing test asserts exactly that and can fail. Wording nit: "validates under `--strict`" is not literally true for this fixture. The strict run exits 3 on an unrelated `references 'name'` dangling edge from the iso FR skeleton, and the test asserts only the edge-specific part. |
| FND-005 | fixed | Round 1, eac2fb4: FR-205-AC-3 is reworded to the module-observable claim, with `evidence::qualify` cited to quire-rs FR-078. A `quire validate` test asserts exit 0 and no line containing `verif` for a satisfied control that has no `verifies` edge. The conflict with FR-302 is recorded as FND-006. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | medium | FR-205 and FR-302, both on main, disagree on how a risk control verified only by retained evidence is checked. FR-205 says retained evidence binds to the satisfying FR's criteria through `evidence::qualify` and "SHALL require no authored `verifies` edge". FR-302 counts a control as verified only through an incoming `verifies` edge, from a test or from a retained-evidence record referenced by id (FR-302-AC-4). PLAT-1573's `control-has-verification` (#41, `df09e8c`) implements FR-302, so a risk control backed only by evidence on its FR will be reported `control-without-verification`. The reworded FR-205-AC-3 test cannot show this: its fixture control mitigates nothing and no estimate assumes it, so it is outside FR-302's `when_any` scope and passes with #41 too. | spec/functional/FR-205-control-requirement-and-verification-links.md:39-49, spec/functional/FR-205-control-requirement-and-verification-links.md:82, spec/functional/FR-205-control-requirement-and-verification-links.md:93, spec/functional/FR-302-risk-control-implemented-and-verified.md |

## New finding detail

- FND-006: FR-205 is the side that must change. A required relation tests
  one edge hop and cannot follow an `evidence::qualify` binding from an FR's
  criterion back to a control, so FR-302's model is the only one the engine
  can check. FR-302 already provides for retained evidence: a `verifies`
  edge from an evidence record referenced by id, with an empty `to`.
  - Rewrite FR-205's "Retained evidence" paragraph and its Behavior line
    "The module SHALL require no authored `verifies` edge for the
    retained-evidence route" to match FR-302: a risk control's retained
    evidence reaches it through a `verifies` edge from the evidence record.
  - Scope FR-205-AC-3 to what stays true: a control outside FR-302's scope
    raises no missing-verification diagnostic. That is what its test asserts.
  - #41 needs no change for this; FR-302-AC-4 tests the evidence-record
    route.

  #40 rewrote AC-3, so the edit fits there. #40's code does not conflict with
  #41, so deferring the FR-205 prose edit to #41 is also sound, if the lead
  records that.
