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
  - target: "ix://agent-ix/quire-rs/FR-078"
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

The second verification route is retained evidence: caller-supplied evidence
that `agent-ix/quire-rs` FR-078 binds to an acceptance criterion through its
`evidence::qualify` library call. It binds to no control, and not through
`quire extract`. For a control, effectiveness evidence therefore binds to the
acceptance criteria of the `FR` or `NFR` that `satisfies` the control, so a
control with retained evidence is reached through its implementing
requirement. It is not a document with frontmatter edges, so this requirement
does not require an authored `verifies` edge for it, and this module copies no
evidence record.

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
- The module SHALL require no authored `verifies` edge for the retained-evidence route.
- The module SHALL define no `effective`, `verified` or `passed` key on any type it declares.
- The module SHALL declare no completeness relation over `control` until the quire-rs incoming-edge selector exists.
- Quire SHALL make `quire validate --okf --strict` exit non-zero for an edge to an undeclared local id, as FR-007 specifies; a target under a foreign authority is skipped.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-205-AC-1 | A fixture `FR` with a `satisfies` edge to a fixture `control` validates under `quire validate --okf --strict` with no `dangling-reference` for the edge; removing the `control` makes the same edge a `dangling-reference`. | Test |
| FR-205-AC-2 | A fixture `IT` with a `verifies` edge to the fixture `control` validates under `quire validate --okf --strict` with no `dangling-reference` for the edge; removing the `control` makes the same edge a `dangling-reference`. | Test |
| FR-205-AC-3 | For a fixture `FR` that `satisfies` a control, with the control carrying no authored `verifies` edge, `quire validate --okf` raises no missing-`verifies` diagnostic for the control. Qualifying caller-supplied evidence through `evidence::qualify` is quire-rs FR-078's behaviour and is tested there. | Test |
| FR-205-AC-4 | A `satisfies` edge to an undeclared local id makes `quire validate --okf --strict` exit non-zero with stderr naming the source path, `satisfies` and the id. | Test |
| FR-205-AC-5 | The manifest and emitted schemas contain no `effective`, `verified` or `passed` key. | Inspection |
| FR-205-AC-6 | The manifest declares no `required_relations` entry whose `from` is `control`. | Inspection |

## Dependencies

- **Upstream**: [FR-007](./FR-007-authorable-mitigates-edge.md), [FR-204](./FR-204-post-control-risk-estimate.md); `agent-ix/spec-objects-security` FR-007; `agent-ix/quire-rs` FR-078 (retained evidence)
- **Downstream**: PLAT-1524 FR-302 (completeness rules); the quire-rs incoming-edge selector, which has no ticket yet
