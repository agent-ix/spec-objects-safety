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
