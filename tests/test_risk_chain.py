"""The risk-chain object types: harm, hazardous situation and risk estimate
(FR-201..FR-205), their skeletons, their negative fixtures and their mappings.

Record assertions are over hand-built records for the module-specific keys, the
same way `test_record_schemas.py` does it: Quire populates only `fields`,
`clauses`, `operations` and `relations`. Document assertions run the shipped
skeletons and fixtures through the engine.
"""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    EPISTEMIC,
    NEGATIVE_DIR,
    PACKAGE_ROOT,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
    locators,
    object_type,
    schema_of,
    shipped_schema_paths,
)

IDENTITY = {
    "name": "id",
    "type": {
        "target": {"kind": "KernelScalar", "value": "UUID"},
        "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
    },
    "identity": True,
}
BASE = {"fields": [IDENTITY]}
PROVENANCE = {"assertedBy": "A. Person", "assertedAt": "2026-11-12T00:00:00Z"}
JUDGEMENT = {
    "phase": "pre_control",
    "severity": "critical",
    "probability": "remote",
    "rationale": "Injury is likely but survivable.",
    "provenance": PROVENANCE,
}


def valid(validator, record) -> bool:
    return validator.is_valid(record)


def validate_text(quire_engine, type_name, text):
    return quire_engine.validate_document(type_name, str(PACKAGE_ROOT), text)


def filled_estimate(phase="pre_control") -> str:
    text = (SKELETONS_DIR / "risk_estimate.md").read_text()
    for placeholder, value in (
        ("<pre_control | post_control>", phase),
        ("<severity>", "critical"),
        ("<probability>", "remote"),
        ("<why this person judges it so>", "Survivable injury."),
        ("<person>", "A. Person"),
        ("<date or UTC timestamp>", "2026-11-12"),
    ):
        text = text.replace(placeholder, value)
    return text


# ── FR-201: harm ────────────────────────────────────────────────────────────


@pytest.mark.trace("FR-201-AC-1")
def test_harm_is_declared_exported_and_emitted():
    manifest = load_manifest()
    assert object_type("harm")["data_schema"] == {"schema": "schemas/Harm.json"}
    assert "harm" in manifest["semantic"]["exports"]
    assert (PACKAGE_ROOT / "schemas" / "Harm.json").is_file()


@pytest.mark.trace("FR-201-AC-2")
def test_harm_skeleton_validates_and_fails_without_its_description(quire_engine):
    text = (SKELETONS_DIR / "harm.md").read_text()
    assert validate_text(quire_engine, "harm", text)["is_valid"]

    without = re.sub(
        r"## Description\n\n.*?\n\n(?=## Properties)", "", text, flags=re.S
    )
    result = validate_text(quire_engine, "harm", without)
    assert not result["is_valid"]
    assert any("required 'description'" in e["message"] for e in result["errors"])


@pytest.mark.trace("FR-201-AC-3")
@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("severity", "critical"),
        ("probability", "remote"),
        ("score", 3),
        ("status", "accepted"),
        ("acceptance", {"by": "A. Person"}),
    ],
)
def test_harm_forbids_judgement_and_status_keys(schema_registry, key, value):
    validator = schema_registry("Harm")
    assert valid(validator, BASE)
    assert not valid(validator, dict(BASE, **{key: value}))


@pytest.mark.trace("FR-201-AC-4")
def test_harm_admits_a_provenance_naming_a_person(schema_registry):
    assert valid(schema_registry("Harm"), dict(BASE, provenance=PROVENANCE))


@pytest.mark.trace("FR-201-AC-5", "FR-202-AC-5")
def test_existing_hazard_and_failure_mode_documents_still_validate(
    quire_engine, schema_registry
):
    for name in ("hazard", "failure_mode"):
        text = (SKELETONS_DIR / f"{name}.md").read_text()
        assert validate_text(quire_engine, name, text)["is_valid"], name
    # A hazard carrying only the free `context.situation` string is unchanged.
    assert valid(
        schema_registry("Hazard"), dict(BASE, context={"situation": "on a motorway"})
    )


# ── FR-202: hazardous situation and the chain edges ─────────────────────────


@pytest.mark.trace("FR-202-AC-4")
@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("severity", "critical"),
        ("probability", "remote"),
        ("score", 3),
        ("acceptance", {"by": "A. Person"}),
    ],
)
def test_hazardous_situation_forbids_judgement_keys(schema_registry, key, value):
    validator = schema_registry("HazardousSituation")
    assert valid(validator, BASE)
    assert not valid(validator, dict(BASE, **{key: value}))


