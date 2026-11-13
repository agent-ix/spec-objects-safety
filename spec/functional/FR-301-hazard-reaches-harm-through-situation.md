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

Tracked by Linear PLAT-1524. A hazard that no hazardous situation involves, or
a situation that can result in no harm, is a risk chain that stops before it
says anything. The module **SHALL** declare two `traceability.required_relations`
entries that together make "each hazard reaches at least one harm through a
hazardous situation" a corpus check. Both are manifest data read by the
existing upward-trace engine (`agent-ix/quire-rs` FR-058); the engine holds no
archetype name, verb or direction of this chain.

The edges are those of [FR-202](./FR-202-hazardous-situation-object-and-chain.md):
authored on the situation, `involves` to a hazard and `can_result_in` to a
harm. Whatever verb names FR-202 settles, the relations use those names.

### Engine gap: one hop per relation

A required relation tests one edge hop. It cannot say "a hazard has a path of
two hops that ends at a harm". The module therefore declares two relations, one
per hop. Together they are stronger than the plain reading: every hazard has a
situation **and** every situation has a harm, so every hazard reaches a harm,
and a situation that leads nowhere is also reported. No engine change is
needed, and none is assumed.

## Inputs

- The `hazard`, `hazardous_situation` and `harm` documents of a bundle, with the safety module loaded.

## Outputs

- Advisory findings `hazard-without-situation` and `situation-without-harm`, each naming the document and the declaration.

## Behavior

- The manifest SHALL declare a relation `hazard-has-situation`: `from: hazard`, `edges: [involves]`, `to: [hazardous_situation]`, `direction: incoming`, `check: hazard-without-situation`.
- The manifest SHALL declare a relation `situation-has-harm`: `from: hazardous_situation`, `edges: [can_result_in]`, `to: [harm]`, `direction: outgoing`, `check: situation-without-harm`.
- `situation-without-harm` is the check named in FR-202; this requirement is the single declaration of it, and FR-202 SHALL NOT declare a second one.
- Each relation SHALL carry its own `trace:<check>` severity key, advisory by default; a repository promotes one without the other by key.
- A dangling edge SHALL NOT satisfy either relation, because `to` is constrained (FR-058).
- The relations SHALL carry no `exclude` glob and no per-project data.
- A hazard that is authored with only the free string `context.situation` and no situation object the tooling SHALL report `hazard-without-situation`; the string is not a situation.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-301-AC-1 | The manifest declares `hazard-has-situation` and `situation-has-harm` with exactly the fields above, and `quire` loads the module without a declaration error. | Test |
| FR-301-AC-2 | A fixture bundle of hazard H1, situation S1 (`involves` H1, `can_result_in` harm M1) and M1 yields no `hazard-without-situation` and no `situation-without-harm` finding. | Test |
| FR-301-AC-3 | Removing S1 from the fixture yields exactly one `hazard-without-situation` finding naming H1. | Test |
| FR-301-AC-4 | Removing the `can_result_in` edge from S1 yields exactly one `situation-without-harm` finding naming S1 and none for H1. | Test |
| FR-301-AC-5 | A hazard with `context.situation` text and no situation document yields one `hazard-without-situation` finding. | Test |
| FR-301-AC-6 | A `can_result_in` edge to an id no loaded document declares does not satisfy `situation-has-harm`; S1 is reported. | Test |
| FR-301-AC-7 | `--severity trace:hazard-without-situation=error` makes the run exit non-zero while `situation-without-harm` findings stay warnings; with no flag the run exits 0. | Test |
| FR-301-AC-8 | With two situations on one hazard, one reaching a harm and one not, only the second is reported. | Test |

## Dependencies

- **Upstream**: [FR-202](./FR-202-hazardous-situation-object-and-chain.md), [FR-201](./FR-201-harm-object-type.md), [FR-008](./FR-008-mitigation-coverage-findings.md) (the same mechanism, applied to mitigation); `agent-ix/quire-rs` FR-058
- **Downstream**: [FR-304](./FR-304-chain-edges-cannot-cycle.md), [FR-305](./FR-305-risk-summary-report.md)
