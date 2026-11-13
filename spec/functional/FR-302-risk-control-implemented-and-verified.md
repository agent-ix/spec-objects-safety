---
id: FR-302
title: "Every risk control is implemented by a requirement and has a verification, declared as manifest data"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-205"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-301"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-302: Every risk control is implemented by a requirement and has a verification, declared as manifest data

## Description

Tracked by Linear PLAT-1524. A risk control with no implementing requirement is
a wish, and one with no verification is unproven. The links are authorable under
[FR-205](./FR-205-control-requirement-and-verification-links.md); this
requirement owns the completeness rules that read them and which controls they
apply to. The module declares exactly one relation per `check` token (NFR-300).

### What the rule checks

- **Implemented**: the control has an incoming `satisfies` edge from an `FR` or `NFR`.
- **Verified**: the control has an incoming `verifies` edge from any document: a test document, or a retained evidence record of an Inspection or Analysis owned by `agent-ix/engineering-assurance` and referenced by id.

The rule tests that the edge exists. It does not test that the verification
passed, and it does not test Test Matrix tagging of the verifying document;
the Test Matrix is read by its own command. No field of the control records
"effective" (FR-205). Whether the control works is read by a person from the
matrix and the evidence.

### Scope: which controls are reported

Only a control used as a risk control is in scope: a control with an outgoing
`mitigates` edge to a `hazard` or `failure_mode` (`mitigates` is written on the
control, FR-007), **or** an incoming `assumes` edge from a `risk_estimate`
(FR-204). A security control that does neither is not reported.

The `where` selector (FR-058) filters on a top-level frontmatter field of the
`from` document and cannot express this. The edge-conditioned selector is the
optional relation key `when_any` (quire-rs FR-058, ticket **PLAT-1674**): a list
of conditions, each `{verb, direction, other: [kinds]}`, where the `from`
document is in scope if any one condition holds. The scope here is therefore:

`when_any: [{verb: mitigates, direction: outgoing, other: [hazard, failure_mode]}, {verb: assumes, direction: incoming, other: [risk_estimate]}]`

The relations SHALL NOT be declared, in this module or any other, without that
scope. Declared unscoped they would report every unrelated security control.

## Inputs

- `control`, `FR`, `NFR`, test and retained-evidence documents.

## Outputs

- Advisory findings `control-without-requirement` and `control-without-verification`.

## Behavior

- The manifest SHALL declare `control-has-requirement`: `from: control`, `edges: [satisfies]`, `to: [FR, NFR]`, `direction: incoming`, `check: control-without-requirement`, with the scope above.
- The manifest SHALL declare `control-has-verification`: `from: control`, `edges: [verifies]`, `to: []`, `direction: incoming`, `check: control-without-verification`, with the scope above.
- The verification relation SHALL declare an empty `to`, so that an edge from a retained-evidence record owned by another repository counts.
- Each relation SHALL be advisory and tunable on its own `trace:<check>` key.
- The relations SHALL NOT read, set or require an `effective`, `verified`, `passed` or `status`-derived value.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-302-AC-1 | The manifest declares both relations with the fields and scope above and loads without a declaration error. | Test |
| FR-302-AC-2 | A control that mitigates a hazard, is satisfied by an `FR` and is verified by a test document yields no finding. | Test |
| FR-302-AC-3 | The same control without the `satisfies` edge yields exactly one `control-without-requirement` finding; without the `verifies` edge, exactly one `control-without-verification` finding. | Test |
| FR-302-AC-4 | A `verifies` edge from a retained-evidence record referenced by id satisfies `control-without-verification`. | Test |
| FR-302-AC-5 | A control assumed by a `post_control` estimate that mitigates no hazard is reported when it lacks either link. | Test |
| FR-302-AC-6 | A control that mitigates no hazard or failure mode and is assumed by no estimate yields neither finding. | Test |
| FR-302-AC-7 | A verification whose evidence records a failing result still satisfies the relation, and no module key records the result. | Test |
| FR-302-AC-8 | The scope is stated as the `when_any` shape above and links quire-rs ticket PLAT-1674 as its provider. | Inspection |

## Dependencies

- **Upstream**: [FR-205](./FR-205-control-requirement-and-verification-links.md), [FR-204](./FR-204-post-control-risk-estimate.md), [FR-301](./FR-301-hazard-reaches-harm-through-situation.md); `agent-ix/quire-rs` FR-058 and PLAT-1674 (edge-conditioned scope selector)
- **Downstream**: [FR-305](./FR-305-risk-summary-report.md)
