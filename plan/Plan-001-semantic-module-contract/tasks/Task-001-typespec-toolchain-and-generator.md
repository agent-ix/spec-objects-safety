---
id: Task-001
title: "FR-002 — TypeSpec toolchain, schema generator and drift gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-safety/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-safety/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-013
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-014
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-015
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-016
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-020
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-021
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-022
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-023
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-024
    type: verifies
  - target: ix://agent-ix/spec-objects-safety/TC-025
    type: verifies
---
# Task-001: FR-002 — TypeSpec toolchain, schema generator and drift gate

## Scope

Stand up the emission toolchain: `typespec/main.tsp` importing `@agent-ix/semantic-core`
0.1.0, the pinned `@typespec/compiler` / `@typespec/json-schema` 1.15.0 devDependencies,
`scripts/generate-schemas.mjs`, and the drift gate that fails `make lint` when the
committed bytes and the source disagree.

## Subtasks

- [x] **Source.** `typespec/main.tsp` with `@jsonSchema` based on the manifest `version`, and `typespec/tspconfig.yaml` selecting the official JSON Schema emitter.
- [x] **Generator.** Compile with `tsp compile`, keep only this namespace's files, normalize any relative `$id`/`$ref`, render two-space JSON, write `toolchain.json`, and rewrite the manifest digests textually so YAML anchors and comments survive.
- [x] **Drift gate.** `--check` writes nothing and names every differing, stale or mis-digested file; `make lint` runs it.
- [x] **Packaging inputs.** `.gitattributes` pins `eol=lf` on the digested file types; `package-lock.json` resolves public packages from npmjs and `@agent-ix/semantic-core` from npm.ix, with no repository `.npmrc`.
- [x] **Bump procedure.** A base version differing from the manifest version fails naming both; a coordinated bump re-emits every `$id`, `$ref` and digest.

## Deliverables

- `typespec/main.tsp`, `typespec/tspconfig.yaml`
- `scripts/generate-schemas.mjs`
- `package.json`, `package-lock.json`, `.gitattributes`
- `make schemas`, `make schemas-check`

## Notes

- The generator is the only writer of `schemas/` and the only editor of `data_schema.digest`. A wrong schema is fixed in the source and regenerated, never hand-edited.
- The emission step runs on a developer machine, not in CI: `@agent-ix` resolves through the user-level npm config.
- Unblocks: Task-003, Task-004.
