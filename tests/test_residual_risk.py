"""The residual-risk object types: acceptability policy, residual risk,
benefit-risk and the overall evaluation (FR-101, FR-103, FR-104, FR-106,
FR-107), their skeletons and their negative fixtures.

Record assertions are over hand-built records for the module-specific keys, as
`test_risk_chain.py` does. Document assertions run filled copies of the shipped
skeletons through the engine. The cross-row rules of a policy, the checks of a
reference's far end, and the reports of FR-102, FR-105 and FR-107 are not here:
the engine's table assertions cannot state the first, a required relation
cannot test the second, and the third is the quoin report.
"""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    PACKAGE_ROOT,
    SKELETONS_DIR,
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

SEVERITIES = ["minor", "serious", "fatal"]
PROBABILITIES = ["rare", "possible", "likely"]
REGIONS = [
    {"name": "acceptable", "outside_acceptable": False},
    {"name": "reduce further", "outside_acceptable": True},
    {"name": "unacceptable", "outside_acceptable": True},
]
CELLS = [
    {"severity": s, "probability": p, "region": REGIONS[(i + j) // 2]["name"]}
    for i, s in enumerate(SEVERITIES)
    for j, p in enumerate(PROBABILITIES)
]
POLICY = {
    "severities": SEVERITIES,
    "probabilities": PROBABILITIES,
    "regions": REGIONS,
    "cells": CELLS,
}
ACCEPTED = {
    "decision": "accepted",
    "rationale": "Within policy.",
    "decided_by": "A. Person",
}
NOT_ACCEPTED = dict(ACCEPTED, decision="not_accepted")
UNDECIDED = {"decision": "undecided", "rationale": "Not yet reviewed."}


def valid(validator, record) -> bool:
    return validator.is_valid(record)


def validate_text(quire_engine, type_name, text):
    return quire_engine.validate_document(type_name, str(PACKAGE_ROOT), text)


def without(mapping, key):
    return {k: v for k, v in mapping.items() if k != key}


def skeleton(name) -> str:
    return (SKELETONS_DIR / f"{name}.md").read_text()


def filled(name, replacements) -> str:
    text = skeleton(name)
    for placeholder, value in replacements.items():
        assert placeholder in text, placeholder
        text = text.replace(placeholder, value)
    return text


DECISION_FILL = {
    "<undecided, accepted or not_accepted>": "accepted",
    "<why the person decided so>": "Within the policy.",
    "<person who decided, empty while undecided>": "A. Person",
}


def filled_policy() -> str:
    text = skeleton("acceptability_policy")
    levels = {
        "| <severity level> |\n\n## Probability": "\n".join(
            f"| {s} |" for s in SEVERITIES
        )
        + "\n\n## Probability",
        "| <probability level> |\n\n## Regions": "\n".join(
            f"| {p} |" for p in PROBABILITIES
        )
        + "\n\n## Regions",
        "| <region> | <true or false> |": "\n".join(
            f"| {r['name']} | {str(r['outside_acceptable']).lower()} |" for r in REGIONS
        ),
        "| <severity level> | <probability level> | <region> |": "\n".join(
            f"| {c['severity']} | {c['probability']} | {c['region']} |" for c in CELLS
        ),
    }
    for placeholder, value in levels.items():
        assert placeholder in text, placeholder
        text = text.replace(placeholder, value, 1)
    return text


def filled_residual_risk() -> str:
    return filled("residual_risk", DECISION_FILL)


def filled_benefit_risk() -> str:
    return filled(
        "benefit_risk",
        dict(
            DECISION_FILL,
            **{"<the benefit that justifies the residual risks>": "Faster braking."},
        ),
    )


def filled_evaluation() -> str:
    return filled(
        "overall_residual_risk_evaluation",
        dict(DECISION_FILL, **{"<product>": "Brake controller"}),
    )


FILLED = {
    "acceptability_policy": filled_policy,
    "residual_risk": filled_residual_risk,
    "benefit_risk": filled_benefit_risk,
    "overall_residual_risk_evaluation": filled_evaluation,
}


# ── FR-101: acceptability policy ────────────────────────────────────────────


@pytest.mark.trace("FR-101-AC-1")
def test_the_policy_type_is_declared_and_its_schema_requires_the_four_parts():
    manifest = load_manifest()
    assert object_type("acceptability_policy")["data_schema"] == {
        "schema": "schemas/AcceptabilityPolicy.json"
    }
    assert "acceptability_policy" in manifest["semantic"]["exports"]
    assert set(schema_of("PolicyTable")["required"]) == {
        "severities",
        "probabilities",
        "regions",
        "cells",
    }
    assert schema_of("PolicyRegion")["required"] == ["name", "outside_acceptable"]
    assert set(locators(object_type("acceptability_policy"))) >= {
        "severity_levels",
        "probability_levels",
        "regions",
        "cells",
    }


@pytest.mark.trace("FR-101-AC-2", "FR-101-AC-8")
def test_a_three_by_three_policy_with_two_regions_outside_validates(
    schema_registry, quire_engine
):
    assert valid(schema_registry("PolicyTable"), POLICY)
    assert valid(schema_registry("AcceptabilityPolicy"), dict(BASE, policy=POLICY))
    assert sum(r["outside_acceptable"] for r in REGIONS) == 2
    result = validate_text(quire_engine, "acceptability_policy", filled_policy())
    assert result["is_valid"], result["errors"]


@pytest.mark.trace("FR-101-AC-5")
@pytest.mark.parametrize("key", ["severities", "probabilities"])
def test_a_repeated_level_name_fails_naming_the_level(schema_registry, key):
    repeated = dict(POLICY, **{key: [POLICY[key][0]] * 2})
    errors = list(schema_registry("PolicyTable").iter_errors(repeated))
    assert errors
    assert POLICY[key][0] in errors[0].message


@pytest.mark.trace("FR-101-AC-1")
@pytest.mark.parametrize("key", ["severities", "probabilities", "regions", "cells"])
def test_each_part_of_the_policy_must_be_present_and_non_empty(schema_registry, key):
    table = schema_registry("PolicyTable")
    assert not valid(table, without(POLICY, key))
    assert not valid(table, dict(POLICY, **{key: []}))


@pytest.mark.trace("FR-101-AC-7")
def test_a_region_without_its_flag_fails_and_the_schema_has_no_default(
    schema_registry, quire_engine
):
    region = schema_registry("PolicyRegion")
    assert not valid(region, {"name": "unacceptable"})
    assert not valid(region, {"name": "unacceptable", "outside_acceptable": "yes"})
    assert (
        "default" not in schema_of("PolicyRegion")["properties"]["outside_acceptable"]
    )
    assert '"default"' not in json.dumps(schema_of("PolicyRegion"))

    text = filled_policy().replace("| unacceptable | true |", "| unacceptable |  |")
    result = validate_text(quire_engine, "acceptability_policy", text)
    assert not result["is_valid"]
    assert any("Outside acceptable" in e["message"] for e in result["errors"])


@pytest.mark.trace("FR-101-AC-6")
def test_the_policy_skeleton_fails_until_filled_and_no_policy_ships(quire_engine):
    result = validate_text(
        quire_engine, "acceptability_policy", skeleton("acceptability_policy")
    )
    assert not result["is_valid"]
    messages = " ".join(e["message"] for e in result["errors"])
    for part in ("Severity level", "Probability level", "Outside acceptable", "Region"):
        assert part in messages, part

    documents = [
        path
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".yaml", ".yml"}
        and re.search(r"^type: acceptability_policy$", path.read_text(), re.M)
    ]
    assert documents == [SKELETONS_DIR / "acceptability_policy.md"]


@pytest.mark.trace("FR-101-AC-6")
def test_a_blank_policy_cell_fails_at_the_document(quire_engine):
    text = filled_policy()
    first_cell = re.search(r"^\| minor \| rare \| (.+) \|$", text, re.M)
    assert first_cell
    blanked = text.replace(first_cell.group(0), "| minor | rare |  |")
    result = validate_text(quire_engine, "acceptability_policy", blanked)
    assert not result["is_valid"]
    assert any("Region" in e["message"] for e in result["errors"])


# ── FR-103 / FR-106 / FR-107: decisions ─────────────────────────────────────

DECISION_RECORDS = [
    ("ResidualRisk", "Determination", {}),
    ("BenefitRisk", "BenefitDetermination", {"benefit": "Faster braking."}),
    (
        "OverallResidualRiskEvaluation",
        "EvaluationDetermination",
        {"product": "Brake controller"},
    ),
]
DECISION_IDS = [name for name, _, _ in DECISION_RECORDS]


def record_with(schema_registry, record, determination, extra):
    return schema_registry(record).is_valid(
        dict(BASE, determination=dict(extra, **determination))
    )


@pytest.mark.parametrize(
    ("record", "_union", "extra"), DECISION_RECORDS, ids=DECISION_IDS
)
def test_accepted_not_accepted_and_undecided_all_validate(
    schema_registry, record, _union, extra
):
    for determination in (ACCEPTED, NOT_ACCEPTED, UNDECIDED):
        assert record_with(schema_registry, record, determination, extra), determination


@pytest.mark.parametrize(
    ("record", "_union", "extra"), DECISION_RECORDS, ids=DECISION_IDS
)
def test_a_decided_record_needs_a_named_decider_and_a_rationale(
    schema_registry, record, _union, extra
):
    for decided in (ACCEPTED, NOT_ACCEPTED):
        for missing in ("decided_by", "rationale"):
            assert not record_with(
                schema_registry, record, without(decided, missing), extra
            )
        for empty in ("decided_by", "rationale"):
            assert not record_with(
                schema_registry, record, dict(decided, **{empty: ""}), extra
            )
        for placeholder in ("<person>", "<why>"):
            for key in ("decided_by", "rationale"):
                assert not record_with(
                    schema_registry, record, dict(decided, **{key: placeholder}), extra
                )


@pytest.mark.parametrize(
    ("record", "_union", "extra"), DECISION_RECORDS, ids=DECISION_IDS
)
def test_an_undecided_record_refuses_a_decider(schema_registry, record, _union, extra):
    assert not record_with(
        schema_registry, record, dict(UNDECIDED, decided_by="A. Person"), extra
    )
    assert not record_with(
        schema_registry, record, without(UNDECIDED, "rationale"), extra
    )


@pytest.mark.trace("FR-103-AC-5")
@pytest.mark.parametrize(
    ("record", "_union", "extra"), DECISION_RECORDS, ids=DECISION_IDS
)
def test_a_decision_must_be_one_of_the_three_and_has_no_default(
    schema_registry, record, _union, extra
):
    for determination in (
        without(ACCEPTED, "decision"),
        dict(ACCEPTED, decision="approved"),
        dict(ACCEPTED, decision=""),
    ):
        assert not record_with(schema_registry, record, determination, extra)
    assert '"default"' not in json.dumps(schema_of(record))


NEW_MODELS = {
    "AcceptabilityPolicy",
    "PolicyTable",
    "PolicyRegion",
    "PolicyCell",
    "ResidualRisk",
    "Determination",
    "DecisionState",
    "BenefitRisk",
    "BenefitDetermination",
    "OverallResidualRiskEvaluation",
    "EvaluationDetermination",
}


@pytest.mark.trace("FR-103-AC-6", "FR-106-AC-5", "FR-107-AC-6", "FR-104-AC-3")
def test_no_schema_declares_a_score_region_ratio_total_date_or_history():
    banned = {
        "severity",
        "probability",
        "score",
        "region",
        "level",
        "acceptable",
        "acceptance",
        "ratio",
        "weight",
        "total",
        "date",
        "decided_at",
        "history",
        "timestamp",
    }
    for name in (
        "ResidualRisk",
        "Determination",
        "BenefitRisk",
        "BenefitDetermination",
        "OverallResidualRiskEvaluation",
        "EvaluationDetermination",
    ):
        properties = set(schema_of(name).get("properties", {}))
        assert not banned & properties, (name, banned & properties)
    for path in shipped_schema_paths():
        if path.stem in NEW_MODELS:
            assert '"default"' not in path.read_text(), path.name


@pytest.mark.trace("FR-103-AC-6", "FR-106-AC-5", "FR-107-AC-6")
@pytest.mark.parametrize(
    "key", ["score", "region", "ratio", "total", "date", "severity", "probability"]
)
@pytest.mark.parametrize(
    ("record", "_union", "extra"), DECISION_RECORDS, ids=DECISION_IDS
)
def test_a_decision_refuses_a_computed_or_dated_member(
    schema_registry, record, _union, extra, key
):
    assert not record_with(schema_registry, record, dict(ACCEPTED, **{key: 1}), extra)
    assert not schema_registry(record).is_valid(dict(BASE, **{key: 1}))


@pytest.mark.trace("FR-106-AC-2")
def test_a_benefit_risk_needs_a_non_empty_benefit_statement(schema_registry):
    for benefit in ("", "<the benefit>"):
        assert not record_with(
            schema_registry, "BenefitRisk", ACCEPTED, {"benefit": benefit}
        )
    assert not record_with(schema_registry, "BenefitRisk", ACCEPTED, {})


@pytest.mark.trace("FR-107-AC-8")
def test_an_evaluation_needs_a_non_empty_product(schema_registry):
    for product in ("", "<product>"):
        assert not record_with(
            schema_registry,
            "OverallResidualRiskEvaluation",
            ACCEPTED,
            {"product": product},
        )
    assert not record_with(
        schema_registry, "OverallResidualRiskEvaluation", ACCEPTED, {}
    )


# ── skeletons and filled documents ──────────────────────────────────────────


@pytest.mark.trace("FR-101-AC-6", "FR-103-AC-5")
@pytest.mark.parametrize("name", sorted(FILLED))
def test_each_shipped_skeleton_fails_as_shipped_and_its_filled_copy_validates(
    quire_engine, name
):
    shipped = validate_text(quire_engine, name, skeleton(name))
    assert not shipped["is_valid"], name
    result = validate_text(quire_engine, name, FILLED[name]())
    assert result["is_valid"], (name, result["errors"])


@pytest.mark.trace("FR-103-AC-1", "FR-103-AC-3", "FR-106-AC-1", "FR-107-AC-1")
@pytest.mark.parametrize("name", sorted(set(FILLED) - {"acceptability_policy"}))
@pytest.mark.parametrize("decision", ["accepted", "not_accepted"])
def test_a_decided_document_validates(quire_engine, name, decision):
    text = FILLED[name]().replace("| accepted |", f"| {decision} |")
    assert validate_text(quire_engine, name, text)["is_valid"]


@pytest.mark.trace("FR-103-AC-3", "FR-103-AC-5")
@pytest.mark.parametrize("name", sorted(set(FILLED) - {"acceptability_policy"}))
def test_an_undecided_document_validates_and_a_blank_or_unknown_decision_fails(
    quire_engine, name
):
    text = FILLED[name]()
    undecided = text.replace("| accepted |", "| undecided |").replace(
        "| A. Person |", "|  |"
    )
    assert validate_text(quire_engine, name, undecided)["is_valid"]
    for bad in ("", "approved"):
        result = validate_text(
            quire_engine, name, text.replace("| accepted |", f"| {bad} |")
        )
        assert not result["is_valid"], bad
        assert any("Decision" in e["message"] for e in result["errors"]), bad


@pytest.mark.trace("FR-103-AC-2", "FR-106-AC-3", "FR-107-AC-2")
@pytest.mark.parametrize("name", sorted(set(FILLED) - {"acceptability_policy"}))
@pytest.mark.parametrize("decision", ["accepted", "not_accepted"])
def test_a_decided_document_without_a_named_decider_fails(quire_engine, name, decision):
    text = FILLED[name]().replace("| accepted |", f"| {decision} |")
    for blank in ("|  |\n", "| <person> |\n"):
        result = validate_text(
            quire_engine, name, text.replace("| A. Person |\n", blank, 1)
        )
        assert not result["is_valid"], blank
        assert any(
            "decided_by" in e["message"] or "Decided by" in e["message"]
            for e in result["errors"]
        ), blank


@pytest.mark.trace("FR-103-AC-3", "FR-106-AC-3", "FR-107-AC-2")
@pytest.mark.parametrize("name", sorted(set(FILLED) - {"acceptability_policy"}))
def test_an_undecided_document_that_names_a_decider_fails(quire_engine, name):
    text = FILLED[name]().replace("| accepted |", "| undecided |")
    result = validate_text(quire_engine, name, text)
    assert not result["is_valid"]
    assert any("decided_by" in e["message"] for e in result["errors"])


@pytest.mark.trace("FR-106-AC-2", "FR-107-AC-8")
@pytest.mark.parametrize(
    ("name", "old", "label"),
    [
        ("benefit_risk", "| Faster braking. |", "benefit"),
        ("overall_residual_risk_evaluation", "| Brake controller |", "product"),
    ],
)
def test_an_empty_stated_value_fails_at_the_document(quire_engine, name, old, label):
    text = FILLED[name]()
    assert old in text
    result = validate_text(quire_engine, name, text.replace(old, "|  |", 1))
    assert not result["is_valid"], label


@pytest.mark.trace("FR-103-AC-2")
@pytest.mark.parametrize("name", sorted(set(FILLED) - {"acceptability_policy"}))
def test_an_empty_rationale_fails_at_the_document(quire_engine, name):
    text = FILLED[name]()
    result = validate_text(
        quire_engine, name, text.replace("| Within the policy. |", "|  |", 1)
    )
    assert not result["is_valid"]
