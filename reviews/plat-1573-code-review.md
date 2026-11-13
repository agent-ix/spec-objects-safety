---
id: SR-063
title: "Code review of PLAT-1573 control completeness relations scoped by when_any (spec-objects-safety#41)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; pyproject.toml, poetry.lock, spec_objects_safety/manifest.yaml, tests/test_manifest.py, tests/test_risk_chain.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...5e7dd46)"
review_set: subset
---
# Code review of PLAT-1573 control completeness relations scoped by when_any (spec-objects-safety#41)

## Summary

Ticket: PLAT-1573. PR `agent-ix/spec-objects-safety#41`, head `5e7dd46`, five
commits. The PR raises `quire` to `^0.60.0` (pyproject and lock). It declares
`control-has-requirement` and `control-has-verification` in
`spec_objects_safety/manifest.yaml`, scoped by `when_any`. It rewrites the
FR-205-AC-6 guard to "no unscoped control relation", widens `test_tc011` to
accept `spec-objects-security` kinds and checks every `when_any` condition, and
adds five integration tests for FR-302-AC-1, 2, 3, 5, 6 and 7. There is no Rust
and no React, so rust-review and review-react do not apply.

Run evidence (quire CLI 0.45.0, engine 0.60.0, from a temp prefix via
`QUIRE_BIN`; quoin 0.30.1): through `locked-build.sh`, the focused selection
over `tests_integration/test_risk_chain_edges.py`, `tests/test_manifest.py` and
`tests/test_risk_chain.py` gave 20 passed. One unrelated test errored because
`@agent-ix/semantic-core` is not installed in the worktree (environment only).
A scratchpad probe ran two manifest mutations against fixtures built with the
PR's own helpers:

- `other: [hazard, failure_mode]` changed to `other: [hazard]`: a control that
  mitigates only a `failure_mode` and has no links gives 1 and 1 findings with
  the real manifest, and 0 and 0 with the mutant.
- `to: []` on `control-has-verification` changed to `to: [IT, TC]`: a control
  verified only by an `NFR` gives 0 findings with the real manifest and 1
  `control-without-verification` with the mutant.

No test in the suite builds either fixture, so both mutants pass every test.

## Verdict

Changes requested, medium only. The manifest matches FR-302 field for field:
both relations are `from: control`, scoped by exactly the FR-302 `when_any`
(`mitigates` outgoing to `hazard`/`failure_mode`, `assumes` incoming from
`risk_estimate`), `direction: incoming`, with `edges: [satisfies]`,
`to: [FR, NFR]` and `edges: [verifies]`, `to: []`. Each relation and each check
token is declared once (`test_risk_chain.py:190` asserts check uniqueness).

The new tests are behavioural and can fail. The AC-3 test removes one edge at a
time and expects exactly one finding of that check and none of the other. The
AC-5 test expects one finding per check naming `CTRL-001` for a control that is
only assumed by a post-control estimate. The AC-6 test is the negative of the
same fixture, and it would fail if the scope were dropped. The `test_tc011`
change does not weaken it: it adds the security module's kinds (needed for
`from: control`), asserts `control` is among them, and adds checks on every
`when_any` verb and `other` kind. The FR-205-AC-3 tag on the AC-6 test is true;
it duplicates the existing FR-205-AC-3 test at line 783. Nothing computes or
stores a score, region or acceptance. There is no pin, hash, file-count or
inventory test, no `mappings.yaml`, no vendored schema, no paywalled standard
text and no roadmap.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The test tagged FR-302-AC-1 checks only that validation exits 0 and reports no finding. It never asserts the declared fields. The `failure_mode` half of the `when_any` scope and `to: []` on `control-has-verification` are untested: mutating either passes every test (probe in Summary). | tests_integration/test_risk_chain_edges.py:830-838, spec_objects_safety/manifest.yaml:670-687 |
| FND-002 | medium | The test tagged FR-302-AC-7 writes the failing result as body prose (`Result: failed.`), which no relation could read. It does not assert the second clause, "no module key records the result". | tests_integration/test_risk_chain_edges.py:880-892 |

## Finding detail

- FND-001: add a unit assertion that each relation equals the FR-302 shape
  (`from`, `when_any`, `edges`, `to`, `direction`, `check`). Add one
  integration case each for a control that mitigates only a `failure_mode`
  and for a control verified only by a non-test document (for example an
  `NFR`). Both cases are FR-302 Behavior, testable today.
- FND-002: record the failure in a frontmatter field such as
  `status: failed`, which is the `status`-derived value FR-302 Behavior names.
  In the same test, assert that neither relation and no declared type has a
  `result`, `status`, `passed`, `verified` or `effective` key.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | low | `test_a_verifies_edge_from_a_non_test_document_counts_as_verification` is tagged FR-302-AC-2. AC-2 is about a control "verified by a test document", but this test uses an `NFR` verifier. It actually backs the empty `to:` that FR-302 Behavior requires, one of "the fields above" in FR-302-AC-1. Retag it FR-302-AC-1. | tests_integration/test_risk_chain_edges.py:885-893 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, b29e139. `test_the_control_relations_declare_the_specified_shape_and_scope` asserts the exact relation names, `edges`, `to`, `direction`, `check` and `when_any` (equal to the FR-302 scope) for both relations. A failure-mode-only fixture and an `NFR`-verifier fixture were added. The reviewer re-ran both mutants against a copy of b29e139 and both are now killed. `other: [hazard]` fails the shape test and the failure-mode test. `to: [IT, TC]` fails the shape test and the non-test-verifier test. |
| FND-002 | fixed | Round 1, b29e139. TC-901 now carries `status: failed` in frontmatter, and the test asserts it landed there. The test then walks the manifest and asserts that no key, and no `field`/`fields` selector value, is `status`, `result`, `passed`, `verified` or `effective`. The TC skeleton has no `status` field, but quire 0.45.0 accepts the extra key: the reviewer's probe shows no diagnostic for TC-901 or `status`, with or without `--strict`. That is acceptable, because a frontmatter `status` is exactly the `status`-derived value FR-302 Behavior says the relations must not read, so it is the right adversarial input. |
