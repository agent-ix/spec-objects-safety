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

## Outputs

- The reference-only support models `EvidenceRef` and the `SemanticId` relation targets.

## Behavior

- The module SHALL enumerate its declared object types in the manifest.
- No declared object type SHALL be a type another module owns.
- The module SHALL NOT declare a `control`, `risk`, `asset`, `threat`, `vulnerability`, `incident` or evidence-record object type.
- A consumer SHALL reach a control through the incoming `mitigates` edge the manifest `traceability` model already declares.
- No record schema SHALL list a control on a hazard or a failure mode.
- The catalog SHALL make that edge authorable, and [FR-007](./FR-007-authorable-mitigates-edge.md) states how: the `control` end gains `hazard` and `failure_mode` as `mitigates` targets. This module does not change the relation, the verb or the direction.
- A consumer SHALL reach an evidence record through `EvidenceRef.target`, a `SemanticId`.
- No schema in this module SHALL copy an evidence record's content.
- `EvidenceRef.kind` SHALL stay an open string, because the closed evidence-kind vocabulary belongs to `agent-ix/engineering-assurance`.
- The module SHALL NOT change the direction, the verb, or the object type of any edge the `traceability` model declares, because `agent-ix/spec-objects-security`'s hazard-coverage work reads that model across repositories.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-006-CON-1 | This module SHALL mint no safety-only synonym for a verb or a type another module already declares. | Architecture | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | The manifest declares `hazard` and `failure_mode` among its enumerated object types, and no object type named by `spec-objects-security`, `spec-objects-architecture` or `spec-objects-operational`. | Test |
| FR-006-AC-2 | No shipped schema declares a `controls` or `mitigations` key, and the only cross-module reference shape is a `SemanticId`. | Test |
| FR-006-AC-4 | Every `allowed_links` verb and every `traceability` verb exists in the `spec-artifacts-iso` edge vocabulary as a forward key or a declared inverse label. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md)
- **Downstream**: `agent-ix/spec-objects-security#13`, `agent-ix/spec-objects-architecture#8`, `agent-ix/spec-objects-operational#6`
