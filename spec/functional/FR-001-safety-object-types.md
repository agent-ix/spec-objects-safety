---
id: FR-001
title: "The module declares hazard and failure_mode as separate object types"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "satisfies"
---
# FR-001: The module declares hazard and failure_mode as separate object types

## Description

The module **SHALL** declare two object types, each with a body contract, an
authoring skeleton, and a role.

### Why two types and not one

A `failure_mode` answers **"what breaks"**. A `hazard` answers **"what state
must never be reached"**. The second is not derivable from the first, which is
the reason STPA exists: components each behaving exactly as specified can still
interact into a harmful state, and a model that treats hazards as a variety of
failure would lose precisely those.

The shapes differ for the same reason. FMEA scores a failure on **effect,
cause, detection**; hazard analysis scores a state on **severity, likelihood**.
Collapsing them would force one table to mean two things depending on which
type declared it.

`Detection` is the column that earns `failure_mode` its own type: a failure
nobody can observe is a different engineering problem from the same failure
with an alarm on it, and neither severity nor likelihood carries that.

### No new verbs

The ticket that asked for this module assumed safety-chain verbs — `causes`,
`contributes_to` — would be added to the iso vocabulary. Applying that
vocabulary's own first criterion for an addition, *"check the existing 76 — a
near-synonym is a reason not to add"*, says otherwise.

`arises_from` ("Risk arises from a threat/vulnerability", governance) records
exactly the fact `causes` would, read from the hazard end — which is also the
natural authoring direction, since an author writing a hazard document lists
what it arises from. And a hazard arising from several failure modes is several
`arises_from` edges, so `contributes_to` would be a second word for the same
thing.

The causal edge is therefore authored from the hazard only: one edge, one place
to write it. `failure_mode` declares no outgoing safety verb of its own.

No role is declared either. `allowed_links` target concrete object types, as
`spec-objects-security`'s `threat` does, so the `safety-relevant` capability tag
this module first reached for turned out to be unnecessary.

### Why a separate module and not an extension of spec-objects-security

Hazard and failure mode are IEC 61508 / ISO 26262 / FMEA territory. The 23
object types in `spec-objects-security` are STRIDE, identity and crypto.
Merging them would make one module's applicability signals answer for two
regulatory domains — a repository doing threat modelling would inherit hazard
prompts, and one doing safety analysis would inherit STRIDE.

### Condition, not event

A hazard's `Condition` is a **state**. "The brakes fail" is a failure mode
wearing a hazard's name; "the vehicle cannot decelerate on operator command"
stays true regardless of which failure produced it, which is what lets several
failure modes link to one hazard and what lets a hazard exist with none behind
it.

### Mitigation is optional, deliberately

An identified-but-unmitigated hazard is a real and reportable state. Requiring
the section would push an author to write a placeholder rather than leave the
gap visible — and the gap is the finding.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | The manifest declares exactly `hazard` and `failure_mode`, each with a `data_schema` and at least one role. | Test (TC-002) |
| FR-001-AC-2 | `hazard` requires a `Condition` section body and an `Assessment` table with columns exactly `Severity \| Likelihood \| Rationale`; `Mitigation` is optional. | Test (TC-003) |
| FR-001-AC-3 | `failure_mode` requires a `Description` section body and an `Analysis` table with columns exactly `Effect \| Cause \| Detection`. | Test (TC-003) |
| FR-001-AC-4 | Each object type ships an authoring skeleton whose sections supply every heading its contract requires. | Test (TC-005, TC-006) |
| FR-001-AC-5 | The manifest validates against the FR-035 module-manifest schema, with no skip and no escape hatch — the gate ships with the module rather than being retrofitted. | Test (TC-001) |
| FR-001-AC-6 | Every lexicon entry is exactly `{definition: <non-empty string>}`, asserted structurally so an unquoted comma inside a YAML flow mapping cannot silently truncate one. | Test (TC-004) |
| FR-001-AC-7 | Every `allowed_links` verb is present in the iso edge vocabulary — as a forward key or as a declared inverse label — so a future edit reaching for a new verb fails here rather than minting one locally. | Test (TC-007) |

## Constraints

| ID | Constraint | Type | Validation |
|----|-----------|------|------------|
| FR-001-CON-1 | Hazard identification and scoring are authored judgement. Nothing in this module computes, infers, or defaults either. | Design | Inspection |
| FR-001-CON-2 | Every `allowed_links` verb SHALL already exist in the iso vocabulary. No safety-only verb is minted. | Design | Test (TC-007) |

## Dependencies

- **Upstream**: [StR-001](../stakeholder/StR-001-safety-object-types.md); `spec-artifacts-iso` FR-004 (the edge vocabulary the safety-chain verbs join)
- **Downstream**: `spec-objects-security#5` bidirectional hazard↔requirement coverage, as declared required-relations against quire-rs FR-058
