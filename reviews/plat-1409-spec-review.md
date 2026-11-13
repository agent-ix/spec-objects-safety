---
id: SR-031
title: "Spec review (base) of PLAT-1409 harm, hazardous situation, risk estimate and control links (spec-objects-safety#34)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-201..FR-205, spec/non-functional/NFR-201, spec/functional/index.md, spec/non-functional/index.md (git diff origin/main...plat-1409-spec)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-202"
    type: "references"
---
# Spec review (base) of PLAT-1409 harm, hazardous situation, risk estimate and control links (spec-objects-safety#34)

## Summary

Ticket: PLAT-1409. Review set: subset (base checklist, dependency analysis,
EARS conformance). This file is the base checklist. I read the PR diff, the
module manifest, FR-004 and FR-007 on `origin/main`, the `spec-artifacts-iso`
`edge_types` and archetype `allowed_links` on `origin/main`, the
`spec-objects-security` `control` and `risk` types on `origin/main`, and the
quire-rs Tier-1/Tier-2 edge checks (`src/validate_document.rs`,
`src/corpus/validate.rs`) and `required_relations` engine
(`src/corpus/required_relations.rs`) on `origin/main`.

`quire validate --scope . "spec/**/*.md"` (quire 0.44.0, engine 0.59.1)
reports no errors in any new file, only EARS warnings (see the EARS review).
The one failing document is `spec/tests.md` (TestMatrix column headings). It
fails the same way on `origin/main`, so that failure predates this PR.

The diff names no standard and quotes no standard clause. IDs FR-201..FR-205
and NFR-201 do not collide with PR #33 (FR-101..FR-107, NFR-100). No
requirement creates a hash, digest, pin, ledger or file-tracking record. The
`provenance` fields are person attributions FR-004 already defines, not file
tracking.

Answer to the author's open question 1 (edge verbs). `involves`/`involved_in`
and `can_result_in`/`possible_result_of` are not in the `spec-artifacts-iso`
`edge_types`. An existing verb fits: `arises_from` (governance, "Risk arises
from a threat/vulnerability"). This module already uses it for
hazard-from-failure-mode and lists it in `acyclic_edges`. Recommendation:
author `hazardous_situation arises_from hazard` and
`harm arises_from hazardous_situation`. That reuses one verb, and the existing
acyclicity check then covers the whole failure mode, hazard, situation, harm
chain. The only vocabulary change is an inverse label on `arises_from` (for
example `gives_rise_to`) in `spec-artifacts-iso`. PLAT-160 added `specified_by`
to `specifies` the same way, and FR-004-CON-1 there counts that as no new verb.
If the situation end must author both hops, no existing verb reads correctly
for situation-to-harm (`triggers` and `affects` mean something else). Then
`can_result_in` should be added as a new `edge_types` entry with its inverse.
Either way FR-202 has to pick one, not defer the choice (FND-001).

Answer to the author's open question 2 (`satisfies`/`verifies` to a
`control`). Measured against quire-rs `origin/main`: both are accepted today
with no widening. `FR`/`NFR`/`IT`/`TC` `allowed_links` in `spec-artifacts-iso`
are plain verb lists, so no target is constrained. `satisfies` is not a forward
verb; it is the declared inverse of `satisfied_by`. Tier-1 accepts any declared
inverse label (that is also why an `NFR` may author it, though `NFR`
`allowed_links` omits it). Tier-2 normalizes `(FR, satisfies, control)` to
`(control, satisfied_by, FR)`. `control.allowed_links` in
`spec-objects-security` has no `satisfied_by` entry, so the target check skips
the edge. `verifies` is in `IT`, `TC` and `NFR` `allowed_links`, but not `FR`.
It is a forward verb with no inverse, unconstrained. So no change is needed in
either module for the edges to validate. The descriptions are worded for a
stakeholder requirement and a requirement, but nothing reads them. The
consequence is FND-010: the "no `disallowed-edge-target`" criteria cannot fail.

## Verdict

