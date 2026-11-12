---
id: SR-019
title: "Spec review (integrity) of PLAT-1477 FR-009 (spec-objects-safety#32)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-009-safety-nfr-needs-mitigation-target.md, spec/functional/FR-007-authorable-mitigates-edge.md, spec/functional/index.md, spec/tests.md (git diff origin/main...1ea2900)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-009"
    type: "references"
---
# Spec review (integrity) of PLAT-1477 FR-009 (spec-objects-safety#32)

## Summary

Ticket: PLAT-1477. Read against PLAT-1477 and PLAT-370 (both as data) and
quire-rs `origin/main` FR-058-AC-4 and FR-058-AC-12..22.

`quire validate --scope .` on the changed files reports FR-009, FR-007 and the
index as valid. `spec/tests.md` fails structural validation on its column
headers, but it fails the same way on `origin/main`, so that failure predates
this PR. TC-099..TC-102 are unique ids. `quoin matrix` shows FR-009-AC-1..5 as
`tagged`. The EARS form of the FR-009 Behavior statements was checked: each is
one `SHALL` with a named subject.

## Verdict

FR-009 states the rule as data and traces it to FR-058 correctly. Its
`to: []` rationale is accurate (FR-058-AC-4, measured). The changes requested
are as follows. FR-009-AC-5 claims a `--strict` exit 0 that no real bundle
containing an NFR can meet. Two TC rows went stale. FR-009 should also state
what `to: []` lets through.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-009-AC-5 says that without `--severity`, `--okf --strict` "still exits 0". Any bundle with an NFR also triggers iso's `unowned-quality-characteristic`, which is an error under `--strict`, so the run exits 3 (measured with iso v0.25.0 and with the harness's 0.22.0). The criterion should say what FR-058-AC-18 says: the finding stays a warning under `--strict`, and a bundle whose only faults are these findings stays valid. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:64 |
| FND-002 | low | The TC-010 row still reads "two independently tunable relations", but the test now asserts three. | spec/tests.md:94 |
| FND-003 | low | The TC-011 row still reads "Every relation names an object type this module declares", but the relation set now names `NFR`, which is iso's archetype. | spec/tests.md:95 |
| FND-004 | low | FR-009 does not state what `to: []` admits. Any outgoing `mitigates` edge discharges the obligation: one to a security `threat` or `risk`, or one to a mistyped local id, which only `dangling-reference` reports. That is weaker than PLAT-370's "traces to an upstream threat/hazard". The trade-off is justified, but the requirement should name the accepted consequence. | spec/functional/FR-009-safety-nfr-needs-mitigation-target.md:26-31 |

## Not findings

- FR-007 tweak ("the two hazard-end relations"): accurate after FR-009.
- `depends_on` `ix://agent-ix/quire-rs/FR-058`: correct cross-repo dependency.

## Dispositions

Round 1, head `a024948`. `quire validate --scope .` on FR-009 exits 0.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-009-AC-5 is restated as FR-058-AC-18 states it. The Behavior line notes that unrelated strict errors are not this rule's. |
| FND-002 | fixed | The TC-010 row reads "three independently tunable relations (the hazard and failure-mode relations `incoming`, the NFR relation `outgoing`)". |
| FND-003 | fixed | The TC-011 row reads "an object type this module declares or an archetype `spec-artifacts-iso` declares". |
| FND-004 | fixed | FR-009 gains a "What `to: []` lets through" section that names threat, risk, cross-repo and mistyped-id targets as the accepted cost. |
