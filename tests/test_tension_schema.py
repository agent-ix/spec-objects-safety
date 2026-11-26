"""Behavior checks for the authored tension record (FR-401..FR-403)."""

from __future__ import annotations

import copy

import pytest

from tests.conftest import MANIFEST_PATH, object_types, schema_of
from tests.test_record_schemas import valid


@pytest.mark.trace("FR-401-AC-1")
def test_manifest_exports_the_emitted_tension_schema():
    import yaml

    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    entry = next(item for item in manifest["object_types"] if item["name"] == "tension")
    assert "tension" in manifest["semantic"]["exports"]
    assert entry["data_schema"]["schema"] == "schemas/Tension.json"
    assert entry["frontmatter_schema_ref"] == "schemas/TensionFrontmatter.json"
    assert schema_of("Tension")["$id"].endswith("/Tension.json")
    assert schema_of("TensionFrontmatter")["$id"].endswith("/TensionFrontmatter.json")


@pytest.mark.trace("FR-401-AC-2")
def test_tension_accepts_each_disposition(schema_registry, tension_record):
    validator = schema_registry("Tension")
    assert valid(validator, tension_record)

    resolved = dict(tension_record, status="resolved-by-design")
    assert valid(validator, resolved)

    accepted = copy.deepcopy(tension_record)
    accepted.update(status="accepted-by-person", decided_by="A. Person")
    assert valid(validator, accepted)

    for status in ("unknown", "accepted", "resolved"):
        invalid_status = dict(tension_record, status=status)
        assert not valid(validator, invalid_status), status


@pytest.mark.trace("FR-402-AC-1", "FR-403-AC-5")
def test_tension_frontmatter_requires_two_conflicts_and_refuses_open_resolution(
    schema_registry,
):
    validator = schema_registry("TensionFrontmatter")
    frontmatter = {
        "status": "open",
        "relationships": [
            {"target": "ix://agent-ix/quoin/FR-020", "type": "conflicts_with"},
            {"target": "ix://agent-ix/quire-rs/NFR-008", "type": "conflicts_with"},
        ],
    }
    assert valid(validator, frontmatter)

    one_conflict = dict(frontmatter, relationships=frontmatter["relationships"][:1])
    assert not valid(validator, one_conflict)

    open_with_resolution = copy.deepcopy(frontmatter)
    open_with_resolution["relationships"].append(
        {
            "target": "ix://agent-ix/spec-objects-architecture/PART-001",
            "type": "resolved_by",
        }
    )
    assert not valid(validator, open_with_resolution)

    resolved = copy.deepcopy(frontmatter)
    resolved["status"] = "resolved-by-design"
    resolved["relationships"].append(
        {
            "target": "ix://agent-ix/spec-objects-architecture/PART-001",
            "type": "resolved_by",
        }
    )
    assert valid(validator, resolved)

    accepted = dict(frontmatter, status="accepted-by-person", decided_by="A. Person")
    assert valid(validator, accepted)

    unknown_edge = copy.deepcopy(frontmatter)
    unknown_edge["relationships"][0]["type"] = "references"
    assert not valid(validator, unknown_edge)


@pytest.mark.trace("FR-401-AC-3")
def test_tension_requires_an_explicit_status(schema_registry, tension_record):
    validator = schema_registry("Tension")
    missing_status = copy.deepcopy(tension_record)
    del missing_status["status"]
    assert not valid(validator, missing_status)


@pytest.mark.trace("FR-401-AC-4", "FR-402-AC-4", "NFR-401-M-1")
def test_tension_schema_is_generic_and_has_no_computed_or_personal_metadata(
    schema_registry, tension_record
):
    schema = schema_of("Tension")
    properties = schema["properties"]
    assert not {"severity", "likelihood", "date", "history", "recorded_by"} & set(
        properties
    )
    assert "relations" not in properties
    person_named = {
        name
        for name in properties
        if "person" in name.lower() or "decider" in name.lower()
    }
    assert person_named <= {"decided_by"}
    assert "decided_by" in properties
    assert "default" not in properties["status"]
    assert "default" not in properties["decided_by"]
    assert not any(obj.get("name") == "person" for obj in object_types())

    validator = schema_registry("Tension")
    assert not valid(validator, dict(tension_record, severity="critical"))
    assert not valid(validator, dict(tension_record, likelihood="probable"))


@pytest.mark.trace("FR-403-AC-1", "FR-403-AC-2", "FR-403-AC-3")
def test_only_person_named_acceptance_is_valid(schema_registry, tension_record):
    validator = schema_registry("Tension")
    accepted = dict(tension_record, status="accepted-by-person", decided_by="A. Person")
    assert valid(validator, accepted)

    for decided_by in (None, "", "   ", "<person>"):
        candidate = copy.deepcopy(accepted)
        if decided_by is None:
            del candidate["decided_by"]
        else:
            candidate["decided_by"] = decided_by
        errors = list(validator.iter_errors(candidate))
        assert errors, decided_by
        if decided_by is None:
            assert any("decided_by" in error.message for error in errors)
        else:
            assert any(list(error.path) == ["decided_by"] for error in errors)


@pytest.mark.trace("FR-403-AC-4")
def test_nonaccepted_tensions_refuse_deciders(schema_registry, tension_record):
    validator = schema_registry("Tension")
    for status in ("open", "resolved-by-design"):
        candidate = dict(tension_record, status=status, decided_by="A. Person")
        assert not valid(validator, candidate), status
