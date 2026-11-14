---
id: SR-407
title: "Gap analysis — spec-objects-safety FR-009 change"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-009-safety-nfr-needs-mitigation-target.md, spec_objects_safety/manifest.yaml, tests/test_manifest.py, tests_integration/test_reverse_mitigates.py"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/SPEC-001", type: references }
---

## Summary

Checked FR-009 against the changed manifest and tests, with computed matrix and reverse-gap checks. The manifest implements the constrained relation, but the matrix does not bind the tests for AC-9 or AC-10.

## Verdict

**FAIL** — two in-scope FR-009 criteria are untagged in the computed Test Matrix.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | AC-9 is tagged as TC-104, which maps to AC-7; Quoin leaves AC-9 unbound and Quire reports the marker as a near miss. | FR-009-AC-9, tests_integration/test_reverse_mitigates.py::test_cross_repository_target_counts_only_when_its_repository_is_loaded |
| FND-002 | high | The incoming `to: []` assertions have no FR-009-AC-10 binding; the matrix maps AC-10 to TC-107, but the assertions are in TC-010. | FR-009-AC-10, tests/test_manifest.py::test_tc010_hazard_coverage_is_declared_not_coded |

## Coverage

- Reconciliation: `quoin matrix --repo . --json` (quoin 0.30.1; Quire 0.45.0, engine 0.60.0).
- FR-009: AC-1 through AC-8 tagged; AC-9 and AC-10 untagged. Quoin reported 152 untagged criteria across the full repository; the other 150 are outside this ticket's instructed review scope.
- Evidence: no run evidence is recorded for the computed matrix. The focused test command passed independently.
- Untraced behaviors / stubs in reviewed changes: 0.
- Plan completion: not assessed
- Semantic review: skipped (optional method not requested).

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Commit `26538d1` separates the loaded-target TC-104 test from a new unloaded-target test tagged TC-106 / FR-009-AC-9. |
| FND-002 | fixed | Commit `26538d1` adds a dedicated TC-107 / FR-009-AC-10 test for both incoming relations. |
| FND-003 | fixed | Commit `e94369b` changes the three TestMatrix headers in `spec/tests.md` to the declared `Status` column. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | high | Quire rejects the TestMatrix tables because their headers say `Coverage Status` while the declared column is `Status`; the changed FR-009 summary status is in the invalid table. | spec/tests.md:52,58,64 |