@pytest.mark.trace("FR-202-AC-10", "FR-203-AC-13", "FR-201-AC-1")
def test_lexicon_and_types_hold_the_chain_words():
    manifest = load_manifest()
    lexicon = manifest["lexicon"]
    assert "hazardous situation" in lexicon
    assert "probability" in lexicon
    assert "harm" in lexicon
    assert "risk" not in {ot["name"] for ot in manifest["object_types"]}
    assert "hazardous_situation" in manifest["semantic"]["exports"]
    assert "risk_estimate" in manifest["semantic"]["exports"]


@pytest.mark.trace("FR-202-AC-3", "FR-203-AC-8")
def test_each_chain_edge_is_allowed_to_exactly_its_target_type():
    links = {
        ot["name"]: ot.get("allowed_links", {})
        for ot in load_manifest()["object_types"]
    }
    assert links["hazardous_situation"] == {"arises_from": ["hazard"]}
    assert links["harm"] == {"arises_from": ["hazardous_situation"]}
    assert links["risk_estimate"] == {
        "estimates": ["hazardous_situation"],
        "assumes": ["control"],
    }
    # The effect end authors each fact; the cause end lists nothing.
    assert "hazardous_situation" not in links["hazard"].get("arises_from", [])


@pytest.mark.trace("FR-205-AC-6")
def test_no_completeness_relation_is_declared_over_control_without_a_scope():
    relations = load_manifest()["traceability"]["required_relations"]
    assert not [r for r in relations if r["from"] == "control" and "when_any" not in r]


@pytest.mark.trace("FR-202-AC-6", "FR-301-AC-10")
def test_each_completeness_check_is_declared_by_exactly_one_relation():
    relations = load_manifest()["traceability"]["required_relations"]
    checks = [r["check"] for r in relations]
    assert len(checks) == len(set(checks))
    assert "situation-without-hazard" in checks


@pytest.mark.trace("FR-202-AC-9")
def test_arises_from_stays_acyclic_across_the_whole_chain():
    assert "arises_from" in load_manifest()["traceability"]["acyclic_edges"]


def test_hazardous_situation_skeleton_validates_and_needs_a_description(quire_engine):
    text = (SKELETONS_DIR / "hazardous_situation.md").read_text()
    assert validate_text(quire_engine, "hazardous_situation", text)["is_valid"]
    without = re.sub(
        r"## Description\n\n.*?\n\n(?=## Properties)", "", text, flags=re.S
    )
    assert not validate_text(quire_engine, "hazardous_situation", without)["is_valid"]


# ── FR-203 / FR-204: risk estimate ──────────────────────────────────────────


@pytest.mark.trace("FR-203-AC-1")
def test_a_complete_pre_control_judgement_validates(schema_registry):
    validator = schema_registry("RiskEstimate")
    assert valid(validator, dict(BASE, estimate=JUDGEMENT))
    assert valid(schema_registry("EstimateJudgement"), JUDGEMENT)
    assert valid(
        schema_registry("EstimateJudgement"), dict(JUDGEMENT, phase="post_control")
    )


@pytest.mark.trace("FR-203-AC-2")
@pytest.mark.parametrize(
    "missing", ["phase", "severity", "probability", "rationale", "provenance"]
)
def test_each_judgement_member_is_required(schema_registry, missing):
    partial = {k: v for k, v in JUDGEMENT.items() if k != missing}
    assert not valid(schema_registry("EstimateJudgement"), partial)
    assert not valid(schema_registry("RiskEstimate"), dict(BASE, estimate=partial))


@pytest.mark.trace("FR-203-AC-2")
def test_provenance_requires_who_and_when(schema_registry):
    validator = schema_registry("EstimateJudgement")
    for missing in ("assertedBy", "assertedAt"):
        provenance = {k: v for k, v in PROVENANCE.items() if k != missing}
        assert not valid(validator, dict(JUDGEMENT, provenance=provenance))


@pytest.mark.trace("FR-203-AC-3", "FR-203-AC-14")
def test_markers_validate_through_the_marker_branch_only(schema_registry):
    judgement = schema_registry("EstimateJudgement")
    text_branch = schema_registry("EstimateLevelText")
    marker_branch = schema_registry("EpistemicState")
    for marker in EPISTEMIC:
        assert valid(judgement, dict(JUDGEMENT, severity=marker, probability=marker))
        assert not valid(text_branch, marker)
        assert valid(marker_branch, marker)
    assert set(schema_of("EstimateLevelText")["not"]["enum"]) == set(EPISTEMIC)


