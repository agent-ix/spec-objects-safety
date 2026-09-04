---
id: HAZ-001
title: "VehicleCannotDecelerate"
type: hazard
object: hazard
---
<!-- hazard authoring skeleton (spec-objects-safety). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: hazard, object: hazard.
     - "## Condition" (H2) is REQUIRED.
     - "## Assessment" (H2) is REQUIRED: a table with headers exactly
       Severity | Likelihood | Rationale and at least one data row.
     - "## Properties" (H2): one typed row per attribute, header exactly
       `Field | Type | Multiplicity | Constraints`. At least one row carries
       the `identity` constraint. A ```sysml``` fence is the alternate form of
       the same declarations (hazard.sysml.md); one artifact carries one form.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```ocl``` fence.
     - "## Mitigation" (H2) is OPTIONAL.
     - Keep headings unique per level; never leave a section empty.

     WRITE THE CONDITION AS A STATE, NOT AN EVENT. "The brakes fail" is a
     failure mode wearing a hazard's name. "The vehicle cannot decelerate on
     operator command" is a state, and it stays true regardless of which
     failure produced it — which is what lets several failure modes link to
     one hazard, and what lets a hazard exist with no failure behind it at
     all. STPA exists because components each behaving exactly as specified
     can still reach a harmful state together.

     SEVERITY is how bad the harm is if the state is reached:
       negligible | marginal | critical | catastrophic
     LIKELIHOOD is how often the state is expected to be reached:
       incredible | improbable | remote | occasional | probable | frequent
     Both are checked by lint rules (`quire lint`). If you work to a specific
     standard, map its scale onto these buckets rather than adding a column.

     AN AXIS NOBODY SCORED IS WRITTEN AS SUCH, never left blank and never
     written as the safe end of the scale. `Hazard.json` admits `unknown`,
     `not_assessed` and `not_applicable` on every scored axis precisely so
     that "nobody looked" cannot be read as "negligible".

     THE PROPERTIES TABLE IS NOT A SECOND ASSESSMENT. It declares the hazard's
     own attributes — its identity, its condition text, when it was first
     observed. Severity, likelihood, exposure and controllability live in the
     Assessment table above and are typed by `HazardAssessment` in the emitted
     schema; restating them as fields would create a second copy that drifts.

     MITIGATION IS OPTIONAL ON PURPOSE. An identified-but-unmitigated hazard
     is a real and reportable state. Requiring the section would make authors
     write a placeholder instead of leaving the gap visible. There is no
     `controls` key on the record for the same reason: the mitigation edge is
     authored from the requirement's end (`mitigates`), and the manifest's
     traceability model reads it from there. -->
# [HAZ-001] VehicleCannotDecelerate

## Condition

The vehicle does not reduce speed when the operator commands deceleration,
while the vehicle is moving under its own power on a public road.

## Assessment

| Severity | Likelihood | Rationale |
| -------- | ---------- | --------- |
| critical | remote | Loss of commanded deceleration on a public road injures occupants and other road users; the redundant hydraulic path makes the state remote rather than occasional. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| hazard_id | UUID | 1..1 | identity |
| condition | String | 1..1 | minLength: 1 |
| first_observed_at | Timestamp | 0..1 | |

## Invariants

The clauses this hazard declaration enforces. Each clause owns one `ocl` fence
under its own `### <clauseId>` heading; the fence text is carried verbatim and
never evaluated here.

### AcceptedHazardCarriesProvenance

```ocl
context Hazard
inv AcceptedHazardCarriesProvenance:
  self.status = LifecycleStatus::accepted implies self.provenance->notEmpty()
```

### UnassessedSeverityIsNotClosed

```ocl
context Hazard
inv UnassessedSeverityIsNotClosed:
  self.assessment.severity = EpistemicState::not_assessed implies self.status <> LifecycleStatus::closed
```

## Mitigation

The braking requirements that address this state link here with `mitigates`.
Omit this whole section if nothing mitigates the hazard yet — that absence is
the finding, and the `unmitigated-hazard` check reports it.
