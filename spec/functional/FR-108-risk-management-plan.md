---
id: FR-108
title: "A risk management plan records scope, responsibilities, control-verification and production methods, and references the acceptability criteria"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "depends_on"
---
# FR-108: A risk management plan records scope, responsibilities, control-verification and production methods, and references the acceptability criteria

## Description

Tracked by Linear PLAT-1834. A risk management process starts from a plan that
people write: what the plan covers, who is responsible for what, how the risk
controls will be verified, and how production and post-production information
will be collected. The module SHALL declare a `risk_management_plan` object
type holding those four parts and a reference to the acceptability criteria.

The plan holds a reference to the acceptability criteria, never the criteria.
The criteria are the `acceptability_policy` ([FR-101](./FR-101-acceptability-policy.md))
that people wrote; the plan names it with a `references` relationship. People
accept risk. The plan records no score, class, acceptability or approval, and
the module ships no plan, no default responsibility and no default method.

## Inputs

- A document of type `risk_management_plan` authored by a person.
- The module manifest and the emitted schema for the type.

## Outputs

- A validated plan document, or a validation failure naming the offending table and, for a cell, its column.
- A warning, `plan-without-acceptability-criteria`, naming a plan that references no acceptability policy.

## Behavior

- The `risk_management_plan` type SHALL require four tables: scope, responsibilities, control verification methods, and production and post-production methods, each with at least one row.
- The scope table SHALL have one column, `Scope`.
- The responsibilities table SHALL have the columns `Responsibility` and `Assigned to`.
- The control verification methods table SHALL have the columns `Method` and `Applies to`.
- The production and post-production methods table SHALL have the columns `Activity` and `Method`.
- If a table cell is empty or an unfilled placeholder, then validation SHALL fail naming the table and the column.
- If a table has no data row, then validation SHALL fail naming the table.
- The type SHALL allow `references` edges to `acceptability_policy` documents and no other type.
- If a plan references no `acceptability_policy`, then the tooling SHALL report `plan-without-acceptability-criteria` naming the plan, as a warning.
- The schema SHALL NOT declare a score, class, acceptability or approval property.
- The module SHALL NOT ship a plan document, a default responsibility or a default method.
- The skeleton SHALL carry a placeholder in every plan row.
- The skeleton SHALL carry no other content than its plan rows, its identity row and its invariant clause.
- The skeleton SHALL fail validation until a person fills every plan row.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-108-AC-1 | The emitted manifest declares a `risk_management_plan` type whose locators require the scope, responsibilities, control verification and production and post-production tables. | Test |
| FR-108-AC-2 | The skeleton with every placeholder filled validates, and the skeleton as shipped fails validation. | Test |
| FR-108-AC-3 | For each of the four tables, a fixture with one cell left as a placeholder fails validation naming the table and the column of that cell, for every cell of the four tables. | Test |
| FR-108-AC-4 | A plan with one `references` edge to an `acceptability_policy` document validates without `plan-without-acceptability-criteria`; a plan with no such edge yields that warning once, naming the plan. | Test |
| FR-108-AC-5 | A `references` edge from a plan to a `hazard` document is disallowed, naming the type. | Test |
| FR-108-AC-6 | Neither the emitted schema, the manifest's `risk_management_plan` locators and columns, nor the skeleton's headings and table headers declare a score, class, acceptability or approval, and the package contains no document of type `risk_management_plan` other than the unfilled skeleton. | Test |
| FR-108-AC-7 | A fixture with a table that has no data row fails validation naming that table, for each of the four tables. | Test |

## Dependencies

- **Upstream**: [FR-101](./FR-101-acceptability-policy.md)
- **Downstream**: quoin FR-200 (the dossier risk management plan renders this record).
