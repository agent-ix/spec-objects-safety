---
id: SR-052
title: "Spec review (integrity) of PLAT-1480 tension record (spec-objects-safety#37)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-001-safety-object-types.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-006-cross-module-references.md, spec/functional/FR-401-tension-object-type.md, spec/functional/FR-403-tension-state-validation.md, spec/functional/FR-404-tension-completeness-rule.md (git diff origin/main...7939beb)"
review_set: subset
---
# Spec review (integrity) of PLAT-1480 tension record (spec-objects-safety#37)

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
| FND-001 | high | FR-401 adds `tension` as a third object type, and this PR amends none of the requirements that say there are exactly two: FR-001 ('declare two object types', FR-001-AC-1 'exactly `hazard` and `failure_mode`'), FR-003 ('`semantic.exports` SHALL name both object types') and FR-006 ('exactly two object types', FR-006-AC-1). The spec now contradicts itself, and the FR-001-AC-1 and FR-006-AC-1 tests fail the moment the manifest gains `tension`. Amend all three in this PR, so that each says the module's declared set, without a count. Sibling PRs #33 and #34 hit the same contradiction. | spec/functional/FR-401-tension-object-type.md:31 |
| FND-002 | medium | An accepted tension records its person twice, as `accepter.name` and as the target of the `accepted_by` edge, and its date twice, as `accepter.acceptedAt` and as the `Provenance.assertedAt` that FR-401 requires. No rule says the two copies agree, so `accepter.name: Alice` with `accepted_by -> ix://.../bob` validates. Keep one source of truth for each: the field for the person (see FND-003), and no second date. | spec/functional/FR-403-tension-state-validation.md:30-32 |
| FND-003 | medium | The same module already has a reviewed shape for 'a named person decided': PR #33 FR-103 has `decided_by` naming a person, rejects role, team and tool names, forbids it while undecided, and stores no decision date because version-control history gives who and when. PR #36 FR-303 relies on that shape. FR-403 invents a second shape (`accepter{name, acceptedAt}`, an `accepted_by` edge, `Provenance`). Reuse `decided_by` and its rules for the accepted state, so the Risk Model has one person-acceptance contract. | spec/functional/FR-403-tension-state-validation.md:30-36 |
| FND-004 | low | `acyclic_edges += resolved_by` guards a cycle that can only form if one tension is `resolved_by` another tension. FR-402 allows `resolved_by` to 'any design element or decision document' and neither allows nor forbids a tension target. Either state that tension-to-tension resolution is allowed (and keep the cycle check), or limit the targets and drop the entry and FR-404-AC-5 under the value test. | spec/functional/FR-404-tension-completeness-rule.md:39-40 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | medium | FR-403's Behavior line 'The schema SHALL apply to `decided_by` the same rejection of role, team and tool names that FR-103 applies', and FR-403-AC-5, point to a rule that merged FR-103 does not have. On main, FR-103 requires only a non-empty `decided_by` and takes who and when from git; its role/team/tool AC was dropped deliberately. As written, AC-5 cannot be implemented ('as it is for FR-103' rejects nothing). Remove the line and AC-5 so `decided_by` matches main: non-empty only. | spec/functional/FR-403-tension-state-validation.md:34-35,55 |
| FND-006 | low | Two-type wording is left after the FR-001, FR-003 and FR-006 amendment. FR-003 still says '`data_schema` on both object types' (line 37) and 'no load failure for either object type' (line 45), and IT-001 still says 'both object types registered' (lines 16, 60). Reword them to 'every declared object type'. | spec/functional/FR-003-semantic-manifest-contract.md:37,45; spec/integration/IT-001-quoin-module-install.md:16,60 |

## Dispositions

Round 1, head `01453e1` (rebased on main). This review was first posted on PLAT-1480 as SR-031; it is committed as SR-052.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-001, FR-003 and FR-006 are amended to describe the declared set without a count, and their ACs match. The two-type wording left in FR-003 and IT-001 is new finding FND-006. |
| FND-002 | fixed | `accepter`, `acceptedAt`, `Provenance` and the `accepted_by` edge are gone. `decided_by` is the only record of the person, and FR-401 forbids a date or a second copy of identity. |
| FND-003 | fixed | FR-403 reuses FR-103's `decided_by` contract (required when accepted, rejected otherwise, no date). The role/team/tool clause is new finding FND-005. |
| FND-004 | fixed | `resolved_by` is no longer added to `acyclic_edges`, and its cycle AC is removed. |

Round 2, head `7476e06`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-005 | fixed | The role/team/tool rejection line and the old FR-403-AC-5 are removed. `decided_by` is non-empty only, which matches merged FR-103 on main. |
| FND-006 | fixed | FR-003 (Outputs, Behavior) and IT-001 (Purpose, SC-04, Expected Results) now say 'every declared object type'. |
