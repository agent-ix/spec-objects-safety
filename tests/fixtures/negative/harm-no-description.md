---
id: negative-006
title: "HarmWithoutDescription"
type: harm
object: harm
expect: "required 'description'"
because: "a harm names what is harmed"
---
# [negative-006] HarmWithoutDescription

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| harm_id | UUID | 1..1 | identity |
| description | String | 1..1 | minLength: 1 |

## Invariants

The clauses this harm declaration enforces. Each clause owns one `ocl` fence
under its own `### <clauseId>` heading; the fence text is carried verbatim and
never evaluated here.

### HarmCarriesNoSeverity

```ocl
context Harm
inv HarmCarriesNoSeverity:
  self.severity->isEmpty()
```
