---
id: SR-056
title: "Code review of PLAT-1410/1411/1558 risk-chain object types (spec-objects-safety#38)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; manifest.yaml, mappings.yaml, typespec/main.tsp, schemas/, skeletons/, tests/, tests_integration/test_risk_chain_edges.py, pyproject.toml, package.json, scripts/stage-npm.mjs (git diff origin/main...4a8d015)"
review_set: subset
---
# Code review of PLAT-1410/1411/1558 risk-chain object types (spec-objects-safety#38)

## Summary

Tickets: PLAT-1410, PLAT-1411, PLAT-1558. PR `agent-ix/spec-objects-safety#38`,
head `4a8d015`, one commit. The PR adds three object types (`harm`,
`hazardous_situation`, `risk_estimate`), their TypeSpec models and emitted
schemas, three skeletons, nine negative fixtures, `mappings.yaml`, a unit
module `tests/test_risk_chain.py` and an integration module
`tests_integration/test_risk_chain_edges.py`. There is no Rust, so rust-review
does not apply.

Run evidence, focused on the diff: `make lint` passes (ruff, black,
schemas-check: 22 schemas match). `pytest tests tests_integration/test_risk_chain_edges.py
tests_integration/test_mitigates_edge.py tests_integration/test_reverse_mitigates.py`
gives 139 passed with quire 0.44.0 (engine 0.59.1), after `npm ci` for
semantic-core.

Golden path: there are no mocks. Record tests use the real emitted schemas
through a `referencing` registry. Document tests run the shipped skeletons and
fixtures through the engine. Integration tests build bundles at runtime from
this module's skeletons and the installed `spec_objects_security` and
`spec_artifacts_iso` packages. Nothing is copied from another repository.

## Verdict

Changes requested on the test side. The schema and manifest work is sound.
`Harm`, `HazardousSituation`, `EstimateJudgement` and `RiskEstimate` are
sealed. No score, region, level, acceptable or acceptance key is stored, and
no member has a default. The `risk_estimate` skeleton fails as shipped and
names each missing value (FR-203-AC-7 test). The negative fixtures each fail
for their declared `expect` text. The coder's decisions hold:

- Nesting the judgement as `estimate` (`EstimateJudgement`) mirrors
  `Hazard.assessment`. The document-level requirement for each value is
  enforced by the manifest locators, and that is tested per value.
- `PENDING_ISO_VERBS` subtracts `estimates` and `assumes` from the two
  vocabulary tests. It copies no iso content. The integration tests read the
  installed iso package. See SR-057 for the missing ticket behind it.

Findings: one medium, three low. FND-001 has to change in this PR, because it
blocks the FR-204 relation SR-057 FND-002 asks for.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `test_no_check_compares_post_control_with_pre_control_values` asserts that the strings `post_control` and `pre_control` are absent from `traceability` and `lint_rules`. This checks text, not behaviour, and it contradicts FR-204, whose `post-control-assumes-control` relation must carry `where: {field: phase, values: [post_control]}`. The test fails as soon as that relation is declared. FR-204-AC-5 is already covered by the integration test `test_a_post_control_value_worse_than_the_pre_control_value_is_not_rejected`. | tests/test_risk_chain.py:317-323 |
| FND-002 | low | `assert len(skeletons) == 7` asserts a file count, not behaviour. The diff changes it from 4 to 7, so each new skeleton needs a test edit, and a missing skeleton is already caught by the per-type checks. | tests/test_skeletons_semantic.py:84 |
| FND-003 | low | `assert MODEL_OF == {...}` compares a test constant from conftest with a literal copy of itself. It can fail only when someone edits one copy and not the other. The diff extends it with the three new types. | tests/test_record_schemas.py:380-386 |
| FND-004 | low | `mappings.yaml` has no consumer. Nothing reads it: quoin FR-087-AC-9 excludes it from measurement, and the quoin template says an object-only module ships no mapping file. It restates the manifest `allowed_links` and locators, and its four tests only check that it agrees with them, which is a drift check on a duplicated fact. The PLAT-1558 ticket asks for it. Either name a consumer or drop the file and its tests. | spec_objects_safety/mappings.yaml:1-55, tests/test_risk_chain.py:393-430 |

## Finding detail

- FND-001: the fix is to delete the test, or replace it with a behavioural
  assertion that a post-control severity worse than the pre-control one
  validates. The integration test already makes that assertion.
- FND-004: low with medium confidence, because the ticket names the file. The
  value test fails: nothing reads it.
