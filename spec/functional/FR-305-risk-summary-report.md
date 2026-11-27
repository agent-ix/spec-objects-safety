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
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
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
empty. `policy_region` is a key of each estimate entry, not of the row: it is the
policy's own label for that estimate's entered levels (FR-102), or `null`:

| Key | Content |
|---|---|
| `hazard` | the hazard id, or `null` for a situation with no hazard |
| `situation` | the situation id, or `null` for a hazard with no situation |
| `harms` | ids of harms that arise from the situation |
| `pre_control` | each pre-control estimate: `estimate` (the id), `severity`, `probability` as entered, and `policy_region` |
| `controls` | each assumed control: `control` (the id), `requirements` (ids), `implementation_verifications` (ids), `effectiveness_verifications` (ids) |
| `post_control` | each post-control estimate: `estimate` (the id), `severity`, `probability` as entered, and `policy_region` |
| `residual_risks` | each record: `residual_risk` (the id), `decision`, `decided_by` as entered |
| `findings` | finding objects with exactly the keys `finding` (the token) and `names` (the ids the token names, `[]` when none), for the completeness tokens of FR-301 to FR-303, FR-204 (`post-control-without-control`) and FR-105 that name this row |

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

The report contract is owned by Quoin FR-169 and FR-170, which carry its
acceptance criteria and tests. See
[Quoin FR-169](https://github.com/agent-ix/quoin/blob/main/spec/functional/FR-169-risk-summary-command.md)
and [Quoin FR-170](https://github.com/agent-ix/quoin/blob/main/spec/functional/FR-170-risk-summary-row-findings.md).

## Dependencies

- **Upstream**: [FR-301](./FR-301-hazard-reaches-harm-through-situation.md), [FR-302](./FR-302-risk-control-implemented-and-verified.md), [FR-303](./FR-303-residual-risk-decided-by-named-person.md), [FR-204](./FR-204-post-control-risk-estimate.md), [FR-102](./FR-102-estimate-levels-resolve-in-policy.md), [FR-104](./FR-104-no-computed-verdicts.md), [NFR-201](../non-functional/NFR-201-no-stored-or-defaulted-risk-values.md)
