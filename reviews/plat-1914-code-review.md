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

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | The resolved-state positive fixture appends target PART-001, but RelationDecl.target requires a qualified ix:// semantic ID. The focused test fails on this malformed target before testing tension state behavior. Independent schema inspection reports relations[2].target regex failure; changing only that value to ix://agent-ix/spec-objects-architecture/PART-001 yields no validation errors. Use a valid qualified fixture target. | tests/test_tension_schema.py:37 |
| FND-005 | high | The shipped Conflict prose locator is not supported by the current semantic extraction path. Both the focused skeleton test and independent Quire Python 0.62.2 validate_document fail with semantic.feature-not-extractable: ## Conflict is not of the form of record key conflict. The shipped tension skeleton therefore does not validate. Integrate the required prose with a supported extraction/schema contract and keep the positive and removed-section cases behavioral. | spec_objects_safety/manifest.yaml:752 |
| FND-006 | high | The new architecture pin is incompatible with the selected security module in the integration environment. Quire relations with all four declared modules refuses the merged traceability model: architecture connection-carries-classification selects record_keys regulatedCategories, absent from its endpoint schemas. With validate --okf, the same module combination produces no tension completeness findings: an open tension with trace:open-tension=error exits 0, and missing accepted-person names also exit 0. Select and test a coherent module set and ensure the validation route actually enforces the required tension checks. | pyproject.toml:43 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Tension now uses PersonName and removes duplicate inline person-name constraints; generated schema references PersonName. |
| FND-002 | fixed | The documented command now uses --okf and names all four registries. End-to-end enforcement defects are separately recorded as FND-005/FND-006. |
| FND-003 | fixed | The architecture module is now declared and pinned, and its exact revision is installed in the tested wdYewofH environment. Registry compatibility is a separate FND-006 defect. |
| FND-004 | fixed | The malformed declaration-relation fixture is removed; authored edge constraints are tested against the generated frontmatter schema, with frontmatter as their single source. |
| FND-005 | fixed | Conflict prose is a supported string literal; the complete skeleton and missing-Conflict checks pass on the locked Python engine. |
| FND-006 | fixed | The guide now runs semantic document validation before bundle/link checks; full five-module positive commands pass and missing decided_by is rejected. Completeness uses filtered named relation reports and documents strict-mode limitations. |

## Disposition pass 1

**FAIL; mergeable=no** at 72a77f466e11d03a94b060f5911d146f24cfdadd. Original findings were fixed, but three newly exposed defects remain unresolved.

Read the retained locked-build focused log `/tmp/plat-1914-safety-pin-focused.log`: 13 passed, 8 failed in 7.76 seconds. Failures comprise one malformed resolved-state fixture, two Conflict-extraction/skeleton failures, and five CLI edge/completeness/acceptance failures. The older initial suggestion that the observed skeleton failure was missing relations is superseded by the concrete log: semantic.feature-not-extractable at Conflict is the first actual failure.

Independent confined probes reproduced the Conflict failure through Quire Python 0.62.2, isolated the invalid PART-001 schema target and its qualified-ID correction, observed open and missing-person CLI cases returning exit 0 without required findings, and exposed the precise incompatible registry diagnostic via `quire relations --flow --json`. No source files or tests were modified.

Checked all diffs since the original review, including both copied original SR files. Independent schema generation drift check passes (42 schemas); Ruff, Black and diff whitespace checks pass. The full suite remains red and no merge readiness is implied.

