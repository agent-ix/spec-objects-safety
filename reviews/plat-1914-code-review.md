---
id: SR-424
title: "code-review — authored tension records"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-safety; PLAT-1914; PR #52; tension schemas, manifest, skeleton, tests and how-to"
review_set: subset
---

## Summary

Reviewed head 0a0df62576cd35b64858f1ac4d47ccc15ac1b08e. FAIL.

## Verdict

**FAIL** — see findings and coverage limits.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Tension duplicates the existing PersonName contract as inline minLength/regex while declaring decided_by as string. PersonName already owns exactly these constraints and is used by the other acceptance records. Reuse decided_by?: PersonName and remove the duplicated conditional property constraints; regenerate emitted schemas. This violates the code-review prohibition on duplicating an existing rule. | typespec/main.tsp:779 |
| FND-002 | medium | The published verification command passes a corpus directory without --okf, so Quire 0.52.0 exits with PathNotAFile instead of checking tensions. Loading only the safety module also omits its required edge/role registries. Show a tested bundle-mode command with the required module set or an equivalent supported discovery setup. | docs/how-to-record-a-requirement-tension.md:75 |
| FND-003 | medium | All new integration validations unconditionally import spec_objects_architecture, but the project declares no such dev dependency or provisioning lane. The supplied Python 3.13 environment returns MISSING for find_spec("spec_objects_architecture"), so _module fails before any Quire check. Provision the dependency through the project or provide an explicitly supported fixture path and lane. | tests_integration/test_tension_completeness.py:95 |

## Reviewed units

```yaml
scope:
- id: FR-405-CON-1
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: No workflow definition SHALL live in this module's object-type vocabulary.
- id: FR-405-AC-1
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: A corpus with no `tension` records raises no tension finding of any kind.
- id: FR-405-AC-2
  path: spec/functional/FR-405-tension-intake.md
  role: examined
  excerpt: 'An emitted `tension` with `status: open` and two `conflicts_with` entries
    validates and is reported by FR-404-AC-1.'
- id: FR-404-CON-1
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The engine SHALL contain no tension-specific code; the rule is two manifest
    entries.
- id: FR-404-CON-2
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The rule SHALL NOT compare, count or weigh tensions against each other;
    each is closed or not.
- id: FR-404-AC-1
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A corpus containing a `tension` with `status: open` is reported under
    `trace:open-tension`, naming that tension, and fails when the key is mapped to
    `error`.'
- id: FR-404-AC-2
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: open` that is the target of an incoming `conflicts_with`
    edge, or of an edge from a dangling or other document, is still reported under
    `trace:open-tension`.'
- id: FR-404-AC-3
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'Setting `status: resolved-by-design` with a `resolved_by` edge to a design
    element clears the finding; the corpus passes.'
- id: FR-404-AC-4
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: resolved-by-design` and no `resolved_by` edge
    is reported under `trace:resolved-tension-without-link`.'
- id: FR-404-AC-5
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: 'A `tension` with `status: accepted-by-person` and a named `decided_by`
    passes both relations; the same record with no `decided_by` still fails schema
    validation (FR-403-AC-1).'
- id: FR-404-AC-6
  path: spec/functional/FR-404-tension-completeness-rule.md
  role: examined
  excerpt: The manifest `traceability` block loads with the two new relations and
    the existing relations unchanged, and a corpus with no `tension` produces output
    identical to one before this FR.
- id: FR-403-CON-1
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'Acceptance is a human act: nothing in this module sets `decided_by` or
    `status: accepted-by-person` on any record.'
- id: FR-403-AC-1
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and no `decided_by` fails validation,
    naming `decided_by`.'
- id: FR-403-AC-2
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and an empty `decided_by` fails
    validation.'
- id: FR-403-AC-3
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: accepted-by-person` and a named person in `decided_by`
    validates.'
- id: FR-403-AC-4
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: open` or `status: resolved-by-design` and a `decided_by`
    fails validation.'
- id: FR-403-AC-5
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: 'A record with `status: open` and a `resolved_by` relation entry fails
    validation.'
- id: FR-403-AC-6
  path: spec/functional/FR-403-tension-state-validation.md
  role: examined
  excerpt: The emitted `Tension.json` has no acceptance-date property and no default
    for `status` or `decided_by`.
- id: FR-401-CON-1
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The module SHALL declare the type with the existing manifest object-type
    grammar and add no new engine mechanism.
- id: FR-401-CON-2
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The type SHALL NOT quote or name text from a paywalled standard.
- id: FR-401-AC-1
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The manifest declares `tension` as an object type and exports it, and a
    `Tension.json` schema is emitted for it.
- id: FR-401-AC-2
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: A `tension` record validates with `status` set to each of `open`, `resolved-by-design`
    and `accepted-by-person` (given each state's other required fields), and fails
    with any other `status` value.
- id: FR-401-AC-3
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: A `tension` record with no `status` fails validation.
- id: FR-401-AC-4
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The emitted `Tension.json` has no property for severity, likelihood, a
    date or a history list.
- id: FR-401-AC-5
  path: spec/functional/FR-401-tension-object-type.md
  role: examined
  excerpt: The `tension` skeleton validates, and an edited copy with its `Conflict`
    section removed fails.
- id: FR-402-CON-1
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: Every verb in `allowed_links` for `tension` SHALL exist in the `spec-artifacts-iso`
    edge vocabulary once PLAT-1675 lands (FR-006-AC-4 continues to hold).
- id: FR-402-AC-1
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` record with two `conflicts_with` relation entries validates;
    one with a single entry fails schema validation.
