---
id: NFR-001
title: "Making the mitigates edge authorable is additive"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-007"
    type: "constrains"
---
# NFR-001: Making the mitigates edge authorable is additive

## Statement

The module SHALL keep `compatibility_posture: additive` while the `mitigates` edge becomes authorable, leaving every value of its frozen `traceability` block and every `allowed_links` entry unchanged.

## Rationale

`spec-objects-security` reads the safety traceability model across the repository boundary. Narrowing `to:` or changing a direction is non-additive and would need a version bump; the widening on the control side needs none.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Traceability keys differing from the pre-change block | 0 | 0 | Manifest comparison test |
| Safety `allowed_links` entries removed or narrowed | 0 | 0 | Manifest comparison test |

## Verification

A test loads the manifest and asserts the `traceability` block and `allowed_links` equal the values this requirement freezes, and that `semantic.compatibility_posture` is `additive`.

## Dependencies

- **Upstream**: [FR-007](../functional/FR-007-authorable-mitigates-edge.md)
