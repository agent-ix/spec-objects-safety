---
id: Task-009
title: "IT-001 — Quoin install roundtrip against a temporary catalog"
type: Task
status: done
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-070
    type: verifies
---
# Task-009: IT-001 — Quoin install roundtrip against a temporary catalog

## Scope

Drive the real Quoin CLI against a temporary config root: install, list, load through
Quire from the installed copy, validate a skeleton against it, and leave the catalog as
it was found.

## Subtasks

- [x] **Isolation.** A temporary `IX_CONFIG_ROOT`, so a developer's own catalog is never a candidate.
- [x] **Install.** Exit zero with no `semantic.*` diagnostic, then listed.
- [x] **Load.** Both types register from the installed copy and every installed digest still matches the installed bytes.
- [x] **Resolve.** A shipped skeleton validates against the installed location, proving the module-relative `schema:` path resolved.

## Deliverables

- `tests_integration/test_quoin_install_roundtrip.py`

## Notes

- The row is carried `🚧`. The test is real and tagged, and it does not pass on the machine this branch was written on: the globally installed `quoin` is a symlink into a live worktree whose `dist/` is missing `dist/schemas/module-manifest.schema.json`, so the install exits non-zero before reaching anything this module owns. It lives in `tests_integration/` so `make test` cannot report a green suite over a broken CLI.
