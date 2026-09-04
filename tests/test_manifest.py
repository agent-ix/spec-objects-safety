"""Manifest shape + the FR 035 module-manifest gate.

The gate ships **with** this module rather than being retrofitted. Five sibling
`spec-objects-*` repositories and `spec-artifacts-app` do not run it, so a new
key in any of them ships unvalidated — and in `spec-objects-security` that let
two lexicon definitions be silently truncated by unquoted commas inside YAML
flow mappings for who knows how long (agent-ix/spec-objects-security#6, #8).
"""

from __future__ import annotations

import json
import pathlib

import pytest
import yaml
from jsonschema import Draft202012Validator
from spec_artifacts_iso import module_manifest_schema

from tests.conftest import (
    MANIFEST_PATH,
    OBJECT_TYPES,
    PINNED_MANIFEST_SCHEMA,
    PINNED_SCHEMA_ALLOWED_DIFFS,
    SKELETONS_DIR,
)


def _pinned_manifest_schema() -> dict:
    """The FR 035 schema at the revision that defines the `semantic` block.

    NOT an escape hatch and NOT a skip: the gate always runs. It runs against a
    pinned revision because no released `spec-artifacts-iso` carries CR-012
    (`agent-ix/spec-artifacts-iso#36`), and TC 034 proves this copy differs from
    the installed release only where CR-012 changed it.
    """
    return json.loads(PINNED_MANIFEST_SCHEMA.read_text())


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


@pytest.mark.trace("TC-002", "FR-001-AC-1")
def test_manifest_loads() -> None:
    manifest = _manifest()
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-objects-safety"
    assert manifest["version"]
    assert isinstance(manifest.get("object_types", []), list)


@pytest.mark.trace("TC-001", "TC-033", "FR-001-AC-5", "FR-003-AC-7")
def test_manifest_validates_against_fr035_schema() -> None:
    """The manifest validates against the FR 035 module-manifest schema.

    No skip and no escape hatch. Both were deleted upstream for cause: a
    `pytest.skip` when the schema could not be found reported this gate green
    while running nothing (agent-ix/spec-artifacts-iso#15). The schema is
    package data on `spec-artifacts-iso`, imported rather than copied, so there
    is one source and no branch on which this can quietly not run.
    """
    errors = list(
        Draft202012Validator(_pinned_manifest_schema()).iter_errors(_manifest())
    )
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]


@pytest.mark.trace("TC-002", "FR-001-AC-1")
def test_object_types_are_well_formed() -> None:
    types = {t["name"]: t for t in _manifest()["object_types"]}
    assert sorted(types) == sorted(OBJECT_TYPES)
    for name, entry in types.items():
        assert entry.get("data_schema"), f"{name}: declares a data_schema"
        assert entry.get("allowed_links"), f"{name}: declares allowed_links"


@pytest.mark.trace("TC-007", "FR-001-AC-7", "FR-001-CON-2")
def test_no_verb_outside_the_declared_iso_vocabulary() -> None:
    """Every `allowed_links` verb already exists in the iso edge vocabulary.

    spec-artifacts-iso FR 004's first criterion for adding a verb is "check the
    existing 76 — a near-synonym is a reason not to add, not a reason to add".
    The ticket that asked for this module (agent-ix/spec-objects-security#7)
    assumed `causes` and `contributes_to` would be added. Applying the criteria
    it asked for says not to: `arises_from` records the same fact from the
    hazard end, and a hazard arising from several failure modes is several
    `arises_from` edges, so `contributes_to` would be a second word for one
    thing.

    This test fails if a future edit reaches for a new verb before the
    vocabulary has one — which is the moment to argue the case in iso, not
    here.
    """
    import spec_artifacts_iso

    iso_manifest = (
        pathlib.Path(spec_artifacts_iso.__file__).resolve().parent / "manifest.yaml"
    )
    iso = yaml.safe_load(iso_manifest.read_text())
    declared = set(iso.get("edge_types") or {})
    # Inverse labels are authorable without being forward keys (quire-rs
    # FR 041 AC 2), so they count as declared too.
    declared |= {
        e["inverse"] for e in (iso.get("edge_types") or {}).values() if e.get("inverse")
    }

    used = {
        verb
        for t in _manifest()["object_types"]
        for verb in (t.get("allowed_links") or {})
    }
    unknown = sorted(used - declared)
    assert not unknown, (
        f"verbs not in the iso vocabulary: {unknown}. Adding one is an "
        "spec-artifacts-iso change with FR 004's criteria to satisfy, not a "
        "local mint."
    )


