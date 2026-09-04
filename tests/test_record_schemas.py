"""Record-schema tests (FR 004): what each object type's schema requires,
forbids and refuses, and the epistemic distinctions the safety domain needs.

**These are schema evidence, not extraction evidence.** Quire 0.46.0 populates a
declaration record's `fields`, `clauses`, `operations` and `relations` only; the
module-specific keys (`assessment`, `context`, `analysis`, `status`,
`provenance`, `evidence`) have no published Markdown mapping yet
(`agent-ix/quoin#335`), so every record below is hand-built. When the mapping
lands these same records become extracted ones and the assertions do not change.
"""

from __future__ import annotations

import copy
import json

import pytest

from tests.conftest import (
    EPISTEMIC,
    MODEL_OF,
    SCALES,
    SEMANTIC_CORE_BASE,
    SEMANTIC_CORE_DIR,
    schema_of,
    shipped_schema_paths,
)

RECORD_MODELS = ("Hazard", "FailureMode")

# The seal the emitter writes for `...Record<never>`: no key outside the
# declared properties survives. Named once so a test can say what it looked for.
SEAL = {"not": {}}


def valid(validator, record) -> bool:
    return validator.is_valid(record)


def identity_field(name: str) -> dict:
    return {
        "name": name,
        "type": {"target": "UUID", "multiplicity": {"lower": 1, "upper": 1}},
        "identity": True,
    }


def plain_field(name: str) -> dict:
    return {
        "name": name,
        "type": {"target": "String", "multiplicity": {"lower": 1, "upper": 1}},
    }


ASSESSMENT = {
    "severity": "critical",
    "likelihood": "remote",
    "rationale": "Loss of commanded deceleration injures occupants.",
}

ANALYSIS = {
    "effect": "Commanded deceleration is not applied.",
    "cause": "The publish task starves.",
    "detection": "direct",
}

PROVENANCE = {
    "assertedBy": "safety-board",
    "assertedAt": "2026-09-04T00:00:00Z",
}


@pytest.mark.trace("TC-035", "FR-004-AC-1")
def test_the_two_record_schemas_differ_and_neither_is_type_object_only():
    hazard, failure_mode = schema_of("Hazard"), schema_of("FailureMode")
    assert set(hazard["properties"]) != set(failure_mode["properties"])
    assert "assessment" in hazard["properties"]
    assert "assessment" not in failure_mode["properties"]
    assert "context" in hazard["properties"]
    assert "context" not in failure_mode["properties"]
    assert "analysis" in failure_mode["properties"]
    assert "analysis" not in hazard["properties"]
    for name, schema in (("Hazard", hazard), ("FailureMode", failure_mode)):
        assert schema["required"] == ["fields"], name
        assert schema["properties"]["fields"]["minItems"] == 1, name
        assert "contains" in schema["properties"]["fields"], name
        assert schema["unevaluatedProperties"] == SEAL, name
        assert set(schema) > {"type"}, name


@pytest.mark.trace("TC-036", "FR-004-AC-2")
def test_hazard_requires_at_least_one_identity_field(schema_registry, hazard_record):
    validator = schema_registry("Hazard")
    assert valid(validator, hazard_record)

    without_flag = copy.deepcopy(hazard_record)
    del without_flag["fields"][0]["identity"]
    assert not valid(validator, without_flag)

    assert not valid(validator, {})
    assert not valid(validator, {"fields": []})


@pytest.mark.trace("TC-037", "FR-004-AC-3")
def test_failure_mode_requires_identity_and_forbids_the_hazard_only_keys(
    schema_registry, failure_mode_record
):
    validator = schema_registry("FailureMode")
    assert valid(validator, failure_mode_record)

    without_flag = copy.deepcopy(failure_mode_record)
    del without_flag["fields"][0]["identity"]
    assert not valid(validator, without_flag)

    for key, value in (
        ("assessment", ASSESSMENT),
        ("context", {"situation": "on a public road"}),
        ("operations", []),
    ):
        record = dict(failure_mode_record, **{key: value})
        assert not valid(validator, record), f"FailureMode admitted `{key}`"


@pytest.mark.trace("TC-038", "FR-004-AC-4")
def test_hazard_forbids_the_failure_mode_only_keys(schema_registry, hazard_record):
    validator = schema_registry("Hazard")
    for key, value in (("analysis", ANALYSIS), ("operations", [])):
        record = dict(hazard_record, **{key: value})
        assert not valid(validator, record), f"Hazard admitted `{key}`"


