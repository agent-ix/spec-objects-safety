---
id: StR-001
title: "Safety analysis is recorded as validated, linkable objects"
type: StR
---
# StR-001: Safety analysis is recorded as validated, linkable objects

## Stakeholder Need

A team working to a safety standard **SHALL** record hazards and
failure modes as first-class specification objects — validated on the same path
as every other artifact, and linkable to the requirements that mitigate them —
rather than as prose in a document nothing checks.

## Rationale

Safety analysis that lives in prose is analysis nothing can check. A hazard
recorded as a paragraph cannot be scored consistently, cannot be counted, and
cannot be linked to the requirement that mitigates it — so nobody can answer
"which hazards have nothing addressing them", which is the only question the
analysis exists to answer.

Recording hazards as validated objects on the same path as every other artifact
makes that question a query instead of a reading exercise.

## Validation Criteria

| ID | Criteria | Validation |
|----|----------|------------|
| StR-001-VC-1 | A hazard and a failure mode each validate against a declared body contract, so an unscored or unstated one is reported rather than accepted. | Test |
| StR-001-VC-2 | A hazard links to the failure modes that cause it and the requirements that mitigate it, using the ecosystem's declared edge vocabulary rather than a safety-only dialect. | Inspection |
