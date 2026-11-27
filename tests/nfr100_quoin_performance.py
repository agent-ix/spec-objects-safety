"""Portable release-bound check for Quoin's residual-risk report.

Run explicitly with QUOIN_BIN pointing at the release CLI under test:
`QUOIN_BIN=/path/to/quoin pytest tests/nfr100_quoin_performance.py`.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import time

import pytest

from tests.conftest import PACKAGE_ROOT


def _write_record(
    scope: pathlib.Path, record_id: str, kind: str, frontmatter: str, body: str
) -> None:
    text = (
        f'---\nid: {record_id}\ntitle: "{record_id}"\ntype: {kind}\n'
        f"object: {kind}\n{frontmatter}---\n# [{record_id}] {record_id}\n\n"
        f"{body}\n## Properties\n\n"
        "| Field | Type | Multiplicity | Constraints |\n"
        "|---|---|---|---|\n| record_id | UUID | 1..1 | identity |\n"
    )
    (scope / f"{record_id}.md").write_text(text)


def _write_5000_residual_risks(scope: pathlib.Path) -> None:
    _write_record(
        scope,
        "POL-1",
        "acceptability_policy",
        "",
        "## Severity levels\n\n| Severity level |\n| --- |\n| Serious |\n\n"
        "## Probability levels\n\n| Probability level |\n| --- |\n| Likely |\n\n"
        "## Regions\n\n| Region | Outside acceptable |\n| --- | --- |\n"
        "| High | true |\n\n"
        "## Cells\n\n| Severity | Probability | Region |\n| --- | --- | --- |\n"
        "| Serious | Likely | High |\n",
    )
    _write_record(
        scope,
        "EST-1",
        "risk_estimate",
        "phase: post_control\n",
        "## Judgement\n\n| Severity | Probability | Rationale |\n| --- | --- | --- |\n"
        "| Serious | Likely | why |\n\n## Provenance\n\n"
        "| Asserted by | Asserted at |\n| --- | --- |\n| Pat | 2026-01-01 |\n",
    )
    for index in range(5_000):
        _write_record(
            scope,
            f"RR-{index:05}",
            "residual_risk",
            "relationships:\n  - target: EST-1\n    type: estimate\n"
            "  - target: POL-1\n    type: references\n",
            "## Determination\n\n| Decision | Rationale | Decided by |\n"
            "| --- | --- | --- |\n| accepted | r | Pat |\n",
        )


def _quoin_executable() -> pathlib.Path:
    configured = os.environ.get("QUOIN_BIN")
    if not configured:
        pytest.fail("QUOIN_BIN must name the release Quoin executable")
    executable = pathlib.Path(configured)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        pytest.fail(f"QUOIN_BIN does not name an executable file: {configured}")
    return executable


@pytest.mark.trace("NFR-100-AC-3", "NFR-100-M-1")
def test_one_report_over_5000_residual_risks_finishes_within_10_seconds(tmp_path):
    _write_5000_residual_risks(tmp_path)
    executable = _quoin_executable()

    started = time.perf_counter()
    result = subprocess.run(
        [
            str(executable),
            "risk",
            "discrepancies",
            str(tmp_path),
            "--module",
            str(PACKAGE_ROOT),
            "--no-project-config",
            "--format",
            "json",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    elapsed = time.perf_counter() - started
    print(f"Quoin report over 5,000 residual risks took {elapsed:.3f}s")

    assert result.returncode == 0, result.stderr
    findings = json.loads(result.stdout)["findings"]
    assert len(findings) == 5_000
    assert findings[0]["refs"]["residual_risk"] == "RR-00000"
    assert findings[-1]["refs"]["residual_risk"] == "RR-04999"
    assert elapsed <= 10, f"5,000-record report took {elapsed:.3f}s (limit: 10s)"
