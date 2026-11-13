---
id: FR-304
title: "The hazard, situation and harm chain is acyclic by construction and the cycle check covers the verbs that can cycle"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-202"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-301"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-304: The hazard, situation and harm chain is acyclic by construction and the cycle check covers the verbs that can cycle

## Description

Tracked by Linear PLAT-1524. The engine reports a cycle over each verb in
`traceability.acyclic_edges` (FR-058). Applying the value test to the chain:
the chain edges are `involves` (situation to hazard) and `can_result_in`
(situation to harm). Their target sets are closed by FR-202: a hazard and a
harm declare no outgoing chain edge. A path of two chain edges therefore cannot
exist, so a cycle over them cannot exist, and declaring them in
`acyclic_edges` would only guard a state the schema already makes unreachable.
That entry would be ceremony, so the module SHALL NOT declare it.

The cycle that can occur in the safety model is the causal one the module
already declares: `arises_from` (hazard to failure mode). This requirement
keeps that declaration and adds a test that the chain cannot cycle.

## Behavior

- `traceability.acyclic_edges` SHALL contain `arises_from` and no chain verb.
- The manifest SHALL declare no outgoing chain edge on `hazard` or `harm`, so no path of two chain edges exists.
- Quire SHALL report a chain edge whose target type is outside its declared set as `disallowed-edge-target` (FR-202); that check keeps the chain acyclic.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-304-AC-1 | The manifest's `acyclic_edges` is exactly the set containing `arises_from`. | Test |
| FR-304-AC-2 | In the manifest, no object type declares an outgoing `involves` or `can_result_in` other than `hazardous_situation`, and the targets of those edges (`hazard`, `harm`) declare neither. | Test |
| FR-304-AC-3 | A fixture in which a `hazard` declares `involves` to another document, or a `harm` declares `can_result_in`, is reported `disallowed-edge-target`, so a chain cycle cannot be authored. | Test |
| FR-304-AC-4 | A fixture where `hazard` H1 `arises_from` failure mode F1 and F1 is made to reach H1 through `arises_from` is reported once as a cycle naming the path. | Test |

## Dependencies

- **Upstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md), [FR-301](./FR-301-hazard-reaches-harm-through-situation.md); `agent-ix/quire-rs` FR-058
