---
id: SR-059
title: "Gap analysis of FR-101..FR-107 and NFR-100 against spec-objects-safety#39"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; spec/functional/FR-101..FR-107, spec/non-functional/NFR-100, spec_objects_safety/, tests/test_residual_risk.py, tests_integration/test_risk_chain_edges.py (git diff origin/main...23a713c)"
review_set: subset
---
# Gap analysis of FR-101..FR-107 and NFR-100 against spec-objects-safety#39

## Summary

Tickets: PLAT-1563, PLAT-1565, PLAT-1568. Scope: the Behavior and Acceptance
Criteria of FR-101 to FR-107 and NFR-100, as they stand on main, against PR
head `23a713c`. Plan completion: not assessed.

Method:

- Read each FR, the manifest, the schemas, the skeletons and the tests.
- Ran `quire matrix` (quire 0.44.0, engine 0.59.1) and `quoin matrix --json`
  (quoin 0.30.1).
- Probed document validation from a scratchpad script.
- Read the quire-rs `RequiredRelation` and `WhereSelector` on `origin/main`
  (`src/traceability.rs`) to judge each engine limit the coder claimed.

Deferred to the quoin report work, PLAT-1570 (Backlog, Risk Model M2):

- FR-102 (all), FR-103-AC-7, FR-104-AC-1, AC-2 and AC-4.
- FR-105 (all), FR-107-AC-3, AC-4, AC-5 and AC-7.
- NFR-100.

Each of these is report behaviour this module cannot carry, so the deferral is
accepted. Nothing in the diff stores, defaults or computes a score, region or
acceptance, so FR-104 and NFR-100 are not violated.

## Verdict

Not mergeable as is. The following criteria are implemented and tested:

- FR-101-AC-1, AC-2, AC-6, AC-7 and AC-8.
- FR-103-AC-1, AC-5 and AC-6, plus AC-4's type half.
- FR-106-AC-1, AC-4, AC-5 and AC-6, plus AC-2's benefit half.
- FR-107-AC-1, AC-6 and AC-8.

Four groups of criteria are unmet at the document level. The coder listed
each one as an engine limit. Judged one by one:

- **Policy cross-row rules** (FR-101-AC-3, AC-4, and AC-5 at document level).
  This is a true limit. FR-058 `where` and `required_relations` work on edges
  between documents, selected by frontmatter, so they cannot say anything
  about rows inside one document. A quire-rs ticket is warranted for
  cross-table assertions: a unique column, a column whose values come from
  another table, and full coverage of the product of two tables. The other
  option is to move the rule into PLAT-1570's check, which reads the policy
  anyway.
- **Decider conditional on the decision** (FR-103-AC-2 and AC-3, FR-106-AC-3,
  FR-107-AC-2). This is a true limit for table assertions, which cannot make
  one column depend on another. But record-sections extraction exists and
  would enforce the rule through the emitted union, if it could read an
  `anyOf` record key (see SR-058 FND-001). A narrow quire-rs ticket is
  warranted.
- **Far-end phase check** (FR-103-AC-4, phase half). This is a true limit.
  `WhereSelector` narrows only the `from` document, and `to` names
  archetypes, not field values. A required relation states presence, never
  absence. A quire-rs ticket is warranted for a target-side selector, for
  example `to_where: {field: phase, values: [post_control]}`.
- **Empty references list on `benefit_risk`** (FR-106-AC-2, list half). This
  is not an engine limit. `required_relations` can state it today (SR-058
  FND-003).

The computed matrix shows every FR-101 to FR-107 criterion as untagged, with
`criterion-tagged-outside-row` on every new tag. This is the same state as
merged #38. The code lead ruled it an engine convention gap outside the PR
(SR-057 FND-003, rejected), so it is not raised again here.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-103-AC-2 (decider half) is unmet at the document level: a filled `residual_risk` with `accepted` and no `Decided by` validates (reproduced). The same holds for FR-103-AC-3 (`undecided` with a decider validates), FR-106-AC-3 and FR-107-AC-2. The tags on schema-only tests claim these criteria for an assertion no document reaches. | tests/test_residual_risk.py:290-320, spec_objects_safety/manifest.yaml:480-487 |
| FND-002 | medium | FR-101-AC-3 and AC-4 are unmet: a policy with a cell removed, or a cell naming an unlisted region, validates (reproduced). FR-101-AC-5 is met only on a hand-built record: a document repeating a severity level validates (reproduced). The PR body defers these to "other work" but names no ticket. | tests/test_residual_risk.py:189-197, spec_objects_safety/manifest.yaml:383-457 |
| FND-003 | medium | FR-103-AC-4's phase half is unmet: an `estimate` edge to a `pre_control` risk_estimate is not refused. It is a true engine limit (FR-058 `where` selects only the `from` document), but it is deferred with no owning ticket. | tests_integration/test_risk_chain_edges.py:453-475 |
| FND-004 | medium | FR-106-AC-2's references-list half is unmet: a `benefit_risk` with no `references` edge validates with no finding. It can be expressed now as a required relation (`from: benefit_risk`, `edges: [references]`, `to: [residual_risk]`, outgoing). The PR body lists it as waiting on other work. | spec_objects_safety/manifest.yaml:595-665 |
| FND-005 | low | NFR-100 (on main) has no `## Acceptance Criteria` section, so quire reports `section-matches-nothing` and mints no criteria. Its `Benchmark` method is also uncatalogued (`uncatalogued-verification-method`). The 10 s bound therefore has no criterion that a later benchmark could be tagged to. | spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md |

## Finding detail

- FND-001: same root cause as SR-058 FND-001. Fix it there, or record a
  deferral to the quire-rs record-sections `anyOf` ticket, and narrow the tags
  until then.
- FND-002 and FND-003: file the quire-rs tickets named in the Verdict, or
  place the policy rules in PLAT-1570. Then record the deferral against a
  ticket id.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1, f6a1aa6: FR-103-AC-2 and AC-3, FR-106-AC-3 and FR-107-AC-2 now hold at the document level. The new tests `test_a_decided_document_without_a_named_decider_fails` and `test_an_undecided_document_that_names_a_decider_fails` run through `validate_document`, and the reviewer reproduced both outcomes independently. |
| FND-002 | deferred | PLAT-1677 (quire-rs, Backlog) item 1, cross-row table assertions, owns FR-101-AC-3, AC-4 and the document half of AC-5. The PR body records the deferral. |
| FND-003 | deferred | PLAT-1677 item 3, a target-side relation selector, owns FR-103-AC-4's phase half. It is cited in the manifest comment at spec_objects_safety/manifest.yaml:664 and in the PR body. |
| FND-004 | fixed | Round 1, f6a1aa6: `benefit-risk-covers-risk` is declared, and `test_a_benefit_risk_with_no_residual_risk_is_reported_once_and_the_edge_clears_it` covers FR-106-AC-2's list half. The relation warns by default and can be promoted to an error with `trace:benefit-risk-without-risk`. |
| FND-005 | fixed | Round 1, f6a1aa6: NFR-100 now has an Acceptance Criteria section (NFR-100-AC-1 to AC-3) and uses the `Test` method. `quire matrix` mints the three criteria, and the section-matches-nothing and uncatalogued-method warnings are gone. |
