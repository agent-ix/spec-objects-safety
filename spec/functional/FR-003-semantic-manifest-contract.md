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
block and reference every exported object type's emitted schema by path and
digest (quoin FR-073), at manifest `version` 0.3.0, so that Quoin verifies the
shipped schemas at install and Quire validates every declaration record against
them, while every existing extraction locator keeps its meaning.

## Inputs

- The emitted schemas and digests of [FR-002](./FR-002-emitted-json-schemas.md).
- The module-manifest schema, **as of `agent-ix/spec-artifacts-iso` CR-012**
  (commit `6686f11`), which adds the optional top-level `semantic` block and the
  `data_schema` reference form. The requirement it implements is
  `filament-core-service` FR-035; `spec-artifacts-iso` ships the schema file and
  packages it as importable data, and is where a change to it lands. No released `spec-artifacts-iso` distribution
  carries it: `v0.18.0` is the newest tag and its schema predates CR-012, which
  is why FR-003-AC-7 pins the gate to a revision rather than to a release.
  `agent-ix/spec-artifacts-iso#36` tracks the release that retires the pin.

## Outputs

- `manifest.yaml` with `version: 0.3.0`, a `semantic` block, and reference-form
  `data_schema` on both object types.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `semantic_core: 0.1.0`, `package: agent-ix/spec-objects-safety`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name both object types: `hazard` and `failure_mode`.
- Every exported object type's `data_schema` SHALL be `{ schema: schemas/<Model>.json, digest: sha256:<hex> }` where `<hex>` is the SHA-256 of the shipped file bytes.
- No exported object type SHALL carry an inline `data_schema`.
- The manifest `version` SHALL be `0.3.0`, because the emitted `$id` embeds it and the previous version was `0.2.0`.
- Every `body_extraction` locator present at version 0.2.0 SHALL remain present with the same `from`, heading, `language`, `required`, `multiple`, and `assert` facets.
- Where an object type gains a locator after 0.2.0, that locator SHALL be `required: false`, so existing artifacts stay valid.
- The `traceability` block SHALL keep its 0.2.0 shape: both `required_relations`, their `edges`, their `direction: incoming`, their distinct `check` keys, and `acyclic_edges: [arises_from]`. `agent-ix/spec-objects-security`'s hazard-coverage work reads them across repositories, so a change here is a change to a neighbour.
- The manifest SHALL load through Quire's registry loader with no load failure for either object type and with the recorded schema digest equal to the manifest digest.
- Measured against quire 0.46.0, and stated as a measurement rather than an obligation: a refused schema drops that object type alone, while a manifest key the loader cannot parse drops every object type of the module, so a consumer sees the module as absent. Both refusals are silent — no diagnostic names the offending key, path, or digest — which `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record as engine defects; the naming half of FR-003-AC-6 is blocked on them and is verified as an explicit expected failure rather than dropped.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-safety`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys, the digests, or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal is the neighbour's own obligation (quoin FR-070) and is evidenced by the clean install of IT-001. | Compatibility | Test |
| FR-003-CON-2 | The manifest SHALL mark every locator added after 0.2.0 `required: false`. | Compatibility | Test |
| FR-003-CON-3 | The suite SHALL never skip the FR-035 gate. While the installed `spec-artifacts-iso` schema predates CR-012 the gate runs against the pinned revision copy, and fails when that copy differs from the installed schema anywhere outside the CR-012 paths. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the two object-type names. | Test |
| FR-003-AC-2 | For every exported type, `data_schema` is the reference form, the referenced file exists, and its SHA-256 equals the recorded digest. | Test |
| FR-003-AC-3 | Every 0.2.0 locator, compared against the checked-in 0.2.0 baseline, is present unchanged; every added locator is `required: false`. | Test |
| FR-003-AC-4 | `quire.Registry.load_from` lists both archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-5 | The `traceability` block is byte-for-byte the 0.2.0 model: two relations, `edges: [mitigates]`, `direction: incoming`, distinct `check` keys, `acyclic_edges: [arises_from]`. | Test |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by Quire's loader naming `foo`; a copy whose digest is altered is refused naming the path. | Test |
| FR-003-AC-7 | The manifest validates against the FR-035 module-manifest schema at CR-012, and that schema differs from the installed `spec-artifacts-iso` release only at the JSON pointers CR-012 introduces. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-safety-object-types.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073; quire-rs FR-069
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [IT-001](../integration/IT-001-quoin-module-install.md)
