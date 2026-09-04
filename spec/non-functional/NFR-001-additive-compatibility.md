---
id: NFR-001
title: "The 0.3.0 module stays additively compatible with 0.2.0 artifacts"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "constrains"
---
# NFR-001: The 0.3.0 module stays additively compatible with 0.2.0 artifacts

## Statement

The module SHALL keep every 0.2.0 extraction locator unchanged, and add only
`required: false` locators, so that every document valid at 0.2.0 stays valid at
0.3.0 with no author action.

## Scope

- Applies to: `spec_objects_safety/manifest.yaml` `body_extraction` locators,
  the `traceability` model, the three advisory lint rules `hazard-severity`,
  `hazard-likelihood` and `failure-mode-detection`, and documents authored
  against version 0.2.0.
- Operational context: advisory-only adoption ahead of promotion; no corpus
  repository is edited.

## Rationale

`compatibility_posture: additive` is declared in the manifest, so it is a
promise a consumer may rely on. A locator whose `required`, heading or `assert`
facet changed would silently reclassify existing documents, and the
`traceability` model is read across repositories by
`agent-ix/spec-objects-security`'s hazard-coverage work — a change there breaks
a neighbour, not just this module.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.2.0 locators changed | 0 | 0 | unit-testing |
| Added locators that are `required: true` | 0 | 0 | unit-testing |
| 0.2.0 skeletons failing validation under 0.3.0 | 0 | 0 | integration-testing |
| `traceability` facts changed | 0 | 0 | unit-testing |
| 0.2.0 lint values no longer admitted | 0 | 0 | unit-testing |

## Verification

The 0.2.0 locator set and the 0.2.0 skeletons are checked in under
`tests/fixtures/baseline-0.2.0/`. One test diffs the live manifest's locators
against that baseline, one asserts every added locator is `required: false`,
one validates each 0.2.0 skeleton under the 0.3.0 module, and one compares the
`traceability` model fact by fact.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.2.0 locator is present with the same `from`, heading, `required` and `assert` facets; zero changed. | Test |
| NFR-001-AC-2 | Every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors. | Test |
| NFR-001-AC-3 | A `## Properties` section holding the legacy prose form yields a warning under `legacy_forms: warning`, not an error. | Test |
| NFR-001-AC-4 | The `traceability` model is unchanged: two relations, `edges: [mitigates]`, `direction: incoming`, distinct `check` keys, `acyclic_edges: [arises_from]`. | Test |
| NFR-001-AC-5 | The three advisory lint allow-lists `hazard-severity`, `hazard-likelihood` and `failure-mode-detection` still admit every value they admitted at 0.2.0, and each now also admits `unknown`, `not_assessed` and `not_applicable`. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md)
- **Downstream**: `agent-ix/spec-objects-security#13`, which reads this module's `traceability` model
