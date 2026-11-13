---
id: FR-301
title: "Every hazard reaches a harm through a hazardous situation, declared as manifest data"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-202"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-201"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-008"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-301: Every hazard reaches a harm through a hazardous situation, declared as manifest data

## Description

Tracked by Linear PLAT-1524. A hazard that no hazardous situation arises from,
a situation that arises from no hazard, or a situation no harm arises from, is a
risk chain that stops before it says anything. The module **SHALL** declare
three `traceability.required_relations` entries that together make "each hazard
reaches at least one harm through a hazardous situation" a corpus check. They
are manifest data read by the existing upward-trace engine (`agent-ix/quire-rs`
FR-058); the engine holds no archetype name, verb or direction of this chain.

The chain uses the one verb of [FR-202](./FR-202-hazardous-situation-object-and-chain.md):
`arises_from`, authored on the later link. A hazardous situation `arises_from` a
hazard, and a harm `arises_from` a hazardous situation. Read from the hazard, the
edges are incoming.

### Engine limit: one hop per relation

A required relation tests one edge hop. It cannot say "a hazard has a two-hop
path that ends at a harm". The module therefore declares one relation per
hop, and the three together imply the path: every hazard has a situation, every
situation has a hazard, and every situation has a harm. They are stricter than
the plain reading, since a situation that leads nowhere is reported too. No
engine change is needed.

### Ownership

This requirement is the single place the three relations are declared. FR-202
specifies the object type and the edges and the checks are owned here. The
module declares exactly one relation per `check` token (NFR-300).

## Inputs

- The `hazard`, `hazardous_situation` and `harm` documents of a bundle, with the safety module loaded.

## Outputs

- Advisory findings `hazard-without-situation`, `situation-without-hazard` and `situation-without-harm`, each naming the document and the declaration.

## Behavior

- The manifest SHALL declare `hazard-has-situation`: `from: hazard`, `edges: [arises_from]`, `to: [hazardous_situation]`, `direction: incoming`, `check: hazard-without-situation`.
- The manifest SHALL declare `situation-has-hazard`: `from: hazardous_situation`, `edges: [arises_from]`, `to: [hazard]`, `direction: outgoing`, `check: situation-without-hazard`.
- The manifest SHALL declare `situation-has-harm`: `from: hazardous_situation`, `edges: [arises_from]`, `to: [harm]`, `direction: incoming`, `check: situation-without-harm`.
- Each relation SHALL carry its own `trace:<check>` severity key, advisory by default.
- A dangling edge SHALL NOT satisfy any of the three relations, because `to` is constrained (FR-058).
- The relations SHALL carry no `exclude` glob and no per-project data.
- If a hazard carries only the free string `context.situation` and no situation document arises from it, then the tooling SHALL report `hazard-without-situation`.
- The tooling SHALL report a situation that has no hazard as `situation-without-hazard`, so that a situation absent from every hazard row is still found.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-301-AC-1 | The manifest declares the three relations with exactly the fields above, and `quire` loads the module without a declaration error. | Test |
| FR-301-AC-2 | A fixture of hazard H1, situation S1 (`arises_from` H1) and harm M1 (`arises_from` S1) yields no finding from any of the three checks. | Test |
| FR-301-AC-3 | Removing S1 yields exactly one `hazard-without-situation` finding naming H1. | Test |
| FR-301-AC-4 | Removing M1 yields exactly one `situation-without-harm` finding naming S1 and none for H1. | Test |
| FR-301-AC-5 | A hazard with `context.situation` text and no situation document yields one `hazard-without-situation` finding. | Test |
| FR-301-AC-6 | A harm `arises_from` an id no loaded document declares does not satisfy `situation-has-harm`; S1 is reported. | Test |
| FR-301-AC-7 | `--severity trace:hazard-without-situation=error` makes the run exit non-zero while the other two checks stay warnings; with no flag the run exits 0. | Test |
| FR-301-AC-8 | With two situations on one hazard, one with a harm and one without, only the second is reported. | Test |
| FR-301-AC-9 | A situation with no `arises_from` edge to a hazard yields exactly one `situation-without-hazard` finding naming it; adding the edge removes it. | Test |
| FR-301-AC-10 | The manifest holds exactly one relation for each of the three `check` tokens. | Inspection |

## Dependencies

- **Upstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md), [FR-201](./FR-201-harm-object-type.md), [FR-008](./FR-008-mitigation-coverage-findings.md) (the same mechanism, applied to mitigation); `agent-ix/quire-rs` FR-058
- **Downstream**: [FR-304](./FR-304-chain-edges-cannot-cycle.md), [FR-305](./FR-305-risk-summary-report.md)
