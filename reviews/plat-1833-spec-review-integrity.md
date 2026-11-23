---
id: SR-411
title: "Spec review (integrity, EARS) — spec-objects-safety FR-010"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-010-hazard-causes-beyond-failure-modes.md, spec/functional/index.md, spec/tests.md"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-010", type: references }
---

## Summary

Ticket: PLAT-1833. Integrity and EARS pass over the new FR-010 and its index and test-matrix rows. `quire validate` on FR-010 reports three EARS grammar warnings. The relationships and dependency links resolve.

## Verdict

**CONDITIONAL** — FR-010 states the change accurately. It quotes no standard text and assigns no score or acceptability. Three Behavior statements have no acceptance criterion, and two statements break EARS form.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Three Behavior SHALLs have no AC: no cause is required (a hazard with no `arises_from` stays valid), no schema key carries severity/likelihood/acceptability for a cause, and the control's own `mitigates` edge stays unchanged — the last describes spec-objects-security's manifest, which this module cannot test or own. | spec/functional/FR-010-hazard-causes-beyond-failure-modes.md:47,50,52 |
| FND-002 | low | EARS warnings: line 27 "A failure mode SHALL allow a reference..." has no system subject, and line 47 holds two SHALLs in one statement. | spec/functional/FR-010-hazard-causes-beyond-failure-modes.md:27,47 |

## Coverage

- Sub-analyses run: spec-integrity-analysis, spec-ears-analysis (via `quire validate` grammar diagnostics). Others not applicable to this diff.
- spec/tests.md: FR-010 summary row and TC-110..TC-113 rows checked against the tagged tests; consistent.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Commit `c58dbb2` deletes the control-`mitigates` SHALL and backs the other two with FR-010-AC-6 (TC-115) and FR-010-AC-7 (TC-116). |
| FND-002 | fixed | `quire validate` on FR-010 at `c58dbb2` reports no EARS or other warning. |
| FND-003 | fixed | Commit `c4b8599` deletes all five `semantic.imports` SHALLs and the imports Input/Output lines from FR-006. `imports: {}` stays specified by FR-003 Behavior line 41 and asserted by TC-026 (`semantic_block["imports"] == {}`). `quire matrix` shows no criterion removed, added or newly untagged versus c58dbb2. |
| FND-004 | fixed | Commit `c4b8599` removes the SHALL NOT bullet and states the SOUP-rule limitation as Description prose. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | FR-006-AC-3 and FR-006-CON-2 were removed, but FR-006 Behavior lines 45-49 still state the `semantic.imports` SHALLs, now with no AC; line 48 ("the manifest SHALL name the open migration issues") is the issue-id tracking rule whose test was deleted as ceremony and should go too. | spec/functional/FR-006-cross-module-references.md:45-49 |
| FND-004 | low | New FR-010 Behavior line 54 is a SHALL NOT with no AC that records an engine limitation (rationale), not module behaviour; it belongs in Description prose. | spec/functional/FR-010-hazard-causes-beyond-failure-modes.md:54 |
