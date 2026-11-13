---
id: US-401
title: "Record conflicting requirements instead of silently picking a reading"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-safety/StR-401"
    type: "traces_to"
---
# US-401: Record conflicting requirements instead of silently picking a reading

## Story

**As a** spec author or planning agent who finds two requirements that cannot both hold
**I want** the conflict recorded as a first-class object that names the clauses in conflict
and how it was closed
**So that** a release cannot go out while a conflict is still open, and a conflict that a
person chose to live with carries that person's name instead of vanishing into whichever
reading the last author preferred.

Source: PLAT-1480 (Risk Model, milestone M3 "Completeness rules as data"). The ticket text is
data; the behaviour below is what this module specifies.

## Context

Today a conflict between two clauses is resolved by whoever happens to notice it, in the
direction they happen to prefer, with no trace. FR-401..FR-405 declare the `tension` object,
its three states, the manifest completeness rule and its intake path.

## Acceptance Examples (Illustrative)

These examples are illustrative only, not test cases.

- An author finds that one requirement demands a response within 200 ms and another demands
  a synchronous audit write. They record a tension naming both and leave it open. The
  completeness check reports it.
- The team adds a design element that satisfies both. The author links it from the tension,
  marks it `resolved-by-design`, and the report is clean.
- A named person decides to live with the conflict. The author records the tension as
  `accepted-by-person` with that person in `decided_by`. Naming nobody is rejected.
