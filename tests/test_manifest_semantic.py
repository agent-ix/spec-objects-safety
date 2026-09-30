"""Manifest contract tests (FR 003): the `semantic` block, its reference-form
`data_schema`, locator preservation, the traceability model this module's
neighbour reads, and what Quire's loader refuses.
"""

from __future__ import annotations

import shutil

import pytest
import yaml

from tests.conftest import (
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    baseline,
    frontmatter,
    locators,
    object_type,
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
    assert semantic_block["semantic_core"] == "0.3.0"
    assert semantic_block["package"] == "agent-ix/spec-objects-safety"
    assert semantic_block["exports"] == list(OBJECT_TYPES)
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["mappings"] == ["typed-table", "sysml-fence", "ocl-clause"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"


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
@pytest.mark.parametrize(
    ("label", "mutate"),
    [
        ("bad-package", lambda block: block.update(package="ix://agent-ix/x")),
        ("unregistered-target", lambda block: block.update(targets=["go"])),
    ],
)
def test_a_semantic_value_the_contract_forbids_is_refused_at_load(
    quire_engine, tmp_path, label, mutate
):
    """FR-003-AC-6 against the engine that reads the manifest.

    The module-manifest schema is applied by quire at load, so a `semantic`
    value the contract forbids costs the module its object types. The oracle is
    the consumer, never a copy of the schema held here (PLAT-902).
    """
    control = module_copy(tmp_path / f"{label}-control")
    assert quire_engine.Registry.load_from(
        [str(control)]
    ).archetype_names(), "the unmutated copy does not load; the control is broken"

    def apply(data):
        mutate(data["semantic"])

    mutant = module_copy(tmp_path / label, apply)
    loaded = quire_engine.Registry.load_from([str(mutant)]).archetype_names()
    assert not loaded, f"{label} loaded anyway: {sorted(loaded)}"
