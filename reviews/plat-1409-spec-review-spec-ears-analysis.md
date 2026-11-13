---
id: SR-033
title: "Spec review (EARS conformance) of PLAT-1409 risk-model requirements (spec-objects-safety#34)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; spec/functional/FR-201..FR-205, spec/non-functional/NFR-201 (git diff origin/main...plat-1409-spec)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-203"
    type: "references"
---
# Spec review (EARS conformance) of PLAT-1409 risk-model requirements (spec-objects-safety#34)

## Summary

Ticket: PLAT-1409. `quire validate --scope . "spec/**/*.md"` (quire 0.44.0)
reports 15 grammar warnings in the new files and none in NFR-201:

- `ears:non-singular` (9): FR-201:40,42; FR-202:59,62; FR-203:47,49,50,51;
  FR-205:60.
- `quality:agentless-passive` (4): FR-202:59,62; FR-203:50; FR-204:41.
- `quality:mixed-modal` (1): FR-203:52.
- `ears:vague-response` (1): FR-205:22 (`be able to`).

I read each statement by hand as well. The error-path statements (FR-202:63-64,
FR-204:41-43) use an explicit "When ... SHALL" or "SHALL report" form. All of
these warnings are advisory and none blocks validation.

## Verdict

Conformant in substance. The compound statements should be split so that each
Behavior bullet carries one obligation that one criterion can trace to.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | 15 advisory EARS warnings in FR-201..FR-205. Nine compound `SHALL` statements (for example FR-203:47 requires five fields and an edge cardinality in one bullet). Four agentless passives (`shall be accepted`, `shall be unchanged`, `shall be forbidden`, `shall be reported`). One mixed `SHALL`/`MAY` (FR-203:52). One vague `be able to` (FR-205:22). Split the compound bullets, name the module or Quire as the actor, and separate the `MAY` from the `SHALL NOT`. | spec/functional/FR-203-pre-control-risk-estimate.md:47-52 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | 33c79d4: Behavior bullets are split into one `SHALL` each, with Quire or the module named as the actor. `quire validate --scope . "spec/**/*.md"` now reports 0 grammar warnings in FR-201..FR-205. |
