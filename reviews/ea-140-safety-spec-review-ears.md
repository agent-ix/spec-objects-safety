---
id: SR-423
title: "Spec review (EARS) — spec-objects-safety EA-140 FR-109"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; Behavior statements in spec/functional/FR-109-risk-management-review.md (git diff origin/main...b5b402c, PR #51)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-109", type: references }
---

## Summary

Ticket: EA-140 (part 1). The thirteen FR-109 Behavior statements were read
against EARS. Ubiquitous statements ("The ... SHALL ...") and the unwanted-
behaviour forms ("If ..., then ... SHALL ...") are well-formed with one
exception. `quire validate --scope .` reports `[ears:non-singular]` on
line 56 only; FR-107 and FR-108 report none.

## Verdict

Conformant except one compound statement (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | "The skeleton SHALL carry a placeholder in every review cell and SHALL fail validation until a person fills them." carries two `shall`s; quire reports `[ears:non-singular]`. Split into two statements (the second is already covered by FR-109-AC-2). | spec/functional/FR-109-risk-management-review.md:56 |
