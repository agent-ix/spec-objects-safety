---
id: SR-064
title: "Gap analysis of PLAT-1573 FR-302 control completeness relations (spec-objects-safety#41)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; FR-302, FR-205-AC-3, FR-205-AC-6 against spec_objects_safety/manifest.yaml and tests (git diff origin/main...5e7dd46)"
review_set: subset
---
# Gap analysis of PLAT-1573 FR-302 control completeness relations (spec-objects-safety#41)

## Summary

Ticket: PLAT-1573. Plan completion: not assessed (planless). The analysis covers
the criteria this PR claims or changes: FR-302-AC-1 to AC-8, FR-205-AC-3 and
FR-205-AC-6, against the two new relations and the tagged tests at head
`5e7dd46`.

`quire matrix --scope .` (CLI 0.45.0) lists every FR-205 and FR-302 row as
`untagged` and warns `criterion-tagged-outside-row` for each tag. This is not
caused by this PR. `spec/tests.md` (TM-001) covers only FR-001 to FR-009 and
IT-001, so tags on later requirements bind to no declared matrix row. The
same is true on `main` for FR-201 and later. Tag-to-criterion bindings were
therefore read from the `@pytest.mark.trace` markers.

| Criterion | Tagged test | State |
| --- | --- | --- |
| FR-302-AC-1 | `test_an_implemented_and_verified_risk_control_yields_no_finding` | partial: loads, but the fields are not asserted (SR-063 FND-001) |
| FR-302-AC-2 | same | backed |
| FR-302-AC-3 | `test_each_missing_link_is_reported_once_by_its_own_check` | backed |
| FR-302-AC-4 | none | gap (FND-001) |
| FR-302-AC-5 | `test_a_control_assumed_by_an_estimate_is_reported_without_mitigating` | backed |
| FR-302-AC-6 | `test_an_unrelated_security_control_is_not_reported` | backed |
| FR-302-AC-7 | `test_a_verification_recording_a_failing_result_still_satisfies_the_relation` | partial (SR-063 FND-002) |
| FR-302-AC-8 | Inspection | met: the FR states the `when_any` shape and links PLAT-1674 |
| FR-205-AC-3 | two tests (lines 783, 872) | backed |
| FR-205-AC-6 | `test_every_completeness_relation_over_control_is_scoped` | backed |

There is no code without an owning requirement: both new relations are FR-302
Behavior. There are no stubs and no coverage inflation.

## Verdict

One gap. FR-302-AC-4 is a runtime property with no test. The coder deferred it
because no installed module declares a retained-evidence record type.
`engineering-assurance` v0.8.2's manifest declares only AssuranceProfile,
MeasurementPlan, ArchitectureDescription, ComponentAssuranceContract and
AssuranceArgument, so that claim is correct.

Recommended disposition: keep FR-302-AC-4 as written, with verification Test.
Do not reword it to Inspection. Whether an evidence record's `verifies` edge
satisfies the relation is engine behaviour, observable in a run, not a property
of the text. Record it as an open gap with a Linear `blocked-by` edge to the
engineering-assurance work that adds the evidence-record type. This PR should
still test the module's half today: SR-063 FND-001 asks for a test that a
`verifies` edge from a non-test document counts, which is exactly what `to: []`
provides. When the record type exists, AC-4's test is the same fixture with
that type.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-302-AC-4 (a `verifies` edge from a retained-evidence record satisfies `control-without-verification`) has no tagged test, and no ticket or `blocked-by` edge tracks the gap. | spec/functional/FR-302-risk-control-implemented-and-verified.md:79 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | Round 1, b29e139. FR-302-AC-4 is correctly left as written (Test), and the module half (`to: []`, a non-test verifier counts) is now tested. But PLAT-1573 still has no blocked-by edge or ticket for the engineering-assurance evidence-record type. Its only relations are blocks PLAT-1576 and blocked-by PLAT-1561 and PLAT-1524. The gap is still untracked. This is a tracker action, not a code change: once the lead creates or links that ticket as blocked-by, the outcome becomes deferred with that ticket id. |
