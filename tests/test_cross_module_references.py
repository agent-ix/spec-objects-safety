"""Cross-module reference tests (FR 006): what this module points at and what
it refuses to redeclare.

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
    MANIFEST_PATH,
    OBJECT_TYPES,
    load_manifest,
    object_types,
    schema_of,
    shipped_schema_paths,
)

# The neighbouring packages whose types this module must not redeclare. The
# TYPE NAMES ARE READ FROM THEIR INSTALLED MANIFESTS, never copied: a hand-kept
# list of someone else's declarations is stale the day the neighbour adds a
# type, and it goes stale silently — the boundary test keeps passing while the
# boundary it describes has moved. `spec-objects-security` alone declares 23
# types and is being migrated concurrently.
NEIGHBOUR_PACKAGES = (
    "spec-objects-security",
    "spec-objects-architecture",
    "spec-objects-operational",
)

MODULE_CATALOG = pathlib.Path.home() / ".ix" / "filament" / "modules"


def neighbour_types() -> dict[str, set[str]]:
    """Every object type the neighbouring modules declare, read from the catalog."""
    owned: dict[str, set[str]] = {}
    for package in NEIGHBOUR_PACKAGES:
        manifest = MODULE_CATALOG / package / "manifest.yaml"
        if not manifest.is_file():
            pytest.fail(
                f"{package} is not installed at {MODULE_CATALOG}, so the "
                "anti-duplication boundary cannot be measured against what it "
                "actually declares. Install the module catalog "
                "(`quoin module install`) rather than hand-copying its type names."
            )
        declared = yaml.safe_load(manifest.read_text()).get("object_types") or []
        owned[package] = {entry["name"] for entry in declared}
    return owned


# The open migration tickets that keep `semantic.imports` empty: a package with
# no semantic contract cannot be pinned at a semantic version.
OPEN_MIGRATIONS = (
    "agent-ix/spec-objects-security#13",
    "agent-ix/spec-objects-architecture#8",
    "agent-ix/spec-objects-operational#6",
)


@pytest.mark.trace("TC-060", "FR-006-AC-1")
def test_the_module_declares_two_types_and_none_a_neighbour_owns():
    declared = {ot["name"] for ot in object_types()}
    assert declared == set(OBJECT_TYPES)
    owned_by = neighbour_types()
    assert all(owned_by.values()), "a neighbouring module declares no object type"
    for package, owned in owned_by.items():
        clash = declared & owned
        assert (
            not clash
        ), f"{sorted(clash)} is {package}'s to declare, not this module's"


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


@pytest.mark.trace("TC-062", "FR-006-AC-3", "FR-006-CON-2")
def test_imports_is_empty_and_the_manifest_says_which_issues_keep_it_empty():
    """An empty pin map with a reason beats an aspirational one.

    `semantic.imports` pins imported semantic *packages* at exact versions. None
    of the neighbours has published a semantic contract, so any version written
    here would be a claim about a contract that does not exist.
    """
    assert load_manifest()["semantic"]["imports"] == {}
    text = MANIFEST_PATH.read_text()
    for issue in OPEN_MIGRATIONS:
        assert issue in text, f"the manifest does not name {issue}"


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

    unknown = sorted(used - vocabulary)
    assert not unknown, f"verbs outside the iso vocabulary: {unknown}"


@pytest.mark.trace("TC-064", "FR-006-CON-1")
def test_no_safety_only_synonym_is_minted():
    """The finding the module was founded on, kept true at 0.3.0.

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