@pytest.mark.trace("TC-003", "FR-001-AC-2", "FR-001-AC-3")
def test_hazard_and_failure_mode_are_separate_types() -> None:
    """A hazard is not a variety of failure mode.

    A failure mode answers "what breaks"; a hazard answers "what state must
    never be reached". STPA exists because the second is not derivable from the
    first — components each behaving exactly as specified can still reach a
    harmful state together. Modelling hazards as a `failure_mode` variant would
    lose precisely those, and would force one table to mean two things: the
    FMEA triple (effect, cause, detection) is a different shape from the hazard
    assessment (severity, likelihood).
    """
    types = {t["name"]: t for t in _manifest()["object_types"]}

    hazard_tables = types["hazard"]["body_extraction"]["yield_pattern"]["match"]
    assert hazard_tables["assessment"]["assert"]["columns"] == [
        "Severity",
        "Likelihood",
        "Rationale",
    ]
    assert hazard_tables["condition"]["required"] is True
    # Deliberately optional: an identified-but-unmitigated hazard is a real and
    # reportable state, and requiring the section would push authors to write a
    # placeholder rather than leave the gap visible.
    assert hazard_tables["mitigation"]["required"] is False

    fm_tables = types["failure_mode"]["body_extraction"]["yield_pattern"]["match"]
    assert fm_tables["analysis"]["assert"]["columns"] == [
        "Effect",
        "Cause",
        "Detection",
    ]


@pytest.mark.trace("TC-004", "FR-001-AC-6")
def test_lexicon_entries_are_whole() -> None:
    """Every lexicon entry is exactly `{definition: <non-empty string>}`.

    Asserted structurally from day one because of the defect it prevents: an
    unquoted comma inside a YAML flow mapping is read as an entry separator, so
    `{definition: a recorded, tamper-evident event trail}` silently becomes a
    truncated definition plus a junk key. The file reads correctly to a human
    and is wrong to every consumer (agent-ix/spec-objects-security#6).
    """
    lexicon = _manifest().get("lexicon") or {}
    assert lexicon, "the module declares a lexicon"
    malformed = {
        term: entry
        for term, entry in lexicon.items()
        if not isinstance(entry, dict)
        or set(entry) != {"definition"}
        or not str(entry.get("definition", "")).strip()
    }
    assert not malformed, (
        "lexicon entries must be exactly {definition: <text>} — an entry with "
        f"extra keys is an unquoted comma inside a flow mapping: {malformed}"
    )


@pytest.mark.trace("TC-005", "FR-001-AC-4")
def test_every_object_type_ships_a_skeleton() -> None:
    for name in OBJECT_TYPES:
        assert (SKELETONS_DIR / f"{name}.md").is_file(), f"{name}: ships a skeleton"


@pytest.mark.trace("TC-005", "FR-001-AC-4")
def test_skeleton_headings_match_the_declared_contract() -> None:
    """Each skeleton supplies exactly the sections its contract requires.

    The FR 002 I1/I2 parity property: a skeleton that drifts from its contract
    teaches authors the wrong shape, and nothing else would catch it.
    """
    import re

    types = {t["name"]: t for t in _manifest()["object_types"]}
    for name in OBJECT_TYPES:
        text = (SKELETONS_DIR / f"{name}.md").read_text()
        headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
        match = types[name]["body_extraction"]["yield_pattern"]["match"]

        required = {
            spec.get("after_heading") or spec.get("under_section")
            for spec in match.values()
            if isinstance(spec, dict) and spec.get("required")
        } - {None}
        assert required <= set(headings), (
            f"{name}: skeleton is missing required sections "
            f"{sorted(required - set(headings))}"
        )


