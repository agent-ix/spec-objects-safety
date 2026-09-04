---
id: FM-001
title: "BrakeControllerStopsPublishing"
type: failure_mode
object: failure_mode
---
<!-- failure_mode authoring skeleton (spec-objects-safety). Fill every section
     with substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: failure_mode,
       object: failure_mode.
     - "## Description" (H2) is REQUIRED.
     - "## Analysis" (H2) is REQUIRED: a table with headers exactly
       Effect | Cause | Detection and at least one data row.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint. A ```sysml``` fence is the alternate form of
       the same declarations (failure_mode.sysml.md).
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     A FAILURE MODE IS NOT A HAZARD. This type answers "what breaks"; a
     `hazard` answers "what state must never be reached". One failure mode can
     contribute to several hazards, and a hazard can exist with no failure
     mode behind it. The causal edge is authored from the hazard end
     (`arises_from`), so nothing is written here to state it twice.

     DETECTION is the column that earns this type:
       none      — nothing observes it; discovered only by its effect
       indirect  — inferable from other signals, by someone looking
       direct    — an explicit signal exists for this failure
       automatic — detected and acted on without a human
     A failure nobody can detect is a different engineering problem from the
     same failure with an alarm on it, and neither severity nor likelihood
     carries that. Checked by the `failure-mode-detection` lint rule.

     `none` MEANS "NOTHING OBSERVES IT", which is an answer. When nobody has
     evaluated detectability yet, `FailureMode.json` admits `not_assessed`;
     the two must never be collapsed, because one is the worst case on the
     axis and the other is an empty backlog row.

     THE PROPERTIES TABLE IS NOT A SECOND ANALYSIS. It declares the failure
     mode's own attributes; effect, cause and detection live in the Analysis
     table above and are typed by `FailureAnalysis` in the emitted schema. -->
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

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| failure_mode_id | UUID | 1..1 | identity |
| component | String | 1..1 | minLength: 1 |
| wrong_behaviour | String | 1..1 | nonEmpty |
| first_seen_in_release | String | 0..1 | pattern: /^v[0-9]+\.[0-9]+\.[0-9]+$/ |
| observed_occurrences | Integer | 0..1 | min: 0 |

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
