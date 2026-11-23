---
id: SR-409
title: "Code review — spec-objects-safety FR-010 hazard causes"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, tests/test_cross_module_references.py, tests_integration/test_risk_chain_edges.py"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-010", type: references }
---

## Summary

Ticket: PLAT-1833. PR agent-ix/spec-objects-safety#48 at 1d7b38a, diff `origin/main...HEAD`. The manifest change is two list edits: `hazard.arises_from` gains `soup_record`, `threat`, `vulnerability`, `control`, and `failure_mode.references` gains the `systems-part` role. Focused tests pass against `origin/main` checkouts of spec-objects-security, spec-artifacts-iso and spec-objects-architecture (20 unit, 1 integration). Reverting `arises_from` to `[failure_mode]` makes TC-113 fail, so the integration test can fail.

## Verdict

**CONDITIONAL** — the manifest change is correct and minimal. No compat layer, pin, SHA, score or acceptability key is added. `systems-part` is a sound target: a reviewer probe with spec-objects-architecture loaded validated a `failure_mode` `references` edge to a real `part` document with no edge diagnostic, and a dangling target was still reported. Plain `part` behaves identically; the UnknownRole the coder saw comes from not loading spec-objects-architecture, not from `part` being wrong. Two low findings in the new test code remain.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | TC-113 re-implements the existing `validate()` command inline and hand-rolls its assertions instead of `clean_of_edge_errors(validate(tmp_path))`, dropping that helper's `returncode == 0` and `[unknown-type]` checks; the third assertion (substring `HAZ-001.md` in joined lines containing `edge`) is opaque. | tests_integration/test_risk_chain_edges.py:978-1016 |
| FND-002 | low | Formatting-only rewrap of an unrelated FR-103 assertion is mixed into the PR. | tests_integration/test_risk_chain_edges.py:467-472 |

## Coverage

- Focused tests: `tests/test_cross_module_references.py`, `tests/test_manifest.py` (20 passed), `tests_integration/test_risk_chain_edges.py -k each_cause` (1 passed), `-o addopts=""`, quire 0.52.0 (engine 0.62.2).
- Mutation probes: `arises_from: [failure_mode]` fails TC-113; `references: [..., part]` and `[..., systems-part]` both validate a failure_mode to part edge when spec-objects-architecture is loaded.
