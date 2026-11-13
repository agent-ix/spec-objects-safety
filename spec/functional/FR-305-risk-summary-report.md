---
id: FR-305
title: "A quoin risk summary report reads the whole chain and states what each person entered"
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
# FR-305: A quoin risk summary report reads the whole chain and states what each person entered

## Description

Tracked by Linear PLAT-1524; implemented under the quoin ticket PLAT-1576. The
quoin CLI **SHALL** provide a read-only command `quoin risk-summary <scope>
[--format markdown|json]` that reports the whole chain: hazard, hazardous
situation, harm, estimates, controls with their requirement and verification,
and the residual-risk decision. The report is a view of what people wrote. It
computes no score, assigns no region the policy does not list, and settles no
acceptance ([FR-104](./FR-104-no-computed-verdicts.md), NFR-201).

### Output contract

`--format json` writes one JSON object to standard output with the keys
`attribution` (a string) and `rows` (an array). `--format markdown` (the default)
writes the same rows as one table with the same columns and the attribution
statement above it. A row has these keys, all present, `null` or `[]` when
empty:

| Key | Content |
|---|---|
| `hazard` | the hazard id, or `null` for a situation with no hazard |
| `situation` | the situation id, or `null` for a hazard with no situation |
| `harms` | ids of harms that arise from the situation |
| `pre_control` | each pre-control estimate: id, `severity`, `probability` as entered |
| `controls` | each assumed control: id, `requirements` (ids), `verifications` (ids) |
| `post_control` | each post-control estimate: id, `severity`, `probability` as entered |
| `residual_risks` | each record: id, `decision`, `decided_by` as entered |
| `policy_region` | the policy's own label for the entered levels (FR-102), or `null` |
| `findings` | the completeness finding tokens of FR-301 to FR-303 and FR-105 that name this row |

There is one row per hazard and situation pairing. A hazard with no situation
has one row with `situation: null`. A situation with no `arises_from` edge to a
hazard has one row with `hazard: null`. A situation arising from two hazards
appears in two rows. Several estimates on one situation are all listed
(FR-203). Rows are ordered by hazard id then situation id, with `null` last.

### Read-only and deterministic

The command writes into no authored document and stores nothing. It is a
rendering and may be regenerated at will.

## Inputs

- A bundle with the safety module and the modules it references loaded; an `acceptability_policy` where regions are wanted.

## Outputs

- The report in the form above on standard output.

## Behavior

- The command SHALL list every hazard and every situation, including those missing a link.
- Where a value is absent or an epistemic member (`unknown`, `not_assessed`, `not_applicable`), the report SHALL show it as such, with no substituted scale value or blank.
- The report SHALL contain no numeric score, no ranking and no overall verdict.
- The report SHALL state that regions come from the project's policy and decisions from the named person (FR-104).
- The command SHALL modify no document.
- The command SHALL produce byte-identical output for identical inputs.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-305-AC-1 | Over a complete fixture chain, `--format json` yields one row per hazard and situation pairing, each key holding the entered value, and the output parses as one JSON object with `attribution` and `rows`. | Test |
| FR-305-AC-2 | A hazard with no situation yields a row with `situation: null` and `hazard-without-situation` in `findings`. | Test |
| FR-305-AC-3 | A fixture with `probability: not_assessed` shows `not_assessed` in its row and `policy_region: null`. | Test |
| FR-305-AC-4 | A fixture residual risk with `decision: undecided` shows `undecided`, and no row shows `accepted` that a person did not write. | Test |
| FR-305-AC-5 | No row key and no top-level key is numeric, a rank, or a verdict: the JSON keys of every row equal the set in the contract table exactly. | Test |
| FR-305-AC-6 | Running the command leaves every fixture file byte-identical. | Test |
| FR-305-AC-7 | Two runs over the same fixtures give identical output in both formats, ordered by hazard id then situation id. | Test |
| FR-305-AC-8 | A control without a verification appears in its row with `control-without-verification` in `findings`; adding the verification removes it. | Test |
| FR-305-AC-9 | A situation with no `arises_from` edge to a hazard yields a row with `hazard: null` and `situation-without-hazard` in `findings`. | Test |
| FR-305-AC-10 | Two estimates on one situation both appear in the row, and no key marks either as in force. | Test |

## Dependencies

- **Upstream**: [FR-301](./FR-301-hazard-reaches-harm-through-situation.md), [FR-302](./FR-302-risk-control-implemented-and-verified.md), [FR-303](./FR-303-residual-risk-decided-by-named-person.md), [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-104](./FR-104-no-computed-verdicts.md), [NFR-201](../non-functional/NFR-201-no-stored-or-defaulted-risk-values.md)