Dependency comparison: ISO old resolved revision 9342304894c8473539b64acd959024e551bccf0e to new 54519e4523c01c52d2c99c08dc0bd4b70793a8e8 (confirmed merge of ISO #78). `git diff --name-status` contains five added review artifacts and changes to FR-004, spec/tests.md, manifest and vocabulary tests. Public data changes are conflicts_with, resolves/resolved_by, and soup_requirement_for allowance on FR/NFR. Repository searches find uses of the tension verbs in the manifest/spec/tests/docs and no use of the SOUP additions. Focused tension tests in the retained log cover the referenced items and fail as stated; no local SOUP tests apply. New architecture revision df01e2430759452fdea23ef95cd7e251976719c3 has no previous local dependency revision to compare. Installed distribution direct_url metadata matches both exact Git pins.

Runtime evidence uses Python 3.13.11/pytest 9.1.1/Quire Python 0.62.2 in `/home/peter/.cache/pypoetry/virtualenvs/spec-objects-safety-wdYewofH-py3.13`; CLI `/home/peter/.npm-global/bin/quire` reports 0.52.0 (engine 0.62.2). Authoring/matrix tool remains explicit Quoin 0.37.0.

Fixed excerpt FND-001:

```text
  decided_by?: PersonName;
```

Fixed excerpt FND-002:

```text
quire validate --okf \
  --module /path/to/spec-artifacts-iso \
  --module /path/to/spec-objects-security \
  --module /path/to/spec-objects-safety \
  --module /path/to/spec-objects-architecture \
  /path/to/corpus
```

Fixed excerpt FND-003:

```text
spec-objects-architecture = {git = "https://github.com/agent-ix/spec-objects-architecture.git", rev = "df01e2430759452fdea23ef95cd7e251976719c3"}
```

## Disposition pass 2

**PASS; mergeable=yes** at aaa299b7a58ea1b7392fd42e4a6fbc789426360e. FND-001 through FND-006 all have a latest fixed outcome. No new findings. Reviewed the complete delta from 72a77f466e11d03a94b060f5911d146f24cfdadd through the paused intermediate revisions and final two trace-only cleanup commits.

The generated frontmatter schema owns authored relationships once; no duplicate relationship table remains. All 45 generated schemas match TypeSpec. The invalid PART-001 declaration-relation fixture is replaced by valid frontmatter tests. The Conflict literal validates. All new/changed tension test markers were audited together: unrelated tags were removed from generic manifest shape and link-rule tests, and the disposition-only test no longer claims relationship-count evidence. Correct dedicated tests retain those criteria. Current examined bindings follow below.

Independent checks and exact limits:

- Quire Python 0.62.2: all four focused unit files passed 36 cases in 4.64 seconds. Environment 0OLJw7sv had stale ISO 0.25.0; the corrected engine-compatibility run explicitly used the exact pinned ISO provider from wdYewofH (54519e4523c01c52d2c99c08dc0bd4b70793a8e8). The initial two vocabulary failures in the stale environment are not product findings. No installed package or product files were modified.
- Quire Python 0.63.2 / CLI 0.53.2, engine 0.63.2: selected schema, three manifest checks, semantic/skeleton and integration files passed 35 cases (27 unit + 8 integration). This is the reviewer's actual selection count, distinct from the coder's 37-unit selection. The later commits remove trace tags only; coder additionally reports the schema module 7/7 and two affected manifest tests 2/2 through locked-build.
- Exact documented five-package commands independently replayed using regfinish-matrix package roots for ISO/business/security/architecture and this safety package. Semantic document validation exits 0 with no warnings; bundle validation exits 0; named relation JSON reports TEN-001 covered. An accepted-by-person negative control omitting decided_by exits 3 and names the missing field. Raw probe summary is retained at /tmp/reviewsafety52/final-doc-probe.txt.
- The guide now explains strict-mode empty/not-tracked behavior and tells readers to inspect coverage states for tension-only gating. Thus valid closed populations are not promised a strict-mode success they cannot attain.
- Schema freshness (45), Ruff, Black and diff whitespace checks pass. No broad full-suite run is claimed. The source runtime and semantic lock remain Quire Python 0.62.2; newer CLI evidence is explicitly versioned. Exact installed ISO/architecture revisions were checked in the previous pass and have not moved again.

The inherited repository matrix gap is separately deferred in SR-425 to the broader PLAT-1914 follow-up under the lead's explicit routing decision. Repository-wide gap freedom is not claimed by this scoped code PASS.

```yaml
bindings:
- test_id: test_no_verb_outside_the_declared_iso_vocabulary
  ac_id: FR-402-CON-1
  trace: correct
- test_id: test_no_verb_outside_the_declared_iso_vocabulary
  ac_id: FR-402-AC-5
  trace: correct
- test_id: test_tension_links_and_completeness_rules_are_manifest_data
  ac_id: FR-404-AC-6
  trace: correct
- test_id: test_the_semantic_block_carries_the_eight_admitted_keys_and_two_exports
  ac_id: FR-401-AC-1
  trace: correct
- test_id: test_tension_skeleton_validates_but_requires_its_conflict_section
  ac_id: FR-401-AC-5
  trace: correct
- test_id: test_manifest_exports_the_emitted_tension_schema
  ac_id: FR-401-AC-1
  trace: correct
- test_id: test_tension_accepts_each_disposition
  ac_id: FR-401-AC-2
  trace: correct
- test_id: test_tension_frontmatter_requires_two_conflicts_and_refuses_open_resolution
  ac_id: FR-402-AC-1
  trace: correct
- test_id: test_tension_frontmatter_requires_two_conflicts_and_refuses_open_resolution
  ac_id: FR-403-AC-5
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
- test_id: test_nonaccepted_tensions_refuse_deciders
  ac_id: FR-403-AC-4
  trace: correct
- test_id: test_tension_rejects_undeclared_links_with_a_named_diagnostic
  ac_id: FR-402-AC-2
  trace: correct
- test_id: test_open_tension_with_resolution_edge_fails_frontmatter_schema
  ac_id: FR-403-AC-5
  trace: correct
- test_id: test_resolved_by_design_edge_to_a_part_clears_the_tension_finding
  ac_id: FR-402-AC-3
  trace: correct
- test_id: test_resolved_by_design_edge_to_a_part_clears_the_tension_finding
  ac_id: FR-404-AC-3
  trace: correct
- test_id: test_open_tension_is_reported_as_uncovered
  ac_id: FR-404-AC-1
  trace: correct
- test_id: test_open_tension_is_reported_as_uncovered
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

Fixed excerpt FND-004:

```text
    resolved = dict(tension_record, status="resolved-by-design")
    assert valid(validator, resolved)
```

Fixed excerpt FND-005:

```text
`One requirement requires immediate processing. The other requires a bounded resource limit; the same operation cannot satisfy both readings.`
```

Fixed excerpt FND-006:

```text
quire validate --scope /path/to/corpus \
  --module /path/to/spec-artifacts-iso/spec_artifacts_iso \
  --module /path/to/spec-objects-safety/spec_objects_safety \
  --module /path/to/spec-objects-business/spec_objects_business \
  --module /path/to/spec-objects-security/spec_objects_security \
  --module /path/to/spec-objects-architecture/spec_objects_architecture \
  'spec/**/*.md'
```
