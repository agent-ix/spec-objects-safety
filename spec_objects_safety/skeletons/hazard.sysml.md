---
id: HAZ-001
title: "VehicleCannotDecelerate"
type: hazard
object: hazard
---
<!-- hazard authoring skeleton, alternate Properties form. Declares exactly the
     same fields as hazard.md, authored as one ```sysml``` fence instead of the
     typed table. One artifact carries one form; the alternate is a separate
     file, never a second block in the same artifact. -->
# [HAZ-001] VehicleCannotDecelerate

## Condition

The vehicle does not reduce speed when the operator commands deceleration,
while the vehicle is moving under its own power on a public road.

## Assessment

| Severity | Likelihood | Rationale |
| -------- | ---------- | --------- |
| critical | remote | Loss of commanded deceleration on a public road injures occupants and other road users; the redundant hydraulic path makes the state remote rather than occasional. |

## Properties

```sysml
attribute hazard_id : UUID[1..1] { identity }
attribute condition : String[1..1] { minLength: 1 }
attribute first_observed_at : Timestamp[0..1]
```

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
