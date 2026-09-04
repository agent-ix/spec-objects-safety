---
id: Task-003
title: "FR-002 — emitted set, toolchain.json, digests and packaging"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/Task-001
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-safety/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-017
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-018
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-019
    type: verifies
---
# Task-003: FR-002 — emitted set, toolchain.json, digests and packaging

## Scope

Commit the fifteen emitted schemas plus `toolchain.json`, and make the wheel, the
sdist and the npm tarball carry them beside the manifest.

## Subtasks

- [x] **Emitted set.** Exactly the two record models and the thirteen support models, recorded in `toolchain.json` with compiler and emitter versions, the `$id` base, the normalization record and an overall digest.
- [x] **Python packaging.** `spec_objects_safety/schemas/*.json` in the wheel and the sdist.
- [x] **npm packaging.** `prepack` stages `manifest.yaml`, `schemas/` and `skeletons/` at the repository root and `postpack` removes them again, so no stray root `manifest.yaml` is left for Filament tooling to discover as a second module.

## Deliverables

- `spec_objects_safety/schemas/` (15 files + `toolchain.json`)
- `scripts/stage-npm.mjs` with `--clean`
- `pyproject.toml` include entries

## Notes

- The `--clean` half is not cosmetic: a leftover root `manifest.yaml` makes `quire validate` in this repository fail with "no archetype registered".
- Unblocks: Task-004.
