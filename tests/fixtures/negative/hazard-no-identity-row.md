---
id: negative-001
title: "HazardWithoutIdentity"
type: hazard
object: hazard
expect: semantic.record-invalid
because: "Hazard.json requires at least one identity field"
---
# [negative-001] HazardWithoutIdentity

## Condition

The vehicle does not reduce speed when the operator commands deceleration.

## Assessment

| Severity | Likelihood | Rationale |
| -------- | ---------- | --------- |
| critical | remote | Injures occupants. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| condition | String | 1..1 | minLength: 1 |
