---
id: SR-022
title: "Spec review (EARS) of PLAT-1520 FR-009 amendment (spec-objects-safety#35)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; spec/functional/FR-009-safety-nfr-needs-mitigation-target.md Behavior and Acceptance Criteria (git diff origin/main...HEAD)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-009"
    type: "references"
---
# Spec review (EARS) of PLAT-1520 FR-009 amendment (spec-objects-safety#35)

## Summary

Ticket: PLAT-1520. This review checks the EARS form of the three Behavior
statements the PR changed or added (lines 56, 58, 59) and of the amended
FR-009-AC-1 and FR-009-AC-3. Line 56 and line 58 each have one `SHALL` and a
named subject. AC-1 is a single checkable statement. The Behavior statements
the PR left unchanged were not re-reviewed here; base SR-021 FND-002 covers
their content.

## Verdict

Minor. One added statement is negative and has no observable response. One
criterion bundles four cases.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | Behavior line 59 ("Quire SHALL NOT let an edge to a document of any other kind, or to a repository that is not loaded, satisfy the obligation") is a negative ubiquitous statement with no observable system response. In EARS unwanted-behaviour form it would read: "If a `safety` NFR's only outgoing `mitigates` edges target a document of another kind or a repository that is not loaded, then Quire SHALL report the NFR". That names the observable, the finding. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:59 |
| FND-002 | low | FR-009-AC-3 bundles four cases in one criterion: a local hazard, a hazard in a loaded sibling repository, an edge to another kind, and an edge to an unloaded repository. When one case fails, the result cannot say which. Split it into a positive and a negative criterion. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:71 |
