---
id: FR-205
title: "A risk control links to the requirement that implements it and the verification that shows it is effective"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-204"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-security/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-302"
    type: "depends_on"
---
# FR-205: A risk control links to the requirement that implements it and the verification that shows it is effective

## Description

PLAT-1409. A control that no requirement implements is a wish, and a control
nothing shows to be effective is an unproven one. The `control` type belongs to
`agent-ix/spec-objects-security`; this requirement fixes the two links a
`control` used as a risk control carries, so a person can author them and a
tool can read them. Nothing here redeclares `control`.

### Edges

| Link | Authored on | Edge | Target |
|---|---|---|---|
| control to requirement | the requirement (`FR` or `NFR`) | `satisfies` (shared vocabulary; inverse `satisfied_by`) | a `control` |
| control to effectiveness verification | a test document (`IT` or `TC`) | `verifies` (shared vocabulary) | a `control` |

The control never lists its own requirement or verification, for the reason
given in FR-007. Both verbs are accepted today with no widening in either
module; the criteria below therefore assert the resolved incoming edge, which
can fail, and not the absence of a diagnostic, which cannot.

### Retained evidence

The second verification route is a retained-evidence record of an Inspection or
Analysis, owned by `agent-ix/engineering-assurance`. It verifies a control the
same way a test does: through a `verifies` edge it authors to the control,
referenced by id. FR-302 owns which controls must have such an edge. This module
copies no evidence record.

### Effectiveness is a link, not a verdict

A link to a verification says a verification exists. Whether it passed, and
whether the control is therefore effective, is recorded by the evidence and
read by a person. The module stores no `effective`, `verified` or `passed`
value on a control.

### Completeness rules

The rules that report a control with no requirement or no verification
(`control-without-requirement`, `control-without-verification`) are declared
once, in PLAT-1524 (FR-302). This requirement does not declare them. They apply
only to controls used as risk controls, meaning controls that mitigate a hazard
or that a post-control estimate assumes. Selecting documents by an incoming
edge needs a selector in `agent-ix/quire-rs` that does not exist today; the
`where` selector of its FR-058 filters only on a field of the document itself.
The rules depend on that selector and SHALL NOT be declared unscoped, because an
unscoped rule would report every unrelated security control.

## Inputs

- `control` documents; `FR`, `NFR`, `IT` and `TC` documents declaring the edges above; caller-supplied retained evidence.

## Outputs

- Resolved incoming `satisfied_by` and `verifies` edges on the control.

## Behavior

- Quire SHALL resolve a `satisfies` edge from an `FR` or `NFR` to a `control` as an incoming `satisfied_by` edge on the control.
- Quire SHALL resolve a `verifies` edge from an `IT` or `TC` to a `control` as an incoming edge on the control.
- A retained-evidence record SHALL verify a control through an authored `verifies` edge to it, as a test does (FR-302).
- The module SHALL define no `effective`, `verified` or `passed` key on any type it declares.
- The module SHALL declare no completeness relation over `control` until the quire-rs incoming-edge selector exists.
- Quire SHALL make `quire validate --okf --strict` exit non-zero for an edge to an undeclared local id, as FR-007 specifies; a target under a foreign authority is skipped.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-205-AC-1 | With a fixture `control` present, `quire validate --okf --strict` over a fixture `FR` with a `satisfies` edge to it reports no `dangling-reference` for that edge; with the `control` removed, it reports one `dangling-reference` naming the `FR` path, `satisfies` and the control id. | Test |
| FR-205-AC-2 | With a fixture `control` present, `quire validate --okf --strict` over a fixture `IT` with a `verifies` edge to it reports no `dangling-reference` for that edge; with the `control` removed, it reports one `dangling-reference` naming the `IT` path, `verifies` and the control id. | Test |
| FR-205-AC-3 | For a fixture `FR` that `satisfies` a control that neither `mitigates` a `hazard` or `failure_mode` nor is `assumes`-d by a `risk_estimate` (outside the FR-302 scope), `quire validate --okf` raises no missing-`verifies` diagnostic for the control. | Test |
| FR-205-AC-4 | A `satisfies` edge to an undeclared local id makes `quire validate --okf --strict` exit non-zero with stderr naming the source path, `satisfies` and the id. | Test |
| FR-205-AC-5 | The manifest and emitted schemas contain no `effective`, `verified` or `passed` key. | Inspection |
| FR-205-AC-6 | The manifest declares no unscoped control relation: every `required_relations` entry whose `from` is `control` carries a `when_any` scope. | Inspection |

## Dependencies

- **Upstream**: [FR-007](./FR-007-authorable-mitigates-edge.md), [FR-204](./FR-204-post-control-risk-estimate.md); `agent-ix/spec-objects-security` FR-007; `agent-ix/engineering-assurance` (retained-evidence records); FR-302
- **Downstream**: PLAT-1524 FR-302 (completeness rules); the quire-rs incoming-edge selector, which has no ticket yet
