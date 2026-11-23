---
id: SR-416
title: "Code review — spec-objects-safety PLAT-1834 risk_management_plan object type"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, spec_objects_safety/schemas/RiskManagementPlan.json, spec_objects_safety/skeletons/risk_management_plan.md, typespec/main.tsp, tests/conftest.py, tests/test_risk_management_plan.py, tests/test_skeletons_semantic.py, tests/fixtures/negative/risk_management_plan-empty-responsibility.md, tests_integration/test_risk_chain_edges.py (git diff origin/main...dbd860e, PR #50)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-108", type: references }
---

## Summary

Ticket: PLAT-1834. PR spec-objects-safety#50, head `dbd860e`, base
`origin/main` `9722bc6` (merge base equals current main; GitHub reports
MERGEABLE).

The PR adds the `risk_management_plan` object type: four required
person-entered tables (Scope; Responsibility | Assigned to; Method | Applies
to; Activity | Method), each with `min_rows: 1` and a non-placeholder
`column_patterns` on every column, `allowed_links: references:
[acceptability_policy]`, a `plan-references-acceptability-criteria` required
relation with check `plan-without-acceptability-criteria`, the emitted
`RiskManagementPlan.json`, a skeleton that fails as shipped, a negative
fixture, and the type's rows in the conftest registries. Manifest hunks are
additive (one object-type block, one export, one relation, the description
string).

What ran (all measured by the reviewer):

- Environment: in-project poetry venv from the lock (quire wheel 0.62.2,
  spec-artifacts-iso git dependency on main at `9342304`, which is current iso
  `main` HEAD, spec-objects-security 0.12.1); `--rootdir .`, `-o addopts=""`.
  CLI `quire 0.52.0 (engine 0.62.2)`.
- Unit: `test_risk_management_plan.py`, `test_skeletons_semantic.py`,
  `test_manifest_semantic.py`, `test_manifest.py`, `test_schema_emission.py`,
  `test_risk_chain.py`, `test_cross_module_references.py`: 111 passed.
- `node scripts/generate-schemas.mjs --check` after `npm ci`: 38 schemas
  match. `ruff check` and `black --check` on tests: clean.
- `tests_integration/test_risk_chain_edges.py`: 68 passed, 3 failed on the PR;
  66 passed, the same 3 failed on an `origin/main` worktree. The 3 are
  `test_a_hazard_may_arise_from_each_cause_type`,
  `test_a_failure_mode_may_reference_a_part` and
  `test_a_failure_mode_reference_to_an_undeclared_part_is_dangling`
  (spec-objects-security 0.12.1 ships no `soup_record` skeleton;
  spec-objects-architecture is not installed). None is caused by this PR; both
  new plan tests pass. The PR body's "10 / 39 failing" counts are from the
  coder's environment and were not reproduced.
- Vocabulary: `references` is declared in spec-artifacts-iso main
  `edge_types` ("Loose, untyped linkage"). `acceptability_policy` is this
  module's own type (FR-101), so the bare name follows how the manifest names
  local targets, and `residual_risk` already uses the same
  `references: [acceptability_policy]` edge. A bundle (policy, hazard, plan
  with edge, plan without, plan to hazard) under `quire validate --okf` with
  iso main, security (0.12.1 and origin/main) and this module: no
  `UnknownEdgeType`, no `disallowed-edge-type`; the only `disallowed-edge-target`
  is the deliberate plan-to-hazard edge.
- Mutation probes on a scratch copy of the manifest: dropping the `Scope`
  pattern, the `Assigned to` pattern, `required` on scope, the relation, or
  adding `hazard` to `allowed_links` each fails a test. Dropping the
  `Applies to` pattern or the production table's `Method` pattern fails none
  (FND-001).

The schema carries only `fields`, `evidence`, `relations`, `clauses` and is
sealed (`additionalProperties: false`, `unevaluatedProperties: not {}`); no
score, class, acceptability or approval member. No ISO 14971 text appears in
the diff. The conftest edits add the type to the parametrising registries
(`OBJECT_TYPES`, `UNFILLED_SKELETONS`, `MODEL_OF`, `SCORED_COLUMNS`); they are
not counts or pins. The negative fixture fails for its own reason (an empty
`Assigned to` cell) and is the only test that kills the `Assigned to`
mutation.

## Verdict

Not mergeable as is, one small fix. Implementation, schema, skeleton and the
edge and relation are correct and tested, but the AC-3 test leaves only the
first cell of each table as a placeholder, so the placeholder guard on two
second columns is unprotected (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `test_a_placeholder_row_in_any_table_fails_naming_the_table` restores only the first-column placeholder of each table (`TABLES` maps each table to one placeholder). FR-108 says any empty or placeholder cell fails naming the table. Removing the `Applies to` pattern (control_verification) or the `Method` pattern (production_post_production) from the manifest passes every test in `tests/` and the plan integration tests (mutation measured). Fix: parametrise over every placeholder in `FILL` (all seven cells) with the table each belongs to, and assert the table name in the error. | tests/test_risk_management_plan.py:38-43, tests/test_risk_management_plan.py:88-95, spec_objects_safety/manifest.yaml:657, spec_objects_safety/manifest.yaml:669 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Fix commit a122426: the AC-3 test is parametrised over all seven placeholders in `CELLS` (table, column) and asserts `'<table>'` and `column '<column>'` in one error. Re-measured: dropping the `Applies to` pattern or the production `Method` pattern now fails a test. |
