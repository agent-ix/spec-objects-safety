---
id: SR-417
title: "Gap analysis — spec-objects-safety PLAT-1834 risk_management_plan (FR-108)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; FR-108-AC-1..AC-6 against spec_objects_safety/manifest.yaml, schemas/RiskManagementPlan.json, skeletons/risk_management_plan.md and tests (git diff origin/main...dbd860e, PR #50)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-108", type: references }
---

## Summary

Ticket: PLAT-1834. Plan completion: not assessed (planless).

`quire matrix --scope .` (quire 0.52.0, engine 0.62.2, ambient module
discovery) lists all six FR-108 criteria. Tests were run as recorded in
SR-416; mutation probes are recorded there.

| Criterion | Tagged test | State |
| --- | --- | --- |
| FR-108-AC-1 | `test_the_plan_type_is_declared_and_requires_its_four_tables` | tagged, backed (making `scope` optional fails it) |
| FR-108-AC-2 | `test_the_filled_skeleton_validates_and_the_shipped_skeleton_fails` | tagged, backed |
| FR-108-AC-3 | `test_a_placeholder_row_in_any_table_fails_naming_the_table` | tagged, partly backed: two second-column guards unprotected (SR-416 FND-001) |
| FR-108-AC-4 | `test_a_plan_with_no_acceptability_policy_is_reported_once_and_the_edge_clears_it` | tagged, backed (dropping the relation fails it) |
| FR-108-AC-5 | `test_a_plan_reference_to_a_hazard_is_disallowed_naming_hazard` | tagged, backed (allowing `hazard` fails it) |
| FR-108-AC-6 | `test_the_plan_declares_no_score_class_acceptability_or_approval` | `method-without-symbol` (Inspection); the test covers only the schema half (FND-001) |

Reverse gap: every added file (manifest block, schema, typespec model,
skeleton, fixture, tests) belongs to FR-108; no unowned code. No stub or
placeholder implementation; the skeleton placeholders are the specified
behaviour. Reviewer inspection of the package: the skeleton is the only
`risk_management_plan` document, and neither it nor the schema declares a
score, class, acceptability or approval member, so AC-6 holds today.

## Verdict

Every criterion is tagged and five are backed by tests that fail when the
behaviour is removed. AC-3 is partly backed (SR-416 FND-001). AC-6 holds by
inspection, but its tagged test checks only the schema.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The test tagged FR-108-AC-6 checks only the JSON schema's top-level property names. The skeleton half ("the skeleton declares no score, class, acceptability or approval property") and the "package contains no `risk_management_plan` document other than the unfilled skeleton" half are not checked: adding a `score` locator to the plan's `body_extraction` passes every test (mutation measured). Either extend the test to the plan's locator names, skeleton table headers and the package's documents of this type, or tag it to the schema half only and leave the rest to inspection. | tests/test_risk_management_plan.py:99-109, spec/functional/FR-108-risk-management-plan.md:60 |
