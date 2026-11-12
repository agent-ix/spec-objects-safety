---
id: SR-017
title: "Spec review of PLAT-1408 FR-002 and Test Matrix changes (spec-objects-safety#31)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-safety; spec/functional/FR-002-emitted-json-schemas.md, spec/tests.md (git diff origin/main...6198eae)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-002"
    type: reviews
---
# Spec review of PLAT-1408 FR-002 and Test Matrix changes (spec-objects-safety#31)

## Summary

Ticket: PLAT-1408. PR `agent-ix/spec-objects-safety#31`, head `6198eae`. Spec
changes in the diff:

- FR-002 Dependencies: `@agent-ix/semantic-core` now comes "from npmjs".
- FR-002-CON-4 now reads: "`package-lock.json` SHALL resolve every package,
  `@agent-ix/semantic-core` included, from `registry.npmjs.org`, and never from
  `npm.ix`, the private dev-only mirror."
- TM-001 (`spec/tests.md`):
  - `covers` edges to FR-007 and FR-008;
  - FR-007 and FR-008 coverage rows flipped to ✅;
  - TC-024 reworded to npmjs-only;
  - new rows TC-093..TC-098;
  - the Coverage Gaps prose rewritten.

Sub-analyses chosen by scope:

- integrity, for the consistency between the matrix rows, the tags and the tests;
- EARS, for the one edited constraint statement.

## Verdict

Clean.

- FR-002-CON-4 is a well-formed ubiquitous SHALL statement. It has one subject
  (`package-lock.json`), one testable property (every `resolved` URL is on
  `registry.npmjs.org`) and one explicit exclusion (`npm.ix`).
- TC-024's row text, the test docstring and the test assertion all say the same
  thing. `quoin matrix` binds FR-002-CON-4 to
  `test_the_lockfile_resolves_public_packages_from_npmjs`.
- The new TC-093..TC-098 rows match the FR-007/FR-008 AC ids in their trace
  tags, and every binding reads correctly against its AC text.
- The rewritten Coverage Gaps section no longer contradicts the coverage table.
- No `GitHub Packages` or `npm.pkg.github` text remains in `spec/`, `tests/`
  or `tests_integration/`.

Two things are not findings, because this PR did not cause them:

- `quire validate` reports three column-header mismatches in `spec/tests.md`
  (`Coverage Status` vs `Status`). The same three appear on `origin/main`.
- The TC-070 row reads ✅ while its test fails at SC-01, and the test's own
  comment says the row is carried 🚧. Both are the same on `origin/main`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
