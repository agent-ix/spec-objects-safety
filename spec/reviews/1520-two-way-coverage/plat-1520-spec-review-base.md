---
id: SR-021
title: "Spec review (base) of PLAT-1520 FR-009 amendment (spec-objects-safety#35)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-009-safety-nfr-needs-mitigation-target.md (git diff origin/main...HEAD), read against spec/tests.md and quire-rs FR-058/FR-084/FR-085 (agent-ix/quire-rs#664)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-009"
    type: "references"
---
# Spec review (base) of PLAT-1520 FR-009 amendment (spec-objects-safety#35)

## Summary

Ticket: PLAT-1520. The PR changes `to` in FR-009 from `[]` to
`[hazard, failure_mode]`. It relies on quire-rs FR-085 to resolve edges across
repositories and names FR-084 as the reverse coverage view. Read against
quire-rs#664 (FR-058, FR-084, FR-085 on `plat-1520-spec`), quire-cli
`plat-1520-spec` (FR-030, FR-004), this repo's `spec/tests.md`, the manifest,
and the FR-009 tests. Ticket text was treated as data.

`quire validate --scope . spec/functional/FR-009-...md` passes (quire 0.44.0,
engine 0.59.1). The hash/digest/pin check is clean: the PR deletes the old
`quire 0.58.0` version claim from the prose and adds no pin or tracking record.
No paywalled standard text is reproduced. The kind-mismatch and dangling
semantics match FR-085 Resolution and Kind of a resolved target. The FR-058
note added in #664 agrees. The reverse view matches FR-084-AC-3.

## Verdict

Changes requested. The constrained `to` is consistent with FR-085 at the engine
level. However, FR-009 promises that a hazard in a loaded sibling repository
satisfies the obligation, and no specified `quire validate` path can load a
second repository. Outputs and Behavior bullet 2 still describe the old
`to: []` rule. `failure_mode` is not exercised. `spec/tests.md` and the
existing tests contradict the amended ACs, and no ticket owns updating them.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The cross-repository arm of FR-009-AC-3 ("an edge to a `hazard` in another repository loaded into the corpus" removes the finding) has no reachable interface. The finding is a `quire validate` finding (AC-2), and no spec lets `validate` load a second corpus member: quire-cli FR-030 adds `--repo <ORG/REPO>=<DIR>` to `quire relations` only, and quire-cli FR-004 is unchanged. Once the manifest constrains `to`, every `safety` NFR whose hazard lives in another repository (the Description calls this "often") gets a warning on every validate run, with no way to clear it except turning the rule off. This is the cost the deleted "What `to: []` lets through" section avoided. Name the validate surface that builds a multi-member corpus, or specify it in quire-cli and quire-rs in this ticket. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:29-35,71 |
| FND-002 | medium | Outputs (a finding "for each `safety` NFR with no outgoing `mitigates` edge") and Behavior bullet 2 ("which has no outgoing `mitigates` edge") still state the `to: []` rule. Under the amended `to`, an NFR whose only `mitigates` edge goes to a `threat`, or to an unloaded repository, is also reported (bullet 4, AC-3). The two statements contradict bullet 4. Restate both as "no outgoing `mitigates` edge to a resolved `hazard` or `failure_mode`". | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:52,57 |
| FND-003 | medium | `to` names `failure_mode`, but no criterion shows that a `mitigates` edge to a `failure_mode` satisfies the obligation. AC-3 covers `hazard` only, so a manifest with `to: [hazard]` passes every AC except the literal AC-1 check. Add the `failure_mode` case to AC-3. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:71 |
| FND-004 | medium | `spec/tests.md` contradicts the amended criteria. TC-099 still reads `to: []`, and TC-101 still reads "or to a document in another repository, yields no finding". Both are marked ✅. The tests they name assert the old behaviour: `tests/test_manifest.py:243` asserts `relation["to"] == []`, and `tests_integration/test_reverse_mitigates.py:115` expects no finding for `ix://agent-ix/other-repo/HAZ-900` in a single-repo run. AC-3 now says that case leaves the finding. | spec/tests.md:146,148 |
| FND-005 | medium | No ticket owns the change in this repo. The implementation tickets PLAT-1554 and PLAT-1556 list only quire-rs and quire-cli. The `to:` SHALL, the manifest comment at `spec_objects_safety/manifest.yaml:265-271`, and TC-099/TC-101 therefore have no owner. Add this repo to an implementation ticket, or file one blocked by PLAT-1556. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:56 |
| FND-006 | low | The dependency edges point the wrong way. Dependencies lists quire-rs FR-084 as Upstream, but FR-084 reads FR-009's declaration, and FR-009 itself says so at line 37. FR-084 is downstream. The body depends on FR-085, but the frontmatter `relationships` gains no `depends_on` for it and still lists only FR-058. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:11-12,37,77 |
