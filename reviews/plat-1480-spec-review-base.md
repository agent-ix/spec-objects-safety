---
id: SR-051
title: "Spec review (base) of PLAT-1480 tension record (spec-objects-safety#37)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-401-tension-object-type.md, spec/functional/FR-402-tension-edges.md, spec/functional/FR-403-tension-state-validation.md, spec/functional/FR-404-tension-completeness-rule.md, spec/functional/FR-405-tension-intake.md, spec/non-functional/NFR-401-tension-generic-and-human-accepted.md, spec/stakeholder/StR-001-safety-object-types.md, spec/usecase/US-401-record-conflicting-requirements.md (git diff origin/main...7939beb)"
review_set: subset
---
# Spec review (base) of PLAT-1480 tension record (spec-objects-safety#37)

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
| FND-001 | high | A tension with `status: open` that also carries a `resolved_by` (or `accepted_by`) edge passes both checks. The FR-404 relation is satisfied by the edge, and FR-403 rejects only an `accepter` on an open record, not a closing edge. So a corpus can hold an open tension and still pass, which breaks the ticket's first acceptance criterion. FR-403 needs a rule that `status: open` forbids `resolved_by` and `accepted_by`, plus an AC for it. Or FR-404 should key the relation on `status` (see SR-053 FND-001). | spec/functional/FR-403-tension-state-validation.md:30-41 |
| FND-002 | medium | FR-402-AC-1 requires a finding when a tension has only one `conflicts_with` edge. quire-rs FR-058 `required_relations` has no cardinality: any one edge satisfies it. Nothing in FR-402 or FR-404 says which mechanism counts two edges. If it is the engine, it contradicts FR-401-CON-1 (no new engine mechanism). Say it is a record-schema rule (`contains` with `minContains: 2` over the `conflicts_with` relations), and make the AC say the record is rejected, not that it draws a finding. | spec/functional/FR-402-tension-edges.md:54 |
| FND-003 | medium | 'The schema SHALL require `accepter.name` to be a person's name' is not checkable by a schema. FR-403-AC-6 rejects only three sentinels, so 'ci-bot', 'Safety Team' or 'claude' would validate as accepters. Sibling PR #33 FR-103-AC-4 already fixes this with a configured non-person list (team and tool names) that the schema rejects. Use the same rule and AC. | spec/functional/FR-403-tension-state-validation.md:33 |
| FND-004 | medium | FR-405 puts SHALLs on the design-gate loop and planning workflows ('SHALL report every open tension to the person running the gate', 'SHALL NOT mark a tension resolved'), but FR-405-CON-1 says those modules own them. No AC in this repo can test them. FR-405-AC-2 restates FR-403-AC-1 and FR-405-AC-3 restates FR-404-AC-1. Either cut FR-405 down to the data contract this module owns (tensions are optional input, and the schema blocks emitted acceptance) and cite the owning ticket for the loop behaviour, or drop it. | spec/functional/FR-405-tension-intake.md:29-37 |
| FND-005 | low | NFR-401's metric 'Source files that branch on the name `tension`: 0 (Test)' is a grep over this package's source, not a behaviour test. The real guarantee, that the engine has no tension-specific code, is FR-404-CON-1 against quire-rs. This package's emitter has to name `Tension.json` anyway. By the value test, drop the metric and its scan. | spec/non-functional/NFR-401-tension-generic-and-human-accepted.md:28 |
| FND-006 | low | FR-402-AC-2 treats `references` as an allowed verb from a tension ('a verb outside the three declared and `references` is reported'). FR-402's Behavior and Outputs declare only `conflicts_with`, `resolved_by` and `accepted_by`. State whether `allowed_links` for `tension` carries `references`. | spec/functional/FR-402-tension-edges.md:55 |
| FND-007 | low | spec/functional/index.md lists FR-404 as 'Completeness rule as manifest data', which truncates the document title ('...: no tension is open at release; accepted tensions name a person'). | functional/index.md:22 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-008 | low | The indexes are stale after the rebase. spec/index.md lists `non-functional` twice: main already had it, and the PR appends it again. In spec/functional/index.md, the FR-402 entry still reads 'what closed it' (the title is now 'what resolved it'), and the FR-405 entry carries the old title ('Planning workflows may emit tensions; ...'). | spec/index.md:16,18; spec/functional/index.md:27,30 |

## Dispositions

Round 1, head `01453e1` (rebased on main). This review was first posted on PLAT-1480 as SR-030; it is committed as SR-051.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-404 now selects on `status`. Relation `tension-is-not-open` (`where: {field: status, values: [open]}`) reports every open tension whatever edges it carries, and FR-404-AC-2 tests the open-plus-`resolved_by` case. How the relation is built is a new finding (SR-053 FND-005). |
| FND-002 | fixed | The two-edge minimum is now a schema rule, and FR-402-AC-1 tests it as a schema failure. |
| FND-003 | fixed | The untestable 'a person's name' statement is removed and acceptance uses `decided_by`. The replacement FR-403-AC-5 brings its own defect (SR-052 FND-005). |
| FND-004 | fixed | FR-405 now binds only this module's record and rules. It contains no SHALL on the workflows or the design-gate loop, and its ACs no longer restate FR-403. |
| FND-005 | fixed | The source-grep metric is removed from NFR-401. |
| FND-006 | fixed | FR-402 now says the allowed links are exactly `conflicts_with` and `resolved_by`, with `references` excluded, and AC-2 matches. |
| FND-007 | fixed | The FR-404 index entry now carries the full title. The other index entries have new staleness (FND-008). |

Round 2, head `7476e06`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-008 | fixed | `spec/index.md` now lists `non-functional` once, and the FR-402 and FR-405 index entries match their document titles. |
