---
id: FR-202
title: "A hazardous situation arises from a hazard and a harm arises from it"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-201"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
---
# FR-202: A hazardous situation arises from a hazard and a harm arises from it

## Description

PLAT-1409. Today a hazard carries its operational situation as the free string
`context.situation`. The module declares `hazardous_situation` as a first-class
object type and declares the chain hazard, hazardous situation, harm as
authored edges with inverses, so that "which harms can this hazard lead to,
through which situations" is a graph query and not a reading of prose.

For this module a hazardous situation is a case in which a hazard state
coincides with something that can be hurt. The manifest `lexicon` carries this
wording, as it does for `harm`.

### Edges: one existing verb, read from the effect end

Both hops reuse the existing `arises_from` verb, which this module already uses
for a hazard arising from a failure mode:

| Edge | Authored on | Target | Cardinality |
|---|---|---|---|
| `arises_from` | `hazardous_situation` | `hazard` | one or more |
| `arises_from` | `harm` | `hazardous_situation` | one or more |

The effect end authors each fact, so a hazard never lists its situations and a
situation never lists its harms (the rule of FR-007: no duplicated fact that
can drift). The verb is already in the module's `acyclic_edges`, so one check
covers the whole failure mode, hazard, situation, harm chain.

The only vocabulary change is one inverse label on `arises_from` (for example
`gives_rise_to`) in `spec-artifacts-iso`, so that each hop can be read from the
cause end by extraction. That change belongs to `spec-artifacts-iso` and is
needed before the inverse criterion below can pass; the same mechanism added
`specified_by` for `specifies`. No new verb is added.

### Existing hazards stay valid

`HazardContext.situation` remains a valid optional string. A hazard with it and
no situation object validates exactly as before. There is no migration and no
requirement that the string be converted.

### What this requirement does not declare

The completeness rules that report a hazard with no situation, a situation
with no hazard and a situation with no harm are declared once, with the
traceability relations of PLAT-1524 (FR-301, including `situation-without-hazard`).
This requirement defines the types and the edges only.

## Inputs

- `hazard` and `harm` documents; `hazardous_situation` documents.

## Outputs

- A `hazardous_situation` object type, schema and skeleton; resolved forward and inverse chain edges.

## Behavior

- The manifest SHALL declare `hazardous_situation` and export it in `semantic.exports`.
- The `hazardous_situation` schema SHALL require an identity field, a title and a description of the case.
- The manifest `lexicon` SHALL carry an entry for `hazardous situation` in the module's own words.
- The manifest SHALL allow `arises_from` from `hazardous_situation` to `hazard` and from `harm` to `hazardous_situation`.
- Quire SHALL report `disallowed-edge-target` naming the target type when either `arises_from` edge targets any other type.
- Quire SHALL resolve the inverse of each chain edge on its target, with the target declaring nothing.
- The module SHALL treat a situation as arising from one or more hazards; the check that reports a situation with none is `situation-without-hazard`, declared only in PLAT-1524 FR-301.
- The `hazardous_situation` schema SHALL forbid the keys `severity`, `probability`, `score` and `acceptance`.
- The module SHALL keep `hazard.context.situation` accepted and its schema unchanged.
- Quire SHALL make `quire validate --okf --strict` exit non-zero for an edge whose target is an undeclared local id, as FR-007 specifies.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-202-AC-1 | A fixture bundle of one hazard, one situation with `arises_from` to it and one harm with `arises_from` to the situation validates with no diagnostic. | Test |
| FR-202-AC-2 | `quire extract` over the fixture shows the resolved inverse of each chain edge on the hazard and on the situation, though neither document declares it. | Test |
| FR-202-AC-3 | A situation with `arises_from` to a `harm`, or a harm with `arises_from` to a `hazard`, is reported `disallowed-edge-target` naming the target type. | Test |
| FR-202-AC-4 | A `hazardous_situation` carrying `severity`, `probability`, `score` or `acceptance` fails validation. | Test |
| FR-202-AC-5 | An existing hazard fixture with `context.situation` and no situation object validates unchanged. | Test |
| FR-202-AC-6 | FR-202 declares no `required_relations` entry of its own: the relations whose `from` is `hazardous_situation`, including the `situation-without-hazard` check, are declared once, in PLAT-1524 FR-301, and no check token is declared by two relations. | Inspection |
| FR-202-AC-7 | A situation with two `arises_from` edges to two hazards validates with no diagnostic and both inverses resolve. | Test |
| FR-202-AC-8 | An `arises_from` edge to an undeclared local id makes `quire validate --okf --strict` exit non-zero with stderr naming the source path, `arises_from` and the missing id. | Test |
| FR-202-AC-9 | A cycle among chain edges is reported by the existing `arises_from` acyclicity check. | Test |
| FR-202-AC-10 | The manifest `lexicon` has an entry `hazardous situation`. | Inspection |

## Dependencies

- **Upstream**: [FR-201](./FR-201-harm-object-type.md); [FR-001](./FR-001-safety-object-types.md); the inverse label on `arises_from` in `spec-artifacts-iso`
- **Downstream**: [FR-203](./FR-203-pre-control-risk-estimate.md)
