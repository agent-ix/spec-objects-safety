---
id: NFR-100
title: "Residual-risk findings are advisory, deterministic and bounded"
type: NFR
quality_attribute: safety
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-105"
    type: "constrains"
---
# NFR-100: Residual-risk findings are advisory, deterministic and bounded

## Statement

The residual-risk tooling SHALL produce identical findings for identical inputs, SHALL leave every authored document unmodified, and SHALL complete over a project of 5,000 residual-risk records within 10 seconds.

## Rationale

Tracked by Linear PLAT-1523. A finding that varies between runs, or a check that edits decisions, would let a tool stand in for the named decider.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Differing output bytes across two runs on identical inputs | 0 | 0 | Test |
| Authored files changed by a run | 0 | 0 | Test |
| Wall time for 5,000 fixture residual-risk records | 3 s | 10 s | Benchmark |

## Verification

A test runs the discrepancy report twice over a fixture bundle and compares output and file hashes; a benchmark generates 5,000 records and times one run.

## Dependencies

- **Upstream**: [FR-105](../functional/FR-105-decision-policy-discrepancy-report.md)
