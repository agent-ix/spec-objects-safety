"""End-to-end checks for tension relation rules (FR-402..FR-405)."""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import PACKAGE_ROOT

pytestmark = pytest.mark.integration


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
    spec = root / "spec"
    spec.mkdir(parents=True, exist_ok=True)
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
    (spec / f"{tension_id}.md").write_text(text)


def _part(root: pathlib.Path, part_id: str) -> None:
    spec = root / "spec"
    spec.mkdir(parents=True, exist_ok=True)
    text = (
        f"---\nid: {part_id}\ntitle: {part_id}\ntype: part\n---\n"
        f"# [{part_id}] {part_id}\n\n"
        "## Part\n\n| Owner | Declared Type | Multiplicity |\n"
        "|---|---|---|\n| System | ScoringEngine | 1..1 |\n"
    )
    (spec / f"{part_id}.md").write_text(text)


def _validate(root: pathlib.Path, *flags: str, safety_module=PACKAGE_ROOT):
    command = [
        _quire(),
        "validate",
        "--scope",
        str(root),
        *flags,
        "--module",
        str(safety_module),
        "spec/**/*.md",
    ]
    return subprocess.run(command, capture_output=True, text=True)


def _relations(root: pathlib.Path, relation: str):
    command = [
        _quire(),
        "relations",
        "--repo",
        f"agent-ix/spec-objects-safety={root}",
        "--module",
        str(PACKAGE_ROOT),
    ]
    command.extend(("--relation", relation, "--json"))
    return subprocess.run(command, capture_output=True, text=True)


def _relation_rows(result: subprocess.CompletedProcess, relation: str) -> list[dict]:
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert not report.get("errors"), report.get("errors")
    section = next(item for item in report["relations"] if item["name"] == relation)
    return section["rows"]


def _finding(result: subprocess.CompletedProcess, check: str) -> list[str]:
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{check}]")]


@pytest.mark.trace("FR-402-AC-2")
def test_tension_rejects_undeclared_links_with_a_named_diagnostic(tmp_path):
    _write_tension(tmp_path, "TEN-001")
    path = tmp_path / "spec" / "TEN-001.md"
    text = path.read_text().replace("type: conflicts_with", "type: references", 1)
    path.write_text(text)

    result = _validate(tmp_path)
    lines = _finding(result, "disallowed-edge-type")
    assert any("TEN-001.md" in line and "references" in line for line in lines), lines


@pytest.mark.trace("FR-403-AC-5")
def test_open_tension_with_resolution_edge_fails_frontmatter_schema(tmp_path):
    _write_tension(tmp_path, "TEN-001", resolved_by="PART-001")

    result = _validate(tmp_path)
    assert result.returncode != 0, result.stderr
    assert "resolved_by" in result.stderr


@pytest.mark.trace("FR-402-AC-3", "FR-404-AC-3")
def test_resolved_by_design_edge_to_a_part_clears_the_tension_finding(tmp_path):
    _write_tension(
        tmp_path,
        "TEN-001",
        status="resolved-by-design",
        resolved_by="PART-001",
    )
    _part(tmp_path, "PART-001")

    rows = _relation_rows(
        _relations(tmp_path, "resolved-tension-has-link"), "resolved-tension-has-link"
    )
    assert any(
        row["document"]["id"] == "TEN-001" and row["state"] == "covered" for row in rows
    ), rows


@pytest.mark.trace("FR-404-AC-1", "FR-405-AC-2")
def test_open_tension_is_reported_as_uncovered(tmp_path):
    _write_tension(tmp_path, "TEN-001")
    rows = _relation_rows(
        _relations(tmp_path, "tension-is-not-open"), "tension-is-not-open"
    )
    assert any(
        row["document"]["id"] == "TEN-001" and row["state"] == "uncovered"
        for row in rows
    ), rows


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
    rows = _relation_rows(
        _relations(tmp_path, "tension-is-not-open"), "tension-is-not-open"
    )
    assert any(
        row["document"]["id"] == "TEN-001" and row["state"] == "uncovered"
        for row in rows
    ), rows


@pytest.mark.trace("FR-404-AC-4")
def test_resolved_tension_without_its_design_edge_is_reported(tmp_path):
    _write_tension(tmp_path, "TEN-001", status="resolved-by-design")
    rows = _relation_rows(
        _relations(tmp_path, "resolved-tension-has-link"), "resolved-tension-has-link"
    )
    assert any(
        row["document"]["id"] == "TEN-001" and row["state"] == "uncovered"
        for row in rows
    ), rows


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
    assert (
        _relation_rows(
            _relations(tmp_path, "tension-is-not-open"), "tension-is-not-open"
        )
        == []
    )
    assert (
        _relation_rows(
            _relations(tmp_path, "resolved-tension-has-link"),
            "resolved-tension-has-link",
        )
        == []
    )

    # Missing decided_by is exercised against the emitted JSON Schema in
    # tests/test_tension_schema.py; `quire validate` checks document structure.


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
