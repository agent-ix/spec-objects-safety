"""FR-007 and FR-008: the `mitigates` edge is authorable and the coverage checks fire.

The fixtures are built from this module's own skeletons plus the
`spec-objects-security` control skeleton, and validated by the `quire` CLI with
both modules (and the iso edge vocabulary) loaded. The other modules come from
an installed package or from the checkout named by an environment variable;
nothing is copied into this repository.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_safety"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"

pytestmark = pytest.mark.integration

SECURITY_ENV = "SPEC_OBJECTS_SECURITY_MODULE"
ISO_ENV = "SPEC_ARTIFACTS_ISO_MODULE"
QUIRE_ENV = "QUIRE_BIN"


def _module(package: str, env: str) -> pathlib.Path:
    value = os.environ.get(env)
    if value:
        return pathlib.Path(value)
    spec = importlib.util.find_spec(package)
    if spec is not None and spec.origin:
        return pathlib.Path(spec.origin).parent
    pytest.fail(f"{package} is not installed and {env} names no checkout")


def _quire() -> str:
    found = os.environ.get(QUIRE_ENV) or shutil.which("quire")
    if not found:
        pytest.fail(f"the `quire` CLI is not on PATH and {QUIRE_ENV} is unset")
    return found


def _skeleton(directory: pathlib.Path, name: str, old: str, new: str) -> str:
    text = (directory / f"{name}.md").read_text()
    return text.replace(old, new)


def _bundle(root, hazards, failure_modes, mitigates):
    """Write a bundle: `mitigates` maps a control id to the target ids it names."""
    security = _module("spec_objects_security", SECURITY_ENV) / "skeletons"
    for hid in hazards:
        (root / f"{hid}.md").write_text(
            _skeleton(SKELETONS_DIR, "hazard", "HAZ-001", hid)
        )
    for fid in failure_modes:
        (root / f"{fid}.md").write_text(
            _skeleton(SKELETONS_DIR, "failure_mode", "FM-001", fid)
        )
    for cid, targets in mitigates.items():
        edges = "".join(f"  - target: {t}\n    type: mitigates\n" for t in targets)
        text = _skeleton(security, "control", "CTRL-001", cid)
        text = text.replace(
            "object: control\n---", f"object: control\nrelationships:\n{edges}---", 1
        )
        (root / f"{cid}.md").write_text(text)


def _validate(root, *flags):
    return subprocess.run(
        [
            _quire(),
            "validate",
            "--okf",
            *flags,
            "--module",
            str(_module("spec_artifacts_iso", ISO_ENV)),
            "--module",
            str(_module("spec_objects_security", SECURITY_ENV)),
            "--module",
            str(PACKAGE_ROOT),
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def _findings(result, check):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{check}]")]


@pytest.mark.trace("TC-093", "FR-007-AC-1", "FR-007-AC-2")
def test_control_mitigating_hazard_and_failure_mode_is_accepted(tmp_path):
    _bundle(tmp_path, ["HAZ-001"], ["FM-001"], {"CTRL-001": ["HAZ-001", "FM-001"]})
    result = _validate(tmp_path)
    assert "disallowed-edge-target" not in result.stderr, result.stderr
    assert "DisallowedEdgeType" not in result.stderr, result.stderr
    # Quire tolerates a type it cannot load, so prove both modules loaded and
    # that the edge resolved: neither target is reported unmitigated.
    assert "[unknown-type]" not in result.stderr, result.stderr
    assert _findings(result, "unmitigated-hazard") == [], result.stderr
    assert _findings(result, "unmitigated-failure-mode") == [], result.stderr


@pytest.mark.trace("TC-094", "FR-007-AC-3")
def test_strict_validate_fails_on_an_undeclared_mitigates_target(tmp_path):
    _bundle(tmp_path, ["HAZ-001"], [], {"CTRL-001": ["HAZ-999"]})
    result = _validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(_findings(result, "dangling-reference")), "")
    assert (
        "CTRL-001.md" in line and "mitigates" in line and "HAZ-999" in line
    ), result.stderr


@pytest.mark.trace("TC-095", "FR-007-AC-4")
def test_mitigates_to_another_type_is_still_disallowed(tmp_path):
    security = _module("spec_objects_security", SECURITY_ENV) / "skeletons"
    _bundle(tmp_path, ["HAZ-001"], [], {"CTRL-001": ["ASSET-001"]})
    (tmp_path / "ASSET-001.md").write_text((security / "asset.md").read_text())
    result = _validate(tmp_path)
    line = next(iter(_findings(result, "disallowed-edge-target")), "")
    assert "ASSET-001" in line and "'asset'" in line, result.stderr


@pytest.mark.trace("TC-096", "FR-008-AC-1", "FR-008-AC-3", "FR-008-AC-4")
def test_unmitigated_hazard_fires_only_for_the_unmitigated_hazard(tmp_path):
    _bundle(tmp_path, ["HAZ-001", "HAZ-002"], [], {"CTRL-001": ["HAZ-001"]})
    findings = _findings(_validate(tmp_path), "unmitigated-hazard")
    assert len(findings) == 1 and "HAZ-002" in findings[0], findings

    _bundle(tmp_path, ["HAZ-001", "HAZ-002"], [], {"CTRL-001": ["HAZ-001", "HAZ-002"]})
    assert _findings(_validate(tmp_path), "unmitigated-hazard") == []

    bare = tmp_path / "bare"
    bare.mkdir()
    _bundle(bare, ["HAZ-001", "HAZ-002"], [], {})
    assert len(_findings(_validate(bare), "unmitigated-hazard")) == 2


@pytest.mark.trace("TC-097", "FR-008-AC-2")
def test_unmitigated_failure_mode_fires_only_for_the_unmitigated_one(tmp_path):
    _bundle(tmp_path, [], ["FM-001", "FM-002"], {"CTRL-001": ["FM-001"]})
    findings = _findings(_validate(tmp_path), "unmitigated-failure-mode")
    assert len(findings) == 1 and "FM-002" in findings[0], findings


@pytest.mark.trace("TC-098", "FR-008-AC-5")
def test_the_two_checks_are_tunable_independently(tmp_path):
    _bundle(tmp_path, ["HAZ-001"], ["FM-001"], {})
    result = _validate(tmp_path, "--severity", "trace:unmitigated-hazard=error")
    assert result.returncode != 0, result.stderr
    hazard = _findings(result, "unmitigated-hazard")
    assert len(hazard) == 1 and not hazard[0].startswith("warning:"), result.stderr
    failure_mode = _findings(result, "unmitigated-failure-mode")
    assert len(failure_mode) == 1 and failure_mode[0].startswith(
        "warning:"
    ), result.stderr