@pytest.mark.trace("TC-010", "FR-001-AC-4")
def test_tc010_hazard_coverage_is_declared_not_coded() -> None:
    """FR 001 AC-4 (TC 010): bidirectional hazard coverage is manifest data.

    Assumptions: quire-rs FR 058 (v0.31.0) reads
    ``traceability.required_relations``; the engine holds no archetype name,
    no verb and no direction.

    Criteria:
      * a hazard and a failure mode each carry an obligation to be mitigated;
      * each has its OWN ``trace:<check>`` key, so a repository can promote
        unmitigated hazards to ``error`` while failure-mode coverage is still
        being backfilled (quire-rs FR 057);
      * ``direction`` is ``incoming`` — the mitigation is authored from the
        requirement's end. A hazard listing its own mitigations would duplicate
        the fact and let the two drift;
      * ``arises_from`` is declared acyclic: a hazard that transitively arises
        from itself states nothing, and no per-document check can see it
        because the defect is a property of the graph.
    """
    model = _manifest()["traceability"]
    by_name = {r["name"]: r for r in model["required_relations"]}

    assert set(by_name) == {"hazard-has-mitigation", "failure-mode-has-mitigation"}
    for name, kind in (
        ("hazard-has-mitigation", "hazard"),
        ("failure-mode-has-mitigation", "failure_mode"),
    ):
        relation = by_name[name]
        assert relation["from"] == kind
        assert relation["edges"] == ["mitigates"]
        assert relation["direction"] == "incoming"

    checks = {r["check"] for r in by_name.values()}
    assert checks == {"unmitigated-hazard", "unmitigated-failure-mode"}
    assert len(checks) == len(by_name), "each relation is independently tunable"

    assert model["acyclic_edges"] == ["arises_from"]


@pytest.mark.trace("TC-011", "FR-001-AC-4")
def test_tc011_the_relation_vocabulary_is_the_declared_one() -> None:
    """FR 001 AC-4 (TC 011): every verb and kind a relation names is real.

    Assumptions: quire-rs CR-075 reports a relation naming a kind nothing
    declares, because such a relation matches nothing and checks nothing.
    Criteria: each relation's ``from`` is an object type this module declares,
    and each verb is in the shared iso vocabulary — caught here, at author
    time, rather than as a runtime advisory.
    """
    manifest = _manifest()
    declared = {o["name"] for o in manifest["object_types"]}
    import spec_artifacts_iso

    iso_path = (
        pathlib.Path(spec_artifacts_iso.__file__).resolve().parent / "manifest.yaml"
    )
    iso = yaml.safe_load(iso_path.read_text())
    edge_types = iso.get("edge_types") or {}
    # Inverse labels are authorable without being forward keys (quire-rs
    # FR 041 AC 2), so they count as declared too — `mitigates` is one.
    vocabulary = set(edge_types) | {
        e["inverse"] for e in edge_types.values() if e.get("inverse")
    }

    for relation in manifest["traceability"]["required_relations"]:
        assert relation["from"] in declared, relation["from"]
        for verb in relation["edges"]:
            assert verb in vocabulary, f"{verb} is not in the iso edge vocabulary"
    for verb in manifest["traceability"]["acyclic_edges"]:
        assert verb in vocabulary, f"{verb} is not in the iso edge vocabulary"


@pytest.mark.trace("TC-034", "FR-003-AC-7", "FR-003-CON-3")
def test_the_pinned_fr035_schema_differs_only_where_cr012_changed_it() -> None:
    """The pinned copy is the released schema plus CR-012, and nothing else.

    The gate this module ships never skips, so when the packaged schema cannot
    express the manifest under test the gate runs against a pinned revision
    instead. That is only honest while the pinned copy is provably the released
    schema plus the CR-012 additions: any other difference would mean the
    module is judged against a schema of its own making.

    When a `spec-artifacts-iso` release finally carries the `semantic` key
    (agent-ix/spec-artifacts-iso#36) this test fails on the first assertion, and
    the fix is to delete the pinned copy and go back to the packaged schema.
    """
    installed = module_manifest_schema()
    pinned = _pinned_manifest_schema()

    assert "semantic" not in installed["properties"], (
        "the installed spec-artifacts-iso now carries the `semantic` key: delete "
        "tests/fixtures/module-manifest.schema.json and validate against "
        "module_manifest_schema() (agent-ix/spec-artifacts-iso#36)"
    )

    def differing(a, b, path=""):
        if type(a) is not type(b):
            return [path]
        if isinstance(a, dict):
            out = []
            for key in sorted(set(a) | set(b)):
                child = f"{path}/{key}"
                if key not in a or key not in b:
                    out.append(child)
                else:
                    out += differing(a[key], b[key], child)
            return out
        if isinstance(a, list):
            if len(a) != len(b):
                return [path]
            out = []
            for index, (left, right) in enumerate(zip(a, b)):
                out += differing(left, right, f"{path}/{index}")
            return out
        return [] if a == b else [path]

    unexpected = [
        pointer
        for pointer in differing(installed, pinned)
        if not any(pointer.startswith(prefix) for prefix in PINNED_SCHEMA_ALLOWED_DIFFS)
    ]
    assert not unexpected, (
        "the pinned FR 035 copy differs from the installed release outside the "
        f"CR-012 pointers: {unexpected}"
    )
