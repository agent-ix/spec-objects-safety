"""Cross-module reference tests (FR 006): what this module points at and the
types it declares.

The safety domain overlaps four neighbours — security (control, risk, asset),
architecture (interface, external contract), operational (incident, runbook) and
assurance (evidence records). Every overlap is a chance to mint a second copy of
someone else's type, and a second copy of a control is a control that drifts out
of step with the one being audited.
"""

from __future__ import annotations

import json
import pathlib

import pytest
import yaml

from tests.conftest import (
    OBJECT_TYPES,
    PENDING_ISO_VERBS,
    load_manifest,
    object_types,
    schema_of,
    shipped_schema_paths,
)


@pytest.mark.trace("TC-060", "FR-006-AC-1")
def test_the_module_declares_exactly_its_object_types():
    declared = {ot["name"] for ot in object_types()}
    assert declared == set(OBJECT_TYPES)


@pytest.mark.trace("TC-061", "FR-006-AC-2")
def test_the_only_cross_module_reference_shape_is_a_semantic_id():
    """A control is named, never restated.

    The mitigation edge is authored from the requirement's end, so no record key
    lists it. Everything this module does point outwards at — an evidence record,
    a causal edge's target — is a `SemanticId`, which resolves to whoever owns
    the thing rather than copying it.
    """
    for path in shipped_schema_paths():
        schema = json.loads(path.read_text())
        properties = schema.get("properties") or {}
        for forbidden in ("controls", "mitigations"):
            assert forbidden not in properties, f"{path.name} declares `{forbidden}`"

    evidence = schema_of("EvidenceRef")
    assert evidence["required"] == ["target"]
    assert evidence["properties"]["target"]["$ref"].endswith("SemanticId.json")
    # `kind` stays open on purpose: the closed evidence-kind vocabulary belongs
    # to engineering-assurance, and minting one here would be a fifth copy.
    assert evidence["properties"]["kind"]["type"] == "string"
    assert "enum" not in evidence["properties"]["kind"]

    for model in ("Hazard", "FailureMode"):
        relations = schema_of(model)["properties"]["relations"]["items"]
        assert relations["$ref"].endswith("RelationDecl.json"), model


@pytest.mark.trace("TC-063", "FR-006-AC-4", "StR-001-VC-2")
def test_every_verb_this_module_uses_exists_in_the_iso_vocabulary():
    import spec_artifacts_iso

    iso_path = (
        pathlib.Path(spec_artifacts_iso.__file__).resolve().parent / "manifest.yaml"
    )
    iso = yaml.safe_load(iso_path.read_text())
    edge_types = iso.get("edge_types") or {}
    # Inverse labels are authorable without being forward keys, so they count as
    # declared too. `mitigates` is not one of them — it is a forward key with no
    # `inverse:` facet — but `part_of` and its siblings are, so the union is what
    # "declared" means here.
    vocabulary = set(edge_types) | {
        entry["inverse"] for entry in edge_types.values() if entry.get("inverse")
    }
    assert vocabulary, "the iso module declares no edge vocabulary"

    manifest = load_manifest()
    used = {
        verb
        for ot in manifest["object_types"]
        for verb in (ot.get("allowed_links") or {})
    }
    for relation in manifest["traceability"]["required_relations"]:
        used |= set(relation["edges"])
    used |= set(manifest["traceability"]["acyclic_edges"])

    unknown = sorted(used - vocabulary - PENDING_ISO_VERBS)
    assert not unknown, f"verbs outside the iso vocabulary: {unknown}"


@pytest.mark.trace("TC-109", "FR-006-AC-4")
def test_pending_iso_verbs_are_registered_locally_until_migration():
    """Pending shared verbs still need entries for a composed edge registry."""
    manifest = load_manifest()
    local_edge_types = manifest.get("edge_types") or {}
    assert PENDING_ISO_VERBS <= set(local_edge_types), sorted(
        PENDING_ISO_VERBS - set(local_edge_types)
    )


@pytest.mark.trace("TC-064", "FR-006-CON-1")
def test_no_safety_only_synonym_is_minted():
    """The finding the module was founded on, kept true.

    The ticket that created this module assumed `causes` and `contributes_to`
    would be added to the shared vocabulary. Applying that vocabulary's own
    criterion — a near-synonym is a reason not to add — said use the existing
    `arises_from` instead. This test fails if the migration quietly reintroduced
    either word, in an edge, a schema key or a lexicon entry.
    """
    manifest = load_manifest()
    synonyms = {"causes", "contributes_to", "caused_by", "contributes"}
    used = {
        verb
        for ot in manifest["object_types"]
        for verb in (ot.get("allowed_links") or {})
    }
    assert not used & synonyms, sorted(used & synonyms)

    for path in shipped_schema_paths():
        properties = (json.loads(path.read_text()).get("properties") or {}).keys()
        assert not set(properties) & synonyms, path.name

    # And the causal edge still has exactly one home: the hazard end.
    hazard_links = next(
        ot for ot in manifest["object_types"] if ot["name"] == "hazard"
    )["allowed_links"]
    failure_links = next(
        ot for ot in manifest["object_types"] if ot["name"] == "failure_mode"
    )["allowed_links"]
    assert "arises_from" in hazard_links
    assert "arises_from" not in failure_links


# ── FR-010: causes beyond failure modes ─────────────────────────────────────


def _links(name: str) -> dict:
    return next(ot for ot in object_types() if ot["name"] == name)["allowed_links"]


@pytest.mark.trace("TC-110", "FR-010-AC-1")
def test_a_hazard_may_arise_from_every_cause_type():
    assert _links("hazard")["arises_from"] == [
        "failure_mode",
        "soup_record",
        "threat",
        "vulnerability",
        "control",
    ]


@pytest.mark.trace("TC-111", "FR-010-AC-2")
def test_a_failure_mode_may_reference_the_part_it_sits_in():
    assert set(_links("failure_mode")["references"]) == {
        "failure_mode",
        "hazard",
        "systems-part",
    }


@pytest.mark.trace("TC-112", "FR-010-AC-3", "FR-010-AC-4")
def test_causes_are_referenced_not_declared_and_no_verb_is_added():
    foreign = {"soup_record", "threat", "vulnerability", "control", "part"}
    assert not foreign & {ot["name"] for ot in object_types()}
    assert "arises_from" not in _links("failure_mode")
    assert load_manifest()["traceability"]["acyclic_edges"] == ["arises_from"]
    assert set(_links("hazard")) == {"arises_from", "references"}
    assert set(_links("failure_mode")) == {"references"}


@pytest.mark.trace("TC-115", "FR-010-AC-6")
def test_no_required_relation_obliges_a_hazard_to_have_a_cause():
    relations = load_manifest()["traceability"]["required_relations"]
    assert [
        r["name"]
        for r in relations
        if r["from"] == "hazard"
        and "arises_from" in r["edges"]
        and r["direction"] == "outgoing"
    ] == []


@pytest.mark.trace("TC-116", "FR-010-AC-7")
def test_no_hazard_or_failure_mode_key_scores_a_cause():
    scored = ("cause", "severity", "likelihood", "probab", "accept")
    for name in ("Hazard", "FailureMode"):
        keys = set(schema_of(name)["properties"]) - {"assessment"}
        assert not [k for k in keys if any(w in k.lower() for w in scored)], name
