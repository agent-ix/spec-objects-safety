"""Additive-compatibility tests (NFR 001): what 0.3.0 promised not to change.

`compatibility_posture: additive` is a promise a consumer may rely on, and the
`traceability` model is read across a repository boundary by
`agent-ix/spec-objects-security`'s hazard-coverage work. Both are asserted here
against the 0.2.0 bytes, checked in under `tests/fixtures/baseline-0.2.0/`.
"""

from __future__ import annotations

import pytest

from tests.conftest import (
    BASELINE_DIR,
    PACKAGE_ROOT,
    baseline,
    frontmatter,
    load_manifest,
    locators,
    object_type,
)

LEGACY_SKELETONS = ("hazard.md", "failure_mode.md")


@pytest.mark.trace("TC-065", "NFR-001-AC-1")
def test_zero_020_locators_changed():
    record = baseline("locators.json")
    changed = []
    for name, old in record["locators"].items():
        new = locators(object_type(name))
        for key, facets in old.items():
            if new.get(key) != facets:
                changed.append(f"{name}.{key}")
    assert not changed, f"0.2.0 locators changed at 0.3.0: {changed}"


@pytest.mark.trace("TC-066", "NFR-001-AC-2")
def test_every_020_skeleton_still_validates_under_030(quire_engine):
    """The 0.2.0 authoring form, kept and re-run.

    These files carry no `## Properties` section at all, which is what every
    document written against 0.2.0 looks like. Under 0.3.0 the declaration is
    `not_applicable` rather than empty, so the record requirement does not bite
    and the document stays valid with no author action — which is the whole
    content of the additive promise.
    """
    for name in LEGACY_SKELETONS:
        path = BASELINE_DIR / "skeletons" / name
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (name, result["errors"])


@pytest.mark.trace("TC-067", "NFR-001-AC-3")
def test_a_legacy_prose_properties_block_is_reported_as_a_legacy_form(quire_engine):
    """The warning half of the criterion, which does hold today."""
    path = BASELINE_DIR / "legacy-properties-prose.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    warnings = [w["message"] for w in result.get("warnings", [])]
    assert any("semantic.properties-" in message for message in warnings), warnings


@pytest.mark.trace("TC-067", "NFR-001-AC-3")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "NFR 001 AC 3 requires a legacy prose `## Properties` block to be a "
        "warning and NOT an error under `legacy_forms: warning`. quire 0.46.0 "
        "validates the `unavailable` declaration as `{}` and then reports "
        "`semantic.record-invalid` for the missing `fields`, so the document "
        "errors as well as warning. Blocked on agent-ix/quire-rs#391. The "
        "schema is not relaxed to make this pass and the test is not skipped."
    ),
)
def test_a_legacy_prose_properties_block_is_not_an_error(quire_engine):
    path = BASELINE_DIR / "legacy-properties-prose.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert result["is_valid"], result["errors"]


@pytest.mark.trace("TC-068", "NFR-001-AC-4")
def test_the_traceability_model_is_unchanged_from_020():
    """A neighbour's edges live here.

    `spec-objects-security` reads which object type carries a mitigation
    obligation, which verb satisfies it and which direction it is authored from.
    Changing any of those from this side would silently repoint the neighbour's
    coverage check, so 0.3.0 changes none of them.
    """
    model = load_manifest()["traceability"]
    assert model == baseline("traceability.json")

    by_name = {relation["name"]: relation for relation in model["required_relations"]}
    assert set(by_name) == {"hazard-has-mitigation", "failure-mode-has-mitigation"}
    for name, kind in (
        ("hazard-has-mitigation", "hazard"),
        ("failure-mode-has-mitigation", "failure_mode"),
    ):
        relation = by_name[name]
        assert relation["from"] == kind
        assert relation["edges"] == ["mitigates"]
        assert relation["direction"] == "incoming"
    assert {relation["check"] for relation in by_name.values()} == {
        "unmitigated-hazard",
        "unmitigated-failure-mode",
    }
    assert model["acyclic_edges"] == ["arises_from"]


@pytest.mark.trace("TC-069", "NFR-001-AC-5")
def test_the_widened_lint_allow_lists_still_admit_every_020_value():
    """Widening an advisory allow-list is not a relaxation of the gate.

    At 0.2.0 the only way past these advisories was to write a scale value, so
    an author who had not scored an axis was nudged towards `negligible` or
    `none` — the exact collapse the module exists to prevent. 0.3.0 adds the
    three epistemic tokens the schemas admit, and removes nothing.
    """
    old = {rule["id"]: rule for rule in baseline("lint_rules.json")}
    new = {rule["id"]: rule for rule in load_manifest()["lint_rules"]}
    assert set(new) == set(old), "a lint rule was added or dropped"

    epistemic = {"unknown", "not_assessed", "not_applicable"}
    for rule_id, previous in old.items():
        current = new[rule_id]
        for facet in ("type", "section", "column"):
            assert current[facet] == previous[facet], f"{rule_id}.{facet} changed"
        dropped = sorted(set(previous["allowed"]) - set(current["allowed"]))
        assert not dropped, f"{rule_id} no longer admits {dropped}"
        assert epistemic <= set(
            current["allowed"]
        ), f"{rule_id} still refuses an honestly unscored axis"
