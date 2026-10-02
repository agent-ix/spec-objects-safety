"""Emission tests for the schema set (FR 002), its `$id`/`$ref` shape, the drift gate,
determinism, and packaging.

The emitted set is fifteen files: the two object-type records `Hazard` and
`FailureMode`, and the thirteen support models they compose — the identity
marker, the four structured value models, and the eight closed vocabularies
that carry the safety scales and the epistemic states.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import tarfile
import zipfile

import pytest

from tests.conftest import (
    MANIFEST_PATH,
    MODEL_OF,
    MODULE_BASE,
    OBJECT_TYPES,
    REPO_ROOT,
    SCHEMAS_DIR,
    SEMANTIC_CORE_BASE,
)

GENERATOR = REPO_ROOT / "scripts" / "generate-schemas.mjs"


def run_generator(
    *args: str, cwd: pathlib.Path | None = None
) -> subprocess.CompletedProcess:
    """Run the generator that belongs to `cwd`: it resolves its own repo root
    from its file location, so a throwaway tree must run its own copy."""
    root = cwd or REPO_ROOT
    return subprocess.run(
        ["node", str(root / "scripts" / "generate-schemas.mjs"), *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def shipped_schemas() -> dict[str, dict]:
    return {
        path.name: json.loads(path.read_text())
        for path in sorted(SCHEMAS_DIR.glob("*.json"))
    }


def worktree_copy(tmp_path: pathlib.Path) -> pathlib.Path:
    """A throwaway copy of the tree the generator needs, so no test mutates the repo."""
    root = tmp_path / "tree"
    root.mkdir(parents=True)
    for item in ("typespec", "scripts", "package.json", "package-lock.json"):
        source = REPO_ROOT / item
        target = root / item
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    (root / "spec_objects_safety").mkdir()
    shutil.copy2(MANIFEST_PATH, root / "spec_objects_safety" / "manifest.yaml")
    shutil.copytree(SCHEMAS_DIR, root / "spec_objects_safety" / "schemas")
    (root / "node_modules").symlink_to(REPO_ROOT / "node_modules")
    return root


@pytest.mark.trace("TC-013", "FR-002-AC-2")
def test_every_schema_declares_2020_12_and_an_id_matching_its_file_name():
    base = MODULE_BASE
    for name, schema in shipped_schemas().items():
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema", name
        assert schema["$id"] == f"{base}{name}", name


@pytest.mark.trace("TC-014", "FR-002-AC-3")
def test_every_ref_resolves_to_a_shipped_sibling_or_semantic_core():
    base = MODULE_BASE
    shipped = shipped_schemas()
    refs: list[tuple[str, str]] = []

    def walk(owner: str, node) -> None:
        if isinstance(node, list):
            for item in node:
                walk(owner, item)
        elif isinstance(node, dict):
            if "$ref" in node:
                refs.append((owner, node["$ref"]))
            for key, value in node.items():
                if key != "$ref":
                    walk(owner, value)

    for name, schema in shipped.items():
        walk(name, schema)
    assert refs, "the emitted schemas make no cross-reference at all"
    for owner, ref in refs:
        if ref.startswith(base):
            assert (
                ref[len(base) :] in shipped
            ), f"{owner} references an unshipped sibling {ref}"
        else:
            assert ref.startswith(SEMANTIC_CORE_BASE), f"{owner} references {ref}"


@pytest.mark.trace("TC-015", "FR-002-AC-4")
def test_schemas_check_is_green_on_the_committed_tree_and_names_a_mutation(tmp_path):
    assert run_generator("--check").returncode == 0

    tree = worktree_copy(tmp_path)
    target = tree / "spec_objects_safety" / "schemas" / "Hazard.json"
    target.write_text(
        target.read_text().replace('"type": "object"', '"type":  "object"', 1)
    )
    mutated = run_generator("--check", cwd=tree)
    assert mutated.returncode != 0
    assert "Hazard.json" in mutated.stderr


@pytest.mark.trace("TC-017", "FR-002-AC-6")
def test_the_built_wheel_and_sdist_carry_every_exported_schema(tmp_path):
    dist = tmp_path / "dist"
    build = subprocess.run(
        ["poetry", "build", "--output", str(dist)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if build.returncode != 0:
        pytest.fail(f"`poetry build` failed:\n{build.stdout}\n{build.stderr}")
    wheel = next(dist.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    for name in OBJECT_TYPES:
        assert f"spec_objects_safety/schemas/{MODEL_OF[name]}.json" in names
    sdist = next(dist.glob("*.tar.gz"))
    with tarfile.open(sdist) as archive:
        members = {pathlib.PurePosixPath(m).parts[1:] for m in archive.getnames()}
    for name in OBJECT_TYPES:
        assert ("spec_objects_safety", "schemas", f"{MODEL_OF[name]}.json") in members


@pytest.mark.trace("TC-021", "FR-002-CON-3")
def test_two_generator_runs_over_one_source_are_byte_identical(tmp_path):
    tree = worktree_copy(tmp_path)
    assert run_generator(cwd=tree).returncode == 0
    first = {
        p.name: p.read_bytes() for p in (tree / "spec_objects_safety/schemas").iterdir()
    }
    assert run_generator(cwd=tree).returncode == 0
    second = {
        p.name: p.read_bytes() for p in (tree / "spec_objects_safety/schemas").iterdir()
    }
    assert first == second


@pytest.mark.trace("TC-022", "FR-002-CON-1")
def test_the_build_uses_the_official_emitter_only_and_no_file_is_hand_edited():
    """FR 002 CON-1, inspection: the generator shells out to the official
    compiler and writes only what the emitter produced."""
    source = (REPO_ROOT / "scripts" / "generate-schemas.mjs").read_text()
    assert "@typespec/compiler/entrypoints/cli.js" in source
    assert (
        "@typespec/json-schema"
        in json.loads((REPO_ROOT / "package.json").read_text())["devDependencies"]
    )
    # No emitter of our own, and the only writer of `schemas/` is this script.
    for path in REPO_ROOT.glob("scripts/*.mjs"):
        assert "emitter" not in path.name
    # A hand edit would make the drift gate red; that gate is the standing check.
    assert run_generator("--check").returncode == 0


@pytest.mark.trace("TC-023", "FR-002-CON-2")
def test_no_npmrc_no_local_dependency_and_exact_toolchain_pins():
    assert not (REPO_ROOT / ".npmrc").exists()
    package = json.loads((REPO_ROOT / "package.json").read_text())
    assert "devDependencies" in package
    assert "dependencies" not in package or not package["dependencies"]
    for section in ("dependencies", "devDependencies"):
        for name, spec in (package.get(section) or {}).items():
            assert not spec.startswith(("file:", "link:")), f"{name} -> {spec}"
            assert "<" not in spec, f"{name} carries an upper bound: {spec}"


@pytest.mark.trace("TC-024", "FR-002-CON-4")
def test_the_lockfile_resolves_public_packages_from_npmjs():
    """`@agent-ix/semantic-core` is published to a real, CI-reachable registry
    (GitHub Packages), never the private `npm.ix` dev-only mirror. Every package
    in the lockfile SHALL now resolve from a real registry and none from
    `npm.ix`."""
    lock = json.loads((REPO_ROOT / "package-lock.json").read_text())
    for path, entry in lock["packages"].items():
        resolved = entry.get("resolved")
        if not resolved:
            continue
        assert "npm.ix" not in resolved, f"{path} -> {resolved}"
        if path.endswith("@agent-ix/semantic-core"):
            assert resolved.startswith(
                "https://npm.pkg.github.com/"
            ), f"{path} -> {resolved}"
        else:
            assert resolved.startswith(
                "https://registry.npmjs.org/"
            ), f"{path} -> {resolved}"


@pytest.mark.trace("TC-018", "FR-002-AC-7")
def test_the_npm_tarball_ships_the_schemas_beside_the_manifest(tmp_path):
    staged = [
        REPO_ROOT / "manifest.yaml",
        REPO_ROOT / "schemas",
        REPO_ROOT / "skeletons",
    ]
    assert not any(path.exists() for path in staged), (
        "the npm payload is already staged at the repository root; a stray "
        "root manifest.yaml makes every Filament tool discover the repo root "
        "as a second module"
    )
    try:
        pack = subprocess.run(
            ["npm", "pack", "--pack-destination", str(tmp_path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        if pack.returncode != 0:
            pytest.fail(f"`npm pack` failed:\n{pack.stdout}\n{pack.stderr}")
        # `postpack` removes the staged copies again; assert it actually ran,
        # because a leftover root manifest.yaml silently breaks `quire validate`.
        assert not any(path.exists() for path in staged), (
            "npm pack left the staged payload at the repository root; "
            "scripts/stage-npm.mjs --clean did not run"
        )
    finally:
        for path in staged:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
    tarball = next(tmp_path.glob("*.tgz"))
    with tarfile.open(tarball) as archive:
        names = set(archive.getnames())
    assert "package/manifest.yaml" in names
    for name in OBJECT_TYPES:
        assert f"package/schemas/{MODEL_OF[name]}.json" in names


@pytest.mark.trace("TC-020", "FR-002-AC-9")
def test_schemas_check_names_a_stale_committed_schema_and_writes_nothing(tmp_path):
    tree = worktree_copy(tmp_path)
    out = tree / "spec_objects_safety" / "schemas"
    stale = out / "Stale.json"
    stale.write_text("{}\n")
    before = {p.name: p.read_bytes() for p in out.iterdir()}
    manifest_before = (tree / "spec_objects_safety" / "manifest.yaml").read_bytes()
    result = run_generator("--check", cwd=tree)
    assert result.returncode != 0
    assert "Stale.json" in result.stderr and "stale" in result.stderr
    after = {p.name: p.read_bytes() for p in out.iterdir()}
    assert before == after
    assert (
        tree / "spec_objects_safety" / "manifest.yaml"
    ).read_bytes() == manifest_before
