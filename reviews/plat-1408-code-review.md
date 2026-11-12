---
id: SR-015
title: "Code review of PLAT-1408 mitigates-edge tests (spec-objects-safety#31)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; tests/test_mitigates_edge.py, spec/tests.md (git diff origin/main...a5135f1)"
review_set: subset
---
# Code review of PLAT-1408 mitigates-edge tests (spec-objects-safety#31)

## Summary

Ticket: PLAT-1408. PR `agent-ix/spec-objects-safety#31`, head `a5135f1`, diff
`origin/main...HEAD`: one new test module (`tests/test_mitigates_edge.py`, six
tests TC-093..TC-098) and the matching `spec/tests.md` rows. No manifest change.

Run evidence, focused only. `quire-cli#168` (head `8a68460`) was built against
`quire-rs#647` (head `96d1ddf`) through a cargo `[patch]`, and the six tests
ran with that binary as `QUIRE_BIN`, `spec-objects-security#40` (head
`75e7e48`) as `SPEC_OBJECTS_SECURITY_MODULE`, and `PYTHONPATH=.`: 6 passed.
Negative control with `spec-objects-security` `origin/main` (no widening):
TC-093 fails with two `disallowed-edge-target` diagnostics, the rest pass.
With the installed `quire 0.40.0`, TC-094 fails (`--strict` exits 0), as the
author reported.

Golden path and mock boundaries: there are no mocks. The tests drive the real
`quire` CLI over fixture bundles built at runtime from this module's skeletons
and the `spec-objects-security` control and asset skeletons. Nothing is copied
into the repo.

Dependency design. The author's choice that a missing `quire`, security module
or iso module fails the test instead of skipping it matches this repository's
own policy. `tests/conftest.py` says "they never skip, because a skipped row is
not coverage", and TC-057's scan bans skips. Reading the other modules from an
installed package or a checkout named by an environment variable is the route
FR-007's Dependencies section names ("from its own checkout or git
dependency"). It is not vendoring or copying. The defect is elsewhere: the
tests sit in the default `make test` suite but neither the security module nor
the CLI is a declared or pinned dependency (FND-002).

## Verdict

Changes requested. The tests are correct against the full upstream stack, and
all nine FR-007/FR-008 criteria are tagged. Two problems still block the merge.
`make lint` is red (FND-001). The tests sit in the unit suite but depend on
tooling that is neither declared nor released, so `make test` on `main` goes
red at merge time (FND-002). Two low findings concern test robustness.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `make lint` fails on the new file: ruff E501 (93 > 88) and `black --check` "would reformat". | tests/test_mitigates_edge.py:156 |
| FND-002 | medium | The six tests run in the default `tests/` suite (`make test`) but depend on a `quire` CLI binary that is not pinned and must contain the unreleased quire-cli#168 and quire-rs#647 for TC-094. They also need `spec_objects_security`, which is not a declared dependency in `pyproject.toml`, while `spec-artifacts-iso` is. A clean `poetry install && make test` therefore fails all six tests. Merging before security#40, quire-cli#168 and quire-rs#647 are released leaves `main` red. The `pyproject.toml` testpaths comment sends ambient-CLI rows to `tests_integration/`. | tests/test_mitigates_edge.py:27-40, pyproject.toml |
| FND-003 | low | `_module` checks `find_spec` before the env var, so an installed package always wins. `SPEC_ARTIFACTS_ISO_MODULE` is dead code (iso is an installed dev dependency), and once security is installed `SPEC_OBJECTS_SECURITY_MODULE` can no longer point the test at a checkout such as security#40. | tests/test_mitigates_edge.py:27-34 |
| FND-004 | low | TC-098 asserts that no hazard finding is a `warning:` and that the exit code is non-zero. It never asserts that a hazard finding is reported as an `error:`, so the test still passes if the hazard findings disappear while some other error sets the exit code. | tests/test_mitigates_edge.py:151-160 |

## Finding detail

- FND-001: `ruff check tests/test_mitigates_edge.py` reports E501 at 156:89, and
  `black --check` would reformat the file. `make lint` runs both.
- FND-002: `ls $VENV/bin | grep quire` is empty; the quire wheel ships no CLI,
  so the test falls back to `shutil.which("quire")`, the globally installed npm
  binary (0.40.0 here), which fails TC-094. Remedies: declare
  `spec-objects-security` as a dev dependency (internal-pypi or git), and either
  pin the CLI once #168 is released (for example an `@agent-ix/quire`
  devDependency in `package.json`) or move the module to `tests_integration/`
  as the repository's own convention says. Land it after the three upstream PRs.
- FND-003: invert the order: env var first, then `find_spec`.
- FND-004: add `assert any(l.startswith("error:") for l in _findings(result, "unmitigated-hazard"))`.

## Not findings

- Fail-not-skip on missing tooling is the repo's own policy, not a defect.
- No vendoring: fixtures are generated in `tmp_path` from authoritative skeletons.
- Trace tags: all nine FR-007/FR-008 criteria are bound (`quoin matrix`), and every binding reads correctly against its AC.
