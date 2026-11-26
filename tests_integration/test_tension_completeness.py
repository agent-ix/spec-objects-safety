"""End-to-end checks for tension relation rules (FR-402..FR-405)."""

from __future__ import annotations

import importlib.util
import os
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import PACKAGE_ROOT

pytestmark = pytest.mark.integration


def _module(package: str) -> pathlib.Path:
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.origin:
        pytest.fail(f"{package} is not installed")
    return pathlib.Path(spec.origin).resolve().parent


def _quire() -> str:
    return (
        os.environ.get("QUIRE_BIN")
        or shutil.which("quire")
        or pytest.fail("set QUIRE_BIN or put the quire command on PATH")
    )


def _write_tension(
    root: pathlib.Path,
    tension_id: str,
    *,
    status: str = "open",
    conflicts: tuple[str, ...] = ("REQ-A", "REQ-B"),
    resolved_by: str | None = None,
    decided_by: str | None = None,
) -> None:
    source = (PACKAGE_ROOT / "skeletons" / "tension.md").read_text()
    body = re.sub(r"^---\n.*?\n---\n", "", source, count=1, flags=re.DOTALL)
    frontmatter = {
        "id": tension_id,
        "title": f"{tension_id}Conflict",
        "type": "tension",
        "object": "tension",
        "status": status,
    }
    if decided_by is not None:
        frontmatter["decided_by"] = decided_by
    edges = [{"target": target, "type": "conflicts_with"} for target in conflicts]
    if resolved_by is not None:
        edges.append({"target": resolved_by, "type": "resolved_by"})
    frontmatter["relationships"] = edges
    text = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\n{body}"
    (root / f"{tension_id}.md").write_text(text)


def _remove_frontmatter_field(path: pathlib.Path, field: str) -> None:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    assert match, f"{path.name} has no frontmatter"
    frontmatter = yaml.safe_load(match.group(1))
    del frontmatter[field]
    path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\n{match.group(2)}"
    )


def _part(root: pathlib.Path, part_id: str) -> None:
    source = _module("spec_objects_architecture") / "skeletons" / "part.md"
    text = (
        source.read_text()
        .replace("scoring_engine", part_id)
        .replace("ScoringEngine", f"{part_id.title().replace('-', '')}")
    )
    (root / f"{part_id}.md").write_text(text)


def _validate(root: pathlib.Path, *flags: str, safety_module=PACKAGE_ROOT):
    command = [
        _quire(),
        "validate",
        "--okf",
        *flags,
        "--module",
        str(_module("spec_artifacts_iso")),
        "--module",
        str(_module("spec_objects_security")),
        "--module",
        str(safety_module),
        "--module",
        str(_module("spec_objects_architecture")),
        str(root),
    ]
    return subprocess.run(command, capture_output=True, text=True)


def _finding(result: subprocess.CompletedProcess, check: str) -> list[str]:
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{check}]")]


@pytest.mark.trace("FR-402-AC-2")
def test_tension_rejects_undeclared_links_with_a_named_diagnostic(tmp_path):
    _write_tension(tmp_path, "TEN-001")
    path = tmp_path / "TEN-001.md"
    text = path.read_text().replace("type: conflicts_with", "type: references", 1)
    path.write_text(text)

    result = _validate(tmp_path)
    lines = _finding(result, "disallowed-edge-target")
    assert any("TEN-001.md" in line and "references" in line for line in lines), lines


@pytest.mark.trace("FR-402-AC-3", "FR-404-AC-3")
def test_resolved_by_design_edge_to_a_part_clears_the_tension_finding(tmp_path):
    _write_tension(
        tmp_path,
        "TEN-001",
        status="resolved-by-design",
        resolved_by="PART-001",
    )
    _part(tmp_path, "PART-001")

    result = _validate(tmp_path)
    assert result.returncode == 0, result.stderr
    assert _finding(result, "resolved-tension-without-link") == []
    assert "TEN-001.md" not in "\n".join(_finding(result, "disallowed-edge-target"))


@pytest.mark.trace("FR-404-AC-1", "FR-405-AC-2")
def test_open_tension_is_named_and_fails_when_its_check_is_an_error(tmp_path):
    _write_tension(tmp_path, "TEN-001")
    result = _validate(
        tmp_path,
        "--severity",
        "trace:open-tension=error",
    )
    assert result.returncode != 0, result.stderr
    lines = _finding(result, "open-tension")
    assert any("TEN-001.md" in line for line in lines), lines


@pytest.mark.trace("FR-404-AC-2")
def test_incoming_conflicts_with_edge_does_not_close_an_open_tension(tmp_path):
    _write_tension(tmp_path, "TEN-001")
    _write_tension(
        tmp_path,
        "TEN-002",
        status="accepted-by-person",
        conflicts=("REQ-C", "REQ-D", "TEN-001"),
        decided_by="A. Person",
    )
    result = _validate(tmp_path)
    lines = _finding(result, "open-tension")
    assert any("TEN-001.md" in line for line in lines), lines


@pytest.mark.trace("FR-404-AC-4")
def test_resolved_tension_without_its_design_edge_is_reported(tmp_path):
    _write_tension(tmp_path, "TEN-001", status="resolved-by-design")
    result = _validate(tmp_path)
    lines = _finding(result, "resolved-tension-without-link")
    assert any("TEN-001.md" in line for line in lines), lines


@pytest.mark.trace("FR-404-AC-5")
def test_named_person_acceptance_passes_but_missing_name_fails(tmp_path):
    _write_tension(
        tmp_path,
        "TEN-001",
        status="accepted-by-person",
        decided_by="A. Person",
    )
    accepted = _validate(tmp_path)
    assert accepted.returncode == 0, accepted.stderr
    assert _finding(accepted, "open-tension") == []
    assert _finding(accepted, "resolved-tension-without-link") == []

    _remove_frontmatter_field(tmp_path / "TEN-001.md", "decided_by")
    refused = _validate(tmp_path)
    assert refused.returncode != 0, refused.stderr
    assert "decided_by" in refused.stderr


@pytest.mark.trace("FR-404-AC-6", "FR-405-AC-1")
def test_corpus_without_tensions_has_identical_validation_output(tmp_path):
    """The two rules do not change validation output when no tension exists."""
    baseline = tmp_path / "baseline-module"
    shutil.copytree(PACKAGE_ROOT, baseline)
    manifest_path = baseline / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest["traceability"]["required_relations"] = [
        rule
        for rule in manifest["traceability"]["required_relations"]
        if rule["name"] not in {"resolved-tension-has-link", "tension-is-not-open"}
    ]
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))

    corpus = tmp_path / "corpus"
    corpus.mkdir()
    current = _validate(corpus)
    before = _validate(corpus, safety_module=baseline)
    assert current.returncode == before.returncode
    assert current.stdout == before.stdout
    assert current.stderr == before.stderr