The structure is sound: no stored score, region or acceptance; human-entered
values; facts authored at one end. Changes are needed before implementation.
FR-202 must decide its verbs. FR-202 and FR-203 have gaps between Behavior and
criteria. FR-203 does not say how a pre-control estimate relates to the
existing `hazard.assessment` or to the security module's `risk`. FR-201 lets a
harm carry `status: accepted`. FR-205's no-warning criteria are vacuous. The
cross-PR and dependency defects are in the dependency review (SR-032), and
three of those are high.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-202 leaves the chain verbs undecided ("decided against that vocabulary's own criteria; whichever words are chosen"), yet AC-1..AC-3, AC-6 and AC-7 name `involves` and `can_result_in`. Neither verb nor its inverse exists in `spec-artifacts-iso` `edge_types`. Decide in the spec. Recommended: `arises_from` for both hops (situation to hazard, harm to situation), plus one inverse label in iso. | spec/functional/FR-202-hazardous-situation-object-and-chain.md:31-40 |
| FND-002 | medium | The FR-202 edge table says `involves` targets "`hazard` (one or more)", but Behavior says "zero or more `involves` edges". No criterion and no advisory check covers a situation that involves no hazard. Make the cardinality agree, and add a criterion (or a `situation-without-hazard` check) for the zero case. | spec/functional/FR-202-hazardous-situation-object-and-chain.md:33,59 |
| FND-003 | low | The FR-202 definition "a circumstance in which a person, property or the environment is exposed to a hazard" closely paraphrases a paywalled standard's defined term. Use the module's own wording, and put it in the manifest `lexicon` as FR-201 does for `harm`. | spec/functional/FR-202-hazardous-situation-object-and-chain.md:24-25 |
| FND-004 | medium | FR-201 forbids an `acceptance` key on a harm, but admits `status` with the hazard rule, and `LifecycleStatus` includes `accepted`. So a harm can carry an acceptance through `status: accepted`. A harm has no severity, so accepting it means nothing, and NFR-201 places acceptance outside these records. Either restrict harm `status` to members other than `accepted`, or drop `status` from harm. | spec/functional/FR-201-harm-object-type.md:41 |
| FND-005 | medium | FR-203 adds pre-control severity and probability on `risk_estimate`, but `hazard.assessment` (FR-004) already carries a required severity and likelihood per hazard. FR-203 does not say whether `hazard.assessment` is the pre-control estimate, is superseded, or is a separate judgement. Two places for one judgement will drift, which is the rule FR-202 cites against duplication. State the relation. | spec/functional/FR-203-pre-control-risk-estimate.md:21-27 |
| FND-006 | medium | FR-004 says "No schema SHALL declare a safety-domain type that another module already owns; a control, risk ... is named by `SemanticId`". `spec-objects-security` already declares `risk` with `likelihood` and `impact`. FR-203 declares `risk_estimate` without saying why it is not that `risk`, or how the two relate. Add the boundary statement, or reference `risk`. | spec/functional/FR-203-pre-control-risk-estimate.md:17-19 |
| FND-007 | medium | FR-203 Behavior requires "exactly one outgoing `estimates` edge", but no criterion tests an estimate with zero or two `estimates` edges. AC-7 covers only a wrong target type. The FR also does not say which mechanism enforces the count: frontmatter `relationships` are not schema-counted, and `required_relations` checks presence only. Add the error-path criteria and name the mechanism. | spec/functional/FR-203-pre-control-risk-estimate.md:47 |
| FND-008 | low | FR-203 names the field `probability` but reuses the `Likelihood` members. The module lexicon defines likelihood as "how often the hazard state is expected to be reached", which is not the probability of harm in a situation. Rename the field to `likelihood`, or add a lexicon entry for `probability`. | spec/functional/FR-203-pre-control-risk-estimate.md:24-26 |
| FND-009 | medium | FR-204 says both "the estimate authors the `assumes_controls` list" (a field) and "edges to controls". If it is a schema field, quire's `disallowed-edge-target` and dangling-target checks never see it, so AC-3 and AC-4 cannot pass. If it is a frontmatter relationship, `assumes_controls` is a noun phrase, not a verb like the rest of the vocabulary. Say which, and if it is an edge, use a verb such as `assumes`. | spec/functional/FR-204-post-control-risk-estimate.md:23-24,40-42 |
| FND-010 | medium | FR-205-AC-1 and AC-2 pass only on the absence of `disallowed-edge-target`. quire-rs never emits that warning for these edges: `satisfies` normalizes to `control satisfied_by`, which `control` does not constrain, and iso `verifies` is unconstrained. So both criteria pass with any target type and cannot fail. Assert the resolved incoming edge on the control in `quire extract` output instead. | spec/functional/FR-205-control-requirement-and-verification-links.md:68-69 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-011 | medium | FR-204 says "The schema SHALL require a `post_control` estimate to carry at least one `assumes` edge", and FR-203 says "The schema SHALL forbid an assumed-controls edge on a `pre_control` estimate". Edges are frontmatter `relationships:`, which the record schema never sees: the yield pattern extracts id, title, type and sections, and FR-004 itself routes edges to the traceability model rather than a schema key. So FR-204-AC-2 and FR-203-AC-6 cannot pass as specified. Use a `required_relations` entry (`from: risk_estimate`, `where: {field: phase, values: [post_control]}`, `edges: [assumes]`, `direction: outgoing`) and make AC-2 expect its advisory warning. `phase` must then be a frontmatter field. For the pre-control prohibition, either name an engine mechanism that rejects an edge by phase, or drop it. | spec/functional/FR-204-post-control-risk-estimate.md:48; spec/functional/FR-203-pre-control-risk-estimate.md:73 |
| FND-012 | low | FR-203 now types `severity`/`probability` as "a non-empty string or an `EpistemicState` member". A free string also matches `unknown`, `not_assessed` and `not_applicable`, so nothing stops a project from naming a level `not_assessed`, and FR-203-AC-3 ("stay distinct from every level string") cannot be shown. Exclude the three members from the level string (for example `not: {enum: [...]}`), and add a criterion that a level string equal to one of them is refused. | spec/functional/FR-203-pre-control-risk-estimate.md:71,85 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | 33c79d4: FR-202 uses `arises_from` for both hops. It needs one `spec-artifacts-iso` inverse label, which is listed as an upstream dependency. AC-1..AC-9 use that verb. |
| FND-002 | fixed | 33c79d4: the table says one or more. `situation-has-hazard` is declared outgoing. AC-6 tests the zero case and AC-7 two hazards. |
| FND-003 | fixed | 33c79d4: the definition is in the module's own wording ("a case in which a hazard state coincides with something that can be hurt") and is placed in the lexicon (AC-10). |
| FND-004 | fixed | 33c79d4: the harm schema forbids `status`. AC-3 includes `status: accepted`. |
| FND-005 | fixed | 33c79d4: FR-203 "Relation to other judgements" makes `hazard.assessment` and the estimate different subjects, neither derived from the other. AC-12 tests this. |
| FND-006 | fixed | 33c79d4: FR-203 states `risk_estimate` is not security `risk` and does not redeclare it. AC-13 checks that no `risk` type is declared. |
| FND-007 | fixed | 33c79d4: presence is enforced by `estimate-has-situation` (AC-9). The upper bound is explicitly not enforced, and AC-10 tests two edges. |
| FND-008 | fixed | 33c79d4: a lexicon entry `probability` is added with its own meaning (AC-13). |
| FND-009 | fixed | 33c79d4: the link is an edge, the verb is `assumes`, and AC-1 asserts the resolved incoming edge. Schema enforcement of that edge is new finding FND-011. |
| FND-010 | fixed | 33c79d4: FR-205-AC-1 and AC-2 assert the resolved incoming `satisfied_by`/`verifies` edge in `quire extract`, which can fail. |
| FND-011 | fixed | Round 2 (4ef0e38): FR-204 declares `post-control-assumes-control` with `where: {field: phase, values: [post_control]}`, `to: [control]`, outgoing. AC-2, AC-7, AC-8 and AC-9 test the warning, the pre-control silence, promotion and the dangling-target case. FR-203 makes `phase` a top-level frontmatter key (AC-6) and states that the pre-control edge ban is not enforced. |
| FND-012 | fixed | Round 2 (4ef0e38): FR-203 types a level as a non-empty string equal to none of the three `EpistemicState` members, or as exactly one of them. AC-14 checks that the emitted level branch excludes the markers. |
