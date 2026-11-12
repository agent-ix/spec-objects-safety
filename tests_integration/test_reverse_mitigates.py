"""FR-009: a safety-classified NFR that mitigates nothing is reported.

The fixtures are the installed `spec-artifacts-iso` NFR skeleton and this
module's own hazard skeleton, validated by the `quire` CLI with the modules
loaded. The reverse relation is declared in the manifest with the `where`
selector of quire-rs FR-058; nothing is copied into this repository.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import re
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_safety"

pytestmark = pytest.mark.integration

QUIRE_ENV = "QUIRE_BIN"
CHECK = "unjustified-safety-nfr"


def _module(package: str) -> pathlib.Path:
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.origin:
        pytest.fail(f"{package} is not installed")
    return pathlib.Path(spec.origin).parent


def _quire() -> str:
    found = os.environ.get(QUIRE_ENV) or shutil.which("quire")
    if not found:
        pytest.fail(f"the `quire` CLI is not on PATH and {QUIRE_ENV} is unset")
    return found


def _nfr(root, nfr_id, quality_attribute, mitigates=()):
    """Write an NFR from the iso skeleton, with one `mitigates` edge per target."""
    text = (_module("spec_artifacts_iso") / "skeletons" / "nfr.md").read_text()
    text = text.replace("NFR-001", nfr_id)
    text = re.sub(
        r"^quality_attribute: .*$",
        f"quality_attribute: {quality_attribute}",
        text,
        flags=re.M,
    )
    edges = "".join(f"  - target: {t}\n    type: mitigates\n" for t in mitigates)
    relationships = f"relationships:\n{edges}" if edges else ""
    text = re.sub(r"relationships:\n(?:  .*\n)+", relationships, text, count=1)
    # The skeleton's example upstream link would be a dangling reference.
    text = re.sub(r"\[(FR-001)\]\([^)]*\)", r"\1", text)
    (root / f"{nfr_id}.md").write_text(text)


def _hazard(root, hazard_id="HAZ-001"):
    text = (PACKAGE_ROOT / "skeletons" / "hazard.md").read_text()
    (root / f"{hazard_id}.md").write_text(text.replace("HAZ-001", hazard_id))


def _validate(root, *flags):
    return subprocess.run(
        [
            _quire(),
            "validate",
            "--okf",
            *flags,
            "--module",
            str(_module("spec_artifacts_iso")),
            "--module",
            str(PACKAGE_ROOT),
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def _findings(result):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{CHECK}]")]


@pytest.mark.trace("TC-100", "FR-009-AC-2")
def test_safety_nfr_without_a_mitigates_edge_is_reported(tmp_path):
    _nfr(tmp_path, "NFR-001", "safety")
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    findings = _findings(result)
    assert len(findings) == 1, result.stderr
    assert "NFR-001" in findings[0] and "'safety'" in findings[0], findings


@pytest.mark.trace("TC-101", "FR-009-AC-3", "FR-009-AC-4")
def test_mitigating_or_differently_classified_nfr_is_not_reported(tmp_path):
    _hazard(tmp_path)
    _nfr(tmp_path, "NFR-001", "safety", ["HAZ-001"])
    _nfr(tmp_path, "NFR-002", "safety", ["ix://agent-ix/other-repo/HAZ-900"])
    _nfr(tmp_path, "NFR-003", "performance_efficiency")
    _nfr(tmp_path, "NFR-004", "security")
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    assert _findings(result) == [], result.stderr
    # Prove the rule is live over this very bundle: dropping one edge reports it.
    _nfr(tmp_path, "NFR-002", "safety")
    findings = _findings(_validate(tmp_path))
    assert len(findings) == 1 and "NFR-002" in findings[0], findings


@pytest.mark.trace("TC-102", "FR-009-AC-5")
def test_finding_is_advisory_and_tunable(tmp_path):
    _nfr(tmp_path, "NFR-001", "safety")
    strict = _validate(tmp_path, "--strict")
    assert len(_findings(strict)) == 1, strict.stderr
    promoted = _validate(tmp_path, "--severity", f"trace:{CHECK}=error")
    assert promoted.returncode != 0, promoted.stderr
    assert len(_findings(promoted)) == 1, promoted.stderr
    assert not _findings(promoted)[0].startswith("warning:"), promoted.stderr
