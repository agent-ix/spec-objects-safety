"""Portable checks for risk-report behavior supplied by the installed Quoin CLI."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess

import pytest

from tests.conftest import PACKAGE_ROOT, SKELETONS_DIR


def _quoin() -> str:
    """Return the explicitly configured Quoin binary or fail with its name."""
    binary = os.environ.get("QUOIN_BIN")
    if not binary:
        pytest.fail("QUOIN_BIN must name the installed quoin CLI")
    path = pathlib.Path(binary)
    if not path.is_file() or not os.access(path, os.X_OK):
        pytest.fail(f"QUOIN_BIN does not name an executable file: {binary}")
    return binary


def _quire() -> str:
    """Return the explicitly configured Quire binary or fail with its name."""
    binary = os.environ.get("QUIRE_BIN") or shutil.which("quire")
    if not binary:
        pytest.fail("QUIRE_BIN must name the scoped quire CLI")
    return binary


def _scoped_module_roots() -> list[pathlib.Path]:
    """Resolve the explicitly required process, ISO and safety module roots."""
    roots = []
    for variable, package in (
        ("SPEC_ARTIFACTS_PROCESS_ROOT", "spec_artifacts_process"),
        ("SPEC_ARTIFACTS_ISO_ROOT", "spec_artifacts_iso"),
    ):
        value = os.environ.get(variable)
        if not value:
            pytest.fail(f"{variable} must name its explicit Quire module root")
        root = pathlib.Path(value)
        if not (root / "manifest.yaml").is_file():
            root = root / package
        if not (root / "manifest.yaml").is_file():
            pytest.fail(f"{variable} has no manifest.yaml below {value}")
        roots.append(root)
    roots.append(PACKAGE_ROOT)
    return roots


def _with_relationships(text: str, edges: list[tuple[str, str]]) -> str:
    block = "".join(f"  - target: {target}\n    type: {kind}\n" for kind, target in edges)
    return text.replace("\n---\n", f"\nrelationships:\n{block}---\n", 1)


def _policy(root: pathlib.Path) -> None:
    text = (SKELETONS_DIR / "acceptability_policy.md").read_text()
    for placeholder, value in (
        ("<severity level>", "critical"),
        ("<probability level>", "remote"),
        ("<region>", "outside"),
        ("<true or false>", "true"),
    ):
        text = text.replace(placeholder, value)
    (root / "POL-1.md").write_text(text.replace("POL-001", "POL-1"))


def _estimate(root: pathlib.Path) -> None:
    text = (SKELETONS_DIR / "risk_estimate.md").read_text().replace("EST-001", "EST-1")
    for placeholder, value in (
        ("<pre_control | post_control>", "post_control"),
        ("<severity>", "critical"),
        ("<probability>", "remote"),
        ("<why this person judges it so>", "The condition may cause injury."),
        ("<person>", "A. Person"),
        ("<date or UTC timestamp>", "2026-11-26"),
    ):
        text = text.replace(placeholder, value)
    (root / "EST-1.md").write_text(text)


def _residual_risk(root: pathlib.Path, risk_id: str, decision: str) -> None:
    text = (SKELETONS_DIR / "residual_risk.md").read_text().replace("RR-001", risk_id)
    for placeholder, value in (
        ("<undecided, accepted or not_accepted>", decision),
        ("<why the person decided so>", "Recorded for the fixture."),
        ("<person who decided, empty while undecided>", "A. Person" if decision != "undecided" else ""),
    ):
        text = text.replace(placeholder, value)
    text = _with_relationships(
        text, [("estimate", "EST-1"), ("references", "POL-1")]
    )
    (root / f"{risk_id}.md").write_text(text)


def _bundle(root: pathlib.Path, decision: str = "accepted", count: int = 1) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _policy(root)
    _estimate(root)
    for index in range(count):
        _residual_risk(root, f"RR-{index:05d}", decision)


def _run_report(root: pathlib.Path, *, strict: bool = False) -> subprocess.CompletedProcess[str]:
    command = [
        _quoin(),
        "risk",
        "discrepancies",
        str(root),
        "--module",
        str(PACKAGE_ROOT),
        "--no-project-config",
        "--format",
        "json",
    ]
    if strict:
        command.append("--strict")
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _snapshot(root: pathlib.Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*.md"))
    }


class TestPortableQuoinReports:
    """Exercise report contracts against the Quoin executable selected by QUOIN_BIN."""

    @pytest.mark.trace("FR-104-AC-1")
    def test_validation_and_discrepancy_report_leave_authored_files_unchanged(self, tmp_path):
        """Validation and report execution preserve every authored fixture byte.

        Assumptions:
            A complete local policy can be validated by the installed Quire engine.
            The report binary is provided explicitly through QUOIN_BIN.

        Criteria:
            The Quire validation succeeds, the Quoin report runs, and the authored
            Markdown files are byte-identical before and after both operations.
        """
        _bundle(tmp_path)
        before = _snapshot(tmp_path)
        modules = _scoped_module_roots()
        validated = subprocess.run(
            [
                _quire(),
                "validate",
                "--okf",
                *[arg for module in modules for arg in ("--module", str(module))],
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert validated.returncode == 0, validated.stderr
        report = _run_report(tmp_path)
        assert report.returncode == 0, report.stderr
        assert json.loads(report.stdout)["findings"]
        assert _snapshot(tmp_path) == before

    @pytest.mark.trace("FR-105-AC-7")
    def test_discrepancies_are_warnings_unless_strict_mode_is_requested(self, tmp_path):
        """Discrepancies exit successfully by default and fail under strict mode.

        Assumptions:
            The fixture has an accepted residual risk in a region marked outside
            the acceptable region.

        Criteria:
            Default execution exits zero with the finding; strict execution exits
            nonzero for the same finding.
        """
        _bundle(tmp_path)
        warning = _run_report(tmp_path)
        assert warning.returncode == 0, warning.stderr
        assert json.loads(warning.stdout)["findings"][0]["finding"] == (
            "accepted-outside-acceptable-region"
        )
        strict = _run_report(tmp_path, strict=True)
        assert strict.returncode != 0, strict.stderr
        assert "accepted-outside-acceptable-region" in strict.stdout + strict.stderr

