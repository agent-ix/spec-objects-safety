"""The risk management review object type (FR-109): its skeleton, its schema and
its document-level refusals.

Document assertions run filled copies of the shipped skeleton through the
engine, as `test_risk_management_plan.py` does. The references to the plan and
the overall evaluation are edges; their allowed targets and completeness
relations are in `tests_integration/test_risk_chain_edges.py`.
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

TYPE = "risk_management_review"

FILL = {
    "<person who reviewed>": "A. Reviewer",
    "<yes, partly or no>": "yes",
    "<ready or not_ready>": "ready",
    "<the reviewer's statement>": "The plan was carried out.",
}
COLUMNS = {
    "<person who reviewed>": "Reviewer",
    "<yes, partly or no>": "Plan executed",
    "<ready or not_ready>": "Post-production readiness",
    "<the reviewer's statement>": "Statement",
}
FORBIDDEN = ("score", "class", "accept", "approv")


def skeleton() -> str:
    return (SKELETONS_DIR / f"{TYPE}.md").read_text()


def filled(**overrides) -> str:
    text = skeleton()
    for placeholder, value in {**FILL, **overrides}.items():
        assert placeholder in text, placeholder
        text = text.replace(placeholder, value)
    return text


def validate_text(quire_engine, text):
    return quire_engine.validate_document(TYPE, str(PACKAGE_ROOT), text)


@pytest.mark.trace("FR-109-AC-1")
def test_the_review_type_is_declared_with_its_row_and_allowed_references():
    manifest = load_manifest()
    assert object_type(TYPE)["data_schema"] == {
        "schema": "schemas/RiskManagementReview.json"
    }
    assert TYPE in manifest["semantic"]["exports"]
    review = locators(object_type(TYPE))["review"]
    assert review["required"] is True
    assert review["assert"]["columns"] == list(COLUMNS.values())
    assert review["assert"]["min_rows"] == 1
    assert review["assert"]["max_rows"] == 1
    assert object_type(TYPE)["allowed_links"] == {
        "reviews": ["risk_management_plan"],
        "references": ["overall_residual_risk_evaluation"],
    }


@pytest.mark.trace("FR-109-AC-2")
def test_the_filled_skeleton_validates_and_the_shipped_skeleton_fails(quire_engine):
    result = validate_text(quire_engine, filled())
    assert result["is_valid"], result["errors"]
    assert not validate_text(quire_engine, skeleton())["is_valid"]


@pytest.mark.trace("FR-109-AC-3")
@pytest.mark.parametrize("placeholder", sorted(COLUMNS))
def test_a_placeholder_in_any_cell_fails_naming_the_table_and_column(
    quire_engine, placeholder
):
    column = COLUMNS[placeholder]
    result = validate_text(quire_engine, filled(**{placeholder: placeholder}))
    assert not result["is_valid"], placeholder
    assert any(
        "'review'" in e["message"] and f"column '{column}'" in e["message"]
        for e in result["errors"]
    ), result["errors"]


@pytest.mark.trace("FR-109-AC-4")
@pytest.mark.parametrize(
    ("placeholder", "column", "value"),
    [
        ("<yes, partly or no>", "Plan executed", "mostly"),
        ("<ready or not_ready>", "Post-production readiness", "accepted"),
    ],
)
def test_a_value_outside_the_closed_set_fails_naming_the_column(
    quire_engine, placeholder, column, value
):
    result = validate_text(quire_engine, filled(**{placeholder: value}))
    assert not result["is_valid"], value
    assert any(
        "'review'" in e["message"] and f"column '{column}'" in e["message"]
        for e in result["errors"]
    ), result["errors"]


def _mentions(names) -> list[str]:
    return [n for n in names if any(word in n.lower() for word in FORBIDDEN)]


@pytest.mark.trace("FR-109-AC-7")
def test_the_review_declares_no_score_class_acceptability_or_approval():
    schema = schema_of("RiskManagementReview")
    assert not _mentions(schema["properties"])
    assert schema["additionalProperties"] is False
    assert any(
        path.name == "RiskManagementReview.json" for path in shipped_schema_paths()
    )

    review = locators(object_type(TYPE))
    assert not _mentions(review)
    columns = [
        column
        for locator in review.values()
        for column in (locator.get("assert") or {}).get("columns", [])
    ]
    assert columns, "the review locators declare no columns"
    assert not _mentions(columns)

    # The skeleton, outside its authoring comment and its invariant clauses:
    # no heading, table header or Field cell names one. Cell values such as
    # `partly` are the reviewer's own entries and are not checked here.
    body = skeleton().split("-->", 1)[1].split("## Invariants", 1)[0]
    lines = body.splitlines()
    headings = [h[3:] for h in lines if h.startswith("## ")]
    headers = [
        cell.strip()
        for line, nxt in zip(lines, lines[1:])
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

    reviews = [
        path.relative_to(PACKAGE_ROOT)
        for path in PACKAGE_ROOT.rglob("*.md")
        if f"type: {TYPE}\n" in path.read_text()
    ]
    assert reviews == [SKELETONS_DIR.relative_to(PACKAGE_ROOT) / f"{TYPE}.md"]
