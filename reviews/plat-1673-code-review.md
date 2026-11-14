---
id: SR-406
title: "Code review — spec-objects-safety PLAT-1673"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, tests/test_manifest.py, tests_integration/test_reverse_mitigates.py, tests/__init__.py; FR-009"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-009", type: references }
---

## Summary

Reviewed frozen PR #43 at `8206bd9f0211fd1b4d24afb5b8960b5d488807ad`, including the manifest constraint/version bump and the FR-009 test changes. The behavior assertions cover the requested target, wrong-kind, cross-repository, filtering, and severity cases; two changed acceptance assertions lack valid matrix bindings.

## Verdict

**FAIL** — FR-009-AC-9 and FR-009-AC-10 are untagged in the computed matrix, despite assertions being present.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | AC-9 is tagged as TC-104, which maps to AC-7; Quoin leaves AC-9 unbound and Quire reports the marker as a near miss. | tests_integration/test_reverse_mitigates.py:158; spec/tests.md:151,153 |
| FND-002 | high | The incoming `to: []` assertions have no FR-009-AC-10 binding; the matrix maps AC-10 to TC-107, but the assertions are in TC-010. | tests/test_manifest.py:189-226; spec/tests.md:94,154 |

## Review notes

- Manifest target kinds match FR-009-AC-1, and the module version increases from 0.3.0 to 0.4.0.
- Both incoming relations retain `to: []`; same-repository hazard and failure-mode targets, wrong-kind threat, loaded/unloaded cross-repository targets, non-safety quality attributes, strict warning severity, and severity promotion are asserted.
- `tests/__init__.py` is a local package marker; no duplicate fixture source or unrelated repository access was found.
- No applicable AssuranceProfile was found. Python code-review checks found no source implementation changes, stubs, weak behavioral assertions, or boundary-mock issues in the reviewed additions.
- `quoin matrix` reports 152 untagged criteria repository-wide; the two findings above are the untagged criteria in this review's FR-009 scope. No run evidence is recorded in the matrix.
