---
type: master-requirements
name: spec-objects-safety
org: agent-ix
component_type: filament-module
---
# Master Requirements Specification

## Purpose

Declare the **safety** object types — `hazard` and `failure_mode` — so safety
analysis is recorded as validated, linkable specification objects rather than
as prose nothing can check.

## Scope

In scope: two object types, their body contracts, their authoring skeletons,
and a domain lexicon.

Out of scope: bidirectional hazard↔requirement coverage checking, which is
declared required-relations against quire-rs FR-058 rather than code in this
module (agent-ix/spec-objects-security#5); and automated hazard identification,
which does not exist — identification and scoring are authored judgement.

## System Overview

A Filament Module, activated by `filament-core-service` and reached through
`cloudmanager-local-sync`. It ships `manifest.yaml` plus one authoring skeleton
per object type, and contributes its object types, `allowed_links` and lexicon
to the merged registry that `quire validate` reads.

Its lineage is IEC 61508 / ISO 26262 / FMEA / STPA. That is a different
regulatory domain from the STRIDE, identity and crypto types in
`spec-objects-security`, which is why the two are separate modules: merged,
one module's applicability signals would answer for both.

## Requirements Architecture

One stakeholder requirement and one functional requirement.
[StR-001](./stakeholder/StR-001-safety-object-types.md) states the need — safety
analysis as validated, linkable objects.
[FR-001](./functional/FR-001-safety-object-types.md) satisfies it by declaring
the two object types, and carries the reasoning for why they are two types
rather than one.

## References

- IEC 61508 — functional safety of electrical/electronic systems
- ISO 26262 — road-vehicle functional safety
- FMEA — failure mode and effects analysis (the effect/cause/detection triple)
- STPA — systems-theoretic process analysis, the reason a hazard is not
  derivable from a set of failure modes
- `spec-artifacts-iso` FR-004 — the edge-type and role vocabulary the
  safety-chain verbs join
