---
id: negative-005
title: "HazardWithNoAssessment"
type: hazard
object: hazard
expect: "required 'assessment'"
because: "a hazard cannot be recorded unscored"
---
# [negative-005] HazardWithNoAssessment

## Condition

The vehicle does not reduce speed when the operator commands deceleration.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| hazard_id | UUID | 1..1 | identity |
