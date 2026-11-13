---
id: FR-203
title: "A pre-control risk estimate records person-entered severity and probability for a hazardous situation"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-202"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-004"
    type: "depends_on"
---
# FR-203: A pre-control risk estimate records person-entered severity and probability for a hazardous situation

## Description

PLAT-1409. The module declares `risk_estimate` as an object type whose `phase`
is `pre_control` or `post_control`. This requirement fixes the shape and the
pre-control case; [FR-204](./FR-204-post-control-risk-estimate.md) adds what a
post-control estimate names.

An estimate is the record of one person's judgement of how bad (`severity`) and
how likely (`probability`) the harm is for one hazardous situation, before any
control is assumed.

### Levels are the project's, checked against its policy

The levels on an estimate are values a person enters. The module does not fix
them to a closed list: the project's acceptability policy (PLAT-1523, FR-101)
names the severity and probability levels, and the check of an estimate's
levels against the policy is FR-102 there. The estimate schema therefore types
`severity` and `probability` as non-empty strings that are none of the three
`EpistemicState` members (`unknown`, `not_assessed`, `not_applicable`) of
[FR-004](./FR-004-type-distinct-safety-schemas.md), or as exactly one of those
members. A project cannot name a level `not_assessed`, so a marker stays
distinct from every level. The `Severity` and `Likelihood` lists of FR-004 remain the
vocabulary of `hazard.assessment` and constrain nothing on an estimate.

`probability` is the chance that the situation leads to the harm. That is not
the hazard-state frequency the existing `likelihood` entry defines, so the
manifest `lexicon` gains an entry `probability`.

### Entered, never derived

Every value on an estimate is entered by a named person. The module declares no
default for severity, probability or phase, and derives no score, region or
acceptance. Those prohibitions are stated once, in PLAT-1523 FR-104, and apply
here; this requirement adds no second statement of them. An absent value stays
absent.

### Relation to other judgements

- **`hazard.assessment`** (FR-004) is the judgement of the hazard state as such. A `risk_estimate` is the judgement of one hazardous situation. They are different subjects, neither supersedes the other, and the module derives neither from the other. An author who records both enters both.
- **Security `risk`** (`agent-ix/spec-objects-security`) is a register entry for a threat or vulnerability. A `risk_estimate` is not a `risk`: it estimates harm in one hazardous situation, declares none of `risk`'s fields and does not redeclare the type (FR-004). The two meet only by id reference, if an author chooses to reference one.
- **Provenance.** The estimate carries FR-004's `Provenance`, including `assertedAt`. The residual-risk decision (PLAT-1523 FR-103) differs: it takes decision time from version control.

## Inputs

- A `hazardous_situation` ([FR-202](./FR-202-hazardous-situation-object-and-chain.md)).

## Outputs

- A `risk_estimate` object type, schema and skeleton; a resolved `estimates` edge to a situation.

## Behavior

- The manifest SHALL declare `risk_estimate` and export it in `semantic.exports`.
- The schema SHALL require `phase`.
- The schema SHALL require `severity` and `probability`.
- The schema SHALL require `rationale` and `provenance`, with `assertedBy` and `assertedAt`.
- The schema SHALL give `phase` the members `pre_control` and `post_control` and no default.
- The schema SHALL type `severity` and `probability` as a non-empty string that equals none of the `EpistemicState` members, or as one of those members.
- The module SHALL declare `phase` as a top-level frontmatter key of `risk_estimate`, so that required relations can select on it.
- The schema SHALL forbid the keys `score`, `region`, `level`, `acceptable` and `acceptance`.
- The module SHALL NOT enforce an absence of `assumes` edges on a `pre_control` estimate: edges are frontmatter relationships that the record schema does not see, and no engine mechanism rejects an edge by the source's field value.
- The manifest SHALL declare `estimates` as a verb from `risk_estimate` to `hazardous_situation`, a new entry with an inverse in `spec-artifacts-iso`.
- The manifest SHALL declare a required relation `estimate-has-situation` (`from: risk_estimate`, `edges: [estimates]`, `to: [hazardous_situation]`, `direction: outgoing`, `check: estimate-without-situation`), advisory and tunable on its own key. The engine tests presence, not count, so an upper bound of one is not enforced.
- The module SHALL ship a skeleton whose severity, probability and phase are placeholders that fail validation until a person replaces them.
- The module SHALL leave the choice among several estimates of one situation to the people who authored them.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-203-AC-1 | A `pre_control` estimate fixture with every required field and an `estimates` edge to a situation validates. | Test |
| FR-203-AC-2 | Removing each of `phase`, `severity`, `probability`, `rationale` or `provenance` in turn makes validation fail, one fixture per field. | Test |
| FR-203-AC-3 | `severity: unknown`, `not_assessed` and `not_applicable` are each accepted and stay distinct from every level string in the extracted data. | Test |
| FR-203-AC-4 | A fixture whose severity is a level string that appears in no FR-004 list validates; an empty string fails. | Test |
| FR-203-AC-5 | A fixture with `score`, `region`, `level`, `acceptable` or `acceptance` fails validation. | Test |
| FR-203-AC-6 | `phase` is a top-level frontmatter key in the shipped skeleton and in every fixture, and not a body-extracted field. | Inspection |
| FR-203-AC-7 | The shipped `risk_estimate` skeleton fails validation as shipped. | Test |
| FR-203-AC-8 | An `estimates` edge to anything but a `hazardous_situation` is reported `disallowed-edge-target` naming the type. | Test |
| FR-203-AC-9 | An estimate with no `estimates` edge yields exactly one `estimate-without-situation` warning and exit 0; adding the edge removes it. | Test |
| FR-203-AC-10 | An estimate with two `estimates` edges to two situations validates with no diagnostic, and the module reports no upper-bound finding. | Test |
| FR-203-AC-11 | Two estimates of one situation both validate, and neither extraction nor validation output designates one of them. | Test |
| FR-203-AC-12 | A `hazard` fixture with `assessment` and a `risk_estimate` of its situation validate together, and no output derives one from the other. | Test |
| FR-203-AC-13 | The manifest `lexicon` has an entry `probability`, and the module declares no type named `risk`. | Inspection |
| FR-203-AC-14 | The emitted schema's level branch excludes `unknown`, `not_assessed` and `not_applicable`, and a fixture with `severity: not_assessed` validates only through the marker branch, which extraction reports as an `EpistemicState`, never as a level. | Test |

## Dependencies

- **Upstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md); [FR-004](./FR-004-type-distinct-safety-schemas.md); PLAT-1523 FR-101, FR-102 and FR-104 (levels, level check, no computed verdicts); `estimates` verb in `spec-artifacts-iso`
- **Downstream**: [FR-204](./FR-204-post-control-risk-estimate.md)
