---
id: SR-412
title: "Code review — spec-objects-safety PLAT-1837 implementation and effectiveness verification edges"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, tests/conftest.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...3748247, PR #49)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-205", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-302", type: references }
---

## Summary

Ticket: PLAT-1837. PR spec-objects-safety#49, head `3748247`.

The PR replaces `control-has-verification` (edge `verifies`) with two
`when_any`-scoped advisory relations, `control-has-implementation-verification`
(edge `verifies_implementation`) and `control-has-effectiveness-verification`
(edge `verifies_effectiveness`). The two verbs are declared in this module's
`edge_types` and added to `PENDING_ISO_VERBS` in `tests/conftest.py`.

What ran (all measured by the reviewer):

- Environment: poetry venv with spec-artifacts-iso 0.25.0,
  spec-objects-security 0.12.1, quire wheel 0.62.2; `PYTHONPATH` and
  `--rootdir` set to the worktree, `-o addopts=""`.
- `tests_integration/test_risk_chain_edges.py` with the installed
  `quire 0.52.0 (engine 0.62.2)`: 63 passed, 3 failed. The 3 failures are the
  FR-010 tests (`soup_record` skeleton missing from spec-objects-security
  0.12.1) and fail identically on an `origin/main` worktree (61 passed,
  3 failed). All 18 control and verification tests pass, including the new
  `test_implementation_and_effectiveness_verification_are_not_interchangeable`
  and `test_the_shared_verifies_verb_satisfies_neither_verification_check`.
- The same 18 tests with `quire 0.52.1 (engine 0.62.2)` from npmjs (latest),
  installed into a scratch prefix via `QUIRE_BIN`: 18 passed.
- `tests/test_manifest.py` and `tests/test_cross_module_references.py`:
  21 passed. `black --check` and `ruff check` on the two changed test files: clean.
- Mutation probes on a scratch copy of the manifest: adding `verifies` to both
  relations fails the AC-9 test; adding `verifies_effectiveness` to the
  implementation relation fails the AC-1 shape test and the not-interchangeable
  test; giving the implementation relation the requirement's `check` token fails
  the AC-3 test. The new tests discriminate.

The PR body's claim that quire 0.52.0 "predates `where`/`when_any`" and that
26 finding tests fail on main is not reproduced: engine v0.62.2 already carries
`when_any` (quire-rs `src/corpus/required_relations.rs` at tag v0.62.2), and the
finding tests pass with it. The coder's failures came from its environment.

No compatibility layer for `control-has-verification` remains in the manifest
or the spec. `verifies` alone yields both verification findings (tested, and
the intended no-compat behaviour). No rule reads or assigns an
acceptability, pass/fail or effectiveness verdict.

## Verdict

Not mergeable. The relations and their tests work, but the two new verbs are
reported as `disallowed-edge-type` on every correctly authored verification
edge, because they exist only in this module's `edge_types` and no source
type allows them (FND-001). The conftest allowlist hides that from the
vocabulary tests under a comment that now misdescribes it (FND-002). One
assertion still names the removed token and can never fail (FND-003).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Every authored `verifies_implementation` or `verifies_effectiveness` edge from an `IT` or `TC` to a control draws `warning: ... edge type 'verifies_implementation' on 'IT-902' ... is not in the resolved allowed_links vocabulary [disallowed-edge-type]` (measured with quire 0.52.0, plain and `--strict`; a `verifies` edge in the same bundle draws none). The verbs are declared only in this module's `edge_types`; `IT`/`TC` (spec-artifacts-iso), retained-evidence records (engineering-assurance) and `control` (spec-objects-security) do not allow them. So the documented way to verify a control is flagged as a disallowed edge every time it is used. The FR-205-AC-2 test filters only `dangling-reference` and misses this. Fix: the verbs must be allowed on their source types in the owning module (spec-artifacts-iso vocabulary and `allowed_links`, plus the evidence-record type), and the FR-205-AC-2 test should assert no `disallowed-edge-type` for those edges. | spec_objects_safety/manifest.yaml:53-54, tests_integration/test_risk_chain_edges.py:347-373 |
| FND-002 | medium | `PENDING_ISO_VERBS` now holds `verifies_implementation` and `verifies_effectiveness`, under a comment saying these are verbs spec-artifacts-iso "has not declared yet" with "Expiry: when PLAT-1676 lands". PLAT-1676 (Backlog) covers only `estimates`, `assumes` and the `arises_from` inverse, so this expiry can never clear the new verbs, and FR-205 calls them "declared by this module", not pending in iso. The allowlist is what lets the FR-006-AC-4 vocabulary tests pass while FND-001 is live. The ticket-pinned expiry prose is tracking ceremony: delete it. Remove the two verbs from the set once FND-001 places them in the shared vocabulary. The manifest comment above `edge_types` ("The three risk-judgement verbs ... (TC-063)") is also stale. | tests/conftest.py:61-74, spec_objects_safety/manifest.yaml:46-48 |
| FND-003 | medium | `test_each_missing_link_is_reported_once_by_its_own_check` still asserts `findings(result, "control-without-verification") == []`. That token no longer exists, so the assertion is always true. A regression that reports an implementation or effectiveness finding when only the requirement is missing would pass. Assert `IMPL_CHECK` and `EFF_CHECK` are empty instead. | tests_integration/test_risk_chain_edges.py:933 |
