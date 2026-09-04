---
id: negative-003
title: "HazardWithBothPropertiesForms"
type: hazard
object: hazard
expect: semantic.properties-both-forms
because: "one artifact carries one Properties form; the alternate is a separate file"
---
# [negative-003] HazardWithBothPropertiesForms

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

```sysml
attribute hazard_id : UUID[1..1] { identity }
```
