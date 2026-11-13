---
id: negative-21
title: "acceptability_policy-no-cells"
type: acceptability_policy
object: acceptability_policy
expect: "required 'cells'"
because: "the cell table is required"
---
# [negative-21] acceptability_policy-no-cells

## Severity levels

| Severity level |
| -------------- |
| minor |
| serious |
| fatal |

## Probability levels

| Probability level |
| ----------------- |
| rare |
| possible |
| likely |

## Regions

| Region | Outside acceptable |
| ------ | ------------------ |
| acceptable | false |
| reduce further | true |
| unacceptable | true |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| policy_id | UUID | 1..1 | identity |
| reviewed_at | Timestamp | 0..1 | |

## Invariants

The clauses this acceptability-policy declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### PolicyCarriesNoScore

```ocl
context AcceptabilityPolicy
inv PolicyCarriesNoScore:
  self.score->isEmpty()
```
