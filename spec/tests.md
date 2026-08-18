---
id: TM-001
title: "spec-objects-safety Test Matrix"
type: TestMatrix
---
# Test Matrix

## Overview

Maps every acceptance criterion to the test that backs it. The FR-035 gate
ships with the module, so no row here is `🚧` on the day it lands.

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-002 | ✅ Complete |
| FR-001 | FR-001-AC-2 | TC-003 | ✅ Complete |
| FR-001 | FR-001-AC-3 | TC-003 | ✅ Complete |
| FR-001 | FR-001-AC-4 | TC-005 | ✅ Complete |
| FR-001 | FR-001-AC-5 | TC-001 | ✅ Complete |
| FR-001 | FR-001-AC-6 | TC-004 | ✅ Complete |
| FR-001 | FR-001-AC-7 | TC-007 | ✅ Complete |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | The manifest validates against the FR-035 module-manifest schema, imported from spec-artifacts-iso rather than copied — no skip and no escape hatch, both of which reported a gate green while running nothing upstream | Unit | P0 | FR-001-AC-5 | ✅ |
| TC-002 | The manifest declares exactly `hazard` and `failure_mode`, each with a `data_schema` and at least one role | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-003 | `hazard` requires Condition + an Assessment table (Severity, Likelihood, Rationale) with Mitigation optional; `failure_mode` requires Description + an Analysis table (Effect, Cause, Detection). The two shapes differ because FMEA and hazard analysis score different things | Unit | P0 | FR-001-AC-2, FR-001-AC-3 | ✅ |
| TC-004 | Every lexicon entry is exactly `{definition: <text>}`, asserted structurally — an unquoted comma inside a YAML flow mapping is read as an entry separator and silently truncates the definition | Unit | P0 | FR-001-AC-6 | ✅ |
| TC-005 | Each object type ships a skeleton, and each skeleton supplies every heading its contract requires | Unit | P0 | FR-001-AC-4 | ✅ |
| TC-006 | The pack exposes `MANIFEST_PATH` / `PACK_ROOT` as importable resource data, which is how the activation pipeline reaches it | Unit | P1 | FR-001-AC-4 | ✅ |
| TC-007 | Every `allowed_links` verb exists in the iso edge vocabulary, as a forward key or a declared inverse label. The ticket assumed `causes`/`contributes_to` would be added; applying iso FR-004's "a near-synonym is a reason not to add" says use the existing `arises_from` instead | Unit | P0 | FR-001-AC-7 | ✅ |

## Coverage Gaps

None. Every acceptance criterion has an implemented test, and `quire validate --scope .` reports no diagnostic of any kind over the bundle.
