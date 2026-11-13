---
id: SR-021
title: "Spec review (base) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-safety; spec/functional/FR-101..FR-107, spec/non-functional/NFR-100, spec/functional/index.md, spec/non-functional/index.md, spec/index.md (git diff origin/main...e90c3c0)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-101"
    type: "references"
  - target: "ix://agent-ix/spec-objects-safety/FR-103"
    type: "references"
  - target: "ix://agent-ix/spec-objects-safety/FR-105"
    type: "references"
---
# Spec review (base) of PLAT-1523 acceptability policy and residual risk (spec-objects-safety#33)

## Summary

Ticket: PLAT-1523. Review set: subset (base, integrity, ears-conformance). The
failure-domain checks for edge cases and error paths are part of this base file.
No AssuranceProfile in the repo requires an enforced spec-review run, so this is
a direct review.

Checked:

- `quire validate --scope . "spec/**/*.md"` gives the same three errors at the
  PR head and on `origin/main`. They are the `spec/tests.md` TestMatrix column
  names and the `DuplicateModuleName` notice, so they predate this PR. The new
  files add only EARS and ambiguous-term warnings (see the ears-conformance
  review).
- ID ranges: `origin/main` stops at FR-009 and has no NFR. PLAT-1409 (#34) uses
  FR-201..FR-205 and NFR-201. FR-101..FR-107 and NFR-100 do not clash.
- No standard is named or quoted. The terms used (acceptability policy,
  benefit-risk, overall residual risk) are generic.
- People decide everything. FR-101 ships no default policy. FR-103, FR-106 and
  FR-107 have no default `decision` and no computed region. FR-104 forbids
  derived scores and verdicts, and FR-102 makes the region a lookup of a cell a
  person wrote.

Scope examined (role: examined): FR-101 and FR-101-AC-1..6, FR-102 and
FR-102-AC-1..4, FR-103 and FR-103-AC-1..6, FR-104 and FR-104-AC-1..4, FR-105
and FR-105-AC-1..8, FR-106 and FR-106-AC-1..5, FR-107 and FR-107-AC-1..6,
NFR-100. Context only: FR-004 (EpistemicState, `status: accepted`), and
PLAT-1409 #34 FR-203/FR-204 (`risk_estimate`).

## Verdict

Changes requested: 2 high, 7 medium, 3 low. Most ACs can be tested. The high
findings are these. FR-105 needs a per-region acceptable mark that FR-101 never
declares (author question 1). NFR-100 verifies by comparing file hashes, which
is a hash antipattern and must be removed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-105 reads a per-region "outside the acceptable region" mark, but FR-101 neither declares nor requires one. The FR-101 Behavior and FR-101-AC-1 require only level lists, a region list and cells. As written, FR-105's rules cannot be evaluated against a valid policy. FR-101 should require every region entry to carry a person-authored acceptable/outside flag with no default, plus an AC that fails a region missing the flag. | spec/functional/FR-101-acceptability-policy.md:40, spec/functional/FR-105-decision-policy-discrepancy-report.md:24-32 |
| FND-002 | high | NFR-100 Verification "compares output and file hashes". A test that hashes files is the hash antipattern. FR-104-AC-1 already states the real check (fixture files stay byte-identical). Delete "and file hashes" and compare file contents. | spec/non-functional/NFR-100-advisory-deterministic-risk-findings.md:30 |
| FND-003 | medium | FR-103 rejects a `decided_by` naming a role, team or tool. FR-103-AC-4 tests only membership in a "configured non-person list" whose location, format and owner are not specified. A denylist cannot establish that a value names a person, so the Behavior clause is broader than anything an AC can verify. Specify an allowlist roster of people (a project-authored document) that `decided_by` must resolve into. The denylist would then be unnecessary. | spec/functional/FR-103-residual-risk-record.md:39,51 |
| FND-004 | medium | FR-105 says nothing about an `accepted` residual risk outside the acceptable region whose benefit-risk record is `not_accepted`. Neither rule fires, so a real disagreement is reported as nothing. Add a finding (for example `benefit-risk-not-accepted`) and an AC. | spec/functional/FR-105-decision-policy-discrepancy-report.md:30-31 |
| FND-005 | medium | FR-105 has no rule for an `accepted` (or `not_accepted`) residual risk whose levels resolve to no region. That happens when a level is `not_assessed`/`unknown`, or not a policy member (FR-102 then reports no region). Such a risk gets no discrepancy finding, so an acceptance over an unassessed estimate passes silently. Add a finding and an AC. | spec/functional/FR-105-decision-policy-discrepancy-report.md:30-34, spec/functional/FR-102-estimate-levels-resolve-in-policy.md:33-34 |
| FND-006 | medium | FR-107 `residual-risk-not-considered` needs to know which residual risks belong to "the product". FR-103's `residual_risk` carries no product reference, and FR-107 does not say what type its product reference targets. The warning cannot be computed as specified. State the membership rule (for example every `residual_risk` in the bundle) and the product reference target. | spec/functional/FR-107-overall-residual-risk-evaluation.md:26,28 |
| FND-007 | medium | FR-103 puts post-control severity and probability levels inline. PLAT-1409 (#34 FR-203/FR-204) declares a `risk_estimate` with `phase: post_control` that holds the same values. Two homes for one judgement can disagree. Once the PLAT-1409 types exist, `residual_risk` should reference the post-control `risk_estimate` (author question 3). Terminology also diverges: FR-004 and FR-203 use the `Likelihood` scale, and FR-101/FR-102 say "probability". | spec/functional/FR-103-residual-risk-record.md:38 |
| FND-008 | medium | FR-104-AC-3 is an Inspection, "a search of the package for such definitions returns none", with no stated search target. "No scoring function" cannot fail in a reproducible way. The Behavior subject "No tool" / "Every tool built on these types" also reaches beyond this module's tooling. Bound the subject to this module's tooling, and restate the AC as observable output (no numeric field in any emitted schema or report, which FR-102-AC-4 already does). | spec/functional/FR-104-no-computed-verdicts.md:16,23-26,35 |
| FND-009 | medium | FR-004 already lets a hazard carry `status: accepted` with provenance. FR-103 adds a separate `residual_risk.decision: accepted`. Neither FR-103 nor FR-105 says how the two relate, or whether a hazard `status: accepted` without an accepted residual risk is a discrepancy. That leaves two acceptance records with no rule between them. | spec/functional/FR-103-residual-risk-record.md:17-21, spec/functional/FR-004-type-distinct-safety-schemas.md:66 |
| FND-010 | medium | FR-106 Behavior fails a reference that does not resolve to a `residual_risk` document. FR-106-AC-4 tests only an undeclared id, and no AC covers a reference resolving to another type (for example a `hazard`). That error path has no criterion. | spec/functional/FR-106-benefit-risk-record.md:28,38 |
| FND-011 | low | FR-107 `evaluation-accepted-with-open-risk` covers considered risks that are `undecided` or `not_accepted`. FR-107-AC-4 tests only `not_accepted`. | spec/functional/FR-107-overall-residual-risk-evaluation.md:29,40 |
| FND-012 | low | FR-102-AC-3 refers to "the finding" for a `not_assessed` probability, but FR-102 Behavior does not say a not-assessed level produces a finding. FR-102 also lists "unassessed or unknown" and leaves out FR-004's `not_applicable`. | spec/functional/FR-102-estimate-levels-resolve-in-policy.md:34,43 |

## Author questions

1. FR-105 reading the mark from the policy region list is the right design. The
   project's people decide which regions are acceptable, and the tool only reads
   that. FR-101 must declare and require the mark (FND-001). It needs to be one
   flag per region with no default, so the three-region example (acceptable /
   further control required / unacceptable) works as two outside regions.
2. A configured non-person denylist is weak (FND-003). It can only reject the
   names someone remembered to list, and anything else passes as a person. An
   allowlist roster of people works better: a project-authored document that
   `decided_by` must resolve into, which validation can check. The commit author
   alone is not enough, because an agent may commit the file. If a roster is out
   of scope for v1, drop the schema-level "SHALL reject role/team/tool" claim and
   keep only what an AC can test.
3. Deferring the `depends_on` edges to PLAT-1409 objects is fine while #34 is
   unmerged. FND-007 records the duplication that the later edge must resolve.
