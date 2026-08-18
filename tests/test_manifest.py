"""Manifest shape + the FR-035 module-manifest gate.

The gate ships **with** this module rather than being retrofitted. Five sibling
`spec-objects-*` repositories and `spec-artifacts-app` do not run it, so a new
key in any of them ships unvalidated — and in `spec-objects-security` that let
two lexicon definitions be silently truncated by unquoted commas inside YAML
flow mappings for who knows how long (agent-ix/spec-objects-security#6, #8).
"""

from __future__ import annotations

import pathlib

import yaml
from jsonschema import Draft202012Validator
from spec_artifacts_iso import module_manifest_schema

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_safety"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
SKELETONS_DIR = PKG_ROOT / "skeletons"

OBJECT_TYPES = ["hazard", "failure_mode"]


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def test_manifest_loads() -> None:
    manifest = _manifest()
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-objects-safety"
    assert manifest["version"]
    assert isinstance(manifest.get("object_types", []), list)


def test_manifest_validates_against_fr035_schema() -> None:
    """The manifest validates against the FR-035 module-manifest schema.

    No skip and no escape hatch. Both were deleted upstream for cause: a
    `pytest.skip` when the schema could not be found reported this gate green
    while running nothing (agent-ix/spec-artifacts-iso#15). The schema is
    package data on `spec-artifacts-iso`, imported rather than copied, so there
    is one source and no branch on which this can quietly not run.
    """
    errors = list(
        Draft202012Validator(module_manifest_schema()).iter_errors(_manifest())
    )
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]


def test_object_types_are_well_formed() -> None:
    types = {t["name"]: t for t in _manifest()["object_types"]}
    assert sorted(types) == sorted(OBJECT_TYPES)
    for name, entry in types.items():
        assert entry.get("data_schema"), f"{name}: declares a data_schema"
        assert entry.get("roles"), f"{name}: declares at least one role"


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


def test_every_object_type_ships_a_skeleton() -> None:
    for name in OBJECT_TYPES:
        assert (SKELETONS_DIR / f"{name}.md").is_file(), f"{name}: ships a skeleton"


def test_skeleton_headings_match_the_declared_contract() -> None:
    """Each skeleton supplies exactly the sections its contract requires.

    The FR-002 I1/I2 parity property: a skeleton that drifts from its contract
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