- id: FR-402-AC-2
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` that authors `references` or any other verb outside `conflicts_with`
    and `resolved_by` draws an undeclared-link diagnostic naming the tension.
- id: FR-402-AC-3
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: A `tension` authoring `resolved_by` to a design element document resolves
    and passes the edge check.
- id: FR-402-AC-4
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: The `tension` schema declares no property naming a person other than `decided_by`,
    and the manifest declares no person object type.
- id: FR-402-AC-5
  path: spec/functional/FR-402-tension-edges.md
  role: examined
  excerpt: Once PLAT-1675 lands, every verb in the `tension` `allowed_links` exists
    in the iso edge vocabulary as a forward key or declared inverse.
- id: NFR-401-M-1
  path: spec/non-functional/NFR-401-tension-generic-and-human-accepted.md
  role: examined
  excerpt: 'Schema defaults for `decided_by` or `status`: target 0, threshold 0, method
    Test.'
```

## Coverage

Explicit released Quoin `/tmp/regfinish-quoin-v0.37.0/quoin` 0.37.0 and Quire `/home/peter/.npm-global/bin/quire` 0.52.0 (engine 0.62.2); authoring contract spec-artifacts-process@v0.36.0. No applicable AssuranceProfile found. Exact model identifier is not exposed; marker records model=unknown. No spec or plan files changed, so spec-review is inapplicable. Review artifacts are scratch files for lead custody; repository source was not changed.

Inspected every changed path and the relevant existing PersonName type, schema generator, integration helper patterns, package dependencies and requirement text. The schema and state branches match the authored three-disposition design on inspection. No new test stubs or mock replacements were found. Each new test carries criterion trace tags. Schema/model changes implement declarative criteria; there are no new production implementation functions to tag.

The documented verification command was exercised against `/tmp/reviewsafety52/corpus` with the actual safety module: it reports `PathNotAFile` and missing registry diagnostics. The exact queued Python environment independently reports spec_objects_architecture MISSING; security and ISO packages are installed. Focused pytest remains queued under the dispatching lead's locked-build command at review time, so no passing result is claimed. Diff whitespace check passed. Ruff, Black and schema-generation checks are recorded after completion below.

Completed independent checks: schema emitter drift check passed (42 schemas); Ruff passed for all seven touched Python files; Black passed for all seven touched Python files.

## Examined test bindings

```yaml
bindings:
- test_id: test_manifest_exports_the_emitted_tension_schema
  ac_id: FR-401-AC-1
  trace: correct
- test_id: test_tension_accepts_each_disposition_and_requires_two_conflict_edges
  ac_id: FR-401-AC-2
  trace: correct
- test_id: test_tension_accepts_each_disposition_and_requires_two_conflict_edges
  ac_id: FR-402-AC-1
  trace: correct
- test_id: test_tension_requires_an_explicit_status
  ac_id: FR-401-AC-3
  trace: correct
- test_id: test_tension_schema_is_generic_and_has_no_computed_or_personal_metadata
  ac_id: FR-401-AC-4
  trace: correct
- test_id: test_tension_schema_is_generic_and_has_no_computed_or_personal_metadata
  ac_id: FR-402-AC-4
  trace: correct
- test_id: test_tension_schema_is_generic_and_has_no_computed_or_personal_metadata
  ac_id: NFR-401-M-1
  trace: correct
- test_id: test_only_person_named_acceptance_is_valid
  ac_id: FR-403-AC-1
  trace: correct
- test_id: test_only_person_named_acceptance_is_valid
  ac_id: FR-403-AC-2
  trace: correct
- test_id: test_only_person_named_acceptance_is_valid
  ac_id: FR-403-AC-3
  trace: correct
- test_id: test_nonaccepted_tensions_refuse_deciders_and_open_refuses_resolution_edges
  ac_id: FR-403-AC-4
  trace: correct
- test_id: test_nonaccepted_tensions_refuse_deciders_and_open_refuses_resolution_edges
  ac_id: FR-403-AC-5
  trace: correct
- test_id: test_tension_skeleton_validates_but_requires_its_conflict_section
  ac_id: FR-401-AC-5
  trace: correct
- test_id: test_tension_rejects_undeclared_links_with_a_named_diagnostic
  ac_id: FR-402-AC-2
  trace: correct
- test_id: test_resolved_by_design_edge_to_a_part_clears_the_tension_finding
  ac_id: FR-402-AC-3
  trace: correct
- test_id: test_resolved_by_design_edge_to_a_part_clears_the_tension_finding
  ac_id: FR-404-AC-3
  trace: correct
- test_id: test_open_tension_is_named_and_fails_when_its_check_is_an_error
  ac_id: FR-404-AC-1
  trace: correct
- test_id: test_open_tension_is_named_and_fails_when_its_check_is_an_error
  ac_id: FR-405-AC-2
  trace: correct
- test_id: test_incoming_conflicts_with_edge_does_not_close_an_open_tension
  ac_id: FR-404-AC-2
  trace: correct
- test_id: test_resolved_tension_without_its_design_edge_is_reported
  ac_id: FR-404-AC-4
  trace: correct
- test_id: test_named_person_acceptance_passes_but_missing_name_fails
  ac_id: FR-404-AC-5
  trace: correct
- test_id: test_corpus_without_tensions_has_identical_validation_output
  ac_id: FR-404-AC-6
  trace: correct
- test_id: test_corpus_without_tensions_has_identical_validation_output
  ac_id: FR-405-AC-1
  trace: correct
```
