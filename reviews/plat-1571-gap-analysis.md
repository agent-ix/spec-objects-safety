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
