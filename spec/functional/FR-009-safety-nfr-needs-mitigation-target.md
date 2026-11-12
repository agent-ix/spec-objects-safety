---
id: FR-009
title: "A safety-classified NFR that mitigates nothing is reported as unjustified scope"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-008"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-058"
    type: "depends_on"
---
# FR-009: A safety-classified NFR that mitigates nothing is reported as unjustified scope

## Description

[FR-008](./FR-008-mitigation-coverage-findings.md) reads the `mitigates` edge
from the hazard end: a hazard nothing mitigates is reported. This requirement
reads it from the requirement end. A non-functional requirement that claims to
be about safety and answers no hazard or failure mode is scope nobody asked
for, and no per-document check can see it.

The classification is the `quality_attribute` frontmatter field that
`spec-artifacts-iso` declares on `NFR` with `safety` among its values. The
module declares the obligation as data, using the `where` selector of
`agent-ix/quire-rs` FR-058 (FR-058-AC-12..22) to narrow it to NFRs holding
`safety`. The NFR authors the edge, so the direction is `outgoing`. `to` stays
empty: the hazard an NFR answers is usually declared in another repository, and
FR-058 does not let a dangling edge satisfy a constrained `to`.

The finding is advisory (`warning`, exit 0) and is tunable on its own key,
`trace:unjustified-safety-nfr`.

## Inputs

- Documents of type `NFR` (`spec-artifacts-iso`) with a `quality_attribute`.
- Documents of type `hazard` or `failure_mode`, or an edge to one declared elsewhere.
- The `spec-artifacts-iso` and `spec-objects-safety` manifests loaded together.

## Outputs

- A `[unjustified-safety-nfr]` finding for each `safety` NFR with no outgoing `mitigates` edge, naming the NFR, the declaration and the selector (`quality_attribute` and its value).

## Behavior

- The manifest SHALL declare a `required_relations` entry `from: NFR` with `where: {field: quality_attribute, values: [safety]}`, `edges: [mitigates]`, `to: []`, `direction: outgoing` and `check: unjustified-safety-nfr`.
- Quire SHALL report an NFR whose `quality_attribute` is `safety` and which has no outgoing `mitigates` edge.
- Quire SHALL report nothing for a `safety` NFR with an outgoing `mitigates` edge, including an edge to a document in another repository.
- Quire SHALL report nothing for an NFR whose `quality_attribute` is any other value.
- The finding SHALL be a warning under `--okf` and under `--okf --strict`, and `--severity trace:unjustified-safety-nfr=error` SHALL promote it.
- The module SHALL NOT narrow the `to: []` of `hazard-has-mitigation` or `failure-mode-has-mitigation`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [safety]`, `edges: [mitigates]`, `to: []`, `direction: outgoing` and `check: unjustified-safety-nfr`. | Test |
| FR-009-AC-2 | Over a bundle holding a `safety` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-safety-nfr` finding, naming the NFR and the value `safety`. | Test |
| FR-009-AC-3 | Giving that NFR a `mitigates` edge to a `hazard` removes the finding, as does an edge to a document in another repository. | Test |
| FR-009-AC-4 | An NFR whose `quality_attribute` is not `safety` and which has no `mitigates` edge yields no `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-5 | `--severity trace:unjustified-safety-nfr=error` makes the run exit non-zero, and without it `--okf --strict` still exits 0. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-mitigation-coverage-findings.md); `agent-ix/quire-rs` FR-058 (`where` selector, AC-12..22); `spec-artifacts-iso` (`NFR` and `quality_attribute`)
