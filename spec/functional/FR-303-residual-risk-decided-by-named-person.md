---
id: FR-303
title: "Every risk with a post-control estimate has a residual-risk decision by a named person, and an accepted risk outside the acceptable region has a benefit-risk record"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-105"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-106"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-104"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-303: Every risk with a post-control estimate has a residual-risk decision by a named person, and an accepted risk outside the acceptable region has a benefit-risk record

## Description

Tracked by Linear PLAT-1524. Acceptance of residual risk is a human decision
([FR-104](./FR-104-no-computed-verdicts.md)). The completeness rules therefore
check that the decision **exists and is attributed**, and never what it is.
They split by what the engine can express.

### Existence: manifest data

A post-control estimate ([FR-204](./FR-204-post-control-risk-estimate.md))
with no `residual_risk` record ([FR-103](./FR-103-residual-risk-record.md)) is a
judgement nobody has decided on. A relation with `where` (FR-058) selects only
post-control estimates by their `phase` field, so a pre-control estimate is
never reported.

### Decidedness and person: schema and report, not manifest

Two parts of the ticket's rule cannot be a required relation. A relation tests
whether an edge exists, and cannot test the value of a field on the document
at the other end. "The decision is not `undecided`" and "`decided_by` names a
person" are field values of the residual risk.

- The person rule is already a schema rule: FR-103 requires a non-empty `decided_by` naming a person when the decision is `accepted` or `not_accepted`, and forbids it when `undecided`.
- The decided rule is the advisory finding `residual-risk-undecided` of [FR-105](./FR-105-decision-policy-discrepancy-report.md).
- The benefit-risk rule is FR-105's `accepted-outside-acceptable-region`: the policy marks which regions are outside the acceptable one, so the rule needs policy data, and policy data is not in the manifest (FR-101).

This is an engine gap and is stated, not hidden: a required relation has no
field-value test on its target. This requirement does not ask quire-rs to gain
one. The schema and the FR-105 report cover the rule, and this spec records
that coverage so a reader does not look for a manifest entry that is not there.

### Engine gap: the reference from residual risk to estimate

FR-103 gives `residual_risk` a reference to "the risk it concerns" and does not
name its edge verb or target type. This requirement assumes the reference
targets the `risk_estimate` the decision is about and is authored on the
residual risk, as the situation authors its edges (FR-202). If FR-103 settles a
different target, the `to` list and `from` below follow it. The relation is
otherwise independent of that choice.

## Inputs

- `risk_estimate` documents with `phase: post_control`, and `residual_risk` documents.

## Outputs

- The advisory finding `post-control-estimate-without-decision`, plus the existing FR-105 findings, unchanged.

## Behavior

- The manifest SHALL declare `post-control-estimate-has-decision`: `from: risk_estimate`, `where: {field: phase, values: [post_control]}`, `edges:` the reference verb FR-103 declares, `to: [residual_risk]`, `direction: incoming`, `check: post-control-estimate-without-decision`.
- A `pre_control` estimate SHALL NOT be reported by this relation.
- A `residual_risk` with `decision: undecided` SHALL satisfy this relation, because the relation tests that a record exists, and the `undecided` state is reported by FR-105 under `residual-risk-undecided`.
- The relation SHALL produce a finding only and SHALL NOT create or change a residual-risk record on a person's behalf (FR-104).
- The relation SHALL be advisory and tunable on its own `trace:<check>` key.
- Every case below that a relation cannot express SHALL be covered by the schema or the FR-105 report, as stated in this requirement.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-303-AC-1 | The manifest declares `post-control-estimate-has-decision` with the fields above and loads without a declaration error. | Test |
| FR-303-AC-2 | A `post_control` estimate with no residual-risk record yields exactly one `post-control-estimate-without-decision` finding naming the estimate. | Test |
| FR-303-AC-3 | A `pre_control` estimate with no residual-risk record yields no finding. | Test |
| FR-303-AC-4 | Adding a residual-risk record that references the estimate removes the finding, whatever its `decision`. | Test |
| FR-303-AC-5 | A residual-risk record with `decision: undecided` yields `residual-risk-undecided` (FR-105) and no `post-control-estimate-without-decision`. | Test |
| FR-303-AC-6 | A residual-risk record with `decision: accepted` and no `decided_by` fails validation (FR-103), so the person rule is enforced by the schema and not by a relation. | Test |
| FR-303-AC-7 | An `accepted` residual risk in a region the policy marks outside the acceptable region, with no benefit-risk record, yields `accepted-outside-acceptable-region` (FR-105). | Test |
| FR-303-AC-8 | Running the check over fixtures leaves every fixture byte-identical and writes no `decision`, `decided_by` or rationale. | Test |
| FR-303-AC-9 | The manifest holds no policy region, level, score or default decision. | Inspection |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md), [FR-104](./FR-104-no-computed-verdicts.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md), [FR-106](./FR-106-benefit-risk-record.md), [FR-204](./FR-204-post-control-risk-estimate.md); `agent-ix/quire-rs` FR-058 (`where`)
- **Downstream**: [FR-305](./FR-305-risk-summary-report.md)
