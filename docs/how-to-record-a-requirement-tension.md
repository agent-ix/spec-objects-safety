# How to record a requirement tension

Use a tension record when two requirements cannot both be satisfied as written.
The record captures both source requirements, the conflict in plain language,
and the disposition a person authored. Validation does not decide whether the
conflict is acceptable.

## Prerequisites

- Install Quire and make the safety object module available to it.
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

One requirement calls for immediate processing while another caps the work
available to each operation; under the stated load, both cannot be guaranteed.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| tension_id | UUID | 1..1 | identity |
```

An open tension must name at least two requirements or clauses through
`conflicts_with`. It cannot include `resolved_by` or `decided_by`.

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

Run validation against the corpus and the module:

```sh
quire validate --module /path/to/spec-objects-safety /path/to/corpus
```

An open tension validates as a record but is reported as `trace:open-tension`.
A resolved-by-design tension without its outgoing `resolved_by` link is
reported as `trace:resolved-tension-without-link`. An accepted-by-person
tension needs its named decision maker and passes both completeness rules.
Configure a release repository's trace checks as errors when open or unresolved
tensions must block that repository's release.
