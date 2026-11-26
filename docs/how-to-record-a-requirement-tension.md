# How to record a requirement tension

Use a tension record when two requirements cannot both be satisfied as written.
The record captures both source requirements, the conflict in plain language,
and the disposition a person authored. Validation does not decide whether the
conflict is acceptable.

## Prerequisites

- Install Quire and make the ISO, safety, architecture, business, and security
  modules available to it. The shared registry lets validation resolve the
  edge verbs and cross-module object roles declared by those modules.
- Each `--module` path below points to the module package directory that
  contains `manifest.yaml` (usually a subdirectory of the repository checkout).
- Keep both source requirements in the same corpus or load their repositories
  together so the links can be resolved.
- Choose a unique document ID for the tension.

## Write the record

Create a Markdown file such as `spec/tensions/TEN-014.md`:

```markdown
---
id: TEN-014
title: "ImmediateResponseAndBoundedWork"
type: tension
object: tension
status: open
relationships:
  - target: FR-020
    type: conflicts_with
  - target: NFR-008
    type: conflicts_with
---
# [TEN-014] ImmediateResponseAndBoundedWork

## Conflict

`One requirement calls for immediate processing. Another caps the work available to each operation; under the stated load, both cannot be guaranteed.`

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| tension_id | UUID | 1..1 | identity |
```

An open tension must name at least two requirements or clauses through
`conflicts_with`. It cannot include `resolved_by` or `decided_by`.
The frontmatter `relationships` list is the single source for these graph
edges. The completeness report reads these links directly.

## Resolve or accept the conflict

After a design change satisfies both requirements, set `status` to
`resolved-by-design` and add an outgoing `resolved_by` edge to the design
element or decision record that closes the conflict:

```yaml
status: resolved-by-design
relationships:
  - target: FR-020
    type: conflicts_with
  - target: NFR-008
    type: conflicts_with
  - target: PART-042
    type: resolved_by
```

If a person decides to live with the conflict, use `status: accepted-by-person`
and add a non-empty `decided_by: Name`. Do not add a date; the file's version
history records who authored the decision and when.

## Verify the record

First run structural and semantic validation on the documents. This checks the
tension frontmatter against its data schema, including the rule that an
accepted tension names `decided_by`:

```sh
quire validate --scope /path/to/corpus \
  --module /path/to/spec-artifacts-iso/spec_artifacts_iso \
  --module /path/to/spec-objects-safety/spec_objects_safety \
  --module /path/to/spec-objects-business/spec_objects_business \
  --module /path/to/spec-objects-security/spec_objects_security \
  --module /path/to/spec-objects-architecture/spec_objects_architecture \
  'spec/**/*.md'
```

Then validate the corpus in bundle mode with the same registries. This checks
the bundle's cross-document links and completeness:

```sh
quire validate --okf \
  --module /path/to/spec-artifacts-iso/spec_artifacts_iso \
  --module /path/to/spec-objects-safety/spec_objects_safety \
  --module /path/to/spec-objects-business/spec_objects_business \
  --module /path/to/spec-objects-security/spec_objects_security \
  --module /path/to/spec-objects-architecture/spec_objects_architecture \
  /path/to/corpus
```

Then report tension completeness from the same corpus:

```sh
quire relations --repo agent-ix/spec-objects-safety=/path/to/corpus \
  --module /path/to/spec-artifacts-iso/spec_artifacts_iso \
  --module /path/to/spec-objects-safety/spec_objects_safety \
  --module /path/to/spec-objects-business/spec_objects_business \
  --module /path/to/spec-objects-security/spec_objects_security \
  --module /path/to/spec-objects-architecture/spec_objects_architecture \
  --relation tension-is-not-open \
  --relation resolved-tension-has-link \
  --json
```

The report marks an open tension without a closing edge and a
resolved-by-design tension without its outgoing `resolved_by` link as
`uncovered`. An accepted-by-person tension needs its named decision maker and
does not enter either relation's selected population. Inspect the selected
rows in the JSON output for `uncovered`. `--strict` also fails when a selected
relation has no rows or only `not-tracked` rows, so it can fail even when the
tension condition is satisfied; use the row states when this check is a
tension-specific release gate.
