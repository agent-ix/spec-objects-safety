---
id: SR-413
title: "Gap analysis — spec-objects-safety PLAT-1837 implementation and effectiveness verification"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; FR-205, FR-302, FR-305-AC-5, FR-305-AC-8 against spec_objects_safety/manifest.yaml and tests (git diff origin/main...3748247, PR #49)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-205", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-302", type: references }
---

## Summary

Ticket: PLAT-1837. Plan completion: not assessed (planless).

`quire matrix --scope .` (quire 0.52.0) and the `@pytest.mark.trace` markers
were read for every criterion the PR adds or rewrites. Tests were run as
recorded in SR-412 (quire 0.52.0 and 0.52.1; all control and verification
tests pass).

| Criterion | Tagged test | State |
| --- | --- | --- |
| FR-205-AC-2 | `test_requirement_and_verification_edges_resolve_to_a_declared_control` | backed for `dangling-reference`; misses the `disallowed-edge-type` the verbs draw (SR-412 FND-001) |
| FR-205-AC-3 | two tests | backed |
| FR-302-AC-1 | shape test plus three runtime tests | backed (mutation-checked) |
| FR-302-AC-2 | `test_an_implemented_and_verified_risk_control_yields_no_finding` | backed |
| FR-302-AC-3 | two tests | backed, with one vacuous assertion (SR-412 FND-003) |
| FR-302-AC-4 | none | gap (FND-001) |
| FR-302-AC-5 | `test_a_control_assumed_by_an_estimate_is_reported_without_mitigating` | backed |
| FR-302-AC-6 | `test_an_unrelated_security_control_is_not_reported` | backed |
| FR-302-AC-7 | failing-result test | backed |
| FR-302-AC-9 | `test_the_shared_verifies_verb_satisfies_neither_verification_check` | backed (mutation-checked) |
| FR-302-AC-8 | Inspection | met |
| FR-305-AC-5, AC-8 | none | FR-305's report is not implemented in this repository; these rows were untagged before this PR. Context only. |

No code lacks an owning requirement: the two relations and the two verbs are
FR-302 and FR-205 Behavior. There are no stubs and no coverage inflation.

## Verdict

One gap the PR should close. FR-302-AC-4 was rewritten here and still has no
test. `test_a_verifies_edge_from_a_non_test_document_counts_as_verification`
already shows the module half (`to: []` accepts a non-test source for both
verbs) but is tagged only FR-302-AC-1.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-302-AC-4 (a `verifies_implementation` or `verifies_effectiveness` edge from a retained-evidence record satisfies the matching check) was rewritten by this PR and is still `untagged` in `quire matrix`. The non-test-source test covers the module's half but is tagged FR-302-AC-1 only, and asserts both verbs together, so it never shows that a non-test source of one verb leaves the other check firing. Tag a test to AC-4 that gives each verb from a non-test source in turn and asserts only the matching check clears. | spec/functional/FR-302-risk-control-implemented-and-verified.md:82, tests_integration/test_risk_chain_edges.py:910-922 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | medium | FR-302-AC-4 and the FR-205 retained-evidence statement claim a `verifies_implementation` or `verifies_effectiveness` edge from a retained-evidence record works. The test now tagged AC-4 uses an `NFR` source as a stand-in, and neither spec says so. engineering-assurance origin/main declares no retained-evidence record type, and iso#76 allows the verbs only on NFR, IT and TC. A future record type therefore draws `disallowed-edge-type` under `--strict` unless engineering-assurance allows both verbs. State in FR-302 (and FR-205 "Retained evidence") that the record type does not exist yet, that the tagged test proves the module half (`to: []`) with a non-test source, and that the record type must allow both verbs. Track that engineering-assurance work as a blocked-by ticket. | spec/functional/FR-302-risk-control-implemented-and-verified.md:82, spec/functional/FR-205-control-requirement-and-verification-links.md:54-61, tests_integration/test_risk_chain_edges.py:966-984 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, c8f1044. `test_a_non_test_document_verifying_edge_satisfies_the_matching_check` is tagged FR-302-AC-4, parametrized per verb, and asserts the matching check clears while the other still fires. `quire matrix` shows FR-302-AC-4 as tagged. It passes with quire 0.52.0. |
| FND-002 | fixed | Round 2, c6f5f22. FR-302-AC-4 now reads "from a document that is not a test document ... The test uses an `NFR` as the stand-in for a retained-evidence record, because no such record type exists yet." FR-205 "Retained evidence" states the stand-in and that a future record type must allow both verbs in its `allowed_links`. The test carries a matching comment. No ticket ids were added. |
