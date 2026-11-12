---
id: FR-008
title: "The hazard and failure-mode coverage checks report unmitigated objects and stay silent on mitigated ones"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-objects-safety/FR-007"
    type: "depends_on"
---
# FR-008: The hazard and failure-mode coverage checks report unmitigated objects and stay silent on mitigated ones

## Description

`unmitigated-hazard` and `unmitigated-failure-mode` have never been exercised
end to end. A check that matches nothing is indistinguishable from a clean
repository, so a test SHALL show each check firing on one fixture and staying silent on another, with the fixtures authored through the edge of
[FR-007](./FR-007-authorable-mitigates-edge.md).

## Inputs

- A fixture corpus of two `hazard` documents and two `failure_mode` documents, and one `control` document declaring `mitigates` to one hazard and one failure mode.

## Outputs

- Exactly the findings of the two checks over that corpus.

## Behavior

- The `unmitigated-hazard` check SHALL report each `hazard` that has no incoming `mitigates` edge, naming the hazard.
- The `unmitigated-hazard` check SHALL report nothing for a `hazard` that has an incoming `mitigates` edge.
- The `unmitigated-failure-mode` check SHALL report each `failure_mode` that has no incoming `mitigates` edge, naming the failure mode.
- The `unmitigated-failure-mode` check SHALL report nothing for a `failure_mode` that has an incoming `mitigates` edge.
- With `to: []`, the checks SHALL accept an incoming `mitigates` edge from a document of any type.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | Over the two-hazard fixture, `unmitigated-hazard` yields exactly one finding, and it names the hazard with no incoming `mitigates`. | Test |
| FR-008-AC-2 | Over the two-failure-mode fixture, `unmitigated-failure-mode` yields exactly one finding, and it names the failure mode with no incoming `mitigates`. | Test |
| FR-008-AC-3 | Adding the missing `control` edge to the unmitigated hazard removes its finding and leaves zero `unmitigated-hazard` findings. | Test |
| FR-008-AC-4 | A fixture where no hazard is mitigated yields one finding per hazard, so the check is not inert under `to: []`. | Test |
| FR-008-AC-5 | The two checks are tunable independently: setting `trace:unmitigated-hazard` to `error` and leaving `trace:unmitigated-failure-mode` at its default changes only the hazard findings' severity. | Test |

## Dependencies

- **Upstream**: [FR-007](./FR-007-authorable-mitigates-edge.md); `agent-ix/quire-rs` FR-058 (required-relation evaluation)