@pytest.mark.trace("TC-039", "FR-004-AC-5")
def test_an_assessment_is_whole_or_refused_and_not_assessed_is_not_negligible(
    schema_registry,
):
    validator = schema_registry("HazardAssessment")
    assert valid(validator, ASSESSMENT)

    for missing in ("severity", "likelihood", "rationale"):
        partial = {k: v for k, v in ASSESSMENT.items() if k != missing}
        assert not valid(validator, partial), f"an assessment without {missing} passed"

    assert not valid(validator, dict(ASSESSMENT, rationale=""))

    unassessed = dict(ASSESSMENT, severity="not_assessed")
    assert valid(validator, unassessed)
    # The point of the whole exercise: the two records are both valid and are
    # different documents. Nothing in the schema turns the first into the second.
    assert unassessed != dict(ASSESSMENT, severity="negligible")


@pytest.mark.trace("TC-040", "FR-004-AC-6")
def test_every_scored_axis_admits_its_scale_and_the_epistemic_states(schema_registry):
    """Exhaustive over the finite domain: every scale member, every epistemic
    member, and every foreign scale's members, on every axis."""
    axis_model = {
        "severity": "Severity",
        "likelihood": "Likelihood",
        "exposure": "Exposure",
        "controllability": "Controllability",
    }
    assessment = schema_registry("HazardAssessment")
    analysis = schema_registry("FailureAnalysis")

    for axis, model in axis_model.items():
        for member in SCALES[model] + EPISTEMIC:
            assert valid(assessment, dict(ASSESSMENT, **{axis: member})), (axis, member)
        foreign = [
            m for other, members in SCALES.items() if other != model for m in members
        ]
        for member in foreign:
            if member in SCALES[model]:
                continue
            assert not valid(assessment, dict(ASSESSMENT, **{axis: member})), (
                axis,
                member,
            )

    for member in SCALES["Detection"] + EPISTEMIC:
        assert valid(analysis, dict(ANALYSIS, detection=member)), member
    for member in SCALES["Severity"]:
        assert not valid(analysis, dict(ANALYSIS, detection=member)), member

    # No ordinal scale shares a member with the epistemic states, so no consumer
    # can sort "nobody looked" into an ordering with "negligible".
    for model, members in SCALES.items():
        assert not set(members) & set(EPISTEMIC), model
        assert schema_of(model)["enum"] == members, model
    assert schema_of("EpistemicState")["enum"] == EPISTEMIC


@pytest.mark.trace("TC-041", "FR-004-AC-7")
def test_no_schema_declares_a_default_a_controls_key_or_a_mitigations_key():
    for path in shipped_schema_paths():
        text = path.read_text()
        schema = json.loads(text)

        def walk(node, where):
            if isinstance(node, dict):
                assert "default" not in node, f"{path.name}: default at {where}"
                for key, value in node.items():
                    walk(value, f"{where}/{key}")
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    walk(item, f"{where}/{index}")

        walk(schema, "")
        for forbidden in ("controls", "mitigations"):
            assert forbidden not in (schema.get("properties") or {}), (
                f"{path.name} declares `{forbidden}`; the mitigation edge is "
                "authored from the requirement's end"
            )


@pytest.mark.trace("TC-042", "FR-004-AC-8")
def test_accepted_status_requires_provenance(
    schema_registry, hazard_record, failure_mode_record
):
    for model, base in (
        ("Hazard", hazard_record),
        ("FailureMode", failure_mode_record),
    ):
        validator = schema_registry(model)
        assert not valid(validator, dict(base, status="accepted")), model
        assert valid(
            validator, dict(base, status="accepted", provenance=PROVENANCE)
        ), model
        # Only acceptance carries the obligation; the other states do not.
        assert valid(validator, dict(base, status="identified")), model
        assert not valid(
            validator, dict(base, status="accepted", provenance={"assertedBy": "x"})
        ), f"{model}: provenance without assertedAt passed"


@pytest.mark.trace("TC-043", "FR-004-AC-9")
def test_a_hazard_with_no_declared_cause_is_a_valid_record(
    schema_registry, hazard_record
):
    """The STPA case. A hazard that arises from no failure mode is the record
    this module exists to keep, so `relations` carries no minimum."""
    validator = schema_registry("Hazard")
    assert "relations" not in schema_of("Hazard")["required"]
    assert "minItems" not in schema_of("Hazard")["properties"]["relations"]
    assert "contains" not in schema_of("Hazard")["properties"]["relations"]

    assert valid(validator, hazard_record)
    with_cause = dict(
        hazard_record,
        relations=[
            {
                "verb": "arises_from",
                "category": "dependency",
                "target": "ix://agent-ix/spec-objects-safety/FM-001",
            }
        ],
    )
    assert valid(validator, with_cause)


