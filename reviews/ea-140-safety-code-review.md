---
id: SR-420
title: "Code review — spec-objects-safety EA-140 risk_management_review object type"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, spec_objects_safety/schemas/RiskManagementReview.json, spec_objects_safety/skeletons/risk_management_review.md, typespec/main.tsp, tests/conftest.py, tests/test_risk_management_review.py, tests/test_skeletons_semantic.py, tests/fixtures/negative/risk_management_review-placeholder-reviewer.md, tests_integration/test_risk_chain_edges.py (git diff origin/main...b5b402c, PR #51)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-109", type: references }
---

## Summary

Ticket: EA-140 (part 1). PR spec-objects-safety#51, head `b5b402c`, base
`origin/main` `a5d0094` (GitHub reports MERGEABLE).

The PR adds the `risk_management_review` object type: one required Review
table (`Reviewer | Plan executed | Post-production readiness | Statement`,
exactly one row), `column_choices` closing `Plan executed` to
`yes | partly | no` and `Post-production readiness` to `ready | not_ready`,
non-placeholder `column_patterns` on `Reviewer` and `Statement`,
`allowed_links: reviews: [risk_management_plan], references:
[overall_residual_risk_evaluation]`, two traceability relations
(`review-without-plan`, `review-without-overall-evaluation`), the emitted
`RiskManagementReview.json`, a skeleton that fails as shipped, one negative
fixture, and the type's rows in the conftest registries. Manifest hunks are
additive (description string, one export, one object-type block, two
relations). No open PR from another lane touches the manifest at review time.

What ran (all measured by the reviewer):

- Environment: the poetry venv resolved from the lock (quire wheel 0.62.2,
  spec-artifacts-iso git dependency on main at `9342304`, which is current iso
  `main` HEAD per `git ls-remote`, spec-objects-security 0.12.1); CLI
  `quire 0.52.0 (engine 0.62.2)`; `-o addopts=""`.
- `node scripts/generate-schemas.mjs --check` after `npm ci`: 39 schemas
  match. `ruff check` and `black --check` on `tests`, `tests_integration`:
  clean.
- `tests/` plus `tests_integration/test_risk_chain_edges.py`: 288 passed,
  3 failed. The 3 (`test_a_hazard_may_arise_from_each_cause_type`,
  `test_a_failure_mode_may_reference_a_part`,
  `test_a_failure_mode_reference_to_an_undeclared_part_is_dangling`) and
  `test_quoin_install_roundtrip` fail identically on a pristine `origin/main`
  worktree with the same venv (4 failed, 68 passed). With
  spec-objects-architecture `origin/main` on `PYTHONPATH` two of the three
  pass; the third needs a `soup_record` skeleton that spec-objects-security
  0.12.1 does not ship. None is caused by this PR. Every FR-109 test passes.
- Edge vocabulary: `reviews` is declared in spec-artifacts-iso main
  `edge_types` ("A review assesses the target artifact.", inverse
  `reviewed_by`), with no source/target role constraint; `references` is
  iso's loose linkage verb. A bundle (policy, plan, evaluation, review with
  both edges) under `quire validate --okf` with iso main, security and this
  module: exit 0, no `UnknownEdgeType`, no `disallowed-edge-*`, no `RMR-001`
  diagnostic. The two `review-without-*` warnings fire in the locked
  environment (security 0.12.1), so the earlier out-of-scope note about
  security main disabling relation checks does not bite here.
- Two verbs, measured: with `references` used for both targets, each edge
  trips the other relation (`disallowed-edge-target` plus
  `target-kind-mismatch` from the relation whose target list excludes it).
  The coder's reason for `reviews` to the plan holds, and `reviews` fits iso's
  own description of the verb.
- Mutation probes on a scratch worktree: dropping the `Reviewer` pattern, the
  `Statement` pattern, either relation, either `column_choices` entry, or
  adding a `score` schema property or an `Acceptability` column each fails a
  test. Dropping the `Reviewer` pattern also fails
  `test_every_negative_fixture_fails_for_its_own_reason`, so the negative
  fixture is meaningful.
- Direct engine probes: an empty cell in each column, a second data row,
  `TBD` as reviewer and `Yes` (wrong case) each fail validation.

The enum-like cells are the reviewer's own statements with no default and no
derivation (FR-109-AC-8 test passes for `yes/ready` against a `not_accepted`
evaluation and for `no/not_ready`); they are facts a person enters, not a
score, class, acceptability or approval. The schema is sealed and carries only
`fields`, `evidence`, `relations`, `clauses`. No standard text appears in the
diff. The conftest edits add the type to parametrising registries
(`OBJECT_TYPES` compared as a set with the manifest, `UNFILLED_SKELETONS`,
`MODEL_OF`, `SCORED_COLUMNS`); they are not counts or pins.

## Verdict

Code, schema, skeleton, edges and relations are correct and tested. One low
documentation defect: the schema and TypeSpec description say both links are
`references` edges, but the plan link is a `reviews` edge (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The `RiskManagementReview` TypeSpec doc comment and the emitted schema `description` say "The executed plan and the overall residual-risk evaluation are referenced through `references` edges", and the section comment says "The plan and the overall evaluation are `references` edges". The manifest, FR-109 and the skeleton use a `reviews` edge for the plan. Fix the wording in `typespec/main.tsp` and regenerate the schema. | typespec/main.tsp:734, typespec/main.tsp:741, spec_objects_safety/schemas/RiskManagementReview.json:41 |
