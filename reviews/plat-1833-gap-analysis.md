---
id: SR-410
title: "Gap analysis — spec-objects-safety FR-010 hazard causes"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-010-hazard-causes-beyond-failure-modes.md, spec_objects_safety/manifest.yaml, tests/test_cross_module_references.py, tests_integration/test_risk_chain_edges.py"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-010", type: references }
---

## Summary

Ticket: PLAT-1833. Computed matrix (`quire matrix --scope . --format json`) binds all five FR-010 criteria to a test. Two criteria have binders that cannot fail on the full criterion they claim.

## Verdict

**CONDITIONAL** — no untagged criterion and no stub; two medium coverage gaps. The ticket's optional SOUP rule is not delivered. The coder said a required relation cannot express it, and the engine bears this out: `where` matches only string-valued top-level frontmatter, and `known_anomalies` is an array in `SoupRecord.json`. The ticket marks the rule optional, so its absence is not a gap. The coder's other claim, that the rule belongs in spec-objects-security, does not hold: this manifest already declares `control-has-requirement` over the foreign `control` type.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-010-AC-2 is backed only by a unit test comparing the manifest list to the literal `systems-part`; no test validates a failure_mode to part edge with spec-objects-architecture loaded, so a role spelling shared by manifest and test but unknown to architecture would pass. | FR-010-AC-2, tests/test_cross_module_references.py:181-187 |
| FND-002 | medium | FR-010-AC-3's clause "no new edge verb is added" is not asserted by its bound test TC-112: adding `leads_to: [failure_mode]` to hazard leaves TC-112 green and only TC-063 (FR-006-AC-4) fails. | FR-010-AC-3, tests/test_cross_module_references.py:190-195 |

## Coverage

- FR-010-AC-1..AC-5: tagged (TC-110, TC-111, TC-112 x2, TC-113). Run evidence: focused pytest runs, all passed.
- Untraced behaviours in reviewed changes: 0. Stubs: 0.
- Plan completion: not assessed
- Semantic review: skipped (optional method not requested).

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Commit `c58dbb2` adds TC-114 (two integration tests, spec-objects-architecture loaded). Mutating the role to `system-part` in manifest and unit test turns TC-114 red. |
| FND-002 | fixed | Commit `c58dbb2` rewords AC-3 to exact verb sets and TC-112 asserts them; adding `leads_to: [failure_mode]` to hazard now turns TC-112 red. |
| FND-003 | fixed | Commit `c4b8599` drops the TC-062 `verifies` edge, the Imports subtask, the imports scope clause and the manifest-comment deliverable from Task-010; no reference to a removed item remains. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | low | Plan Task-010 still declares `verifies` TC-062 and its "Imports" subtask still promises the three migration issues named in the manifest, though TC-062 and FR-006-AC-3 were deleted. | plan/Plan-001-semantic-module-contract/tasks/Task-010-cross-module-references.md:19,38 |
