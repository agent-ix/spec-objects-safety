---
id: SR-055
title: "Spec review (ears-conformance) of PLAT-1480 tension record (spec-objects-safety#37)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; spec/functional/FR-401-tension-object-type.md, spec/functional/FR-402-tension-edges.md, spec/functional/FR-403-tension-state-validation.md, spec/functional/FR-404-tension-completeness-rule.md, spec/functional/FR-405-tension-intake.md, spec/non-functional/NFR-401-tension-generic-and-human-accepted.md (git diff origin/main...7939beb)"
review_set: subset
---
# Spec review (ears-conformance) of PLAT-1480 tension record (spec-objects-safety#37)

## Summary

Ticket: PLAT-1480. The ticket, PR body and sibling PRs were read as data. Compared against
quire-rs origin/main FR-058, the spec-artifacts-iso origin/main `edge_types`, and sibling PRs
#33, #34 and #36. `quire validate --scope . "spec/**/*.md"` (quire 0.44.0) reports no errors in
the new files. The only structural failure is `spec/tests.md`, which this PR does not change.
There are three EARS warnings (SR-055).

## Verdict

The ticket's acceptance is covered by testable ACs: FR-404-AC-1 (open fails), FR-404-AC-2 and
FR-404-AC-3 (resolve or accept passes), and FR-403-AC-1 (accepted without an accepter is
rejected). The licensing boundary holds: no standard is named or quoted. Acceptance is always a
person's (FR-403-CON-1, FR-405, NFR-401). The findings below must be fixed before merge.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The NFR-401 statement has two SHALLs: generic terms only, and every acceptance taken from a person's written name (quire `ears:non-singular`). Split it into two statements. | spec/non-functional/NFR-401-tension-generic-and-human-accepted.md:14-15 |
| FND-002 | low | 'When tensions are present, the design-gate loop SHALL read their status and edges and SHALL report every `open` tension...' has two SHALLs, and quire reports `ears:unclassifiable` and `ears:missing-subject` on its continuation line. Split it, or remove it with SR-051 FND-004. | spec/functional/FR-405-tension-intake.md:33-34 |

## Dispositions

Round 1, head `01453e1` (rebased on main). This review was first posted on PLAT-1480 as SR-034; it is committed as SR-055.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | NFR-401 is split into two single-SHALL statements, and quire reports no EARS warning on it. |
| FND-002 | fixed | The compound design-gate statement is removed from FR-405, and quire reports no EARS warning on FR-405. |
