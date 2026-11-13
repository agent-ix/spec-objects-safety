---
id: negative-20
title: "acceptability_policy-unfilled-flag"
type: acceptability_policy
object: acceptability_policy
expect: "Outside acceptable"
because: "a region flag has no default and must be set to true or false"
---
# [negative-20] acceptability_policy-unfilled-flag

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
| unacceptable | <true or false> |

## Cells

| Severity | Probability | Region |
| -------- | ----------- | ------ |
| minor | rare | acceptable |
| minor | possible | acceptable |
| minor | likely | reduce further |
| serious | rare | acceptable |
| serious | possible | reduce further |
| serious | likely | reduce further |
| fatal | rare | reduce further |
| fatal | possible | reduce further |
| fatal | likely | unacceptable |

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
