---
id: RMP-001
title: "ProjectRiskManagementPlan"
type: risk_management_plan
object: risk_management_plan
---
<!-- risk_management_plan authoring skeleton (spec-objects-safety). THIS
     SKELETON FAILS VALIDATION AS SHIPPED, ON PURPOSE: every row is a
     placeholder that your project's people replace. This module ships no plan,
     no default responsibility and no default method, and no tool fills one in.
     Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: risk_management_plan,
       object: risk_management_plan.
     - "## Scope" (H2) is REQUIRED: header exactly `Scope`, one row per
       statement of what the plan covers (the product, the lifecycle phases),
       at least one row.
     - "## Responsibilities" (H2) is REQUIRED: header exactly
       `Responsibility | Assigned to`, one row per responsibility, naming the
       person or role it is assigned to.
     - "## Control verification methods" (H2) is REQUIRED: header exactly
       `Method | Applies to`, one row per planned method for verifying that
       risk controls are implemented and effective.
     - "## Production and post-production methods" (H2) is REQUIRED: header
       exactly `Activity | Method`, one row per planned way of collecting and
       reviewing production and post-production information.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     THE ACCEPTABILITY CRITERIA ARE REFERENCED, NOT WRITTEN HERE. Link the plan
     to the acceptability policy your people wrote, one `references`
     relationship, at least one:

       relationships:
         - target: POL-001
           type: references

     People accept risk. No score, class, acceptability or approval is
     recorded in this plan, and no tool computes or defaults one. -->
# [RMP-001] ProjectRiskManagementPlan

## Scope

| Scope |
| ----- |
| <what the plan covers> |

## Responsibilities

| Responsibility | Assigned to |
| -------------- | ----------- |
| <responsibility> | <person or role> |

## Control verification methods

| Method | Applies to |
| ------ | ---------- |
| <planned verification method> | <the controls it verifies> |

## Production and post-production methods

| Activity | Method |
| -------- | ------ |
| <production or post-production activity> | <how it is carried out> |

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
