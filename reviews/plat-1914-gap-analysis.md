---
id: SR-425
title: "gap-analysis — authored tension records"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; PLAT-1914; PR #52; tension schemas, manifest, skeleton, tests and how-to"
review_set: subset
---

## Summary

Reviewed head 0a0df62576cd35b64858f1ac4d47ccc15ac1b08e. FAIL.

## Verdict

**FAIL** — see findings and coverage limits.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Whole-repository matrix reports 46 untagged obligations outside the new tension requirements. These are inherited repository gaps, not newly introduced tension defects; a repository-wide gap-analysis PASS cannot be claimed. Keep their owning work tracked separately from this feature PR. | spec/functional/FR-101-acceptability-policy.md:63 |

## Reviewed units

```yaml
scope:
- id: FR-101-AC-3
  path: spec/functional/FR-101-acceptability-policy.md
  role: examined
  excerpt: The same fixture with one cell removed fails validation and the diagnostic
    names the missing severity and probability pairing.
- id: FR-101-AC-4
  path: spec/functional/FR-101-acceptability-policy.md
  role: examined
  excerpt: A fixture with a duplicated pairing, or a cell naming a region not in the
    region list, fails validation naming the pairing.
- id: FR-102-AC-1
  path: spec/functional/FR-102-estimate-levels-resolve-in-policy.md
  role: examined
  excerpt: For a fixture whose estimate levels exist in the referenced policy, the
    report shows exactly the region label written in that policy cell.
- id: FR-102-AC-2
  path: spec/functional/FR-102-estimate-levels-resolve-in-policy.md
  role: examined
  excerpt: For a fixture whose severity is not in the policy's list, the report contains
    a `level-not-in-policy` finding naming that level and the policy, and no region.
- id: FR-102-AC-3
  path: spec/functional/FR-102-estimate-levels-resolve-in-policy.md
  role: examined
  excerpt: For a fixture whose probability is `not_assessed`, the report contains
    one `level-not-assessed` finding naming `not_assessed`, no region, and no substituted
    level.
- id: FR-102-AC-4
  path: spec/functional/FR-102-estimate-levels-resolve-in-policy.md
  role: examined
  excerpt: The same holds for `unknown` and for `not_applicable`, each yielding a
    `level-not-assessed` finding.
- id: FR-103-AC-7
  path: spec/functional/FR-103-residual-risk-record.md
  role: examined
  excerpt: 'Over a bundle with a hazard at `status: accepted` and a `residual_risk`
    at `undecided`, the tooling reports `residual-risk-undecided` (FR-105) and no
    accepted state for the risk.'
- id: FR-104-AC-1
  path: spec/functional/FR-104-no-computed-verdicts.md
  role: examined
  excerpt: Running validation and the discrepancy report over fixtures leaves the
    bytes of every fixture file unchanged.
- id: FR-104-AC-2
  path: spec/functional/FR-104-no-computed-verdicts.md
  role: examined
  excerpt: 'With a fixture `residual_risk` that has `decision: undecided` and an all-acceptable
    policy, the report contains no accepted state for that risk.'
- id: FR-104-AC-4
  path: spec/functional/FR-104-no-computed-verdicts.md
  role: examined
  excerpt: The report output for a fixture contains the attribution statement naming
    the policy as the source of regions and the named person as the source of decisions.
- id: FR-105-AC-1
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: 'A fixture `accepted` residual risk in a cell whose region has `outside_acceptable:
    true`, with no covering benefit-risk record, yields exactly one `accepted-outside-acceptable-region`
    finding naming the document, `accepted`, the region and the policy.'
- id: FR-105-AC-2
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: Adding an `accepted` benefit-risk record that covers that risk removes
    the finding.
- id: FR-105-AC-3
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: 'A covering benefit-risk record with `decision: undecided` yields `benefit-risk-undecided`
    instead.'
- id: FR-105-AC-4
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: 'A `not_accepted` risk in a cell whose region has `outside_acceptable:
    false` yields `not-accepted-inside-acceptable-region`.'
- id: FR-105-AC-5
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: An `undecided` risk yields `residual-risk-undecided` regardless of region.
- id: FR-105-AC-6
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: 'An `accepted` risk in a cell whose region has `outside_acceptable: false`
    yields no finding.'
- id: FR-105-AC-7
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: All findings exit 0 by default as warnings; with the promote flag the run
    exits non-zero.
- id: FR-105-AC-8
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: Two runs over the same fixtures produce identical output.
- id: FR-105-AC-9
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: An `accepted` risk outside the acceptable region whose only covering benefit-risk
    record is `not_accepted` yields `benefit-risk-not-accepted`.
- id: FR-105-AC-10
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: An `accepted` risk whose estimate has probability `not_assessed`, and one
    whose severity is not in the policy, each yield `decision-without-region`; so
    does a `not_accepted` risk in the same state.
- id: FR-105-AC-11
  path: spec/functional/FR-105-decision-policy-discrepancy-report.md
  role: examined
  excerpt: An `accepted` risk outside the acceptable region covered by one `not_accepted`
    and one `accepted` benefit-risk record yields no benefit-risk finding.
- id: FR-107-AC-3
  path: spec/functional/FR-107-overall-residual-risk-evaluation.md
  role: examined
  excerpt: A fixture bundle with a `residual_risk` missing from the considered list
    yields one `residual-risk-not-considered` warning naming it.
- id: FR-107-AC-4
  path: spec/functional/FR-107-overall-residual-risk-evaluation.md
  role: examined
  excerpt: An `accepted` evaluation over a considered `not_accepted` risk yields `evaluation-accepted-with-open-risk`
    naming that risk.
- id: FR-107-AC-5
  path: spec/functional/FR-107-overall-residual-risk-evaluation.md
  role: examined
  excerpt: Given only decided-accepted considered records and no evaluation document,
    the tooling creates no evaluation and reports no accepted state.
- id: FR-107-AC-7
  path: spec/functional/FR-107-overall-residual-risk-evaluation.md
  role: examined
  excerpt: An `accepted` evaluation over a considered `undecided` risk yields `evaluation-accepted-with-open-risk`
    naming that risk.
- id: FR-202-AC-2
  path: spec/functional/FR-202-hazardous-situation-object-and-chain.md
  role: examined
  excerpt: '`quire extract` over the fixture shows the resolved inverse of each chain
    edge on the hazard and on the situation, though neither document declares it.'
- id: FR-305-AC-1
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: Over a complete fixture chain, `--format json` yields one row per hazard
    and situation pairing, each key holding the entered value, and the output parses
    as one JSON object with `attribution` and `rows`.
- id: FR-305-AC-2
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: 'A hazard with no situation yields a row with `situation: null` and `hazard-without-situation`
    in `findings`.'
- id: FR-305-AC-3
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: 'A fixture with `probability: not_assessed` shows `not_assessed` in its
    estimate entry with that entry''s `policy_region: null`, while another estimate
    in the same row keeps its own label.'
- id: FR-305-AC-4
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: 'A fixture residual risk with `decision: undecided` shows `undecided`,
    and no row shows `accepted` that a person did not write.'
- id: FR-305-AC-5
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: 'No row key and no top-level key is numeric, a rank, or a verdict: the
    JSON keys of every row equal the row table exactly, of every estimate entry equal
    `estimate`, `severity`, `probability`, `policy_region`, of every control entry
    `control`, `requirements`, `implementation_verifications`, `effectiveness_verifications`,
    of every residual-risk entry `residual_risk`, `decision`, `decided_by`, and of
    every finding `finding`, `names`.'
- id: FR-305-AC-6
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: Running the command leaves every fixture file byte-identical.
- id: FR-305-AC-7
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: Two runs over the same fixtures give identical output in both formats,
    ordered by hazard id then situation id.
- id: FR-305-AC-8
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: A control without an implementation or effectiveness verification appears
    in its row with `control-without-implementation-verification` or `control-without-effectiveness-verification`
    in `findings`; adding the matching verification removes it.
- id: FR-305-AC-9
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: 'A situation with no `arises_from` edge to a hazard yields a row with `hazard:
    null` and `situation-without-hazard` in `findings`.'
- id: FR-305-AC-10
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: Two estimates on one situation both appear in the row, and no key marks
    either as in force.
- id: FR-305-AC-11
  path: spec/functional/FR-305-risk-summary-report.md
  role: examined
  excerpt: A post-control estimate with no `assumes` edge yields `post-control-without-control`
    naming the estimate in the `findings` of its situation's rows; adding the edge
    removes it.
- id: NFR-100-AC-1
  path: spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md
  role: examined
  excerpt: Two runs of the discrepancy report over one fixture bundle produce output
    that differs in 0 bytes.
- id: NFR-100-AC-2
  path: spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md
  role: examined
  excerpt: The bytes of every authored fixture file are unchanged after a run.
- id: NFR-100-AC-3
  path: spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md
  role: examined
  excerpt: One run over 5,000 generated residual-risk records completes within 10
    seconds.
- id: FR-405-CON-1
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: No workflow definition SHALL live in this module's object-type vocabulary.
- id: FR-405-AC-1
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: A corpus with no `tension` records raises no tension finding of any kind.
- id: FR-405-AC-2
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: 'An emitted `tension` with `status: open` and two `conflicts_with` entries
    validates and is reported by FR-404-AC-1.'
- id: FR-404-CON-1
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The engine SHALL contain no tension-specific code; the rule is two manifest
    entries.
- id: FR-404-CON-2
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The rule SHALL NOT compare, count or weigh tensions against each other;
    each is closed or not.
- id: FR-404-AC-1
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A corpus containing a `tension` with `status: open` is reported under
    `trace:open-tension`, naming that tension, and fails when the key is mapped to
    `error`.'
- id: FR-404-AC-2
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: open` that is the target of an incoming `conflicts_with`
    edge, or of an edge from a dangling or other document, is still reported under
    `trace:open-tension`.'
