---
id: SR-016
title: "Gap analysis of PLAT-1408 mitigates-edge tests against FR-007 and FR-008 (spec-objects-safety#31)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-007, spec/functional/FR-008, spec/tests.md, tests/test_mitigates_edge.py (git diff origin/main...a5135f1)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-007"
    type: reviews
  - target: "ix://agent-ix/spec-objects-safety/FR-008"
    type: reviews
---
# Gap analysis of PLAT-1408 mitigates-edge tests against FR-007 and FR-008 (spec-objects-safety#31)

## Summary

Ticket: PLAT-1408. Planless. Plan completion: not assessed. The scope is the
merged FR-007 (AC-1..4) and FR-008 (AC-1..5) and the PR's tests, TC-093..TC-098.

## Coverage

- `quoin matrix --repo . --json` (quoin 0.30.1): all 9 criteria are
  `static_status: tagged`, with binders in `tests/test_mitigates_edge.py`.
  Evidence status is "no run evidence", because no report was bound.
- Run census, focused: 6 passed with quire-cli#168 (built against quire-rs#647),
  spec-objects-security#40 and `PYTHONPATH=.`.
- Discrimination: with spec-objects-security `origin/main`, which lacks the
  widening, TC-093 fails as it should. TC-096..TC-098 still pass there; they do
  not depend on the widening.
- Unowned code: none. The diff adds test code only.

## Verdict

The criteria are covered, with one inflation risk. TC-093 is the only test that
guards the FR-007 widening, and it reports success when the safety types never
load (FND-001). The matrix document also now contradicts itself: the coverage
table says FR-007 and FR-008 are covered, while the Coverage Gaps prose and
TM-001's frontmatter still describe them as open or leave them out (FND-002,
FND-003).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-093 (FR-007-AC-1/2) only asserts that `disallowed-edge-target` and `DisallowedEdgeType` are absent. When the safety module's types do not load, quire tolerates `hazard` and `failure_mode` as `[unknown-type]`, emits no edge-target check, and the test passes. Reproduced: with an editable install pointing at a stale checkout, `tests.conftest.PACKAGE_ROOT` resolved to `/home/peter/dev/spec-objects-safety`, and all six tests passed against security `main` with no widening. The test never asserts that the types loaded or that the incoming edge resolved, the second of which is FR-007's stated Output. | tests/test_mitigates_edge.py:99-104, FR-007-AC-1, FR-007-AC-2 |
| FND-002 | low | `spec/tests.md` Coverage Gaps item 1 still says the incoming `mitigates` edge "is authorable nowhere" and that FR-007/FR-008 "rows stay open until their tests exist". In the same document, this PR flips both rows to ✅. | spec/tests.md:169-182 |
| FND-003 | low | TM-001's frontmatter `covers` relationships list FR-001..FR-006 but not FR-007 or FR-008, although the coverage table now claims both covered. | spec/tests.md:1-22 |

## Finding detail

- FND-001: add `assert "[unknown-type]" not in result.stderr`. Also assert the
  edge resolved, for example that there is no `unmitigated-hazard` or
  `unmitigated-failure-mode` finding for HAZ-001 or FM-001.
- FND-002: rewrite or remove item 1 and the "three recorded exceptions" count.
- FND-003: add `covers` entries for FR-007 and FR-008.

## Not findings

- FR-007-AC-3 tests the bare-id case only; that is all the AC requires.
- FR-008 tests split the "two hazards + two failure modes + one control" corpus
  into separate fixtures; AC-1 and AC-2 name separate fixtures, so that is in scope.
- `spec/tests.md` structural-validation column-header errors predate this diff.

## New findings (disposition pass 2)

Scope of this pass: head 6198eae. The tests now run through the installed
`spec-objects-security` 0.12.1 (released FR-007, read from tag v0.12.1:
`control.allowed_links.mitigates` lists exactly threat, risk, vulnerability,
hazard and failure_mode). `quoin matrix`: FR-007-AC-1..4, FR-008-AC-1..5 and
FR-002-CON-4 are all `tagged`, with binders in
`tests_integration/test_mitigates_edge.py` and `tests/test_schema_emission.py`.
Run census: the six tests pass with no override set, `make test` passes (56
tests), and `make test-integrations` gives 6 passed and 1 failed. The failure is
TC-070, `test_quoin_install_roundtrip`, which this PR does not cause: it fails
identically on a detached `origin/main` (7e26017) worktree, at SC-01. quoin
0.30.x lists its ten pinned default modules, `spec-objects-safety` v0.8.0
among them, even under an empty `IX_CONFIG_ROOT`. `~/.ix/filament/registry.json`
had sha256 93841a76… before and after every run.

Discrimination (mutants run against the real engine): every FR-007/FR-008 test
is killed by at least one relevant mutant. Removing the edges kills
TC-093..TC-097; retyping the targets kills TC-093; narrowing the security
manifest kills TC-093; dropping the flags kills TC-094 and TC-098. One
inflation path remains (FND-004).

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | TC-093 (FR-007-AC-1/2) still asserts only that some strings are absent from stderr, never `result.returncode == 0`. If `quire validate` stops before it validates anything (a module load error, a rejected flag, a crash), stderr carries none of the strings the test checks for and the test passes. Reproduced: with the safety `--module` path unloadable, quire exits 3 with only `validating --module '...': No such file or directory` on stderr, and TC-093 passed while the five other tests failed. Run on its own, TC-093 is then green evidence for FR-007 from a run that validated nothing. | tests_integration/test_mitigates_edge.py:98-108 |

## Finding detail (disposition pass 2)

- FND-004: add `assert result.returncode == 0, result.stderr`. The baseline
  fixture exits 0 today, with warnings only.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | TC-093 now asserts no `[unknown-type]` and no unmitigated-hazard or unmitigated-failure-mode finding. Its paths come from `__file__`, so the stale editable-install import no longer applies. Against security origin/main it now fails both with and without PYTHONPATH=. |
| FND-002 | fixed | The Coverage Gaps section drops item 1, now counts two exceptions, and says TC-093..TC-098 are covered in tests_integration/. |
| FND-003 | fixed | TM-001 frontmatter now carries covers edges to FR-007 and FR-008. |
| FND-004 | still-open | Found in disposition pass 2. No fix has landed yet: TC-093 still does not assert `returncode == 0`. |
