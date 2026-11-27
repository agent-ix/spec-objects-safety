---
id: NFR-100
title: "Residual-risk findings are advisory, deterministic and bounded"
type: NFR
quality_attribute: safety
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-102"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-105"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-safety/FR-107"
    type: "constrains"
---
# NFR-100: Residual-risk findings are advisory, deterministic and bounded

## Statement

The residual-risk tooling SHALL produce identical findings for identical inputs.

The residual-risk tooling SHALL leave every authored document unmodified.

The residual-risk tooling SHALL complete over a project of 5,000 residual-risk records within 10 seconds.

## Rationale

Tracked by Linear PLAT-1523. A finding that varies between runs, or a check that edits decisions, would let a tool stand in for the named decider.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Wall time for 5,000 fixture residual-risk records | 3 s | 10 s | Test |

## Verification

A test runs the discrepancy report twice over a fixture bundle and compares the two outputs byte for byte, then compares each fixture file's bytes before and after a run; a test generates 5,000 records and times one run.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-100-AC-3 | One run over 5,000 generated residual-risk records completes within 10 seconds. | Test |

Quoin FR-154 owns and tests deterministic, read-only discrepancy reporting. See
[Quoin FR-154](https://github.com/agent-ix/quoin/blob/main/spec/functional/FR-154-risk-discrepancies-command.md).

## Dependencies

- **Upstream**: [FR-102](../functional/FR-102-estimate-levels-resolve-in-policy.md), [FR-105](../functional/FR-105-decision-policy-discrepancy-report.md), [FR-107](../functional/FR-107-overall-residual-risk-evaluation.md)
