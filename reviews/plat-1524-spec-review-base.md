---
id: SR-041
title: "Spec review (base) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-301..FR-305, spec/non-functional/NFR-300, spec/functional/index.md, spec/non-functional/index.md, spec/index.md (git diff origin/main...b94d61f)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-302"
    type: "references"
---
# Spec review (base) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)

## Summary

Ticket: PLAT-1524. PR `agent-ix/spec-objects-safety#36`, head `b94d61f`. The
review covers only `git diff origin/main...HEAD`. Open PRs #33 (PLAT-1523,
FR-101..107) and #34 (PLAT-1409, FR-201..205) were read for context.

Sub-analyses chosen by scope: integrity (SR-042) and EARS conformance (SR-043).
No AssuranceProfile applies: the repo has none.

`quire validate --scope . "spec/**/*.md"` (quire 0.44.0, engine 0.59.1) gives
no errors on the new files. It gives two `ears:non-singular` warnings
(FR-303:76, FR-305:71). `spec/tests.md` fails on its column headers, but that
file is not in this diff and the failure predates the PR.

The three engine-gap claims were checked against quire-rs `origin/main`
FR-058 and `src/traceability.rs`:

- one hop per relation: true;
- `where` reads only a top-level frontmatter field of the `from` document, so
  it cannot scope by the presence of an edge: true;
- no test on the value of a field of the target document (FR-058-AC-15): true.

## Verdict

The ACs are mostly concrete fixture tests. No standard text or standard name
appears. No score, region or acceptance is stored or defaulted. Changes are
requested on four points:

- FR-302 cannot be built as written.
- FR-302's definition of "verified" is weaker than the ticket asks.
- FR-303 depends on `phase` being frontmatter.
- FR-305 leaves its host and output contract open.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-302-AC-1 and FR-302-AC-8 cannot pass. The incoming-edge selector has no field name or shape, and `RawRequiredRelation` is `deny_unknown_fields`, so any new key fails at module load today. AC-8 needs a link to a quire-rs ticket that does not exist ("an open question for the planner"). File the ticket, link it, and state the selector's declared shape. | spec/functional/FR-302-risk-control-implemented-and-verified.md:46-58,70-71,80,87 |
| FND-002 | medium | FR-302 defines "verified effective" as a test document whose ACs are tagged in the computed Test Matrix, or a retained evidence record. But `control-has-verification` (`to: []`, edge exists) is satisfied by any document with a `verifies` edge, and no AC checks the matrix condition. The ticket asks for "test coverage in the matrix". Either narrow the definition to what the rule checks, or add a rule and AC for the matrix condition. | spec/functional/FR-302-risk-control-implemented-and-verified.md:33-40,71 |
| FND-003 | medium | `post-control-estimate-has-decision` uses `where: {field: phase}`. FR-058 reads only a top-level frontmatter key, but FR-203 does not say that `phase` is frontmatter. If `phase` is body-extracted, as the hazard assessment is, the relation selects nothing. FR-303 should require `phase` as a top-level frontmatter key, with an AC. | spec/functional/FR-303-residual-risk-decided-by-named-person.md:73 |
| FND-004 | medium | FR-305 leaves open which tool hosts the report and what its output contract is ("an open question for the planner"). AC-1, AC-5 ("the machine-readable schema declares none") and AC-8 therefore have nothing to run against. Name the host command and the output format. | spec/functional/FR-305-risk-summary-report.md:52-55,78,82,85 |
| FND-005 | low | Several ACs restate criteria that other FRs already own: FR-303-AC-5/6/7/8 repeat FR-105-AC-5, FR-103-AC-2, FR-105-AC-1 and FR-104-AC-1, and FR-305-AC-8 repeats FR-104-AC-4. One behaviour then traces to two ACs. Cite the owning AC instead. | spec/functional/FR-303-residual-risk-decided-by-named-person.md:88-91 |

## Not findings

- FR-301-AC-1..8 and FR-304-AC-1/2 are concrete and can fail.
- The `depends_on` targets resolve to existing or in-flight ids.
- No paywalled standard text or names appear.
- No score, region or acceptance is stored or defaulted.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | medium | FR-305's row has a single `policy_region` ("the policy's own label for the entered levels"), but a row can hold several pre-control and post-control estimates (FR-305-AC-10). The contract does not say which estimate's levels the region belongs to, so two implementers would differ. Move `policy_region` into each `pre_control`/`post_control` entry, or name the one estimate it is computed from. FR-305-AC-3 should then name that entry. | spec/functional/FR-305-risk-summary-report.md:50,87 |

## Dispositions

Round 1, head `0da287c`. Committed in `reviews/` as SR-041; the review comment on PLAT-1524 carries the pre-renumbering id SR-024. `quire validate --scope . "spec/**/*.md"` reports no error or warning on FR-301..305 or NFR-300.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-302 states the `when_any` selector shape and links quire-rs ticket PLAT-1674, which exists. AC-1 is explicitly conditional on PLAT-1674 landing, by design. |
| FND-002 | fixed | FR-302 now defines "verified" as an incoming `verifies` edge from any document, and says it does not test Test Matrix tagging. |
| FND-003 | fixed | FR-303 requires `phase` as a top-level frontmatter key of `risk_estimate`, in a Behavior bullet, and FR-303-AC-5 tests it. |
| FND-004 | fixed | FR-305 names the host, `quoin risk-summary <scope> [--format markdown\|json]` under PLAT-1576, and gives a JSON output contract with an exact key set. |
| FND-005 | fixed | FR-303 no longer restates FR-103/FR-105 criteria; the attribution AC was removed from FR-305. |

Round 2, head `f5f81e9` (rebased on `origin/main`). `quire validate --scope . "spec/**/*.md"` reports no error or warning on FR-301..305 or NFR-300.

| FND | outcome | reason |
| --- | --- | --- |
| FND-006 | fixed | `policy_region` is now a key of each `pre_control`/`post_control` entry, not of the row. FR-305-AC-3 checks one entry's `null` region beside another entry's label, and FR-305-AC-5 checks the exact key set of every estimate entry. |
