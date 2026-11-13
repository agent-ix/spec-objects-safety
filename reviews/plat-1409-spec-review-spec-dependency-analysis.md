---
id: SR-032
title: "Spec review (dependency) of PLAT-1409 risk-model objects (spec-objects-safety#34)"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-objects-safety; spec/functional/FR-201..FR-205, spec/non-functional/NFR-201, spec/non-functional/index.md, spec/index.md (git diff origin/main...plat-1409-spec), read against PR #33 (plat-1523-spec)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-205"
    type: "references"
---
# Spec review (dependency) of PLAT-1409 risk-model objects (spec-objects-safety#34)

## Summary

Ticket: PLAT-1409. This file covers the dependency lens. It checks the
upstream engine and module capabilities each requirement relies on, and how
the PR fits with PR #33 (PLAT-1523, FR-101..FR-107, NFR-100), which adds to the
same `spec/` tree. The upstream sources were read on `origin/main`:

- quire-rs `src/corpus/required_relations.rs`: `where` selects on a field of
  the `from` document's frontmatter. Presence of an edge is the only
  obligation; there is no cardinality and no condition on other edges.
- quire-rs `src/corpus/validate.rs`: Tier-2 target check.
- `spec-objects-security` manifest: `control`, `risk`.
- `engineering-assurance`: `spec/functional` ends at FR-043, and the manifest
  declares no evidence-record type.
- quire-rs FR-078 "Qualified retained evidence in coverage and trace".

The ID ranges do not clash with PR #33. The content does: the two PRs model the
post-control estimate and the "no computed verdict" rule twice, and disagree
on where severity and probability levels come from.

## Verdict

Not ready. FR-205 relies on a selection that `required_relations` cannot
express. It also cites a retained-evidence requirement and document type that
do not exist where it says they do. FR-203 contradicts PR #33 FR-101/FR-102 on
whether levels form a fixed enum or a project choice. Whichever of #33 and #34
lands second has to be reconciled with the other. The cleanest way is one
pass over both before either merges.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-203 fixes estimate `severity`/`probability` to the closed FR-004 `Severity`/`Likelihood` enums. PR #33 FR-101 says "The severity and probability levels are those the project chooses; the policy names them", and FR-102 checks the estimate's levels against the policy's own lists. Both cannot hold: either every policy must use exactly the FR-004 members, or the estimate schema cannot be a closed enum. Decide one model across both PRs. | spec/functional/FR-203-pre-control-risk-estimate.md:24-26 |
| FND-002 | high | FR-205 Behavior says the module declares `required_relations` with `from: control`, and also that only a control that mitigates a hazard or is assumed by an estimate is reported. quire-rs `required_relations` selects `from` documents only by a `where` on their own frontmatter field, never by an incoming edge. As declared, every security control in the bundle is reported, so FR-205-AC-5 fails. Either name a quire-rs requirement that adds edge-conditioned selection (and depend on it), or drop the scoping. | spec/functional/FR-205-control-requirement-and-verification-links.md:59-60 |
| FND-003 | high | FR-205 cites "`agent-ix/engineering-assurance` FR-078 (retained evidence)". engineering-assurance `origin/main` has no FR-078 (its FRs end at FR-043), and its manifest declares no evidence-record document type that could author `verifies`. Retained evidence is quire-rs FR-078: caller-supplied evidence bound to a declaration, not a frontmatter document. So the retained-evidence half of FR-205-AC-2 and all of AC-8 cannot be built as written. Repoint to the real owner and restate the link, or drop the retained-evidence option. | spec/functional/FR-205-control-requirement-and-verification-links.md:33-36,69,75,79 |
| FND-004 | medium | FR-204's `post-control-without-pre-control` warning is conditioned on the `phase` of estimates that point at a situation. No declared module check can express that (`required_relations` has no condition on the source of an incoming edge), and FR-204 names no upstream requirement that provides one. Name the mechanism and its owner, or remove the check. | spec/functional/FR-204-post-control-risk-estimate.md:43 |
| FND-005 | medium | FR-204 defines the post-control estimate as a `risk_estimate` with `phase: post_control`. PR #33 FR-103 makes `residual_risk` hold "the post-control severity and probability levels" directly. The same judgement would then be authored in two types. One PR must reference the other: `residual_risk` should reference a `post_control` `risk_estimate` rather than restate its levels. FR-203 should also state the provenance difference: `assertedAt` is required here, but #33 FR-103 takes decision time from git and forbids a date field. | spec/functional/FR-204-post-control-risk-estimate.md:17-20 |
| FND-006 | medium | NFR-201 ("No tool stores or defaults a score, region or acceptance") restates PR #33 FR-104 ("No tool computes, stores or defaults a score, a region verdict or an acceptance"), with different scopes and verification. Two requirements for one rule will drift. Keep one, widen its scope to every type from both PRs, and have the other `constrains`/reference it. | spec/non-functional/NFR-201-no-stored-or-defaulted-risk-values.md:17-22 |
| FND-007 | low | PR #33 and this PR each add `spec/non-functional/index.md` as a new file, and both append to the end of `spec/functional/index.md`. The second to merge gets an add/add and a content conflict. This PR also never links `non-functional/index.md` from `spec/index.md` (PR #33 does), so on its own NFR-201 is not reachable from the root index. | spec/non-functional/index.md:1-10 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | 33c79d4: FR-203 no longer uses closed level enums. The levels are the project's, checked by PLAT-1523 FR-102 (now on main). FR-004 lists stay `hazard.assessment` only. |
| FND-002 | fixed | 33c79d4: FR-205 declares no `control` relation (AC-6). The scoped rules move to PLAT-1524 FR-302 and depend on a quire-rs incoming-edge selector that is stated not to exist. |
| FND-003 | still-open | 33c79d4 repoints the dependency to quire-rs FR-078 correctly, but FR-205-AC-3 still cannot be built. quire-rs FR-078 qualifies evidence for a `CriterionIdentity` in the selected inventory, through the `quoin_quire::evidence::qualify` library API, for coverage credit. It binds nothing to a `control` and has no `quire extract` path. "Raises no diagnostic about a missing edge" cannot fail, because AC-6 declares no relation that could raise one. Fix: state that effectiveness evidence binds to the criteria of the FR/NFR that `satisfies` the control, and drop AC-3 or restate it on that criterion. |
| FND-004 | fixed | 33c79d4: `post-control-without-pre-control` is removed. FR-204 declares no pre-control existence check, and AC-6 asserts no diagnostic. |
| FND-005 | fixed | 33c79d4 and main 213df1f: FR-204 is the one post-control home. Main's FR-103 now "references the post-control estimate" (FR-204) and copies no levels. FR-203 states the `assertedAt` vs git-time provenance difference. |
| FND-006 | fixed | 33c79d4: NFR-201 is deleted. FR-203 points to PLAT-1523 FR-104, whose Behavior on main is module-wide ("The module's tooling SHALL NOT ..."). |
| FND-007 | fixed | 33c79d4: `spec/non-functional/` is removed from this PR, so there is no add/add with #33. The remaining append to `spec/functional/index.md` is a rebase matter the coordinator owns. |
| FND-003 | fixed | Round 2 (4ef0e38): FR-205 now says quire-rs FR-078 binds evidence to an acceptance criterion through `evidence::qualify`, not to a control and not through `quire extract`. A control's effectiveness evidence is reached through the criteria of the FR/NFR that `satisfies` it, and AC-3 asserts qualification of that FR's criterion. The upstream `qualify` entry point is still planned (it is not on quire-rs or quoin main), and that dependency is declared (`depends_on` quire-rs FR-078). |
