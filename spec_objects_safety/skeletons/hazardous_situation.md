---
id: SIT-001
title: "OperatorCommandsDecelerationOnPublicRoad"
type: hazardous_situation
object: hazardous_situation
---
<!-- hazardous_situation authoring skeleton (spec-objects-safety). Fill every
     section with substantive content. Contract (manifest body_extraction
     asserts):
     - Frontmatter MUST carry id, title, type: hazardous_situation,
       object: hazardous_situation.
     - "## Description" (H2) is REQUIRED: the case in which the hazard state
       coincides with something that can be hurt.
     - "## Sequence of Events" (H2) is OPTIONAL: the events that lead from the
       hazard state to the harm, in order.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - Keep headings unique per level; never leave a section empty.

     A HAZARDOUS SITUATION IS A CASE, NOT A STATE AND NOT A JUDGEMENT. It
     promotes the free string `context.situation` of a hazard to an object; that
     string stays valid and nothing migrates it. The situation carries no
     severity, probability, score or acceptance: those belong to a risk estimate
     of this situation.

     LINK THE SITUATION TO THE HAZARD IT ARISES FROM. Add one `arises_from`
     relationship per hazard to the frontmatter (one or more):

       relationships:
         - target: HAZ-001
           type: arises_from

     The effect end authors the edge, so a hazard never lists its situations.
     A harm that can follow links to this situation from its own end. -->
# [SIT-001] OperatorCommandsDecelerationOnPublicRoad

## Description

The vehicle cannot decelerate on operator command while it is moving under its
own power on a public road with other road users close ahead.

## Sequence of Events

1. The operator commands deceleration on a public road.
2. The vehicle does not reduce speed.
3. The vehicle reaches the road user ahead.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| situation_id | UUID | 1..1 | identity |
| description | String | 1..1 | minLength: 1 |

## Invariants

The clauses this hazardous-situation declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### SituationCarriesNoScore

```ocl
context HazardousSituation
inv SituationCarriesNoScore:
  self.score->isEmpty()
```
