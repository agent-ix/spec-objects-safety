"""Manifest contract tests (FR 003): the `semantic` block, its reference-form
`data_schema`, locator preservation, the traceability model this module's
neighbour reads, and what Quire's loader refuses.
"""

from __future__ import annotations

import shutil

import pytest
import yaml

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    SKELETONS_DIR,
    baseline,
    frontmatter,
    locators,
    object_type,
    object_types,
    sha256_of,
)

ADMITTED_KEYS = {
    "contract_version",
    "semantic_core",
    "package",
    "exports",
    "imports",
    "targets",
    "mappings",
    "compatibility_posture",
    "legacy_forms",
}


def module_copy(tmp_path, mutate=None):
    """A throwaway copy of the module directory, optionally with a mutated
    manifest. Returns the *search path* the loader walks, not the module dir."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    root = tmp_path / "module"
    shutil.copytree(PACKAGE_ROOT, root)
    if mutate is not None:
        data = yaml.safe_load((root / "manifest.yaml").read_text())
        mutate(data)
        (root / "manifest.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
    return tmp_path


@pytest.mark.trace("TC-026", "FR-003-AC-1", "FR-003-CON-1")
def test_the_semantic_block_carries_the_nine_admitted_keys_and_two_exports(
    semantic_block,
):
    assert set(semantic_block) == ADMITTED_KEYS
    assert semantic_block["contract_version"] == "1.0.0"
    assert semantic_block["semantic_core"] == "0.1.0"
    assert semantic_block["package"] == "agent-ix/spec-objects-safety"
    assert semantic_block["exports"] == list(OBJECT_TYPES)
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["mappings"] == ["typed-table", "sysml-fence", "ocl-clause"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"


@pytest.mark.trace("TC-027", "FR-003-AC-2")
def test_every_exported_type_carries_the_reference_form_and_a_matching_digest():
    for ot in object_types():
        data_schema = ot["data_schema"]
        assert set(data_schema) == {"schema", "digest"}, ot["name"]
        expected = f"schemas/{MODEL_OF[ot['name']]}.json"
        assert data_schema["schema"] == expected, ot["name"]
        path = PACKAGE_ROOT / data_schema["schema"]
        assert path.is_file(), path
        assert data_schema["digest"] == sha256_of(path), ot["name"]
        assert (
            "type" not in data_schema
        ), f"{ot['name']} still carries an inline data_schema"


@pytest.mark.trace("TC-028", "FR-003-AC-3", "NFR-001-AC-1")
def test_every_020_locator_is_unchanged_against_the_checked_in_baseline():
    record = baseline("locators.json")
    assert record["version"] == "0.2.0"
    for name, old in record["locators"].items():
        new = locators(object_type(name))
        for key, facets in old.items():
            assert key in new, f"{name}.{key} was dropped at 0.3.0"
            assert new[key] == facets, f"{name}.{key} changed facets at 0.3.0"


@pytest.mark.trace("TC-029", "FR-003-AC-3", "FR-003-CON-2")
def test_every_locator_added_after_020_is_optional():
    record = baseline("locators.json")
    added = 0
    for name, old in record["locators"].items():
        for key, facets in locators(object_type(name)).items():
            if key in old:
                continue
            added += 1
            assert (
                facets.get("required") is False
            ), f"{name}.{key} was added as required"
    assert added > 0, "no locator was added; FR 005's sections would not be asserted"


@pytest.mark.trace("TC-030", "FR-003-AC-4")
def test_the_registry_loads_both_archetypes_and_every_skeleton_loads_clean(
    quire_engine, skeletons
):
    registry = quire_engine.Registry.load_from([str(REPO_ROOT)])
    names = set(registry.archetype_names())
    for name in OBJECT_TYPES:
        assert name in names, f"{name} did not load from the module"

    for path in skeletons:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic." in e["message"]
        ], path.name


@pytest.mark.trace("TC-031", "FR-003-AC-5", "NFR-001-AC-4")
def test_the_traceability_model_is_fact_for_fact_the_020_model():
    """The one part of this manifest another repository reads.

    `agent-ix/spec-objects-security`'s hazard-coverage work (#5, and the #13
    migration running alongside this one) reads these relations across the repo
    boundary: which object type carries the obligation, which verb satisfies it,
    and which direction it is authored from. A change here is a change to a
    neighbour's edges, so 0.3.0 changes nothing and this test says so fact by
    fact rather than by a whole-document digest, which would also fire on a
    comment.
    """
    from tests.conftest import load_manifest

    assert load_manifest()["traceability"] == baseline("traceability.json")


@pytest.mark.trace("TC-032", "FR-003-AC-6")
def test_an_unknown_semantic_key_and_an_altered_digest_are_refused(
    quire_engine, tmp_path
):
    """Measured against quire 0.46.0: an unknown `semantic` key drops every
    object type of the module (the manifest is refused whole), while a wrong
    digest drops the refused object type alone."""

    def add_unknown_key(data):
        data["semantic"]["foo"] = "bar"

    unknown = module_copy(tmp_path / "unknown", add_unknown_key)
    assert quire_engine.Registry.load_from([str(unknown)]).archetype_names() == []

    def break_digest(data):
        entry = next(ot for ot in data["object_types"] if ot["name"] == "hazard")
        entry["data_schema"]["digest"] = "sha256:" + "0" * 64

    altered = module_copy(tmp_path / "digest", break_digest)
    loaded = set(quire_engine.Registry.load_from([str(altered)]).archetype_names())
    assert "hazard" not in loaded
    assert "failure_mode" in loaded

    text = (SKELETONS_DIR / "hazard.md").read_text()
    for search_path in (unknown, altered):
        with pytest.raises(Exception):
            quire_engine.validate_document("hazard", str(search_path / "module"), text)


@pytest.mark.trace("TC-032", "FR-003-AC-6")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-003-AC-6 requires the refusal to NAME the offending key and schema "
        "path. quire 0.46.0 empties the registry silently instead: no load "
        "failure, no semantic.* code, nothing naming `foo` or the path. Blocked "
        "on agent-ix/quire-rs#221 (unknown key) and agent-ix/quire-rs#394 "
        "(digest). The criterion stands; the schema is not relaxed and the test "
        "is not skipped."
    ),
)
def test_the_refusal_names_the_offending_key_and_path(quire_engine, tmp_path):
    def add_unknown_key(data):
        data["semantic"]["foo"] = "bar"

    unknown = module_copy(tmp_path / "named-key", add_unknown_key)
    with pytest.raises(Exception) as error:
        quire_engine.Registry.load_from([str(unknown)])
    assert "foo" in str(error.value)
