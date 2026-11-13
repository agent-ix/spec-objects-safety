---
id: SR-060
title: "Code review of PLAT-1571/1574 chain and decision completeness relations (spec-objects-safety#40)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; spec_objects_safety/manifest.yaml, tests/test_risk_chain.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...4d37731)"
review_set: subset
---
# Code review of PLAT-1571/1574 chain and decision completeness relations (spec-objects-safety#40)

## Summary

Tickets: PLAT-1571, PLAT-1574, PLAT-1561. PR `agent-ix/spec-objects-safety#40`,
head `4d37731`, one commit. The PR declares four `required_relations` in
`spec_objects_safety/manifest.yaml`. Three are for FR-301
(`hazard-has-situation`, `situation-has-hazard`, `situation-has-harm`) and one
is for FR-303 (`post-control-estimate-has-decision`). It replaces one guard
test in `tests/test_risk_chain.py`, loosens the banned-word check in one
FR-203 test, and adds 14 integration tests for FR-301, FR-303 and FR-304. The
PR has no Rust and no TypeSpec change, so rust-review does not apply.

Note: the assigned worktree `plat-1561-impl` is checked out on
`plat-1573-impl` (commit `df09e8c`, PLAT-1573). The review ran in a detached
worktree at `4d37731`, the PR head.

Run evidence (quire 0.44.0, engine 0.59.1; quoin 0.30.1): after
`make semantic-install`, `pytest tests/test_risk_chain.py
tests_integration/test_risk_chain_edges.py` gave 103 passed. `ruff` and
`black --check` are clean on both changed files. The reviewer also ran probes
from a scratchpad script.

## Verdict

Changes requested. The four relations match the FR text field for field:

- `hazard-has-situation` is `from: hazard`, `edges: [arises_from]`,
  `to: [hazardous_situation]`, `incoming`, `hazard-without-situation`.
- `situation-has-hazard` is `from: hazardous_situation`, `to: [hazard]`,
  `outgoing`, `situation-without-hazard`.
- `situation-has-harm` is `from: hazardous_situation`, `to: [harm]`,
  `incoming`, `situation-without-harm`.
- `post-control-estimate-has-decision` is `from: risk_estimate`,
  `where: {field: phase, values: [post_control]}`, `edges: [estimate]`,
  `to: [residual_risk]`, `incoming`,
  `post-control-estimate-without-decision`.

The relation directions agree with `allowed_links`: `hazardous_situation`
has `arises_from: [hazard]` and `harm` has `arises_from: [hazardous_situation]`.
`acyclic_edges: [arises_from]` is unchanged and covers the chain.

The PR follows the lessons from #38 and #39:

- Each relation is declared once.
- There is no `mappings.yaml` and no `spec/tests.md` row.
- There is no file-count, inventory, hash or pin test.
- No score, region or acceptance is stored or defaulted.

The integration tests are behavioural. A probe confirmed what FR-301-AC-7
literally asks: `--severity trace:hazard-without-situation=error` exits 3 on
a bundle with only a hazard and a harm.

The `selected` change is acceptable. The new relation's own finding line
reads "selected because `phase` is 'post_control'", and the fixture in that
test now emits it. Stripping only that phrase keeps every other use of the
banned words checked.

The defects are in the trace tags. FND-001 is a spec contradiction that this
PR creates, and the test tagged with that criterion asserts its opposite.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-202-AC-6 on main says the manifest declares no relation whose `from` is `hazardous_situation` or whose check is `situation-without-hazard`. This PR declares two such relations, as FR-301 requires, so FR-202-AC-6 is now false. The replacement test is still tagged FR-202-AC-6 but asserts `"situation-without-hazard" in checks`, the opposite of the criterion. The PR does not amend FR-202-AC-6. | tests/test_risk_chain.py:183-188, spec/functional/FR-202-hazardous-situation-object-and-chain.md:91, spec_objects_safety/manifest.yaml:645-662 |
| FND-002 | medium | The FR-205-AC-6 guard is loosened to `r["from"] == "control" and "when_any" not in r`. FR-205-AC-6 on main still says no relation has `from: control`. The matching spec rewording is in the PLAT-1573 commit `df09e8c`, not in this PR. So this PR's test no longer asserts the criterion it is tagged with: a scoped control relation would pass it. | tests/test_risk_chain.py:177-180, spec/functional/FR-205-control-requirement-and-verification-links.md:96 |
| FND-003 | medium | The test tagged FR-301-AC-7 does not run the criterion's case. AC-7 says `trace:hazard-without-situation=error` makes the run exit non-zero while the other two checks stay warnings. The test uses a bundle with no harm. It escalates `situation-without-harm` and expects non-zero, then escalates `hazard-without-situation` and expects exit 0. It never asserts that the other checks stay at warning level. | tests_integration/test_risk_chain_edges.py:671-679 |
| FND-004 | low | FR-304-AC-1 (`acyclic_edges` contains `arises_from`) is asserted by `test_arises_from_stays_acyclic_across_the_whole_chain`, which is tagged only FR-202-AC-9. FR-304-AC-1 has no tagged test. | tests/test_risk_chain.py:191-193 |

## Finding detail

- FND-001: amend FR-202-AC-6 in this PR. For example: "FR-202 declares no
  `required_relations` entry; the situation relations are FR-301's", or
  "the manifest holds exactly one relation with check
  `situation-without-hazard`, the one FR-301 declares". Keep the tag only if
  the reworded criterion matches the assertion. Spec and code land together.
- FND-002: keep `assert not [r for r in relations if r["from"] == "control"]`
  in this PR. Move the `when_any` relaxation to the PLAT-1573 PR, next to its
  FR-205-AC-6 rewording. Rename the test to match.
- FND-003: use a fixture that triggers two chain checks: hazard H1 with no
  situation, and hazard H2 with situation S2 that has no harm. Assert exit 0
  with no flag. Then assert that `trace:hazard-without-situation=error` exits
  non-zero and that the `situation-without-harm` line for S2 still starts
  with `warning:`.
