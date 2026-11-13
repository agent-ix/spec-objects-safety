---
id: negative-007
title: "SituationWithoutDescription"
type: hazardous_situation
object: hazardous_situation
expect: "required 'description'"
because: "a situation describes the case"
---
# [negative-007] SituationWithoutDescription

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| situation_id | UUID | 1..1 | identity |
| description | String | 1..1 | minLength: 1 |

## Invariants

The clauses this hazardous-situation declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### SituationCarriesNoScore

```ocl
context HazardousSituation
inv SituationCarriesNoScore:
  self.score->isEmpty()
```
