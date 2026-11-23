---
id: SR-415
title: "Spec review (EARS) — spec-objects-safety PLAT-1837 FR-205, FR-302"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; Behavior statements added or changed in spec/functional/FR-205-control-requirement-and-verification-links.md and spec/functional/FR-302-risk-control-implemented-and-verified.md (git diff origin/main...3748247, PR #49)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-205", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-302", type: references }
---

## Summary

Ticket: PLAT-1837. Every Behavior statement the PR adds or rewrites was
checked against EARS: the two `Quire SHALL resolve` statements in FR-205, the
option-type statement, the retained-evidence statement, and the three
`The manifest SHALL declare` statements, the `verifies` exclusion, the empty-`to`
statement and the advisory/tunable statement in FR-302. All but one are
ubiquitous statements with a system subject and one response each.

## Verdict

Conformant except one statement whose subject is a document rather than the
system.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | "A retained-evidence record SHALL verify a control through an authored `verifies_implementation` or `verifies_effectiveness` edge to it" makes a document the subject of SHALL, so nothing in the system is obliged to do anything. Restate it with the system as subject, for example "Quire SHALL resolve a `verifies_implementation` or `verifies_effectiveness` edge from a retained-evidence record to a `control` as an incoming edge on the control." | spec/functional/FR-205-control-requirement-and-verification-links.md:101 |
