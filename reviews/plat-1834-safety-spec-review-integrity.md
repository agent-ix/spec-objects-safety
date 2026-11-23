---
id: SR-418
title: "Spec review (integrity) — spec-objects-safety PLAT-1834 FR-108, FR-104"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-108-risk-management-plan.md, spec/functional/FR-104-no-computed-verdicts.md, spec/functional/index.md (git diff origin/main...dbd860e, PR #50)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-108", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-104", type: references }
---

## Summary

Ticket: PLAT-1834. Examined FR-108 (Description, Inputs, Outputs, Behavior,
six ACs, Dependencies), the FR-104 Inputs edit and the index line.
`quire validate --scope .` on the three files exits 0 (one EARS warning,
SR-419).

FR-108 satisfies StR-001 and depends on FR-101, the policy it references.
The ticket's demands are present: scope, responsibilities, acceptability
criteria as a reference (a `references` edge, never the criteria), planned
control-verification methods, planned production and post-production methods;
no score, class, acceptability or approval property; no shipped plan. ISO
14971 is not quoted or cited. The index line and the FR-104 Inputs addition
are consistent with the new type.

## Verdict

Consistent and complete for the ticket, with two small integrity defects: the
Outputs promise more than the Behavior and ACs specify, and the "at least one
row" rule and the skeleton statement are imprecise.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | Outputs promise "a validation failure naming the offending table and column", but the Behavior statement and AC-3 require only "naming the table". Two implementers would read the column requirement differently. Align them: either drop "and column" from Outputs or add the column to the Behavior statement and AC-3 (the negative fixture already asserts the `Assigned to` column). | spec/functional/FR-108-risk-management-plan.md:34, spec/functional/FR-108-risk-management-plan.md:44, spec/functional/FR-108-risk-management-plan.md:57 |
| FND-002 | low | "each with at least one row" is folded into the four-tables statement and no AC covers it. AC-3 replaces a cell, never removes a row. The rule holds today (a zero-row table fails as `required ... is empty` and `0 data row(s)`, measured), but nothing would catch its loss. Add a zero-row case to AC-3 or a separate AC. The skeleton statement "SHALL contain placeholders only" is also inexact: the skeleton ships a filled `plan_id` identity row and the `PlanCarriesNoScore` invariant. Say "every table row is a placeholder". | spec/functional/FR-108-risk-management-plan.md:39, spec/functional/FR-108-risk-management-plan.md:49 |
