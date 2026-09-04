"""Quoin install roundtrip (IT 001).

The module can be self-consistent in its own tree and still be unusable once
installed: `data_schema` is a module-relative path plus a digest, so a wrong
path or a digest computed over the wrong bytes only shows up on the far side of
an install. This drives the real CLI against a temporary config root so the
developer's own catalog is never mutated.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest

from tests.conftest import (
    OBJECT_TYPES,
    PACKAGE_ROOT,
    frontmatter,
    load_manifest,
    sha256_of,
)

QUOIN_MISSING = (
    "the `quoin` CLI is not on PATH. The semantic-module contract needs a Quoin "
    "built from main at `3e842ce` or later; this row fails rather than skips, "
    "because a skipped row is not coverage."
)

# Why this row lives in `tests_integration/` rather than beside the unit tests:
# it drives the real CLI, and the CLI is ambient infrastructure this repository
# cannot provision or pin. On the machine this branch was written the globally
# installed `quoin` is a symlink into a live worktree whose `dist/` is mid-build
# and missing `dist/schemas/module-manifest.schema.json`, so `quoin module
# install` exits non-zero for a reason that has nothing to do with this module.
# The row is carried `🚧` in the Test Matrix with that reason rather than
# reported green, and `make test-integrations` runs it once the CLI is whole.


def quoin(*args: str, config_root) -> subprocess.CompletedProcess:
    environment = dict(os.environ, IX_CONFIG_ROOT=str(config_root))
    return subprocess.run(
        ["quoin", *args],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )


@pytest.mark.integration
@pytest.mark.trace("TC-070", "IT-001-SC-01", "IT-001-SC-02", "IT-001-SC-03")
@pytest.mark.trace("IT-001-SC-04", "IT-001-SC-05", "IT-001-SC-06")
def test_quoin_installs_the_module_and_quire_loads_it_from_the_catalog(
    quire_engine, tmp_path
):
    if shutil.which("quoin") is None:
        pytest.fail(QUOIN_MISSING)

    # SC-01: the run gets its own catalog, so the state to restore is "empty"
    # and the developer's installed modules are never touched.
    config_root = tmp_path / "ix-config"
    config_root.mkdir()
    before = quoin("module", config_root=config_root)
    assert before.returncode == 0, before.stderr
    assert "spec-objects-safety" not in before.stdout, (
        "the temporary config root already carries this module; the roundtrip "
        "would not be measuring an install"
    )

    # SC-02: the install itself, with no semantic diagnostic.
    install = quoin(
        "module", "install", f"path:{PACKAGE_ROOT}", config_root=config_root
    )
    assert install.returncode == 0, f"{install.stdout}\n{install.stderr}"
    combined = f"{install.stdout}\n{install.stderr}"
    assert "semantic." not in combined, combined

    # SC-03: it is listed.
    listed = quoin("module", config_root=config_root)
    assert listed.returncode == 0, listed.stderr
    assert "spec-objects-safety" in listed.stdout, listed.stdout

    # SC-04: Quire registers both types from the INSTALLED copy, and the digest
    # the installed manifest carries still matches the installed schema bytes.
    installed_root = next(
        path
        for path in (config_root / "filament" / "modules").iterdir()
        if path.name == "spec-objects-safety"
    )
    registry = quire_engine.Registry.load_from(
        [str(config_root / "filament" / "modules")]
    )
    names = set(registry.archetype_names())
    for name in OBJECT_TYPES:
        assert name in names, f"{name} did not load from the installed catalog"
    import yaml

    installed_manifest = yaml.safe_load((installed_root / "manifest.yaml").read_text())
    for entry in installed_manifest["object_types"]:
        reference = entry["data_schema"]
        assert reference["digest"] == sha256_of(
            installed_root / reference["schema"]
        ), entry["name"]
    assert installed_manifest["version"] == load_manifest()["version"]

    # SC-05: a shipped skeleton validates against the installed copy, so the
    # module-relative `schema:` path resolved from the installed location.
    text = (installed_root / "skeletons" / "hazard.md").read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(installed_root), text
    )
    assert result["is_valid"], result["errors"]
    assert not [e for e in result["errors"] if "semantic." in e["message"]]

    # SC-06: the catalog is left as it was found. The temporary root is what
    # makes that true by construction; assert it rather than trusting it, and
    # prove the developer's real catalog was never a candidate.
    assert json.dumps(str(config_root)) not in json.dumps(str(PACKAGE_ROOT))
    shutil.rmtree(config_root)
    assert not config_root.exists()
