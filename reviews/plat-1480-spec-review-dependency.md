---
id: SR-053
title: "Spec review (dependency) of PLAT-1480 tension record (spec-objects-safety#37)"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-objects-safety; spec/functional/FR-006-cross-module-references.md, spec/functional/FR-402-tension-edges.md, spec/functional/FR-404-tension-completeness-rule.md (git diff origin/main...7939beb)"
review_set: subset
---
# Spec review (dependency) of PLAT-1480 tension record (spec-objects-safety#37)

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
| FND-001 | medium | The engine gap the PR claims ('`required_relations` cannot read a field value', PR body open question 2) does not exist. quire-rs FR-058 (origin/main) defines an optional `where: {field, values}` that narrows a relation by a top-level frontmatter value (FR-058-AC-12..22), and this repo's own manifest uses it (`safety-nfr-has-mitigation-target`, `where: {field: quality_attribute, values: [safety]}`). So status-to-edge agreement can be manifest data over graph edges: `where: {field: status, values: [resolved-by-design]}` with `edges: [resolved_by]`, and the same for `accepted-by-person`. Today FR-403 instead checks a record-schema `relations` entry, which is not the graph edge FR-404 reads, so the two can disagree. Correct the rationale and either use `where` or state why the schema route is chosen. Either way `status` must be a frontmatter field. | spec/functional/FR-404-tension-completeness-rule.md:45-47 |
| FND-002 | medium | FR-402 depends on spec-artifacts-iso adding `conflicts_with`, `resolved_by` and `accepted_by` to `edge_types`, but no iso ticket is filed or cited (a Linear search finds none). FR-402-AC-5, FR-402-CON-1 and the existing FR-006-AC-4 test all fail until that lands. Vocabulary check against iso origin/main: `conflicts_with` has no synonym (`relates_to` and `peer` are too loose, `blocks` means something else), so adding it is justified. `resolved_by` has none either (`remediates` is runbook-to-incident, `satisfied_by` is StR-only), so it is justified too, as forward `resolves` with inverse `resolved_by` per iso convention. `accepted_by` should not be added (see FND-003). File the iso ticket for the two verbs and add it as a blocks edge. | spec/functional/FR-402-tension-edges.md:36-40 |
| FND-003 | medium | `accepted_by` targets 'an ix:// person reference owned by another repository', but no spec-objects-* or spec-artifacts-* manifest declares a person or roster type, and FR-402 gives no URI form. With `to: []` and FR-402-AC-3 (passes without the target loaded), any string closes the relation, so a mistyped or invented person accepts the conflict. Drop the edge and carry the person as a validated field (`decided_by`, as PR #33 FR-103), and drop `accepted_by` from the FR-404 relation. | spec/functional/FR-402-tension-edges.md:56 |
| FND-004 | low | Because the relation is `to: []`, a dangling or mistyped `resolved_by` target also satisfies it, and only `dangling-reference` would report it. The `to: []` rationale covers person references only. Like FR-009, FR-404 should state this accepted consequence, or put `resolved_by` in its own relation with a constrained `to`. | spec/functional/FR-404-tension-completeness-rule.md:37-38 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | medium | `tension-is-not-open` reports open tensions only because its obligation (an incoming `conflicts_with`) can never be met. Nothing in this module makes that true. FR-402 restricts `conflicts_with` only from the `tension` end, and PLAT-1675 adds the verb ecosystem-wide. Any document, including another tension (FR-402 allows 'any requirement or clause document'), that authors `conflicts_with` to an open tension silently clears `trace:open-tension`, and with `to: []` a dangling or cross-repo edge does too. FR-058 has no direct 'report every selected document' primitive, because a relation can only demand an edge. Two fixes are sound. (1) Replace it with a relation whose satisfiability this module controls: `where: {field: status, values: [open]}`, `edges: [resolved_by]`, `direction: outgoing`, with the record schema rejecting `resolved_by` relation entries when `status: open` (the same `relations` array that FR-402's `minContains` already constrains). An open tension then always either fails the schema or is reported, independent of other modules. (2) If the lead wants a direct expression, file a quire-rs ticket for a field-value finding on FR-058 and keep (1) until it lands. In either case, add an AC that a second document authoring `conflicts_with` to an open tension does not clear the finding. | spec/functional/FR-404-tension-completeness-rule.md:36-43 |

## Dispositions

Round 1, head `01453e1` (rebased on main). This review was first posted on PLAT-1480 as SR-032; it is committed as SR-053.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The incorrect engine-gap rationale is gone. FR-404 now uses FR-058 `where` on the `status` frontmatter field (FR-401 makes `status` a frontmatter field). |
| FND-002 | fixed | PLAT-1675 exists, in team PLAT and in Backlog. Its title is 'spec-artifacts-iso: add conflicts_with and resolved_by edge verbs', and it blocks PLAT-1480. Its body adds exactly the two verbs with the same no-synonym reasoning, and FR-402 and FR-402-AC-5 cite it. |
| FND-003 | fixed | The `accepted_by` edge is dropped. The person is the `decided_by` field, and FR-402-AC-4 asserts that no person property other than `decided_by` and no person object type exist. |
| FND-004 | fixed | FR-404 now states what `to: []` costs. |
