---
id: FR-005
title: "Ship the skeletons as executable typed fixtures with negative counterparts"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-safety/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-safety/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "depends_on"
---
# FR-005: Ship the skeletons as executable typed fixtures with negative counterparts

## Description

Each object type's authoring skeleton SHALL be a document the engine validates
and extracts, declaring its fields in the typed `## Properties` table with a
`sysml` alternate and its clauses as `ocl` fences under `## Invariants`, and
each named refusal SHALL have a fixture that fails for that reason, so the
shipped teaching example and the shipped contract cannot disagree.

## Inputs

- The Quire wheel exposing `extract_semantic`, at 0.46.0. It is not a declared
  dependency: `internal-pypi` serves 0.33.0 at most and no `quire-rs` tag
  carries the semantic layer, so it is provisioned by `make dev-quire` and
  `agent-ix/quire-rs#392` is the blocking issue.
- The emitted schemas of [FR-002](./FR-002-emitted-json-schemas.md) and the
  manifest of [FR-003](./FR-003-semantic-manifest-contract.md).
- The typed-table and `sysml` cell grammars of quoin FR-071 and the clause
  mapping of quoin FR-072.

## Outputs

- `spec_objects_safety/skeletons/{hazard,failure_mode}.md` and their
  `.sysml.md` alternates.
- `tests/fixtures/negative/*.md`, one per named refusal.
- `tests/fixtures/baseline-0.2.0/`, the 0.2.0 locator set and the 0.2.0
  skeletons kept as compatibility fixtures.

## Behavior

- Every skeleton SHALL validate through `quire.validate_document` with zero errors.
- Every skeleton SHALL declare at least one field flagged `identity` in its `## Properties` table.
- Each object type SHALL ship a `.sysml.md` alternate declaring exactly the same fields as its table form.
- The two forms SHALL extract to identical normalized `fields`, with `fieldsForm` `table` and `fence` respectively.
- No artifact SHALL carry both Properties forms.
- When an artifact carries a second Properties form, the engine SHALL refuse the document at that form.
- Every skeleton SHALL declare its clauses as one `ocl` fence under one `### <clauseId>` heading each.
- Every extracted clause SHALL carry a source span.
- Every H2 heading in a skeleton SHALL be a heading some manifest locator names.
- Every heading a required locator names SHALL be present in the skeleton.
- The `## Properties` table SHALL NOT restate a value the `## Assessment` or `## Analysis` table already carries, so the document has one home per fact.
- No skeleton SHALL carry a placeholder token.
- Every asserted section of a skeleton SHALL hold at least 200 characters of body text, so the shipped example teaches the form rather than gesturing at it.
- Skeleton titles SHALL be distinct `Identifier`s outside the kernel-scalar set.
- Each skeleton's frontmatter `object` SHALL equal its `type`.
- The negative fixtures SHALL cover: a hazard with no identity row, a failure mode with no identity row, both Properties forms in one artifact, a non-`Identifier` type token, a hazard with no `Assessment` table, a clause heading with no fence, and an `Analysis` table missing the `Detection` column.
- Every negative fixture SHALL declare `expect` and `because` in its frontmatter.
- Every negative fixture SHALL fail validation.
- Every negative fixture's error message SHALL be longer than its `expect` token, so the fixture fails with a diagnosis rather than a bare code.
- No change under this requirement SHALL touch a corpus repository, a vendored corpus fixture, or a sibling module.
- The semantic tests SHALL fail, never skip, when the Quire wheel is absent.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-005-CON-1 | No change on this branch SHALL touch a corpus repository or a vendored fixture. | Scope | Test |
| FR-005-CON-2 | One artifact carries one Properties form; the alternate is a separate file, never a second block. | Authoring | Test |
| FR-005-CON-3 | A missing engine SHALL fail the suite, never skip it: a skipped row is not coverage. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | All four skeletons validate with zero errors. | Test |
| FR-005-AC-2 | For each object type the table and `sysml` skeletons extract to identical normalized `fields`, with `fieldsForm` `table` and `fence`. | Test |
| FR-005-AC-3 | Under a bundle index built from the skeleton frontmatter every skeleton extracts with zero error diagnostics and zero unresolved type tokens. | Test |
| FR-005-AC-4 | Availability per skeleton is `fields: available`, `clauses: available`, `operations: not_applicable`, matching the locators the type declares. | Test |
| FR-005-AC-5 | Every negative fixture fails with its declared `expect`, its error message is longer than that token, and all seven named cases exist. | Test |
| FR-005-AC-6 | Every skeleton H2 is a heading a manifest locator names, and every required heading is present. | Test |
| FR-005-AC-7 | Every skeleton is placeholder-free and its body outside frontmatter and comments exceeds 200 characters. | Test |
| FR-005-AC-8 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter. | Test |
| FR-005-AC-9 | No `## Properties` row names a column of the `## Assessment` or `## Analysis` table of the same type. | Test |
| FR-005-AC-10 | With the Quire wheel absent, the semantic tests fail naming `make dev-quire` and `agent-ix/quire-rs#392`; none is skipped. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-type-distinct-safety-schemas.md); quoin FR-071/FR-072
- **Downstream**: none in this module; generated-language fixtures are gated on `agent-ix/quoin#290`
