"""Behavior checks for the authored tension record (FR-401..FR-403)."""

from __future__ import annotations

import copy

import pytest

from tests.conftest import object_types, schema_of
from tests.test_record_schemas import valid


def _relation(verb: str, target: str) -> dict[str, str]:
    return {"verb": verb, "category": "governance", "target": target}


@pytest.mark.trace("FR-401-AC-2", "FR-402-AC-1")
def test_tension_accepts_each_disposition_and_requires_two_conflict_edges(
    schema_registry, tension_record
):
    validator = schema_registry("Tension")
    assert valid(validator, tension_record)

    resolved = copy.deepcopy(tension_record)
    resolved.update(status="resolved-by-design")
    resolved["relations"].append(_relation("resolved_by", "PART-001"))
    assert valid(validator, resolved)

    accepted = copy.deepcopy(tension_record)
    accepted.update(status="accepted-by-person", decided_by="A. Person")
    assert valid(validator, accepted)

    for status in ("unknown", "accepted", "resolved"):
        invalid_status = dict(tension_record, status=status)
        assert not valid(validator, invalid_status), status

    one_conflict = copy.deepcopy(tension_record)
    one_conflict["relations"].pop()
    assert not valid(validator, one_conflict)


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
        assert not valid(validator, candidate), decided_by


@pytest.mark.trace("FR-403-AC-4", "FR-403-AC-5")
def test_nonaccepted_tensions_refuse_deciders_and_open_refuses_resolution_edges(
    schema_registry, tension_record
):
    validator = schema_registry("Tension")
    for status in ("open", "resolved-by-design"):
        candidate = dict(tension_record, status=status, decided_by="A. Person")
        assert not valid(validator, candidate), status

    open_with_resolution = copy.deepcopy(tension_record)
    open_with_resolution["relations"].append(_relation("resolved_by", "PART-001"))
    assert not valid(validator, open_with_resolution)

