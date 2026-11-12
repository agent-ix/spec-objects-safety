---
id: SR-020
title: "Gap analysis of PLAT-1477 reverse mitigates rule (spec-objects-safety#32)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-safety; FR-009 vs spec_objects_safety/manifest.yaml and tests (git diff origin/main...1ea2900)"
review_set: subset
---
# Gap analysis of PLAT-1477 reverse mitigates rule (spec-objects-safety#32)

## Summary

Ticket: PLAT-1477, which closes PLAT-370's reverse direction for safety.
Plan completion: not assessed.

The ticket asks for `from: NFR where quality_attribute in [safety]`, direction
`outgoing`, `edges: [mitigates]`, advisory. The manifest delivers exactly that,
and the security half is in spec-objects-security#43. `quoin matrix` shows
FR-009-AC-1..5 all `tagged`, bound to TC-099..TC-102. Every binding reads
correctly against its AC. Mutation evidence is in SR-018: each manifest
mutation fails at least one test. No stubs, no production code without an
owning requirement, no coverage inflation.

## Verdict

One coverage gap: half of FR-009-AC-5 is untested.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-102 (the test named "advisory") runs `--okf --strict` but asserts only that one finding exists. It never asserts the exit code or that the finding is a `warning:` under `--strict`, so the strict half of FR-009-AC-5 is unverified. The literal "exits 0" would fail on this fixture anyway (exit 3, from iso's unknown-type or unowned-quality-characteristic errors; see SR-019 FND-001), which is presumably why the assertion was left out. | tests_integration/test_reverse_mitigates.py:115-118 |

## Finding detail

- FND-001: once SR-019 FND-001 rewords the criterion, assert
  `_findings(strict)[0].startswith("warning:")`. Optionally also assert that
  the strict error count is the same with the rule present and with
  `--severity trace:unjustified-safety-nfr=off`.
