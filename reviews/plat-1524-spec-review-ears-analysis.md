---
id: SR-043
title: "Spec review (EARS conformance) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-safety; spec/functional/FR-301..FR-305 Description and Behavior statements, spec/non-functional/NFR-300 Statement (git diff origin/main...b94d61f)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-303"
    type: "references"
---
# Spec review (EARS conformance) of PLAT-1524 risk-model completeness rules (spec-objects-safety#36)

## Summary

Ticket: PLAT-1524. This review checked every SHALL statement in FR-301..FR-305
and the NFR-300 Statement. The inputs were `quire validate`'s two
`ears:non-singular` warnings and a manual read of each statement's subject and
pattern.

## Verdict

Most statements are singular ubiquitous or unwanted-behaviour forms with a
named subject. There are four low defects. Two are compound SHALLs, one is a
conditional statement with a broken pattern, and two statements use a sibling
document as the SHALL subject.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | "The relation SHALL produce a finding only and SHALL NOT create or change a residual-risk record" holds two SHALLs. Split it into two statements. | spec/functional/FR-303-residual-risk-decided-by-named-person.md:76 |
| FND-002 | low | "The report SHALL modify no document and SHALL produce byte-identical output ... ordered by hazard id then situation id" holds two SHALLs and an ordering rule. Split it. | spec/functional/FR-305-risk-summary-report.md:71 |
| FND-003 | low | "A hazard that is authored with only the free string `context.situation` and no situation object the tooling SHALL report `hazard-without-situation`" is not grammatical. Use the unwanted-behaviour form: "If a hazard carries only `context.situation` and no situation document involves it, then the tooling SHALL report ...". | spec/functional/FR-301-hazard-reaches-harm-through-situation.md:58 |
| FND-004 | low | "FR-202 SHALL NOT declare a second one" (FR-301) and "FR-205 SHALL NOT declare a second copy" (FR-302) make a sibling spec document the subject of a SHALL. That is not a requirement on the system. Recast each as a statement that the module declares exactly one relation per check (NFR-300 already measures this). | spec/functional/FR-301-hazard-reaches-harm-through-situation.md:54 |

## Dispositions

Round 1, head `0da287c`. Committed in `reviews/` as SR-043; the review comment on PLAT-1524 carries the pre-renumbering id SR-026. `quire validate` reports no `ears:non-singular` warning on the changed files.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-303 Behavior now reads "The relation SHALL produce a finding only." as its own statement. |
| FND-002 | fixed | FR-305 splits it into "The command SHALL modify no document." and "The command SHALL produce byte-identical output for identical inputs." |
| FND-003 | fixed | FR-301 reads "If a hazard carries only the free string `context.situation` and no situation document arises from it, then the tooling SHALL report `hazard-without-situation`." |
| FND-004 | fixed | FR-301 and FR-302 now read "The module declares exactly one relation per `check` token (NFR-300)." No sibling document is a SHALL subject. |
