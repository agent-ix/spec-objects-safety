---
id: SR-042
title: "Spec review (integrity) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-301..FR-305, spec/non-functional/NFR-300 (git diff origin/main...b94d61f); context: #33 FR-103..106, #34 FR-202..205, FR-007, spec_objects_safety/manifest.yaml, quire-rs origin/main FR-040, FR-058"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-302"
    type: "references"
---
# Spec review (integrity) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)

## Summary

Ticket: PLAT-1524. This review checks consistency with three sources:

- the open PRs #33 and #34 this PR builds on;
- the shipped manifest;
- quire-rs `origin/main` FR-040 (edge vocabulary) and FR-058 (required
  relations).

## Verdict

The rules are correctly expressed as manifest data, and the engine-gap claims
about FR-058 are accurate. Three high defects block merge:

- FR-302 states the `mitigates` direction backwards.
- FR-302 and FR-205 contradict each other on when the control relations ship.
- FR-303 depends on an edge that FR-103 never names.

Cross-PR duplicates to fix:

- In #34, remove the relation and scoping bullets and AC-3..6 from FR-205.
- In #34, remove the `situation-without-harm` bullet and AC-6 from FR-202.
- In #33, FR-103 should name the residual-risk-to-estimate verb.

The decision not to put `involves`/`can_result_in` in `acyclic_edges` is
correct. FR-304's argument for it cites the wrong diagnostic, though, and
applied consistently the same argument also makes the existing `arises_from`
entry ceremony.

A quire-rs ticket is needed. It should specify a selector that narrows `from`
documents by the presence of an edge with a named verb, direction and
other-end kind, and it must allow OR across directions: an outgoing
`mitigates` or an incoming `assumes_controls`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-302 says a risk control has "an incoming `mitigates` edge", but FR-007 and the manifest have the control author `mitigates`, so the edge is outgoing from the control. The required scope is therefore an outgoing `mitigates` edge to a hazard or failure_mode, OR an incoming `assumes_controls` from a risk_estimate. That changes the shape of the quire-rs selector. | spec/functional/FR-302-risk-control-implemented-and-verified.md:44-48,70 |
| FND-002 | high | FR-302 contradicts FR-205 (#34). FR-205 Behavior says the module SHALL declare both control relations and report only scoped controls, and FR-205-AC-3..6 test that now. FR-302 says FR-205 SHALL NOT declare them, and that they SHALL NOT be declared until the selector exists. Remove the relation and scoping bullets and AC-3..6 from FR-205 in #34, so FR-302 is the only owner. | spec/functional/FR-302-risk-control-implemented-and-verified.md:27-29,52-56 |
| FND-003 | high | FR-303's relation uses "`edges:` the reference verb FR-103 declares", but FR-103 (#33) declares no verb or target. It names only "a reference to the risk". FR-303 files this under "Engine gap", but it is a spec gap in FR-103. FR-103 also gives the residual risk its own post-control severity and probability, which duplicates the FR-204 post_control estimate. Fix in #33: FR-103 names the verb and the `risk_estimate` target and drops the duplicated levels. FR-303 then cites the verb, and FR-303-AC-1 becomes testable. | spec/functional/FR-303-residual-risk-decided-by-named-person.md:54-60,73 |
| FND-004 | medium | FR-301 claims to be the single declaration of `situation-without-harm`, but FR-202 (#34) still specifies the same check in a Behavior bullet and in FR-202-AC-6, which duplicates FR-301-AC-4. Remove both from FR-202 in #34. | spec/functional/FR-301-hazard-reaches-harm-through-situation.md:54 |
| FND-005 | medium | FR-304 Behavior and FR-304-AC-3 say a hazard declaring `involves`, or a harm declaring `can_result_in`, is reported `disallowed-edge-target`. A verb missing from the source's `allowed_links` is the Tier-1 `DisallowedEdgeType` check (FR-040-AC-8), not the Tier-2 target check. Both are warnings (FR-040-AC-10), so the edge still loads, and "a chain cycle cannot be authored" and "by construction" overstate it. Name the right diagnostic. The cycle is reported, not prevented. | spec/functional/FR-304-chain-edges-cannot-cycle.md:36,44 |
| FND-006 | medium | FR-304 applies its value test unevenly. `arises_from` has the same shape as the chain verbs: hazard to failure_mode only, and failure_mode declares no `arises_from`. A cycle over it is possible only through an off-vocabulary edge that Tier-1 already reports, which is the reason given for dropping the chain verbs. FR-304-AC-4 needs exactly such an edge. By FR-304's own argument the `arises_from` entry is ceremony. Delete it, and set AC-1 to an empty `acyclic_edges`, or explain what it guards that the chain verbs do not. | spec/functional/FR-304-chain-edges-cannot-cycle.md:28-30,34,42,45 |
| FND-007 | medium | NFR-300 says each completeness rule of FR-301 to FR-304 SHALL be a `traceability` entry. FR-303 puts the decidedness, person and benefit-risk rules in the schema and in FR-105 instead, and FR-304 declares no entry. The NFR contradicts both. Restrict it to the rules that are relations. | spec/non-functional/NFR-300-completeness-rules-are-data-advisory-and-deterministic.md:22-25 |
| FND-008 | medium | FR-202 allows a situation with zero `involves` edges. No relation reports such a situation, and FR-305's rows are hazard x situation pairs, so it disappears from both the findings and the report. FR-301 claims "a situation that leads nowhere is also reported", but that covers only the harm side. Add an outgoing `situation-has-hazard` relation, or state the gap. | spec/functional/FR-301-hazard-reaches-harm-through-situation.md:37-40,52-53 |
