---
id: FR-305
title: "A risk summary report reads the whole chain and states what each person entered"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-301"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-302"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-303"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-102"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-104"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/NFR-201"
    type: "depends_on"
---
# FR-305: A risk summary report reads the whole chain and states what each person entered

## Description

Tracked by Linear PLAT-1524. The tooling **SHALL** provide a read-only risk
summary report over the whole chain: hazard, hazardous situation, harm,
estimates, controls with their requirement and verification, and the residual
risk decision. The report is a view of what people wrote. It computes no score,
assigns no region the policy does not list, and settles no acceptance
([FR-104](./FR-104-no-computed-verdicts.md), NFR-201).

### Rows

One row per hazard and situation pairing. Each row carries, by reference and as
written in the source documents:

| Column | Source |
|---|---|
| hazard, situation, harm(s) | the chain edges (FR-301) |
| pre-control estimate | severity and probability as entered, or the epistemic member as entered |
| controls | the controls the post-control estimate assumes, each with its implementing requirement and its verification (FR-302) |
| post-control estimate | as entered |
| residual risk | `decision`, `decided_by` as entered; `undecided` shown as `undecided` |
| policy region | the policy's own label for the entered levels, labelled "the policy says" (FR-102); absent when a level is unassessed |
| open findings | the completeness findings of FR-301 to FR-303 and FR-105 that name this row |

Several estimates on one situation are all listed. The report does not choose
between them (FR-203).

### Read-only and deterministic

The report writes into no authored document. It is a rendering and may be
regenerated at will; it is not stored as a source of truth and carries no
decision date. The tooling that hosts it is chosen by the owning quire and
quoin tickets, and is an open question for the planner.

## Inputs

- A bundle with the safety module and the modules it references loaded; an `acceptability_policy` where regions are wanted.

## Outputs

- A report in a human-readable form and a machine-readable form carrying the same rows.

## Behavior

- The report SHALL list every hazard, including a hazard with no situation, as a row with its open `hazard-without-situation` finding.
- Where a value is absent or an epistemic member (`unknown`, `not_assessed`, `not_applicable`), the report SHALL show it as such, with no substituted scale value or blank.
- The report SHALL contain no numeric score, no ranking, no ordering by risk, no overall verdict, and no `acceptable`/`unacceptable` word that does not come from a policy label or a person's decision.
- The report SHALL state that regions come from the project's policy and decisions from the named person (FR-104).
- The report SHALL modify no document and SHALL produce byte-identical output for identical inputs, ordered by hazard id then situation id.
- A chain object that lacks the link a finding names SHALL appear in the report with that finding.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-305-AC-1 | Over a complete fixture chain, the report has one row per hazard and situation pairing, each column holding the entered value. | Test |
| FR-305-AC-2 | A hazard with no situation appears as a row naming `hazard-without-situation`. | Test |
| FR-305-AC-3 | A fixture with `probability: not_assessed` shows `not_assessed` in the row and no policy region. | Test |
| FR-305-AC-4 | A fixture residual risk with `decision: undecided` shows `undecided`, and no row shows `accepted` that a person did not write. | Test |
| FR-305-AC-5 | The report contains no numeric score field, no sort by risk, and no overall verdict; the machine-readable schema declares none. | Inspection |
| FR-305-AC-6 | Running the report leaves every fixture file byte-identical. | Test |
| FR-305-AC-7 | Two runs over the same fixtures give identical output, and the order is by hazard id then situation id. | Test |
| FR-305-AC-8 | The output contains the attribution statement naming the policy as the source of regions and the named person as the source of decisions. | Test |
| FR-305-AC-9 | A control without a verification appears in its row with `control-without-verification`; adding the verification removes the finding from the row. | Test |
| FR-305-AC-10 | Two estimates on one situation both appear, and the report does not mark either as the one in force. | Test |

## Dependencies

- **Upstream**: [FR-301](./FR-301-hazard-reaches-harm-through-situation.md), [FR-302](./FR-302-risk-control-implemented-and-verified.md), [FR-303](./FR-303-residual-risk-decided-by-named-person.md), [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-104](./FR-104-no-computed-verdicts.md), [NFR-201](../non-functional/NFR-201-no-stored-or-defaulted-risk-values.md)
