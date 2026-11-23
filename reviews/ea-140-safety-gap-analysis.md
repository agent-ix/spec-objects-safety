---
id: SR-421
title: "Gap analysis — spec-objects-safety EA-140 risk_management_review (FR-109)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; FR-109-AC-1..AC-8 and the FR-109 Behavior statements against spec_objects_safety/manifest.yaml, schemas/RiskManagementReview.json, skeletons/risk_management_review.md and tests (git diff origin/main...b5b402c, PR #51)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-109", type: references }
---

## Summary

Ticket: EA-140 (part 1). Plan completion: not assessed (planless audit).

Matrix: `quire matrix --scope . --format json` lists FR-109 with 8 criteria,
every one `tagged`:

| AC | Binder |
| --- | --- |
| FR-109-AC-1 | tests/test_risk_management_review.py `test_the_review_type_is_declared_with_its_row_and_allowed_references` |
| FR-109-AC-2 | tests/test_risk_management_review.py `test_the_filled_skeleton_validates_and_the_shipped_skeleton_fails` |
| FR-109-AC-3 | tests/test_risk_management_review.py `test_a_placeholder_in_any_cell_fails_naming_the_table_and_column` (all four cells) |
| FR-109-AC-4 | tests/test_risk_management_review.py `test_a_value_outside_the_closed_set_fails_naming_the_column` |
| FR-109-AC-5 | tests_integration/test_risk_chain_edges.py `test_a_review_missing_its_plan_or_evaluation_is_reported_until_the_edge_is_added` |
| FR-109-AC-6 | tests_integration/test_risk_chain_edges.py `test_a_review_reference_to_a_hazard_is_disallowed_naming_hazard` |
| FR-109-AC-7 | tests/test_risk_management_review.py `test_the_review_declares_no_score_class_acceptability_or_approval` |
| FR-109-AC-8 | tests_integration/test_risk_chain_edges.py `test_the_tooling_does_not_judge_a_review_against_the_evaluation_it_references` |

Each binding was read and is correct. Each AC can fail (mutation measured on a
scratch worktree): Reviewer or Statement pattern removed (AC-3 and the
negative fixture), either relation removed (AC-5), either `column_choices`
entry removed (AC-4), a `score` schema property or an `Acceptability` column
added (AC-7, AC-1). All eight tests pass in the locked environment.

Reverse gap: every manifest addition (type block, export, two relations) is
owned by FR-109; the FR-104 Inputs line is the only other spec change. No
stubs, no skipped or xfail tests, no coverage-only tests.

Requirement-to-code gap: the Behavior statement "The type SHALL allow
`reviews` edges to `risk_management_plan` documents and `references` edges to
`overall_residual_risk_evaluation` documents, and no other edge or target
type" is only half implemented (FND-001).

## Verdict

All eight ACs are tagged, tested and able to fail. One medium gap: the spec
claims the type allows no other edge verb, but a review carrying an extra
`depends_on` edge validates with no diagnostic, and no AC tests that half.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-109 Behavior says the type allows `reviews` and `references` edges "and no other edge or target type". Measured: a review with `reviews`→RMP-001, `references`→ORE-001 and an extra `depends_on`→RMP-001 validates (exit 0) with no diagnostic naming RMR-001; `allowed_links` constrains only the verbs it lists. FR-109-AC-6 tests only a wrong target type (hazard), so nothing exercises the "no other edge" half. No sibling FR (FR-101..FR-108) makes this claim. Fix: narrow the statement to "and no other target type for these edges" (matching what the engine enforces), or add an AC and enforcement for unlisted verbs. | spec/functional/FR-109-risk-management-review.md:50, spec_objects_safety/manifest.yaml:690-692, tests_integration/test_risk_chain_edges.py:711 |
