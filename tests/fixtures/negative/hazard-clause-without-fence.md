---
id: negative-006
title: "HazardWithAClauseHeadingAndNoFence"
type: hazard
object: hazard
expect: semantic.clause-missing-body
because: "a clause heading with no ocl fence declares a clause that has no text"
---
# [negative-006] HazardWithAClauseHeadingAndNoFence

## Condition

The vehicle does not reduce speed when the operator commands deceleration.

## Assessment

| Severity | Likelihood | Rationale |
| -------- | ---------- | --------- |
| critical | remote | Injures occupants. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| hazard_id | UUID | 1..1 | identity |

## Invariants

### AcceptedHazardCarriesProvenance

The clause text is missing.
