---
id: SR-057
title: "Gap analysis of FR-201..FR-205 against spec-objects-safety#38"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-201..FR-205, spec/tests.md, spec_objects_safety/, tests/test_risk_chain.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...4a8d015)"
review_set: subset
---
# Gap analysis of FR-201..FR-205 against spec-objects-safety#38

## Summary

Tickets: PLAT-1410, PLAT-1411, PLAT-1558. Scope: FR-201..FR-205 Behavior and
Acceptance Criteria against the PR head `4a8d015`. Out of scope by the
dispatch brief: the FR-301 chain rules and the FR-302/FR-303 completeness
relations (PLAT-1571/1573/1574). Plan completion: not assessed.

Method: read each FR, the manifest, the schemas and the tests, and run
`quire matrix --scope .` (quire 0.44.0, engine 0.59.1). To test whether the
two FR-203/FR-204 relations are blocked by the engine, the reviewer added them
to a scratch copy of the module outside the repository and validated a bundle
with that copy:

- An estimate with no `estimates` edge got one `estimate-without-situation`
  warning.
- A `post_control` estimate with no `assumes` edge got one
  `post-control-without-control` warning, "selected because `phase` is
  'post_control'".
- A `pre_control` estimate with no `assumes` edge got no finding.
- `--severity trace:post-control-without-control=error` made the run exit 3.

Both relations work today. Neither is blocked by an engine gap, and the
`UnknownEdgeType` advisory for the pending verbs does not stop them.

## Verdict

Not mergeable. FR-201 and FR-202 are implemented and tested, except FR-202-AC-2,
which waits on the iso inverse label. FR-205 has nothing to implement beyond
its inspection criteria. FR-203 and FR-204 each leave their module-owned
required relation undeclared (FND-001, FND-002). These are the module's own
FR text, not FR-301..303 work, so they belong in this PR. The matrix also
shows that no FR-201..FR-205 criterion is backed, because the tags carry no
TC row (FND-003).

What holds: types, exports, lexicon entries (`hazardous situation`,
`probability`), allowed-link targets, sealed schemas, the level and marker
split (`EstimateLevelText` with `not.enum` over the three `EpistemicState`
members), `phase` as a frontmatter key with no default, a skeleton that fails
as shipped, dangling and disallowed-target diagnostics, acyclicity, and no
`required_relations` from `hazardous_situation` or `control`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-203 says the manifest SHALL declare required relation `estimate-has-situation` (`from: risk_estimate`, `edges: [estimates]`, `to: [hazardous_situation]`, outgoing, `check: estimate-without-situation`). It is not declared, and FR-203-AC-9 has no test. The engine supports it today (verified on a scratch copy). | spec_objects_safety/manifest.yaml:379-421 |
| FND-002 | high | FR-204 says the manifest SHALL declare `post-control-assumes-control` (`where: {field: phase, values: [post_control]}`, `edges: [assumes]`, `to: [control]`, outgoing, `check: post-control-without-control`). It is not declared, and FR-204-AC-2, AC-7, AC-8 and AC-9 have no tests. FR-058 `where` on the frontmatter `phase` works today (verified: one warning for post_control, none for pre_control, exit 3 with the severity flag). | spec_objects_safety/manifest.yaml:379-421 |
| FND-003 | medium | `quire matrix` reports all 44 FR-201..FR-205 criteria as untagged or method-without-symbol, with `criterion-tagged-outside-row` on every new tag. The repo binds tests through TC rows in `spec/tests.md`, as in `trace("TC-099", "FR-009-AC-1")`. The new tags carry no TC id, and `spec/tests.md` has no rows for FR-201..FR-205 and no `covers` edge for them, so none of the new tests provides backing. | tests/test_risk_chain.py, tests_integration/test_risk_chain_edges.py, spec/tests.md |
| FND-004 | medium | `PENDING_ISO_VERBS` is a temporary allowance with no tracked expiry. No Linear ticket exists for the spec-artifacts-iso changes FR-202/203/204 depend on: the `estimates` and `assumes` verbs with inverses, and the `arises_from` inverse label. A Linear title search for estimates, assumes, arises_from, gives_rise_to, verb and inverse found nothing in iso. FR-202-AC-2 and the extract half of FR-204-AC-1 cannot pass until those changes land. | tests/conftest.py:57-60, tests_integration/test_risk_chain_edges.py:1-12 |
| FND-005 | medium | FR-205-AC-3 (caller evidence through quire-rs `evidence::qualify` qualifies a criterion of the FR that `satisfies` a control, with no authored `verifies` edge) has no test and no recorded deferral. | spec/functional/FR-205-control-requirement-and-verification-links.md |
| FND-006 | low | The extraction half of FR-203-AC-14 is untested: a `not_assessed` severity should be reported as an `EpistemicState` by extraction, never as a level. The engine extracts the `estimate` row as a raw tab-joined string (`"not_assessed\tremote\tx"`), so only the schema half is asserted. Record a deferral, or narrow the AC to the schema. | tests/test_risk_chain.py:225-235 |
| FND-007 | low | The optional `## Sequence of Events` section on `hazardous_situation` (manifest locator, skeleton, mapping) has no owning requirement in FR-202. Only the PLAT-1410 ticket outcome mentions it. Add it to FR-202 or drop it. | spec_objects_safety/manifest.yaml:288-291, spec_objects_safety/skeletons/hazardous_situation.md:45 |

## Finding detail

- FND-001 and FND-002: add both entries to `traceability.required_relations`,
  plus integration tests for FR-203-AC-9 and FR-204-AC-2, AC-7, AC-8 and AC-9.
  This also requires removing SR-056 FND-001's string-absence test. Note
  FR-204-AC-9: an `assumes` edge to an undeclared id does not satisfy the
  relation because `to` is constrained.
- FND-003: add TC rows to `spec/tests.md` and `covers` edges for FR-201..FR-205,
  and put the TC id on each `trace` marker.
