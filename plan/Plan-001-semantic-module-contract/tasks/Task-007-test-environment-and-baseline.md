---
id: Task-007
title: "FR-005 — Quire provisioning, the no-skip gate and the 0.2.0 baseline"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-safety/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-057
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-065
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-066
    type: verifies
---
# Task-007: FR-005 — Quire provisioning, the no-skip gate and the 0.2.0 baseline

## Scope

Provision the engine the semantic rows need, make its absence a failure rather than a
skip, and check in the 0.2.0 bytes everything additive is measured against.

## Subtasks

- [x] **Provisioning.** `make dev-quire` installs the 0.46.0 wheel from the dev index; `quire` is deliberately not a committed dependency while quire-rs#392 is open.
- [x] **No vacuous skip.** The helper every semantic test goes through fails naming the provisioning path and the issue, and a scan asserts no test in the suite reaches for a skip of its own.
- [x] **Baseline.** The 0.2.0 locator set, traceability model, lint rules and skeletons, checked in under `tests/fixtures/baseline-0.2.0/`.

## Deliverables

- `make dev-quire`
- `tests/conftest.py`
- `tests/fixtures/baseline-0.2.0/`

## Notes

- A skipped row is not coverage: this task is what stops the semantic suite reporting green against no engine at all.
- Unblocks: Task-004, Task-008.
