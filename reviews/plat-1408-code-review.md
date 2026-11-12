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

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | `poetry.lock` resolves `spec-objects-security` 0.1.1, which lacks the #40 widening. With no `SPEC_OBJECTS_SECURITY_MODULE` set, `make test-integrations` fails TC-093 until a security release that includes #40 is published and the lock is bumped. | poetry.lock, pyproject.toml, TC-093 |

## New findings (disposition pass 2)

Scope of this pass: `git diff origin/main...6198eae`, adding c905fee
(spec-objects-security ^0.12.1), 9e72ea7 (quire ^0.58.0) and 6198eae
(semantic-core 0.4.4, tagged `KernelScalar` targets, `kernel_scalars()` read
from the installed package, npmjs-only lockfile test, FR-002/TC-024 text).

Run evidence, against the installed packages with `SPEC_OBJECTS_SECURITY_MODULE`,
`SPEC_ARTIFACTS_ISO_MODULE` and `QUIRE_BIN` unset: `_module` resolved
`spec_objects_security` 0.12.1 and `spec_artifacts_iso` from site-packages, and
the CLI was the ambient `quire 0.42.0 (engine 0.58.0)`. The six mitigates tests
passed. `make lint` passed (ruff, black, and `schemas-check`: 15 schemas match),
and `make test` gave 56 passed at 100% coverage. Both ran in a scratch worktree
of 6198eae, with semantic-core 0.4.4 bytes from filament-core-data `ce72bc51`
(byte-identical to the 0.4.4 release commit 5a665fc5) and the @typespec 1.15.0
toolchain from that checkout's node_modules. No registry command was run.

Mutation check against the real engine: dropping the `mitigates` edges, or
changing the verb to `protects`, kills TC-093..TC-097. Retyping the hazard and
failure-mode fixtures as `asset` kills TC-093, TC-096, TC-097 and TC-098.
Narrowing the security manifest to `[threat, risk, vulnerability]` kills TC-093.
Ignoring `--strict` and `--severity` kills TC-094 and TC-098.

semantic-core 0.4.4: the change matches spec-objects-security#42. `FieldDecl`
targets use the `KernelScalar` arm of `TypeRefTarget`, `{kind, value}`.
`RelationDecl.target` stays a plain `SemanticId`, so `ix://...`, as in the
0.4.4 schema. The regenerated schemas change only the `$ref` base from 0.3.2 to
0.4.4. `poetry.lock` changes only the `quire` and `spec-objects-security`
entries and the content hash. `package-lock.json` changes only semantic-core.
The lockfile test is not vacuous: it covers 75 `resolved` entries, and the
GitHub Packages URL on `main` would fail it. No `GitHub Packages` or
`npm.pkg.github` text remains outside `reviews/`.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | low | Now that `spec-objects-security` ^0.12.1 is a declared dev dependency, the `SPEC_OBJECTS_SECURITY_MODULE` and `SPEC_ARTIFACTS_ISO_MODULE` overrides add no value. `_module` still reads them before the installed package, so a stale variable left in a shell silently points the FR-007/FR-008 evidence at an unreleased checkout and the run still reports green. The module docstring still describes that route. Delete both overrides and read the installed packages only. | tests_integration/test_mitigates_edge.py:1-8, tests_integration/test_mitigates_edge.py:26-37 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | aa961f8 reformats the file. `ruff check .` and `black --check .` report nothing in it. The one remaining E501, at tests/conftest.py:105, is on origin/main unchanged, and this PR does not touch that file. |
| FND-002 | fixed | aa961f8 moves the tests to tests_integration/test_mitigates_edge.py with `pytestmark = pytest.mark.integration`. The unit suite no longer collects them, and spec-objects-security is now a dev dependency from internal-pypi. |
| FND-003 | fixed | `_module` now reads the env var before calling `find_spec`. |
| FND-004 | fixed | TC-098 now asserts exactly one hazard finding, not prefixed `warning:` (quire prints errors with no prefix; verified, exit 3), and exactly one failure-mode `warning:`. |
| FND-005 | fixed | c905fee declares `spec-objects-security = {version = "^0.12.1", source = "internal-pypi"}`, and poetry.lock now resolves 0.12.1. Its manifest lists `mitigates: [threat, risk, vulnerability, hazard, failure_mode]`. The six tests pass with no override set. |
| FND-006 | still-open | Found in disposition pass 2. No fix has landed yet: the env-var overrides are still read before the installed package. |
