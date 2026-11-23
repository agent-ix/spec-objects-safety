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

# Each placeholder, with the table (the locator key the engine names) and the
# column it sits in.
CELLS = {
    "<what the plan covers>": ("scope", "Scope"),
    "<responsibility>": ("responsibilities", "Responsibility"),
    "<person or role>": ("responsibilities", "Assigned to"),
    "<planned verification method>": ("control_verification", "Method"),
    "<the controls it verifies>": ("control_verification", "Applies to"),
    "<production or post-production activity>": (
        "production_post_production",
        "Activity",
    ),
    "<how it is carried out>": ("production_post_production", "Method"),
}
TABLES = sorted({table for table, _ in CELLS.values()})
FORBIDDEN = ("score", "class", "accept", "approv")


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
@pytest.mark.parametrize("placeholder", sorted(CELLS))
def test_a_placeholder_in_any_cell_fails_naming_the_table_and_column(
    quire_engine, placeholder
):
    table, column = CELLS[placeholder]
    text = filled().replace(FILL[placeholder], placeholder, 1)
    result = validate_text(quire_engine, text)
    assert not result["is_valid"], placeholder
    assert any(
        f"'{table}'" in e["message"] and f"column '{column}'" in e["message"]
        for e in result["errors"]
    ), result["errors"]


@pytest.mark.trace("FR-108-AC-7")
@pytest.mark.parametrize(
    "placeholder",
    [
        "<what the plan covers>",
        "<responsibility>",
        "<planned verification method>",
        "<production or post-production activity>",
    ],
)
def test_a_table_with_no_row_fails_naming_the_table(quire_engine, placeholder):
    table, _ = CELLS[placeholder]
    text = skeleton()
    for key, value in FILL.items():
        text = text.replace(key, value)
    row = next(line for line in text.splitlines() if FILL[placeholder] in line)
    result = validate_text(quire_engine, text.replace(row + "\n", "", 1))
    assert not result["is_valid"]
    assert any(
        f"'{table}'" in e["message"] and "0 data row(s)" in e["message"]
        for e in result["errors"]
    ), result["errors"]
    assert any(
        f"required '{table}'" in e["message"] and "is empty" in e["message"]
        for e in result["errors"]
    ), result["errors"]


def _mentions(names) -> list[str]:
    return [n for n in names if any(word in n.lower() for word in FORBIDDEN)]


@pytest.mark.trace("FR-108-AC-6")
def test_the_plan_declares_no_score_class_acceptability_or_approval():
    schema = schema_of("RiskManagementPlan")
    assert not _mentions(schema["properties"])
    assert schema["additionalProperties"] is False
    assert any(
        path.name == "RiskManagementPlan.json" for path in shipped_schema_paths()
    )

    # The manifest block: no locator key and no table column states one.
    plan = locators(object_type(TYPE))
    assert not _mentions(plan)
    columns = [
        column
        for locator in plan.values()
        for column in (locator.get("assert") or {}).get("columns", [])
    ]
    assert columns, "the plan locators declare no columns"
    assert not _mentions(columns)

    # The skeleton, outside its authoring comment and its invariant clauses:
    # no heading and no table cell in a header or Field column names one.
    body = skeleton().split("-->", 1)[1].split("## Invariants", 1)[0]
    headings = [h[3:] for h in body.splitlines() if h.startswith("## ")]
    headers = [
        cell.strip()
        for line, nxt in zip(body.splitlines(), body.splitlines()[1:])
        if line.startswith("|") and nxt.startswith(("| -", "|--"))
        for cell in line.strip("|").split("|")
    ]
    properties = body.split("## Properties", 1)[1]
    fields = [
        line.strip("|").split("|")[0].strip()
        for line in properties.splitlines()
        if line.startswith("|") and not line.startswith(("| Field", "|--", "| -"))
    ]
    assert headings and headers and fields
    assert not _mentions(headings + headers + fields)

    # No shipped plan document except the unfilled skeleton.
    plans = [
        path.relative_to(PACKAGE_ROOT)
        for path in PACKAGE_ROOT.rglob("*.md")
        if f"type: {TYPE}\n" in path.read_text()
    ]
    assert plans == [SKELETONS_DIR.relative_to(PACKAGE_ROOT) / f"{TYPE}.md"]
