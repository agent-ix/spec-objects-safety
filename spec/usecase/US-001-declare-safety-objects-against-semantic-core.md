---
id: US-001
title: "Declare safety objects against the shared semantic core"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-001"
    type: "traces_to"
---
# US-001: Declare safety objects against the shared semantic core

## Story

**As a** maintainer of the safety object module
**I want** the hazard and failure-mode types to be declared once, in the same
declaration grammar every other module uses, and shipped as real schemas
**So that** a reader of a safety document — a person, a generator, or another
module — sees the same contract I authored instead of guessing at it.

This story is the maintainer's perspective in informal language. It does not
prescribe the source language, the schema dialect, or the shape of the manifest;
FR-002..FR-006 choose those.

## Context

The module shipped at version 0.2.0 with `data_schema: {type: object}` on both
of its object types. That is not a contract: it accepts every record, so no
consumer can tell a scored hazard from an empty one, and nothing downstream can
generate a typed reader. Meanwhile the ecosystem has agreed one declaration
grammar (`@agent-ix/semantic-core`) and one module contract (quoin FR-070..075)
that the business and ISO modules have already adopted.

Safety adds one pressure the other modules do not have. A missing assessment in
a business entity is a gap; a missing assessment on a hazard reads, to anything
that sorts or scores, as a *safe* hazard. Whatever this module declares has to
keep "nobody looked" separate from "looked, and it is fine".

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative
only — not test cases and not verification criteria.

### US-001-EX-1: A hazard record is checkable

- **Given** a hazard document declaring its fields in a typed table
- **When** the engine extracts the declaration record
- **Then** the record is validated against a real schema shipped by the module,
  and a hazard with no identity field is reported rather than accepted

### US-001-EX-2: An unassessed axis says so

- **Given** a hazard whose exposure nobody has evaluated
- **When** the assessment is recorded
- **Then** the exposure reads as "not assessed" and cannot be mistaken for the
  safe end of the exposure scale

### US-001-EX-3: A control is referenced, not copied

- **Given** a control that already exists as a `spec-objects-security` object
- **When** a hazard is mitigated by it
- **Then** the hazard names it rather than restating it, so the two cannot drift

## Options (Exploratory)

Approaches discussed: hand-writing the JSON Schemas; generating them from
TypeSpec importing the shared grammar; or leaving `data_schema` inline in the
manifest. Declaring a third object type for controls was also raised and set
aside — `spec-objects-security` already owns `control`.

## Constraints (Contextual)

The module is advisory-only until promotion, and no corpus repository is edited.
Nothing here computes or defaults a safety judgement.

## Dependencies (Contextual)

Upstream: the semantic-core declaration grammar and the Quoin module contract.
Downstream: generated language packages, which are gated elsewhere.

## Priority and Risk (Informative)

High value: without a real schema the module's own acceptance criteria are
unverifiable. The risk if unmet is a safety module whose validity means nothing.

## Notes (Informative)

Open question raised during discovery and answered by FR-006: whether the
cross-module types this module points at should be listed in `semantic.imports`
before those modules publish their own semantic contracts.

## Traceability (Informative)

This story realises the stakeholder need for safety analysis recorded as
validated, linkable objects, and is implemented by FR-002 through FR-006 with
NFR-001 bounding the change.
