"""The risk management plan object type (FR-108): its skeleton, its schema and
its document-level refusals.

Document assertions run filled copies of the shipped skeleton through the
engine, as `test_residual_risk.py` does. The reference to the acceptability
policy is an edge; its allowed target and its completeness relation are in
`tests_integration/test_risk_chain_edges.py`.
"""

from __future__ import annotations

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

TYPE = "risk_management_plan"

FILL = {
    "<what the plan covers>": "Brake controller, whole lifecycle.",
    "<responsibility>": "Keep the risk file current.",
    "<person or role>": "Safety lead",
    "<planned verification method>": "Test against the control requirements.",
    "<the controls it verifies>": "Every risk control.",
    "<production or post-production activity>": "Review field reports.",
    "<how it is carried out>": "Quarterly review by the safety lead.",
}

# The locator key the engine names in its diagnostic, and the placeholder that
# stands in the first cell of that table.
TABLES = {
    "scope": "<what the plan covers>",
    "responsibilities": "<responsibility>",
    "control_verification": "<planned verification method>",
    "production_post_production": "<production or post-production activity>",
}


def skeleton() -> str:
    return (SKELETONS_DIR / f"{TYPE}.md").read_text()


def filled() -> str:
    text = skeleton()
    for placeholder, value in FILL.items():
        assert placeholder in text, placeholder
        text = text.replace(placeholder, value)
    return text


def validate_text(quire_engine, text):
    return quire_engine.validate_document(TYPE, str(PACKAGE_ROOT), text)


@pytest.mark.trace("FR-108-AC-1")
def test_the_plan_type_is_declared_and_requires_its_four_tables():
    manifest = load_manifest()
    assert object_type(TYPE)["data_schema"] == {
        "schema": "schemas/RiskManagementPlan.json"
    }
    assert TYPE in manifest["semantic"]["exports"]
    plan = locators(object_type(TYPE))
    required = {name for name, loc in plan.items() if loc.get("required")}
    assert required >= {
        "scope",
        "responsibilities",
        "control_verification",
        "production_post_production",
    }
    assert object_type(TYPE)["allowed_links"] == {
        "references": ["acceptability_policy"]
    }


@pytest.mark.trace("FR-108-AC-2")
def test_the_filled_skeleton_validates_and_the_shipped_skeleton_fails(quire_engine):
    result = validate_text(quire_engine, filled())
    assert result["is_valid"], result["errors"]
    assert not validate_text(quire_engine, skeleton())["is_valid"]


@pytest.mark.trace("FR-108-AC-3")
@pytest.mark.parametrize("table", sorted(TABLES))
def test_a_placeholder_row_in_any_table_fails_naming_the_table(quire_engine, table):
    placeholder = TABLES[table]
    text = filled().replace(FILL[placeholder], placeholder, 1)
    result = validate_text(quire_engine, text)
    assert not result["is_valid"], table
    assert any(f"'{table}'" in e["message"] for e in result["errors"]), result["errors"]


@pytest.mark.trace("FR-108-AC-6")
def test_the_plan_declares_no_score_class_acceptability_or_approval():
    schema = schema_of("RiskManagementPlan")
    forbidden = ("score", "class", "accept", "approv")
    assert not [
        m for m in schema["properties"] if any(w in m.lower() for w in forbidden)
    ]
    assert schema["additionalProperties"] is False
    assert any(
        path.name == "RiskManagementPlan.json" for path in shipped_schema_paths()
    )
