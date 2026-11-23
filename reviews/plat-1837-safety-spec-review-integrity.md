---
id: SR-414
title: "Spec review (integrity) — spec-objects-safety PLAT-1837 FR-205, FR-302, FR-305"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-205-control-requirement-and-verification-links.md, spec/functional/FR-302-risk-control-implemented-and-verified.md, spec/functional/FR-305-risk-summary-report.md, spec/functional/index.md (git diff origin/main...3748247, PR #49)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-objects-safety/FR-205", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-302", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-305", type: references }
  - { target: "ix://agent-ix/spec-objects-safety/FR-006", type: references }
---

## Summary

Ticket: PLAT-1837. The PR rewrites FR-205 (two authorable verification
edges, control option type boundary), FR-302 (three relations, new AC-9, no
relation over `verifies`) and FR-305 (report keys split). FR-006 was read as
context because it governs where edge verbs may come from.

Checked clean: `control-has-verification` and `control-without-verification`
are gone from every spec file except the intended negative statement in
FR-302 Behavior; FR-302 Behavior, Outputs, ACs and the manifest agree on names,
fields, `to: []`, scope and `check` tokens; FR-305's control-entry keys match
AC-5 and AC-8; the control option type is stated as owned by
spec-objects-security, with no ranking or required value; no statement
assigns acceptability or a verdict. The ISO 14971 references are paraphrase,
with no quoted standard text.

## Verdict

One high contradiction: the new verbs are "declared by this module", which
FR-006 forbids, and FR-205 no longer states how they become authorable on
types other modules own. Two low consistency gaps.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-205 now says `verifies_implementation` and `verifies_effectiveness` are "declared by this module" in `edge_types`. FR-006-AC-4 requires every `traceability` verb to exist in the spec-artifacts-iso edge vocabulary, and FR-006-CON-1 forbids minting verbs locally. The PR also drops FR-205's old claim that both verbs "are accepted today with no widening" without stating the widening the new verbs need: an `IT`, `TC` or retained-evidence record may author them only if its owning module allows them (measured: they draw `disallowed-edge-type`, SR-412 FND-001). FR-205 Dependencies name no spec-artifacts-iso change. Decide the owner: either the verbs are shared vocabulary (spec-artifacts-iso, with `allowed_links` on IT/TC and the evidence-record type) and FR-205 depends on that change, or FR-006 is amended to allow module-declared verbs and FR-205 states how the source types allow them. | spec/functional/FR-205-control-requirement-and-verification-links.md:39-52, spec/functional/FR-205-control-requirement-and-verification-links.md:118-121, spec/functional/FR-006-cross-module-references.md:48,56 |
| FND-002 | low | `spec/functional/index.md` still lists FR-205 and FR-302 under their old titles ("the verification that shows it is effective", "has a verification"). | spec/functional/index.md:31,33 |
| FND-003 | low | New FR-205 Behavior "The module SHALL declare no field that records a control's option type" has no acceptance criterion. FR-205-AC-5 covers only `effective`, `verified` and `passed` keys. Add the option-type field to an Inspection AC or drop the statement, since the Description already states the boundary. | spec/functional/FR-205-control-requirement-and-verification-links.md:102 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, c8f1044. FR-205 now names both verbs as shared vocabulary that this module does not declare. It cites spec-artifacts-iso FR-004-AC-8 and adds a `depends_on` edge and a Dependencies entry for spec-artifacts-iso FR-004. This is consistent with FR-006-AC-4 and FR-006-CON-1 once iso#76 merges. The released dependency is tracked as SR-412 FND-004. |
| FND-002 | fixed | Round 1, c8f1044. `spec/functional/index.md` now carries the new FR-205 and FR-302 titles. |
| FND-003 | fixed | Round 1, c8f1044. The untested option-type SHALL statement and the option-type section are removed. The option type belongs to spec-objects-security#76. |
