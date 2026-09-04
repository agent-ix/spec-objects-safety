---
id: FR-006
title: "Reference architecture, operational, security and assurance types without redeclaring them"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "depends_on"
---
# FR-006: Reference architecture, operational, security and assurance types without redeclaring them

## Description

The module SHALL point at the control, risk, architecture, operational and
evidence types that other modules own, by reference only, and SHALL declare no
type, field or vocabulary that duplicates one of them.

## Inputs

- `agent-ix/spec-objects-security` (`control`, `risk`, `asset`, `threat`,
  `vulnerability`), `agent-ix/spec-objects-architecture` (`interface`,
  `api_endpoint`, `external_contract`), `agent-ix/spec-objects-operational`
  (`incident`, `runbook`, `alert`), and `agent-ix/engineering-assurance`
  (evidence records).
- The `semantic.imports` map defined by quoin FR-070: imported semantic
  packages at exact versions.

## Outputs

- `semantic.imports` in the manifest, and the reference-only support models
  `EvidenceRef` and the `SemanticId` relation targets.

## Behavior

- The module SHALL declare exactly two object types, `hazard` and `failure_mode`.
- The module SHALL NOT declare a `control`, `risk`, `asset`, `threat`, `vulnerability`, `incident` or evidence-record object type.
- A control SHALL be reached through the incoming `mitigates` edge the manifest `traceability` model already declares, and SHALL NOT be listed on the hazard or failure-mode record.
- An evidence record SHALL be reached through `EvidenceRef.target`, a `SemanticId`, and SHALL NOT be copied into this module.
- `EvidenceRef.kind` SHALL stay an open string, because the closed evidence-kind vocabulary belongs to `agent-ix/engineering-assurance`.
- `semantic.imports` SHALL name only packages that publish a semantic contract at an exact version.
- Until `agent-ix/spec-objects-security#13`, `agent-ix/spec-objects-architecture#8` and `agent-ix/spec-objects-operational#6` land, `semantic.imports` SHALL be `{}` and the manifest SHALL record why, because pinning a version a neighbour does not declare is a false claim.
- When a neighbouring module publishes its semantic contract, this module SHALL add it to `semantic.imports` at that exact version in the same change that first names one of its types in a shipped fixture.
- The module SHALL NOT change the direction, the verb, or the object type of any edge the `traceability` model declares, because `agent-ix/spec-objects-security`'s hazard-coverage work reads that model across repositories.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-006-CON-1 | No safety-only synonym SHALL be minted for a verb or a type another module already declares. | Architecture | Test |
| FR-006-CON-2 | `semantic.imports` SHALL be empty rather than aspirational; an unpublished neighbour is recorded in prose, not in the pin map. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | The manifest declares exactly `hazard` and `failure_mode`, and no object type named by `spec-objects-security`, `spec-objects-architecture` or `spec-objects-operational`. | Test |
| FR-006-AC-2 | No shipped schema declares a `controls` or `mitigations` key, and the only cross-module reference shape is a `SemanticId`. | Test |
| FR-006-AC-3 | `semantic.imports` is `{}`, and the manifest states the three open migration issues that keep it empty. | Test |
| FR-006-AC-4 | Every `allowed_links` verb and every `traceability` verb exists in the `spec-artifacts-iso` edge vocabulary as a forward key or a declared inverse label. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md)
- **Downstream**: `agent-ix/spec-objects-security#13`, `agent-ix/spec-objects-architecture#8`, `agent-ix/spec-objects-operational#6`
