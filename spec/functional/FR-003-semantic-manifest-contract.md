---
id: FR-003
title: "Declare the semantic-module contract in the manifest"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-073"
    type: "depends_on"
---
# FR-003: Declare the semantic-module contract in the manifest

## Description

`spec_objects_safety/manifest.yaml` SHALL carry the quoin FR-070 `semantic`
block and reference every exported object type's emitted schema by path
(quoin FR-073), so that Quire validates every
declaration record against them, while every existing extraction locator keeps its meaning.

## Inputs

- The emitted schemas of [FR-002](./FR-002-emitted-json-schemas.md).
- The module-manifest schema of `filament-core-service` FR-035, which defines
  the optional top-level `semantic` block and the `data_schema` reference form.
  It is applied by the consumers that read this manifest — Quire's registry
  loader (FR-003-AC-4, AC-6) and `quoin module install` (IT-001) — and by the
  service at activation. This module holds no copy of it and reads none from a
  package that redistributes one.

## Outputs

- `manifest.yaml` with a `version`, a `semantic` block, and reference-form
  `data_schema` on both object types.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `semantic_core` (the one semantic-core version the module declares it extends), `package: agent-ix/spec-objects-safety`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name both object types: `hazard` and `failure_mode`.
- Every exported object type's `data_schema` SHALL be `{ schema: schemas/<Model>.json }`.
- No exported object type SHALL carry an inline `data_schema`.
- The manifest SHALL load through Quire's registry loader with no load failure for either object type.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-safety`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal is the neighbour's own obligation (quoin FR-070) and is evidenced by the clean install of IT-001. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the two object-type names. | Test |
| FR-003-AC-4 | `quire.Registry.load_from` lists both archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo`, carries a `package` that is not `<org>/<repo>`, or carries an unregistered `targets` value is refused by Quire's loader; an unmutated control loads in each case. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-safety-object-types.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073; quire-rs FR-069
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [IT-001](../integration/IT-001-quoin-module-install.md)
