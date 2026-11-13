---
id: SR-062
title: "Base spec review of FR-305 alignment with quoin risk-summary"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-safety; PR #42 (git diff origin/main...HEAD at 80c38956): spec/functional/FR-305-risk-summary-report.md"
---

# Base spec review of FR-305 alignment with quoin risk-summary

## Summary

Ticket: PLAT-1576. Checklist, consistency and dependency review of the FR-305 amendment against quoin
FR-169 and FR-170 on agent-ix/quoin PR #863 (head 68717d15) and against FR-204 and FR-301..303 here.

The amendment matches quoin exactly. The entry id keys are `estimate`, `control` and `residual_risk`;
findings are `{finding, names}` objects; the token list adds FR-204's `post-control-without-control`;
FR-305-AC-5 now names every key set (row, estimate, control, residual-risk, finding), so it can fail on
any extra or missing key; new FR-305-AC-11 is testable and agrees with FR-170-AC-15. No other contract
line changed, no paywalled standard text or name was added, and no hash, pin or tracking record was
introduced. `quire validate` over the file reports no errors (an environment-only DuplicateModuleName
warning, because the module is both installed and in the checkout).

Examined (role examined): FR-305 Description, Output contract table, FR-305-AC-5 and FR-305-AC-11.
Context only: FR-204, FR-301..303 on `origin/main`; quoin FR-169, FR-170 on PR #863.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-305 now takes a token and AC-11 from FR-204, but the frontmatter has no depends_on edge to FR-204 and the Dependencies Upstream line does not list it. Add both. | FR-305:2-21, FR-305:51, FR-305:99, FR-305-AC-11 |
| FND-002 | low | The Description gains change history ("which aligned the entry keys and the finding shape with the quoin specification"). A requirement states the contract, not how it came to be; the clause stops being news once both PRs land. Drop it. | FR-305:25 |

## Verdict

Mergeable after the two low findings are fixed; neither changes the contract. Merge this PR before, or
with, agent-ix/quoin#863, whose FR-169 "Divergence from the safety module's contract" section becomes
false once this lands.
