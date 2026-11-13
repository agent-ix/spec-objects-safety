---
id: HARM-001
title: "OccupantInjuredInCollision"
type: harm
object: harm
---
<!-- harm authoring skeleton (spec-objects-safety). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: harm, object: harm.
     - "## Description" (H2) is REQUIRED: what is harmed, and how.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     A HARM IS WHAT HAPPENS TO A PERSON, PROPERTY OR THE ENVIRONMENT. It is not
     a hazard (a state) and not a hazardous situation (a case in which a hazard
     state coincides with something that can be hurt).

     A HARM CARRIES NO SEVERITY, NO PROBABILITY AND NO STATUS. Severity belongs
     to a risk estimate, because the same harm is more or less severe depending
     on the situation and the controls in place. An acceptance of a harm means
     nothing: acceptance is recorded only on the residual-risk decision.

     LINK THE HARM TO THE SITUATIONS IT ARISES FROM. Add one `arises_from`
     relationship per hazardous situation to the frontmatter:

       relationships:
         - target: SIT-001
           type: arises_from

     The effect end authors the edge, so a hazardous situation never lists its
     harms. -->
# [HARM-001] OccupantInjuredInCollision

## Description

An occupant of the vehicle suffers physical injury in a collision with another
road user or a fixed object.

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
