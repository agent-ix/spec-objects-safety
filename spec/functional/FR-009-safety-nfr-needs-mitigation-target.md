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
`safety`. The NFR authors the edge, so the direction is `outgoing`. `to` names
`hazard` and `failure_mode`: the hazard an NFR answers is often declared in
another repository, and `agent-ix/quire-rs` FR-085 resolves an edge to a
repository loaded into the same corpus, so a cross-repository target satisfies
the constrained `to`. A target of any other kind is reported by quire as a kind
mismatch (FR-085) and does not satisfy the obligation. An edge to a repository
that is not loaded stays dangling and does not satisfy it either.

The coverage report of `agent-ix/quire-rs` FR-084 reads this declaration as the
reverse view: each `safety` NFR with the hazards it mitigates, and a `safety`
NFR with none as a gap.

The finding is advisory (`warning`, exit 0) and is tunable on its own key,
`trace:unjustified-safety-nfr`.

## Inputs

- Documents of type `NFR` (`spec-artifacts-iso`) with a `quality_attribute`.
- Documents of type `hazard` or `failure_mode`, in this corpus or in another repository loaded with it.
- The `spec-artifacts-iso` and `spec-objects-safety` manifests loaded together.

## Outputs

- A `[unjustified-safety-nfr]` finding for each `safety` NFR with no outgoing `mitigates` edge, naming the NFR, the declaration and the selector (`quality_attribute` and its value).

## Behavior

- The manifest SHALL declare a `required_relations` entry `from: NFR` with `where: {field: quality_attribute, values: [safety]}`, `edges: [mitigates]`, `to: [hazard, failure_mode]`, `direction: outgoing` and `check: unjustified-safety-nfr`.
- Quire SHALL report an NFR whose `quality_attribute` is `safety` and which has no outgoing `mitigates` edge.
- Quire SHALL report nothing for a `safety` NFR with an outgoing `mitigates` edge, including an edge to a `hazard` in another repository loaded into the corpus.
- Quire SHALL NOT let an edge to a document of any other kind, or to a repository that is not loaded, satisfy the obligation.
- Quire SHALL report nothing for an NFR whose `quality_attribute` is any other value.
- The finding SHALL be a warning under `--okf` and under `--okf --strict`; unrelated errors that `--strict` raises (for example iso's `unowned-quality-characteristic`) are not this rule's.
- When `--severity trace:unjustified-safety-nfr=error` is given, Quire SHALL promote the finding to an error.
- The module SHALL NOT narrow the `to: []` of `hazard-has-mitigation` or `failure-mode-has-mitigation`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [safety]`, `edges: [mitigates]`, `to: [hazard, failure_mode]`, `direction: outgoing` and `check: unjustified-safety-nfr`. | Test |
| FR-009-AC-2 | Over a bundle holding a `safety` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-safety-nfr` finding, naming the NFR and the value `safety`. | Test |
| FR-009-AC-3 | Giving that NFR a `mitigates` edge to a `hazard` removes the finding, as does an edge to a `hazard` in another repository loaded into the corpus; an edge to a document of another kind or to a repository that is not loaded leaves the finding. | Test |
| FR-009-AC-4 | An NFR whose `quality_attribute` is not `safety` and which has no `mitigates` edge yields no `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-5 | Under `--okf --strict` the finding is a warning and never an error; strict still exits 3 on warnings by design. `--severity trace:unjustified-safety-nfr=error` promotes it and the run exits non-zero. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-mitigation-coverage-findings.md); `agent-ix/quire-rs` FR-058 (`where` selector, AC-12..22), FR-084 (coverage report), FR-085 (cross-repository resolution); `spec-artifacts-iso` (`NFR` and `quality_attribute`)
