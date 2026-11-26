# How to record a requirement tension

Use a tension record when two requirements cannot both be satisfied as written.
The record captures both source requirements, the conflict in plain language,
and the disposition a person authored. Validation does not decide whether the
conflict is acceptable.

## Prerequisites

- Install Quire and make the ISO, safety, architecture, business, and security
  modules available to it. The shared registry lets validation resolve the
  edge verbs and cross-module object roles declared by those modules.
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

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| immediate_requirement | conflicts_with | FR-020 | 1..1 |
| bounded_work_requirement | conflicts_with | NFR-008 | 1..1 |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| tension_id | UUID | 1..1 | identity |
```

An open tension must name at least two requirements or clauses through
`conflicts_with`. It cannot include `resolved_by` or `decided_by`.
Keep the `Relationships` table and frontmatter `relationships` list aligned:
the table supplies the validated record, and frontmatter supplies the graph
edges Quire reports.

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

Add a `resolved_by` row for `PART-042` to the record's `Relationships` table
as well.

If a person decides to live with the conflict, use `status: accepted-by-person`
and add a non-empty `decided_by: Name`. Do not add a date; the file's version
history records who authored the decision and when.

## Verify the record

Validate the record in bundle mode with the edge, safety, and design-element
registries:

```sh
quire validate --okf \
  --module /path/to/spec-artifacts-iso \
  --module /path/to/spec-objects-safety \
  --module /path/to/spec-objects-business \
  --module /path/to/spec-objects-security \
  --module /path/to/spec-objects-architecture \
  /path/to/corpus
```

Then report tension completeness from the same corpus:

```sh
quire relations --repo agent-ix/spec-objects-safety=/path/to/corpus \
  --module /path/to/spec-artifacts-iso \
  --module /path/to/spec-objects-safety \
  --module /path/to/spec-objects-business \
  --module /path/to/spec-objects-security \
  --module /path/to/spec-objects-architecture \
  --relation tension-is-not-open \
  --relation resolved-tension-has-link \
  --json
```

The report marks an open tension without a closing edge and a
resolved-by-design tension without its outgoing `resolved_by` link as
`uncovered`. An accepted-by-person tension needs its named decision maker and
does not enter either relation's selected population. Add `--strict` when an
uncovered tension must block the release.
