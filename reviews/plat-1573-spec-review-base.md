---
id: SR-065
title: "Base spec review of the FR-302 and FR-205 when_any amendments (spec-objects-safety#41)"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-safety; PR #41 (git diff origin/main...5e7dd46): spec/functional/FR-302-risk-control-implemented-and-verified.md, spec/functional/FR-205-control-requirement-and-verification-links.md"
---
# Base spec review of the FR-302 and FR-205 when_any amendments (spec-objects-safety#41)

## Summary

Ticket: PLAT-1573. This is a checklist, consistency and dependency review of
the two spec edits. The PR changes FR-302 Description, which no longer says
the selector is pending, and FR-302-AC-1, which drops "With PLAT-1674 landed".
It also rewords FR-205-AC-6 to "no unscoped control relation".

Examined: FR-302 Description (scope section), FR-302 Behavior,
FR-302-AC-1 and AC-8, FR-205 Description (Completeness rules), FR-205
Behavior, FR-205-AC-6 and FR-205 Dependencies. Context only: FR-302-AC-2 to
AC-7, FR-205-AC-3.

`quire validate --scope .` over both files exits 0. The only warnings come
from the environment: DuplicateModuleName, because the module is installed and
also in the checkout, and an unused-import note in another module.

## Verdict

Changes requested. The FR-302 edits are correct. The `when_any` literal is
unchanged and still matches the manifest exactly. AC-1 is now unconditional,
and the "SHALL NOT be declared without that scope" rule stays. No paywalled
standard text, roadmap, hash or pin was added.

The FR-205 edit is incomplete. AC-6 now permits scoped control relations, but
three other parts of FR-205 still describe the selector as absent and the
relations as forbidden. FR-205 contradicts itself and the manifest this PR
ships.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-205 Behavior still says "The module SHALL declare no completeness relation over `control` until the quire-rs incoming-edge selector exists." The selector exists and this PR declares two such relations, so the obligation is stale. It also disagrees with the reworded AC-6, which allows scoped relations and forbids only unscoped ones. | spec/functional/FR-205-control-requirement-and-verification-links.md:80, :92 |
| FND-002 | low | FR-205 still calls the selector missing. The Description says it "does not exist today" (line 61). Dependencies lists it as Downstream, "which has no ticket yet" (line 97). It is quire-rs FR-058 / PLAT-1674, released, and it is upstream. | spec/functional/FR-205-control-requirement-and-verification-links.md:59-63, :97 |
| FND-003 | low | FR-302-AC-8 and the Dependencies line still name the ticket PLAT-1674 as the scope's provider. The provider is quire-rs FR-058, which the frontmatter `depends_on` already cites. A ticket id as provider is delivery history, which a requirement should not carry now that the selector has shipped. | spec/functional/FR-302-risk-control-implemented-and-verified.md:83, :87 |

## Finding detail

- FND-001: reword the Behavior line to match AC-6. For example: "The module
  SHALL declare no completeness relation over `control` without the FR-302
  `when_any` scope."
- FND-002: replace line 61's "needs a selector ... that does not exist today"
  with the FR-058 `when_any` reference. Move the selector to Upstream as
  "`agent-ix/quire-rs` FR-058 (`when_any`)".
- FND-003: AC-8 could read "... and cites quire-rs FR-058 as its provider".
  Drop PLAT-1674 from Dependencies, or keep it only as the Description's
  tracking note.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, b29e139. The FR-205 Behavior line now reads "The module SHALL declare no completeness relation over `control` without the FR-302 `when_any` scope.", which agrees with AC-6 and the manifest. |
| FND-002 | still-open | Round 1, b29e139. The Description is fixed: it now cites quire-rs FR-058 `when_any` and no longer says the selector does not exist. The frontmatter gains `ix://agent-ix/quire-rs/FR-058` `depends_on`, a full ix:// target, not a bare id; `quire validate` exits 0 and the foreign authority is skipped. But Dependencies still lists FR-058 under **Downstream** ("`agent-ix/quire-rs` FR-058 (the `when_any` scope)"), which contradicts the new `depends_on` edge. It belongs on the Upstream line. |
| FND-003 | fixed | Round 1, b29e139. FR-302-AC-8 now reads "cites `agent-ix/quire-rs` FR-058 as its provider". The Description and the Upstream line cite FR-058 without the ticket. |
