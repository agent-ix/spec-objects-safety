---
id: FR-303
title: "Every post-control estimate has a residual-risk record, and the decision and decider are enforced by the schema and the discrepancy report"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-105"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-104"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-303: Every post-control estimate has a residual-risk record, and the decision and decider are enforced by the schema and the discrepancy report

## Description

Tracked by Linear PLAT-1524. Acceptance of residual risk is a human decision
([FR-104](./FR-104-no-computed-verdicts.md)). The completeness rules check that
the decision exists and is attributed, never what it is. The rule has three
parts and each is owned where the engine can express it.

| Part | Owner |
|---|---|
| A post-control estimate has a residual-risk record | this requirement, a manifest relation |
| The decision is made (`undecided` is not a decision) | FR-105, finding `residual-risk-undecided` |
| The decider is a named person | FR-103, schema rule on `decided_by` |
| An accepted risk outside the acceptable region has a benefit-risk record | FR-105, finding `accepted-outside-acceptable-region` |

The last three are not manifest relations because a relation tests that an edge
exists and has no test on a field value of the document at the other end
(FR-058), and the region test needs policy data that is not in the manifest
(FR-101). This requirement does not restate them or their criteria.

### The relation

[FR-103](./FR-103-residual-risk-record.md) gives a `residual_risk` an `estimate`
reference to one post-control `risk_estimate`. The relation uses that reference
as an edge: `edges: [estimate]`, authored on the residual risk, so it is
incoming on the estimate. The reference SHALL be a frontmatter relationship
whose verb is `estimate`, so quire's edge checks see it; FR-103 owns that.

`where` (FR-058) reads a top-level frontmatter key of the `from` document.
`phase` therefore SHALL be a top-level frontmatter key of `risk_estimate`, and
not a body-extracted field, for the relation to select only post-control
estimates. [FR-203](./FR-203-pre-control-risk-estimate.md) owns the schema; this
requirement states the dependency so that the two PRs agree.

## Inputs

- `risk_estimate` documents and `residual_risk` documents.

## Outputs

- The advisory finding `post-control-estimate-without-decision`.

## Behavior

- The manifest SHALL declare `post-control-estimate-has-decision`: `from: risk_estimate`, `where: {field: phase, values: [post_control]}`, `edges: [estimate]`, `to: [residual_risk]`, `direction: incoming`, `check: post-control-estimate-without-decision`.
- The relation SHALL NOT report a `pre_control` estimate.
- The relation SHALL be satisfied by a `residual_risk` whose `decision` is `undecided`, because it tests that a record exists.
- The relation SHALL produce a finding only.
- The relation SHALL be advisory and tunable on its own `trace:<check>` key.
- The module SHALL declare `phase` as a top-level frontmatter key of `risk_estimate`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-303-AC-1 | The manifest declares the relation with the fields above and loads without a declaration error. | Test |
| FR-303-AC-2 | A `post_control` estimate with no residual-risk record yields exactly one `post-control-estimate-without-decision` finding naming the estimate. | Test |
| FR-303-AC-3 | A `pre_control` estimate with no residual-risk record yields no finding. | Test |
| FR-303-AC-4 | A residual-risk record referencing the estimate removes the finding whatever its `decision`, including `undecided`. | Test |
| FR-303-AC-5 | The emitted `risk_estimate` schema and skeleton carry `phase` as a top-level frontmatter key, and a fixture with `phase` in the body only is reported by the relation as an unselected estimate (no finding) and by validation as invalid. | Test |
| FR-303-AC-6 | The manifest holds no policy region, level, score or default decision. | Inspection |

## Dependencies

- **Upstream**: [FR-103](./FR-103-residual-risk-record.md), [FR-104](./FR-104-no-computed-verdicts.md), [FR-105](./FR-105-decision-policy-discrepancy-report.md), [FR-203](./FR-203-pre-control-risk-estimate.md), [FR-204](./FR-204-post-control-risk-estimate.md); `agent-ix/quire-rs` FR-058 (`where`)
- **Downstream**: [FR-305](./FR-305-risk-summary-report.md)
