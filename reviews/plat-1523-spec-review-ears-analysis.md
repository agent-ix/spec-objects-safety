---
id: SR-023
title: "Spec review (EARS conformance) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; spec/functional/FR-101..FR-107 Behavior statements, spec/non-functional/NFR-100 Statement (git diff origin/main...e90c3c0)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-104"
    type: "references"
---
# Spec review (EARS conformance) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)

## Summary

Ticket: PLAT-1523. This review checked every Behavior statement in FR-101..FR-107
and the NFR-100 Statement for EARS form. The input was `quire validate`'s
grammar warnings, plus a manual read of each statement's subject and pattern.
Conditional rules use the unwanted-behaviour pattern ("If ..., then the ...
SHALL ...") correctly. The defects are compound statements, a quantifier
standing in for a system subject, and the undefined term "acceptable" (which
the base review raises as FND-001).

Scope examined (role: examined): the FR-101 Behavior (6 statements), FR-102
(3), FR-103 (5), FR-104 (5), FR-105 (7), FR-106 (6), FR-107 (6), and the
NFR-100 Statement.

## Verdict

Seven low findings, all fixed by rewording. None changes meaning.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The FR-101 Behavior line 44 (`[ears:non-singular]`) has two SHALLs, "contain placeholders only" and "fail validation until a person fills every cell". Split it. | spec/functional/FR-101-acceptability-policy.md:44 |
| FND-002 | low | The FR-102 Behavior lines 33-35 (`[ears:non-singular]`) each pair a SHALL with a SHALL NOT. Split each line into one requirement per SHALL. | spec/functional/FR-102-estimate-levels-resolve-in-policy.md:33-35 |
| FND-003 | low | The FR-103 Behavior line 39 (`[ears:non-singular]`) has three obligations in one statement: require the rationale, require `decided_by`, and reject a role, team or tool. Split it. That also isolates the clause the base review flags as FND-003. | spec/functional/FR-103-residual-risk-record.md:39 |
| FND-004 | low | The FR-107 Behavior line 27 (`[ears:non-singular]`) joins the decided case and the undecided case with a semicolon. Split it into two statements. | spec/functional/FR-107-overall-residual-risk-evaluation.md:27 |
| FND-005 | low | The NFR-100 Statement (`[ears:non-singular]`) has three SHALLs (deterministic, unmodified, bounded), and its Measurement table already lists three metrics. Split it into three statements, or into three NFRs. | spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md:14 |
| FND-006 | low | The FR-105 Behavior lines 30-32 (`[quality:ambiguous-term]` "acceptable") use "acceptable region" and "outside the acceptable region" with no defined source. Once FR-101 defines the region flag (base FND-001), name it in these lines. | spec/functional/FR-105-decision-policy-discrepancy-report.md:30-32 |
| FND-007 | low | The FR-104 Behavior statements use "No tool SHALL ..." as the subject. EARS needs a named system subject (for example "The module's tooling SHALL NOT ..."). | spec/functional/FR-104-no-computed-verdicts.md:23-26 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-008 | low | The fix round added a compound statement to FR-101 Behavior (`[ears:non-singular]`): "The schema SHALL declare no default for `outside_acceptable`; an entry without it SHALL fail validation naming the region." Split it in two. | spec/functional/FR-101-acceptability-policy.md:48 |
| FND-009 | low | The fix round added a compound statement to FR-103 Behavior (`[ears:non-singular]`): "The `estimate` reference SHALL resolve to a `risk_estimate` whose `phase` is `post_control`; a reference to any other type or phase SHALL fail validation naming the reference." Split it in two. | spec/functional/FR-103-residual-risk-record.md:53 |

## Dispositions

Round 1, head `3612073`. `quire validate` at this head reports only the two new warnings above for these files.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The FR-101 skeleton statement is split into two. |
| FND-002 | fixed | FR-102 Behavior now has six single-SHALL statements. |
| FND-003 | fixed | FR-103's decided-case statement is split into rationale and `decided_by` statements, and the role clause is removed. |
| FND-004 | fixed | The FR-107 decided and undecided cases are separate statements. |
| FND-005 | fixed | NFR-100's Statement is now three single-SHALL statements. |
| FND-006 | fixed | FR-105 now reads `outside_acceptable: true/false`, and the ambiguous-term warnings are gone. |
| FND-007 | fixed | Every FR-104 Behavior statement now names "The module's tooling" or "The module's report output" as its subject. |
| FND-008 | fixed | Round 2, head `c83872d`: FR-101 Behavior is split into a no-default statement and an if-then failure statement. |
| FND-009 | fixed | Round 2, head `c83872d`: FR-103 Behavior is split into a resolve statement and an if-then failure statement. `quire validate` now reports no EARS warnings. |