@pytest.mark.trace("FR-203-AC-4")
def test_any_non_empty_level_text_validates_and_empty_fails(schema_registry):
    judgement = schema_registry("EstimateJudgement")
    assert valid(judgement, dict(JUDGEMENT, severity="S4-major", probability="P2"))
    assert not valid(judgement, dict(JUDGEMENT, severity=""))
    assert not valid(judgement, dict(JUDGEMENT, probability=""))
    assert not valid(judgement, dict(JUDGEMENT, rationale=""))
    # The hazard scales constrain nothing on an estimate.
    assert "enum" not in schema_of("EstimateLevelText")


@pytest.mark.trace("FR-203-AC-5")
@pytest.mark.parametrize(
    "key", ["score", "region", "level", "acceptable", "acceptance"]
)
def test_an_estimate_forbids_a_score_region_or_acceptance(schema_registry, key):
    assert not valid(schema_registry("EstimateJudgement"), dict(JUDGEMENT, **{key: 1}))
    assert not valid(
        schema_registry("RiskEstimate"), dict(BASE, estimate=JUDGEMENT, **{key: 1})
    )


@pytest.mark.trace("FR-203-AC-6")
def test_phase_is_a_top_level_frontmatter_key_and_not_body_extracted():
    assert (
        locators(object_type("risk_estimate"))["phase"]["from"] == "frontmatter_field"
    )
    assert "phase" in frontmatter((SKELETONS_DIR / "risk_estimate.md").read_text())
    for path in sorted(NEGATIVE_DIR.glob("risk_estimate-*.md")):
        text = path.read_text()
        if path.stem != "risk_estimate-no-phase":
            assert "phase" in frontmatter(text), path.name


@pytest.mark.trace("FR-203-AC-7")
def test_the_shipped_estimate_skeleton_fails_until_a_person_fills_it(quire_engine):
    text = (SKELETONS_DIR / "risk_estimate.md").read_text()
    result = validate_text(quire_engine, "risk_estimate", text)
    assert not result["is_valid"]
    messages = " ".join(e["message"] for e in result["errors"])
    for part in ("'phase'", "Severity", "Probability", "Rationale", "Asserted by"):
        assert part in messages, part


@pytest.mark.trace("FR-203-AC-1", "FR-204-AC-5")
@pytest.mark.parametrize("phase", ["pre_control", "post_control"])
def test_a_filled_estimate_validates_in_either_phase(quire_engine, phase):
    result = validate_text(quire_engine, "risk_estimate", filled_estimate(phase))
    assert result["is_valid"], result["errors"]


@pytest.mark.trace("FR-203-AC-2")
@pytest.mark.parametrize(
    ("label", "old", "new"),
    [
        ("severity", "| critical |", "|  |"),
        ("probability", "| remote |", "|  |"),
        ("rationale", "| Survivable injury. |", "|  |"),
        ("asserted-by", "| A. Person |", "|  |"),
        ("asserted-at", "| 2026-11-12 |", "|  |"),
        ("phase", "phase: pre_control\n", ""),
    ],
)
def test_an_absent_value_fails_validation_at_the_document(
    quire_engine, label, old, new
):
    text = filled_estimate()
    assert old in text, label
    assert not validate_text(quire_engine, "risk_estimate", text.replace(old, new, 1))[
        "is_valid"
    ], label


@pytest.mark.trace("FR-203-AC-3")
def test_markers_are_accepted_at_the_document(quire_engine):
    for marker in EPISTEMIC:
        text = filled_estimate().replace("| critical |", f"| {marker} |")
        assert validate_text(quire_engine, "risk_estimate", text)["is_valid"], marker


# ── FR-205: nothing stores a verdict ────────────────────────────────────────


@pytest.mark.trace("FR-205-AC-5")
def test_no_manifest_or_schema_key_stores_a_verdict():
    banned = {"effective", "verified", "passed"}

    def keys(node):
        if isinstance(node, dict):
            for key, value in node.items():
                yield key
                yield from keys(value)
        elif isinstance(node, list):
            for item in node:
                yield from keys(item)

    assert not banned & set(keys(load_manifest()))
    for path in shipped_schema_paths():
        assert not banned & set(keys(json.loads(path.read_text()))), path.name


# ── negative fixtures ───────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "path",
    sorted(
        p
        for prefix in ("harm", "hazardous_situation", "risk_estimate")
        for p in NEGATIVE_DIR.glob(f"{prefix}-*.md")
    ),
    ids=lambda p: p.stem,
)
def test_each_risk_chain_negative_fixture_fails_for_its_stated_reason(
    quire_engine, path
):
    text = path.read_text()
    front = frontmatter(text)
    result = validate_text(quire_engine, front["type"], text)
    assert not result["is_valid"]
    assert any(front["expect"] in e["message"] for e in result["errors"]), (
        path.name,
        [e["message"] for e in result["errors"]],
    )