- id: FR-404-AC-3
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'Setting `status: resolved-by-design` with a `resolved_by` edge to a design
    element clears the finding; the corpus passes.'
- id: FR-404-AC-4
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: resolved-by-design` and no `resolved_by` edge
    is reported under `trace:resolved-tension-without-link`.'
- id: FR-404-AC-5
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: accepted-by-person` and a named `decided_by`
    passes both relations; the same record with no `decided_by` still fails schema
    validation (FR-403-AC-1).'
- id: FR-404-AC-6
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The manifest `traceability` block loads with the two new relations and
    the existing relations unchanged, and a corpus with no `tension` produces output
    identical to one before this FR.
- id: FR-403-CON-1
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'Acceptance is a human act: nothing in this module sets `decided_by` or
    `status: accepted-by-person` on any record.'
- id: FR-403-AC-1
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and no `decided_by` fails validation,
    naming `decided_by`.'
- id: FR-403-AC-2
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and an empty `decided_by` fails
    validation.'
- id: FR-403-AC-3
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and a named person in `decided_by`
    validates.'
- id: FR-403-AC-4
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: open` or `status: resolved-by-design` and a `decided_by`
    fails validation.'
- id: FR-403-AC-5
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: open` and a `resolved_by` relation entry fails
    validation.'
