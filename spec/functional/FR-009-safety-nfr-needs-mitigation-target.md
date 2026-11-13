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
  - target: "ix://agent-ix/quire-rs/FR-085"
    type: "depends_on"
  - target: "ix://agent-ix/quire-cli/FR-030"
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
that is not loaded is dangling in a corpus whose members declare identities
(FR-085) and does not satisfy it either.

The coverage report of `agent-ix/quire-rs` FR-084 reads this declaration as the
reverse view: each `safety` NFR with the hazards it mitigates, and a `safety`
NFR with none as a gap.

The cross-repository case is reached through `quire validate --okf --repo ORG/REPO=DIR`
(`agent-ix/quire-cli` FR-030), which loads the sibling repositories into one
corpus. Without `--repo`, validate sees one repository and an edge into another
repository is dangling.

The finding is advisory (`warning`, exit 0) and is tunable on its own key,
`trace:unjustified-safety-nfr`.

## Inputs

- Documents of type `NFR` (`spec-artifacts-iso`) with a `quality_attribute`.
- Documents of type `hazard` or `failure_mode`, in this corpus or in another repository loaded with it.
- The `spec-artifacts-iso` and `spec-objects-safety` manifests loaded together.

## Outputs

- A `[unjustified-safety-nfr]` finding for each `safety` NFR that has no outgoing `mitigates` edge to a resolved `hazard` or `failure_mode`, naming the NFR, the declaration and the selector (`quality_attribute` and its value). It is produced by `quire validate --okf`, with `--repo ORG/REPO=DIR` loading the repositories that hold the targets.

## Behavior

- The manifest SHALL declare a `required_relations` entry `from: NFR` with `where: {field: quality_attribute, values: [safety]}`, `edges: [mitigates]`, `to: [hazard, failure_mode]`, `direction: outgoing` and `check: unjustified-safety-nfr`.
- Quire SHALL report an NFR whose `quality_attribute` is `safety` and which has no outgoing `mitigates` edge to a resolved `hazard` or `failure_mode`.
- Quire SHALL report nothing for a `safety` NFR with an outgoing `mitigates` edge to a resolved `hazard` or `failure_mode`, including one in a repository loaded with `--repo`.
- If a `safety` NFR's only outgoing `mitigates` edges target a document of another kind, or a repository that is not loaded, then Quire SHALL report the NFR.
- Quire SHALL report nothing for an NFR whose `quality_attribute` is any other value.
- The finding SHALL be a warning under `--okf` and under `--okf --strict`; unrelated errors that `--strict` raises (for example iso's `unowned-quality-characteristic`) are not this rule's.
- When `--severity trace:unjustified-safety-nfr=error` is given, Quire SHALL promote the finding to an error.
- The manifest SHALL keep `to: []` on `hazard-has-mitigation` or `failure-mode-has-mitigation`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The manifest declares one `required_relations` entry with `from: NFR`, `where` over `quality_attribute` with `values: [safety]`, `edges: [mitigates]`, `to: [hazard, failure_mode]`, `direction: outgoing` and `check: unjustified-safety-nfr`. | Test |
| FR-009-AC-2 | Over a bundle holding a `safety` NFR with no `mitigates` edge, `quire validate --okf` exits 0 and yields exactly one `unjustified-safety-nfr` finding, naming the NFR and the value `safety`. | Test |
| FR-009-AC-3 | Giving that NFR a `mitigates` edge to a `hazard` in the same repository removes the finding. | Test |
| FR-009-AC-4 | An NFR whose `quality_attribute` is not `safety` and which has no `mitigates` edge yields no `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-5 | Under `--okf --strict` the finding is a warning and never an error; strict still exits 3 on warnings by design. `--severity trace:unjustified-safety-nfr=error` promotes it and the run exits non-zero. | Test |
| FR-009-AC-6 | Giving that NFR a `mitigates` edge to a `failure_mode` in the same repository removes the finding. | Test |
| FR-009-AC-7 | `quire validate --okf --repo o/a=<A> --repo o/b=<B> --module $M` over a fixture where the NFR in `o/a` has a `mitigates` edge to a `hazard` in `o/b` yields no `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-8 | An NFR whose only `mitigates` edge targets a `threat` in the same repository still yields the `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-9 | An NFR whose only `mitigates` edge targets a `hazard` in a repository not named by any `--repo` still yields the `unjustified-safety-nfr` finding. | Test |
| FR-009-AC-10 | `hazard-has-mitigation` or `failure-mode-has-mitigation` still declare `to: []` in the manifest. | Test |

## Dependencies

- **Upstream**: [FR-008](./FR-008-mitigation-coverage-findings.md); `agent-ix/quire-rs` FR-058 (`where` selector, AC-12..22), FR-085 (cross-repository resolution); `agent-ix/quire-cli` FR-030 (`validate --okf --repo`); `spec-artifacts-iso` (`NFR` and `quality_attribute`)
- **Downstream**: `agent-ix/quire-rs` FR-084 (reads this declaration as the reverse view of the coverage report)
