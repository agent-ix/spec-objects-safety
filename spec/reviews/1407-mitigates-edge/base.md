---
id: SR-012
title: "Base spec review of the authorable mitigates edge (PR #30)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-001-safety-object-types.md, spec/functional/FR-006-cross-module-references.md, spec/functional/FR-007-authorable-mitigates-edge.md, spec/functional/FR-008-mitigation-coverage-findings.md, spec/non-functional/NFR-001-mitigates-edge-compatibility.md, spec/log.md, spec/tests.md, spec/index.md, spec/functional/index.md, spec/non-functional/index.md"
review_set: subset
---
# Base spec review of the authorable mitigates edge (PR #30)

## Summary

Ticket: PLAT-1407 (with PLAT-203, PLAT-215). Base checklist over
`git diff origin/main...HEAD` of agent-ix/spec-objects-safety#30 at e3a4a6f.
Spec-only diff; no code gates run. Review set: base plus dependency and
integrity (SR-013, SR-014); EARS, evidence, failure-domain, risk-complexity
and scope-boundary skipped as not matching what changed.

The control-end decision for `mitigates` (FR-007), the FR-008 fire/silent
fixture design, and the FR-001-AC-1 wording correction are sound and match
the manifest. Four high defects block merge: NFR-001 and FR-007-AC-5/CON-1
reintroduce the value-freeze baseline check that PR #20 deleted;
`spec/log.md` reintroduces the authored log document PR #25 deleted and fails
`quire validate`; `spec/tests.md` marks TC-002 and FR-001 as covered for a
"declares no roles" clause no test asserts; and FR-007-AC-3 cannot pass on
the shipped quire (measured below).

Measured with quire 0.40.0 (engine 0.56.0) on a fixture whose frontmatter
carries `mitigates` to an absent `HAZ-999`: per-file `quire validate` does not
resolve edges at all (exit 3 only for unrelated structure); `quire validate
--okf` reports `warning: FR-001: dangling reference 'HAZ-999' (edge
'mitigates') has no target in the bundle [dangling-reference]` and exits 0;
`--okf --strict` also exits 0. The message names the source id, not its file
path.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | NFR-001 reintroduces a frozen-value baseline test (traceability block and allowed_links equal "the values this requirement freezes"), the pin/baseline ceremony commit d114110 (#20) deleted along with the old NFR-001; delete NFR-001 and its index | spec/non-functional/NFR-001-mitigates-edge-compatibility.md:14 |
| FND-002 | high | FR-007-AC-5 and FR-007-CON-1 assert the traceability and allowed_links values are "identical to their pre-change values", a snapshot-comparison test of the same kind; delete them and the "frozen traceability block" prose | spec/functional/FR-007-authorable-mitigates-edge.md:34 |
| FND-003 | high | spec/log.md re-adds the authored log document PLAT-1156 (#25) removed; it restates FR-001/FR-007 decisions, fails `quire validate` (no frontmatter `type`), and FR-001 now points at it; delete it and the pointer | spec/log.md:1 |
| FND-004 | high | TC-002 row and FR-001 coverage flipped to passing for "declares no `roles`", but test_object_types_are_well_formed asserts only data_schema and allowed_links; nothing asserts the absence of roles | spec/tests.md:62 |
| FND-005 | high | FR-007-AC-3 cannot pass on quire 0.40.0: per-file validate does not resolve edges, --okf reports dangling-reference as a warning with exit 0 (also with --strict), and the message names the source id, not the file path | spec/functional/FR-007-authorable-mitigates-edge.md:67 |
| FND-006 | medium | FR-008 never names the command whose output carries the unmitigated-hazard findings, so two implementers could test different surfaces | spec/functional/FR-008-mitigation-coverage-findings.md:30 |
| FND-007 | low | The manifest's traceability comment still says the mitigation "is authored from the requirement's end — an FR says what it mitigates", contradicting FR-007's control-end decision | spec_objects_safety/manifest.yaml:245 |

## Verdict

FAIL. Not mergeable until FND-001..FND-005 are fixed. FR-001-AC-1's new text,
FR-006's reworded bullet, FR-007-AC-1/2/4 and FR-008-AC-1..5 were examined and
are otherwise clean.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | e06668b deletes NFR-001, spec/non-functional/index.md and the spec/index.md link |
| FND-002 | fixed | e06668b deletes FR-007-AC-5, the Constraints table with FR-007-CON-1, and "frozen" from No relaxation |
| FND-003 | fixed | e06668b deletes spec/log.md and FR-001's pointer to it |
| FND-004 | fixed | e06668b reverts the TC-002 title, marks FR-001 open, and records the unbacked no-role clause as Coverage Gap 2 |
| FND-005 | fixed | e06668b narrows FR-007-AC-3 to `quire validate --okf --strict` over a bare-id target, specified upstream in quire-cli FR-014-AC-11 |
| FND-006 | fixed | e06668b names `quire validate --okf` and the advisory default (quire-rs FR-058-AC-7), and AC-5 uses `--severity trace:unmitigated-hazard=error` |
| FND-007 | fixed | e06668b changes the manifest comment to "mitigating document's end — a control says what it mitigates" |
