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
