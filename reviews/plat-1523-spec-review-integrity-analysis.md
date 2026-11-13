---
id: SR-022
title: "Spec review (integrity) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-101..FR-107, spec/non-functional/NFR-100, spec/functional/index.md, spec/non-functional/index.md, spec/index.md, spec/tests.md (git diff origin/main...e90c3c0)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-102"
    type: "references"
  - target: "ix://agent-ix/spec-objects-safety/NFR-100"
    type: "references"
---
# Spec review (integrity) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)

## Summary

Ticket: PLAT-1523. This review checked structural integrity: index entries,
`relationships` edges against the prose Dependencies sections, and the
traceability table. All seven FRs and NFR-100 are listed in their indexes, and
`spec/index.md` now links `non-functional/`. Every `relationships` target
resolves to an id in this repo (StR-001, FR-004, FR-101..FR-106). The
FR-101..FR-107 dependency graph has no cycle.

Scope examined (role: examined): the frontmatter `relationships` and the
Dependencies sections of FR-101..FR-107 and NFR-100, the three index files,
and the `spec/tests.md` traceability tables.

## Verdict

Structurally sound. Three low findings: the prose and edge dependencies
disagree, NFR-100 constrains less than its statement covers, and the
traceability table is stale.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The dependency prose and the edges disagree. FR-102 lists FR-103 as Upstream but declares no `depends_on` FR-103 edge. FR-103's Downstream omits FR-102. FR-101's Downstream omits FR-103, although FR-103 declares `depends_on` FR-101. | spec/functional/FR-102-estimate-levels-resolve-in-policy.md:5-10,48, spec/functional/FR-103-residual-risk-record.md:58, spec/functional/FR-101-acceptability-policy.md:60 |
| FND-002 | low | The NFR-100 statement covers all "residual-risk tooling": deterministic output, no authored file modified, and the 5,000-record bound. It declares `constrains` only for FR-105, but FR-107's warnings and FR-102's report are the same tooling. Add `constrains` edges to FR-102 and FR-107, or narrow the statement. | spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md:6-8,14 |
| FND-003 | low | The `spec/tests.md` traceability table was not updated. The StR-001 row still traces to "FR-001..FR-009", and the Functional Requirement Coverage table has no FR-101..FR-107 or NFR-100 rows. Add them as untested/planned rows so the matrix shows the new criteria. | spec/tests.md:54,66-76 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | The fix round hand-wrote coverage rows into `spec/tests.md`: eight `none yet` / "🚧 specified, no tests tagged" rows for FR-101..FR-107 and NFR-100, and an edited StR-001 trace cell. The matrix is computed. `quoin matrix --repo . --json` at `3612073` already lists every FR-101..FR-107 criterion and NFR-100 as `untagged`. The hand rows repeat that state and go stale the moment a test is tagged, so they are tracking ceremony. Remove the eight rows and revert the StR-001 cell. The FR-001..FR-009 rows already on `origin/main` follow the same hand-written pattern. They are outside this diff, but should be removed separately. | spec/tests.md:56,77-84 |

## Dispositions

Round 1, head `3612073`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-102 now declares `depends_on` FR-103. FR-103's Downstream lists FR-102, and FR-101's Downstream lists FR-103. |
| FND-002 | fixed | NFR-100 now constrains FR-102, FR-105 and FR-107, and its Dependencies list all three. |
| FND-003 | rejected | The finding itself was wrong. The test matrix is computed (`quoin matrix` lists the new criteria as untagged with no hand-written rows), so hand-written rows in `spec/tests.md` are not needed. The rows added for it are raised as FND-004. |
