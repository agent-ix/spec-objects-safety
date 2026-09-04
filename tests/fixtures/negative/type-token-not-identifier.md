---
id: negative-004
title: "HazardWithABareTypeToken"
type: hazard
object: hazard
expect: semantic.invalid-type-token
because: "a Type cell must be a kernel scalar or a resolvable declaration name"
---
# [negative-004] HazardWithABareTypeToken

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
| severity | 42 not an identifier | 1..1 | |
