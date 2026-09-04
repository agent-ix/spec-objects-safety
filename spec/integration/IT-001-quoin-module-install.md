---
id: IT-001
title: "Quoin installs the semantic module and Quire loads it from the catalog"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "verifies"
---
# IT-001: Quoin installs the semantic module and Quire loads it from the catalog

## Objective

Verify the integration boundary between this module and the Quoin catalog: a
module whose `data_schema` is a path-and-digest reference must install without a
`semantic.*` diagnostic, appear in the installed module list, and then load
through Quire from the catalog location with both object types registered.
Without this test the module could be self-consistent in its own tree and still
be unusable once installed, which is where a digest or a relative-path defect
would surface.

## Target Integration

The system under test is the `spec-objects-safety` module directory. The
external dependency is the Quoin CLI and the user-level module catalog under
`~/.ix/filament/modules`. The integration exercised is `quoin module install
path:<module dir>` followed by a Quire registry load over the installed copy.

## Preconditions

Quoin is installed at a build carrying the semantic-module contract (`3e842ce`
or later). The Quire wheel exposing `extract_semantic` is present, provisioned
by `make dev-quire`. The test records whatever `spec-objects-safety` entry is
already installed so it can restore it, and runs against a temporary config
root when one can be given, so a developer's catalog is never left mutated.

## Inputs

The module directory `spec_objects_safety/`, containing `manifest.yaml`, the
emitted `schemas/` and the skeletons; every `data_schema` in it is the
reference form `{schema, digest}`.

## Test Procedure

Each step performs one discrete action and has its own success criterion.

1. Record the currently installed `spec-objects-safety` entry, if any.
   - IT-001-SC-01: the prior catalog state is captured before anything is written.
2. Run `quoin module install path:<module dir>`.
   - IT-001-SC-02: the command exits zero and its output carries no `semantic.*` error diagnostic.
3. Run `quoin module` and read the installed list.
   - IT-001-SC-03: `spec-objects-safety` appears in the list.
4. Load the installed module directory through Quire's registry loader.
   - IT-001-SC-04: both `hazard` and `failure_mode` are registered, and the recorded schema digest equals the manifest digest.
5. Validate a shipped skeleton against the installed copy.
   - IT-001-SC-05: validation reports no `semantic.*` load failure, so the referenced schema resolved from the installed location.
6. Restore the catalog to the state recorded in step 1.
   - IT-001-SC-06: the prior entry is reinstated, or the module is removed when none was installed.

## Expected Results

The install succeeds, the module is listed, Quire registers both object types
from the installed copy with matching digests, a skeleton validates against it,
and the developer's catalog ends the run in the state it started in. The test
passes only when every per-step success criterion holds.

## Metadata

- Priority: High
- Target Integration: Quoin module catalog
- Automation: Automated

## Dependencies

**Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), whose
reference-form `data_schema` this test exercises across the install boundary.
**Downstream**: none.

## Notes

Activation against a running `filament-core-service` is a different boundary and
is not covered here: no service instance is available to this repository, and
`agent-ix/filament-core-service#23` — reference-form `data_schema` resolved into
a stored snapshot at activation — is open, so the service would store the
reference verbatim rather than the schema.
