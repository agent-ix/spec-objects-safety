---
id: SR-419
title: "Spec review (EARS) — spec-objects-safety PLAT-1834 FR-108"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; Behavior statements in spec/functional/FR-108-risk-management-plan.md (git diff origin/main...dbd860e, PR #50)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-108", type: references }
---

## Summary

Ticket: PLAT-1834. All eleven FR-108 Behavior statements were checked against
EARS: nine ubiquitous `SHALL` / `SHALL NOT` statements with a system subject
(the type, the tables, the schema, the module, the skeleton) and two unwanted-
behaviour `If ..., then ... SHALL` statements (placeholder cell; plan with no
acceptability policy). `quire validate` reports one `ears:non-singular`
warning, reproduced below.

## Verdict

Conformant except one statement with two responses.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | "The skeleton SHALL contain placeholders only, and SHALL fail validation until a person fills every row." has two `SHALL`s (quire `ears:non-singular`). Split it into one statement per response. | spec/functional/FR-108-risk-management-plan.md:49 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | Fix commit a122426 moved "fail validation" to its own line, but the remaining statement "The skeleton SHALL carry a placeholder in every plan row, and SHALL otherwise carry only its identity row and its invariant clause." still has two SHALLs; quire still reports `[ears:non-singular]` at FR-108 line 50. Split it once more. |
