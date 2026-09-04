---
id: FM-001
title: "BrakeControllerStopsPublishing"
type: failure_mode
object: failure_mode
---
<!-- failure_mode authoring skeleton, alternate Properties form. Declares
     exactly the same fields as failure_mode.md, authored as one ```sysml```
     fence instead of the typed table. One artifact carries one form; the
     alternate is a separate file, never a second block in the same artifact. -->
# [FM-001] BrakeControllerStopsPublishing

## Description

The brake controller stops publishing pressure commands on the vehicle bus
while remaining powered, so the actuator holds its last commanded value
instead of following the operator.

## Analysis

| Effect | Cause | Detection |
| ------ | ----- | --------- |
| The actuator holds its last commanded pressure, so commanded deceleration is not applied. | The controller's publish task starves when the diagnostic task overruns its budget. | direct |

## Properties

```sysml
attribute failure_mode_id : UUID[1..1] { identity }
attribute component : String[1..1] { minLength: 1 }
attribute wrong_behaviour : String[1..1] { nonEmpty }
attribute first_seen_in_release : String[0..1] { pattern: /^v[0-9]+\.[0-9]+\.[0-9]+$/ }
attribute observed_occurrences : Integer[0..1] { min: 0 }
```

## Invariants

The clauses this failure-mode declaration enforces. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### UndetectableFailureIsNotClosed

```ocl
context FailureMode
inv UndetectableFailureIsNotClosed:
  self.analysis.detection = Detection::none implies self.status <> LifecycleStatus::closed
```

### AcceptedFailureCarriesProvenance

```ocl
context FailureMode
inv AcceptedFailureCarriesProvenance:
  self.status = LifecycleStatus::accepted implies self.provenance->notEmpty()
```
