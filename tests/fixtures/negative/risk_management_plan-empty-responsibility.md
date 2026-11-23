---
id: negative-29
title: "risk_management_plan-empty-responsibility"
type: risk_management_plan
object: risk_management_plan
expect: "Assigned to"
because: "a responsibility with no one assigned to it is refused"
---
# [negative-29] risk_management_plan-empty-responsibility

## Scope

| Scope |
| ----- |
| Brake controller, whole lifecycle. |

## Responsibilities

| Responsibility | Assigned to |
| -------------- | ----------- |
| Keep the risk file current. |  |

## Control verification methods

| Method | Applies to |
| ------ | ---------- |
| Test against the control requirements. | Every risk control. |

## Production and post-production methods

| Activity | Method |
| -------- | ------ |
| Review field reports. | Quarterly review by the safety lead. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| plan_id | UUID | 1..1 | identity |

## Invariants

The clauses this risk-management-plan declaration enforces. Each clause owns
one `ocl` fence under its own `### <clauseId>` heading; the fence text is
carried verbatim and never evaluated here.

### PlanCarriesNoScore

```ocl
context RiskManagementPlan
inv PlanCarriesNoScore:
  self.score->isEmpty()
```
