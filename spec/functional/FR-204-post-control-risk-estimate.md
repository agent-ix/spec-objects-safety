---
id: FR-204
title: "A post-control risk estimate names the controls it assumes"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-203"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-007"
    type: "depends_on"
---
# FR-204: A post-control risk estimate names the controls it assumes

## Description

PLAT-1409. A `risk_estimate` whose `phase` is `post_control`
([FR-203](./FR-203-pre-control-risk-estimate.md)) is a judgement made on the
assumption that named controls are in place. An estimate that names none cannot
be checked against anything, so a post-control estimate names them.

This is the one home of the post-control judgement. The residual-risk record of
PLAT-1523 (FR-103) references a `post_control` estimate and holds the decision;
it restates no levels, and this module declares no second post-control record.

The controls are `control` documents owned by `agent-ix/spec-objects-security`,
referenced by id and never redeclared here. The link is an edge, not a field:
the estimate authors an `assumes` relationship to each control, so quire's
target and dangling-target checks see it. A control never lists the estimates
that assume it. `assumes` is a new verb, with an inverse, in
`spec-artifacts-iso`.

All values remain person-entered as in FR-203. The module neither lowers a
post-control value because a control exists nor compares it with the
pre-control value, and it declares no check that a pre-control estimate exists.

## Inputs

- A `post_control` `risk_estimate`; `control` documents.

## Outputs

- Resolved `assumes` edges to controls; findings for missing or mismatched ones.

## Behavior

- The manifest SHALL declare `assumes` as a verb from `risk_estimate` to `control`.
- The manifest SHALL declare a required relation `post-control-assumes-control` (`from: risk_estimate`, `where: {field: phase, values: [post_control]}`, `edges: [assumes]`, `to: [control]`, `direction: outgoing`, `check: post-control-without-control`), advisory and tunable on its own `trace:<check>` key.
- The relation SHALL NOT report a `pre_control` estimate.
- The relation SHALL be this requirement's own: the completeness relations of PLAT-1524 (FR-301, FR-303) do not cover `assumes`, and this requirement duplicates none of them.
- Quire SHALL report `disallowed-edge-target` naming the target type for an `assumes` edge to any document type other than `control`.
- Quire SHALL make `quire validate --okf --strict` exit non-zero for an `assumes` edge to an undeclared local id, as FR-007 specifies.
- The module SHALL NOT compare a post-control estimate with a pre-control one.
- The module SHALL NOT reject a post-control value for being equal to or worse than a pre-control value.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-204-AC-1 | A `post_control` fixture with one `assumes` edge to a `control` validates, and `quire extract` shows the resolved incoming edge on the control. | Test |
| FR-204-AC-2 | A `post_control` fixture with no `assumes` edge yields exactly one `post-control-without-control` warning naming it and exit 0; adding an `assumes` edge to a `control` removes it. | Test |
| FR-204-AC-7 | A `pre_control` fixture with no `assumes` edge yields no `post-control-without-control` finding. | Test |
| FR-204-AC-8 | `--severity trace:post-control-without-control=error` makes the run exit non-zero; with no flag it exits 0. | Test |
| FR-204-AC-9 | An `assumes` edge to an undeclared local id does not satisfy the relation, because `to` is constrained. | Test |
| FR-204-AC-3 | An `assumes` edge to a `hazard` is reported `disallowed-edge-target` naming `hazard`. | Test |
| FR-204-AC-4 | An `assumes` edge to an undeclared local id makes `quire validate --okf --strict` exit non-zero with stderr naming the path, `assumes` and the id. | Test |
| FR-204-AC-5 | A fixture whose post-control severity string equals or ranks worse than its pre-control severity validates with no diagnostic. | Test |
| FR-204-AC-6 | A situation with only a `post_control` estimate validates with no diagnostic. | Test |

## Dependencies

- **Upstream**: [FR-203](./FR-203-pre-control-risk-estimate.md); `agent-ix/spec-objects-security` FR-007 (`control`); the `assumes` verb in `spec-artifacts-iso`
- **Downstream**: [FR-205](./FR-205-control-requirement-and-verification-links.md); PLAT-1523 FR-103
