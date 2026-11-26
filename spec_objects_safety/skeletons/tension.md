---
id: TEN-001
title: "ConflictingRequirementReadings"
type: tension
object: tension
status: open
relationships:
  - target: FR-101
    type: conflicts_with
  - target: FR-102
    type: conflicts_with
---
<!-- tension authoring guide. Replace the example with the actual conflict and
     authored disposition. An open record is valid evidence of a conflict, but
     it remains a release finding until a person records a resolution or
     acceptance. `decided_by` is required only for `accepted-by-person` and is
     never inferred. -->
# [TEN-001] ConflictingRequirementReadings

## Conflict

`One requirement requires immediate processing. The other requires a bounded resource limit; the same operation cannot satisfy both readings.`

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| tension_id | UUID | 1..1 | identity |

## Invariants

The conflict is stated by the authors and is not scored or ranked.
