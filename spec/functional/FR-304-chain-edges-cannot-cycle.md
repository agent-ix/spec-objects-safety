---
id: FR-304
title: "The causal chain from failure mode to harm is checked for cycles through the arises_from verb"
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
# FR-304: The causal chain from failure mode to harm is checked for cycles through the arises_from verb

## Description

Tracked by Linear PLAT-1524. The engine reports a cycle over each verb in
`traceability.acyclic_edges` (FR-058). The module already declares
`arises_from` there. With [FR-202](./FR-202-hazardous-situation-object-and-chain.md)
the same verb carries the whole chain: a hazard arises from a failure mode, a
hazardous situation arises from a hazard, and a harm arises from a hazardous
situation. The one existing entry therefore covers the hazard, situation and harm
chain, and no new entry is needed.

The module does not prevent a cycle. A verb missing from a source's allowed
links is reported as `DisallowedEdgeType`, and a target outside the allowed set as
`disallowed-edge-target`; both are warnings and the edge still loads. A cycle
over `arises_from`, authored by whatever means, is reported by the cycle
check, once, keyed on its smallest member.

## Behavior

- `traceability.acyclic_edges` SHALL contain `arises_from`.
- Quire SHALL report a cycle over `arises_from` once, naming the path, whichever of `failure_mode`, `hazard`, `hazardous_situation` and `harm` it passes through.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-304-AC-1 | The manifest's `acyclic_edges` contains `arises_from`. | Test |
| FR-304-AC-2 | A fixture in which situation S1 `arises_from` hazard H1 and H1 `arises_from` S1 is reported once as a cycle naming both documents. | Test |
| FR-304-AC-3 | A fixture cycle that passes through a harm, a situation and a hazard (a three-document loop) is reported once, not three times. | Test |
| FR-304-AC-4 | An acyclic fixture chain of failure mode, hazard, situation and harm yields no cycle finding. | Test |

## Dependencies

- **Upstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md), [FR-301](./FR-301-hazard-reaches-harm-through-situation.md); `agent-ix/quire-rs` FR-058