- id: FR-403-AC-6
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: The emitted `Tension.json` has no acceptance-date property and no default
    for `status` or `decided_by`.
- id: FR-401-CON-1
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The module SHALL declare the type with the existing manifest object-type
    grammar and add no new engine mechanism.
- id: FR-401-CON-2
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The type SHALL NOT quote or name text from a paywalled standard.
- id: FR-401-AC-1
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The manifest declares `tension` as an object type and exports it, and a
    `Tension.json` schema is emitted for it.
- id: FR-401-AC-2
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: A `tension` record validates with `status` set to each of `open`, `resolved-by-design`
    and `accepted-by-person` (given each state's other required fields), and fails
    with any other `status` value.
- id: FR-401-AC-3
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: A `tension` record with no `status` fails validation.
- id: FR-401-AC-4
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The emitted `Tension.json` has no property for severity, likelihood, a
    date or a history list.
- id: FR-401-AC-5
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The `tension` skeleton validates, and an edited copy with its `Conflict`
    section removed fails.
- id: FR-402-CON-1
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: Every verb in `allowed_links` for `tension` SHALL exist in the `spec-artifacts-iso`
    edge vocabulary once PLAT-1675 lands (FR-006-AC-4 continues to hold).
- id: FR-402-AC-1
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` record with two `conflicts_with` relation entries validates;
    one with a single entry fails schema validation.
- id: FR-402-AC-2
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` that authors `references` or any other verb outside `conflicts_with`
    and `resolved_by` draws an undeclared-link diagnostic naming the tension.
- id: FR-402-AC-3
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` authoring `resolved_by` to a design element document resolves
    and passes the edge check.
- id: FR-402-AC-4
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: The `tension` schema declares no property naming a person other than `decided_by`,
    and the manifest declares no person object type.
- id: FR-402-AC-5
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: Once PLAT-1675 lands, every verb in the `tension` `allowed_links` exists
    in the iso edge vocabulary as a forward key or declared inverse.
- id: NFR-401-M-1
  path: spec/non-functional/NFR-401-tension-generic-and-human-accepted.md
  role: examined
  excerpt: 'Schema defaults for `decided_by` or `status`: target 0, threshold 0, method
    Test.'
```

## Coverage

Explicit released Quoin `/tmp/regfinish-quoin-v0.37.0/quoin` 0.37.0 and Quire `/home/peter/.npm-global/bin/quire` 0.52.0 (engine 0.62.2); authoring contract spec-artifacts-process@v0.36.0. No applicable AssuranceProfile found. Exact model identifier is not exposed; marker records model=unknown. No spec or plan files changed, so spec-review is inapplicable. Review artifacts are scratch files for lead custody; repository source was not changed.

Plan completion: not assessed

Reconciliation: Quoin 0.37.0 matrix. All 37 requirements and 274 obligations inventoried: 202 tagged, 26 method-without-symbol, 46 untagged, 0 ignored-only; all 274 have no run evidence. All test-method criteria in FR-401–405 and NFR-401-M-1 are tagged. Coverage reports zero untracked symbols. The gap finding concerns inherited obligations outside the PR's implementation scope; it is not a claim those features are absent.

Reverse inventory: exported hazard/failure-mode types and structured safety records are owned by FR-001–010, FR-101–109, FR-201–205 and FR-301–305; tension by FR-401–405/NFR-401; schema build/emission and packaging by FR-002; skeleton extraction by FR-005 and semantic registration by FR-003. Module init exports resource paths only. Scripts provide existing generation/staging/build glue. No new unowned behavior, production TODO/pass stubs, or new hollow tests found by surface and pattern inspection. Review scope for actionable new findings remains the PR; code-review separately records its concrete defects. Optional semantic gap-analysis was not separately invoked; code-review performed the requirement-to-assertion inspection requested by the dispatch.

Missing obligation IDs: FR-101-AC-3, FR-101-AC-4, FR-102-AC-1, FR-102-AC-2, FR-102-AC-3, FR-102-AC-4, FR-103-AC-7, FR-104-AC-1, FR-104-AC-2, FR-104-AC-4, FR-105-AC-1, FR-105-AC-2, FR-105-AC-3, FR-105-AC-4, FR-105-AC-5, FR-105-AC-6, FR-105-AC-7, FR-105-AC-8, FR-105-AC-9, FR-105-AC-10, FR-105-AC-11, FR-107-AC-3, FR-107-AC-4, FR-107-AC-5, FR-107-AC-7, FR-202-AC-2, FR-305-AC-1, FR-305-AC-2, FR-305-AC-3, FR-305-AC-4, FR-305-AC-5, FR-305-AC-6, FR-305-AC-7, FR-305-AC-8, FR-305-AC-9, FR-305-AC-10, FR-305-AC-11, NFR-100-AC-1, NFR-100-AC-2, NFR-100-AC-3, NFR-100-M-1, NFR-100-M-2, NFR-100-M-3, NFR-300-M-2, NFR-300-M-3, NFR-300-M-4

Completed independent checks: schema emitter drift check passed (42 schemas); Ruff passed for all seven touched Python files; Black passed for all seven touched Python files.