@pytest.mark.trace("TC-044", "FR-004-AC-10", "FR-004-CON-1")
def test_no_module_schema_redeclares_a_semantic_core_model():
    core = {path.stem for path in SEMANTIC_CORE_DIR.glob("*.json")}
    mine = {path.stem for path in shipped_schema_paths()}
    assert core, "semantic-core is not installed"
    assert not (core & mine), f"redeclared semantic-core models: {sorted(core & mine)}"

    grammar_refs = 0
    for path in shipped_schema_paths():
        for ref in json.dumps(json.loads(path.read_text())).split('"$ref": "')[1:]:
            target = ref.split('"')[0]
            if target.startswith(SEMANTIC_CORE_BASE):
                grammar_refs += 1
                assert target.rsplit("/", 1)[-1].removesuffix(".json") in core, target
    assert grammar_refs > 0, "no grammar item is referenced from semantic-core at all"


@pytest.mark.trace("TC-045", "FR-004-AC-11")
def test_undetectable_and_unassessed_detection_are_different_records(schema_registry):
    validator = schema_registry("FailureAnalysis")
    undetectable = dict(ANALYSIS, detection="none")
    unassessed = dict(ANALYSIS, detection="not_assessed")
    assert valid(validator, undetectable)
    assert valid(validator, unassessed)
    assert undetectable != unassessed
    assert "none" in schema_of("Detection")["enum"]
    assert "none" not in schema_of("EpistemicState")["enum"]


@pytest.mark.trace("TC-046", "FR-004-CON-2")
def test_schema_validity_is_not_a_safety_claim(schema_registry, hazard_record):
    """A record that validates says nothing the document did not say.

    Validation is a shape check. The three facts that would turn it into a
    safety claim — a score, a lifecycle status, an acceptance — are absent from
    a minimal record before validation and absent after it, because no schema in
    this module declares a `default` for any of them.
    """
    validator = schema_registry("Hazard")
    before = copy.deepcopy(hazard_record)
    assert valid(validator, hazard_record)
    assert hazard_record == before
    for key in ("assessment", "status", "provenance", "evidence"):
        assert key not in hazard_record
        assert "default" not in schema_of("Hazard")["properties"][key]


@pytest.mark.trace("TC-047", "FR-004-CON-3")
def test_no_declared_constraint_was_relaxed_to_make_a_fixture_pass():
    """The required/forbidden facts of every model, asserted as a table.

    Relaxing one constraint to make a stubborn fixture pass is the failure this
    guards: every relaxation shows up here as a diff, not as a green run.
    """
    expected_required = {
        "Hazard": ["fields"],
        "FailureMode": ["fields"],
        "HazardAssessment": ["severity", "likelihood", "rationale"],
        "FailureAnalysis": ["effect", "cause", "detection"],
        "HazardContext": ["situation"],
        "Provenance": ["assertedBy", "assertedAt"],
        "EvidenceRef": ["target"],
        "IdentityField": ["identity"],
    }
    for model, required in expected_required.items():
        assert schema_of(model)["required"] == required, model

    # Every object model is sealed, and both records carry the acceptance rule.
    for model in RECORD_MODELS + (
        "HazardAssessment",
        "FailureAnalysis",
        "HazardContext",
        "Provenance",
        "EvidenceRef",
    ):
        assert schema_of(model)["unevaluatedProperties"] == SEAL, model
    for model in RECORD_MODELS:
        rule = schema_of(model)["allOf"][0]
        assert rule["if"]["properties"]["status"]["const"] == "accepted", model
        assert rule["then"]["required"] == ["provenance"], model

    # Non-empty text stays non-empty.
    assert schema_of("HazardAssessment")["properties"]["rationale"]["minLength"] == 1
    for key in ("effect", "cause"):
        assert schema_of("FailureAnalysis")["properties"][key]["minLength"] == 1
    assert schema_of("Hazard")["properties"]["fields"]["minItems"] == 1
    assert schema_of("FailureMode")["properties"]["fields"]["minItems"] == 1
    assert MODEL_OF == {"hazard": "Hazard", "failure_mode": "FailureMode"}
