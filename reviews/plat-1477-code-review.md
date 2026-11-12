---
id: SR-018
title: "Code review of PLAT-1477 reverse mitigates rule (spec-objects-safety#32)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, tests/test_manifest.py, tests_integration/test_reverse_mitigates.py (git diff origin/main...1ea2900)"
review_set: subset
---
# Code review of PLAT-1477 reverse mitigates rule (spec-objects-safety#32)

## Summary

Ticket: PLAT-1477. PR `agent-ix/spec-objects-safety#32`, head `1ea2900`. The PR
adds one `required_relations` entry (`safety-nfr-has-mitigation-target`, `from:
NFR`, `where: {field: quality_attribute, values: [safety]}`, `edges:
[mitigates]`, `to: []`, `direction: outgoing`, `check: unjustified-safety-nfr`),
one unit test (TC-099), TC-010/TC-011 updates and three integration tests
(TC-100..TC-102) that drive the real `quire` CLI (quire 0.43.0, engine 0.58.0).

Evidence:

- Schema: the manifest validates with 0 errors against
  `schema/semantic/v1/module-manifest.schema.json` from filament-core-data
  `origin/main`, which is byte-identical to tag `semantic-schema-v0.6.0`.
  Negative controls (a `where` missing `values`, an empty `values` list, or an
  extra key) each give 1 error.
- Engine: quire engine 0.58.0 loads the manifest, and the rule fires.
- Tests: 13 passed (`tests/test_manifest.py` plus `tests_integration/test_reverse_mitigates.py`).
  `ruff` and `black --check` are clean on both changed files.
- Mutations of the manifest, each rerun against TC-010, TC-011 and TC-099..TC-102:
  removing the rule fails 5 tests; dropping `where` fails 3; `values:
  [security]` fails 4; `values: [safety, performance_efficiency]` fails 2;
  `edges: [traces_to]` fails 2; `direction: incoming` fails 2; `to: [hazard,
  failure_mode]` fails 2 (the cross-repo NFR becomes reported); a module
  `grammar_severity` promoting the check to `error` fails TC-100. Every
  mutation is killed.
- Real-iso cross-check, using the installed default `spec-artifacts-iso`
  v0.25.0 with this PR's module through `--module` (no install). A `safety` NFR
  with no edge is reported, and so is ` Safety ` (case-folded). An NFR with a
  `mitigates` edge to an in-bundle hazard is clean, and so is one with an edge
  to `ix://agent-ix/other-repo/HAZ-900`. A `performance_efficiency` NFR is
  clean. `--okf` exits 0. Under `--okf --strict` the finding stays a
  `warning:`. `--severity trace:unjustified-safety-nfr=error` promotes it.
- The module's own `spec/` holds no NFR. Validating it with this PR's manifest
  and every other installed module yields no `unjustified-safety-nfr` and no
  `undeclared-relation-vocabulary`.
- The coder's caveats were measured. A single-file `quire validate NFR.md`
  warns `disallowed-edge-type` and exits 0. Bundle `--okf` does not warn, but
  `--okf --strict` does, as a warning. A cross-repo `ix://` target satisfies
  `to: []` but not a constrained `to`.
- Vendoring: none. The fixtures are generated in `tmp_path` from the installed
  iso NFR skeleton and this module's hazard skeleton.
- `~/.ix/filament/registry.json` sha256 is unchanged before and after this
  review.

## Verdict

The rule is correct and validates against the schema. Every test assertion is
backed by a mutation that kills it. Two findings concern test fidelity, and
neither changes the rule. The coverage gap in FR-009-AC-5's `--strict` clause
is recorded under gap analysis (SR-020).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The integration harness loads `spec-artifacts-iso` 0.22.0 (the dev dependency), which under quire engine 0.58.0 registers no archetypes: every fixture NFR is `unknown type 'NFR' tolerated under OKF posture`. The tests therefore never exercise the real NFR archetype (frontmatter schema, `allowed_links`). Under the installed iso v0.25.0, the fixture's bare `HAZ-001` target is a frontmatter error (`does not match "^ix://"`). The finding outcomes for AC-2..AC-4 match under v0.25.0, so the behaviour evidence holds, but the fixture is not the `NFR` FR-009's Inputs name. | tests_integration/test_reverse_mitigates.py:44-80, pyproject.toml:40 |
| FND-002 | low | TC-011 widens its check to `declared \| {"NFR"}`, a hard-coded exemption. It should resolve `from` against the archetypes the iso manifest declares (the test already reads that manifest for the edge vocabulary), so that a misspelt foreign kind still fails. | tests/test_manifest.py:272-273 |

## Finding detail

- FND-001: reproduce with `quire validate --okf --module <venv>/spec_artifacts_iso <dir holding the iso FR skeleton>`: the output includes `unknown type 'FR' tolerated under OKF posture`. Copying the installed v0.25.0 module into a directory named `spec_artifacts_iso` gives no unknown-type, so the cause is the module content, not the path. Fix: depend on an iso release that registers its archetypes under engine 0.58 (internal PyPI shows 0.22.0 as latest, so the iso release is the blocker), and author fixture targets as `ix://` ids.
- FND-002: replace the literal with the `name` set of the iso manifest's `artifact_types`.

## Not findings

- `to: []` versus a constrained `to`: the trade-off is deliberate and was measured. See SR-019 FND-004 for the spec-side consequence.
- `disallowed-edge-type` on NFR `mitigates`: real, an iso `allowed_links` gap owned by spec-artifacts-iso, as the ticket's own caveat says.
