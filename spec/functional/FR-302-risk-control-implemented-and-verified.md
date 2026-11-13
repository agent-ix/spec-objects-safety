---
id: FR-302
title: "Every risk control is implemented by a requirement and has a verification, declared as manifest data"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-205"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-301"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
  - target: "ix://agent-ix/engineering-assurance/FR-078"
    type: "depends_on"
---
# FR-302: Every risk control is implemented by a requirement and has a verification, declared as manifest data

## Description

Tracked by Linear PLAT-1524. A risk control with no implementing requirement
is a wish, and one with no verification is unproven. The links are authorable
under [FR-205](./FR-205-control-requirement-and-verification-links.md); this
requirement fixes the completeness rules that read them, and fixes which
documents they apply to.

The two relations of FR-205 (`control-without-requirement` and
`control-without-verification`) are the rules. This requirement is the single
declaration of them, and FR-205 SHALL NOT declare a second copy.

### What counts as verified effective

A `verifies` edge to the control from either of:

- a test document whose acceptance criteria are tagged in the computed Test Matrix, or
- a retained evidence record of an Inspection or Analysis (`agent-ix/engineering-assurance` FR-078), referenced by id.

The rule tests that the edge exists. It does not test that the verification
passed, and no field of the control records "effective" (FR-205). Whether the
control works is read by a person from the matrix and the evidence.

### Engine gap: scope by incoming edge

Only controls used as risk controls should be reported: a control that mitigates
a hazard or is assumed by a post-control estimate. A control of
`agent-ix/spec-objects-security` that does neither is outside this module's
concern. The `where` selector (FR-058) filters on a field of the `from` document;
it cannot filter on "has an incoming `mitigates` or `assumes_controls` edge".
The engine therefore lacks this scoping.

This requirement names the gap and does not assume it away. The target is a
selector in `agent-ix/quire-rs` that narrows `from` documents by the presence of
an incoming edge of a named verb, declared as manifest data like every other
field. Until that selector exists, the two relations SHALL NOT be declared
unscoped (that would report every unrelated security control, against
FR-205-AC-5), and the module SHALL ship FR-205 behaviour for these two checks
only once the selector is available. The quire-rs ticket for the selector is
an open question for the planner.

## Inputs

- `control`, `FR`, `NFR`, test and retained-evidence documents.

## Outputs

- Advisory findings `control-without-requirement` and `control-without-verification`.

## Behavior

- The manifest SHALL declare `control-has-requirement`: `from: control`, `edges: [satisfies]`, `to: [FR, NFR]`, `direction: incoming`, `check: control-without-requirement`, scoped by the incoming-edge selector to controls with an incoming `mitigates` edge from, or an `assumes_controls` reference by, a risk document.
- The manifest SHALL declare `control-has-verification`: `from: control`, `edges: [verifies]`, `to: []`, `direction: incoming`, `check: control-without-verification`, with the same scope.
- `to` for the verification relation SHALL be empty, so that an edge from a retained-evidence record owned by another repository counts.
- Each relation SHALL be advisory and tunable on its own `trace:<check>` key.
- The relations SHALL NOT read, set or require an `effective`, `verified`, `passed` or `status`-derived value.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-302-AC-1 | The manifest declares both relations with the fields above and loads without a declaration error. | Test |
| FR-302-AC-2 | A control that mitigates a hazard, is satisfied by an `FR` and is verified by a test document yields no finding. | Test |
| FR-302-AC-3 | The same control without the `satisfies` edge yields exactly one `control-without-requirement` finding; without the `verifies` edge it yields exactly one `control-without-verification` finding. | Test |
| FR-302-AC-4 | A `verifies` edge from a retained-evidence record referenced by id satisfies `control-without-verification`. | Test |
| FR-302-AC-5 | A control assumed by a `post_control` estimate and mitigating no hazard is reported when it lacks either link. | Test |
| FR-302-AC-6 | A control that mitigates no hazard and is assumed by no estimate yields neither finding. | Test |
| FR-302-AC-7 | A verification that failed (evidence records a failing result) still satisfies the relation, and no module key records the result. | Test |
| FR-302-AC-8 | The spec names the incoming-edge scoping as an engine gap and links the quire-rs ticket that supplies it. | Inspection |

## Dependencies

- **Upstream**: [FR-205](./FR-205-control-requirement-and-verification-links.md), [FR-301](./FR-301-hazard-reaches-harm-through-situation.md); `agent-ix/quire-rs` FR-058 and the scoping selector it lacks; `agent-ix/engineering-assurance` FR-078
- **Downstream**: [FR-305](./FR-305-risk-summary-report.md)
