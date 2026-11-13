"""FR-202, FR-203, FR-204 and FR-205: the chain edges and the estimate and
control links, over document bundles validated by the `quire` CLI.

Fixtures are this module's own skeletons plus the installed
`spec-objects-security` control skeleton and the `spec-artifacts-iso` FR and IT
skeletons. Nothing is copied into this repository.

`estimates` and `assumes` are verbs `spec-artifacts-iso` has not declared yet
(PLAT-1676), so the engine reports `UnknownEdgeType` for them as an advisory at
module load; every run below exits 0 regardless. FR-202-AC-2 and the resolved
incoming-edge half of FR-204-AC-1 need the `arises_from` inverse label and the
verb inverses from PLAT-1676 and are not asserted here until it lands.
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
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"

pytestmark = pytest.mark.integration

QUIRE_ENV = "QUIRE_BIN"
LOCAL = "ix://agent-ix/spec-objects-safety"


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


def _with_edges(text: str, edges) -> str:
    block = "".join(f"  - target: {t}\n    type: {v}\n" for v, t in edges)
    text = re.sub(r"^relationships:\n(?:  .*\n)+", "", text, count=1, flags=re.M)
    return (
        re.sub(r"\n---\n<!--", f"\nrelationships:\n{block}---\n<!--", text, count=1)
        if block
        else text
    )


def _write(root, name, source, new_id, old_id, edges=()):
    text = (source / f"{name}.md").read_text().replace(old_id, new_id)
    (root / f"{new_id}.md").write_text(_with_edges(text, edges))


def hazard(root, hid="HAZ-001"):
    _write(root, "hazard", SKELETONS_DIR, hid, "HAZ-001")


def situation(root, sid, *arises_from):
    _write(
        root,
        "hazardous_situation",
        SKELETONS_DIR,
        sid,
        "SIT-001",
        [("arises_from", t) for t in arises_from],
    )


def harm(root, mid, *arises_from):
    _write(
        root,
        "harm",
        SKELETONS_DIR,
        mid,
        "HARM-001",
        [("arises_from", t) for t in arises_from],
    )


def estimate(root, eid, phase="post_control", severity="critical", **edges):
    text = (SKELETONS_DIR / "risk_estimate.md").read_text().replace("EST-001", eid)
    for placeholder, value in (
        ("<pre_control | post_control>", phase),
        ("<severity>", severity),
        ("<probability>", "remote"),
        ("<why this person judges it so>", "Survivable."),
        ("<person>", "A. Person"),
        ("<date or UTC timestamp>", "2026-11-12"),
    ):
        text = text.replace(placeholder, value)
    pairs = [("estimates", t) for t in edges.get("estimates", ())]
    pairs += [("assumes", t) for t in edges.get("assumes", ())]
    (root / f"{eid}.md").write_text(_with_edges(text, pairs))


def control(root, cid="CTRL-001"):
    text = (_module("spec_objects_security") / "skeletons" / "control.md").read_text()
    (root / f"{cid}.md").write_text(text.replace("CTRL-001", cid))


DECISION_FILL = {
    "<undecided, accepted or not_accepted>": "accepted",
    "<why the person decided so>": "Within the policy.",
    "<person who decided, empty while undecided>": "A. Person",
    "<the benefit that justifies the residual risks>": "Faster braking.",
    "<product>": "Brake controller",
}


def decision_doc(root, kind, did, old_id, edges=()):
    """A filled residual_risk, benefit_risk or evaluation carrying `edges`."""
    text = (SKELETONS_DIR / f"{kind}.md").read_text().replace(old_id, did)
    for placeholder, value in DECISION_FILL.items():
        text = text.replace(placeholder, value)
    (root / f"{did}.md").write_text(_with_edges(text, edges))


def residual_risk(root, rid, *, estimate=(), policy=()):
    edges = [("estimate", t) for t in estimate] + [("references", t) for t in policy]
    decision_doc(root, "residual_risk", rid, "RR-001", edges)


def benefit_risk(root, bid, *covers):
    decision_doc(
        root, "benefit_risk", bid, "BR-001", [("references", t) for t in covers]
    )


def evaluation(root, oid, *considers):
    decision_doc(
        root,
        "overall_residual_risk_evaluation",
        oid,
        "ORE-001",
        [("references", t) for t in considers],
    )


def policy(root, pid="POL-001"):
    text = (
        (SKELETONS_DIR / "acceptability_policy.md").read_text().replace("POL-001", pid)
    )
    for placeholder, value in (
        ("<severity level>", "minor"),
        ("<probability level>", "rare"),
        ("<region>", "acceptable"),
        ("<true or false>", "false"),
    ):
        text = text.replace(placeholder, value)
    (root / f"{pid}.md").write_text(text)


def requirement(root, rid, kind, edge, target):
    """An iso FR or IT (a TC would do) carrying one edge to `target`."""
    text = (_module("spec_artifacts_iso") / "skeletons" / f"{kind}.md").read_text()
    text = text.replace(f"{kind.upper()}-001", rid)
    # The skeleton's example body links would be dangling references.
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./|\./)[^)]*\)", r"\1", text)
    (root / f"{rid}.md").write_text(_with_edges(text, [(edge, target)]))


def validate(root, *flags):
    return subprocess.run(
        [
            _quire(),
            "validate",
            "--okf",
            *flags,
            "--module",
            str(_module("spec_artifacts_iso")),
            "--module",
            str(_module("spec_objects_security")),
            "--module",
            str(PACKAGE_ROOT),
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def findings(result, check):
    return [line for line in result.stderr.splitlines() if line.endswith(f"[{check}]")]


def clean_of_edge_errors(result):
    assert result.returncode == 0, result.stderr
    for token in ("disallowed-edge-target", "dangling-reference", "[unknown-type]"):
        assert token not in result.stderr, result.stderr


@pytest.mark.trace("FR-202-AC-1")
def test_a_hazard_situation_harm_chain_validates(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-202-AC-7")
def test_a_situation_may_arise_from_two_hazards(tmp_path):
    hazard(tmp_path, "HAZ-001")
    hazard(tmp_path, "HAZ-002")
    situation(tmp_path, "SIT-001", "HAZ-001", "HAZ-002")
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-202-AC-3")
def test_a_chain_edge_to_another_type_is_disallowed_naming_the_type(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    situation(tmp_path, "SIT-002", "HARM-001")
    harm(tmp_path, "HARM-002", "HAZ-001")
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("SIT-002:" in line and "'harm'" in line for line in lines), lines
    assert any("HARM-002:" in line and "'hazard'" in line for line in lines), lines


@pytest.mark.trace("FR-202-AC-8")
def test_strict_validate_fails_on_an_undeclared_arises_from_target(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-999")
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(findings(result, "dangling-reference")), "")
    assert "SIT-001.md" in line and "arises_from" in line and "HAZ-999" in line, line


@pytest.mark.trace("FR-202-AC-8")
def test_strict_validate_fails_on_a_harm_that_names_an_undeclared_situation(tmp_path):
    harm(tmp_path, "HARM-001", "SIT-999")
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(findings(result, "dangling-reference")), "")
    assert "HARM-001.md" in line and "arises_from" in line and "SIT-999" in line, line


@pytest.mark.trace("FR-203-AC-8")
def test_an_estimates_edge_to_a_hazard_is_disallowed_naming_the_type(tmp_path):
    hazard(tmp_path)
    estimate(tmp_path, "EST-001", estimates=["HAZ-001"])
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("EST-001:" in line and "'hazard'" in line for line in lines), lines


@pytest.mark.trace("FR-203-AC-10", "FR-203-AC-11", "FR-204-AC-6")
def test_estimates_of_one_situation_and_of_two_validate_without_a_choice(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    situation(tmp_path, "SIT-002", "HAZ-001")
    estimate(tmp_path, "EST-001", "pre_control", estimates=["SIT-001", "SIT-002"])
    control(tmp_path)
    estimate(
        tmp_path, "EST-002", "post_control", estimates=["SIT-001"], assumes=["CTRL-001"]
    )
    result = validate(tmp_path)
    clean_of_edge_errors(result)
    assert findings(result, "post-control-without-control") == [], result.stderr
    assert findings(result, "estimate-without-situation") == [], result.stderr
    # The engine's own "selected because `phase` is ..." wording is not a choice
    # among estimates.
    stderr = result.stderr.replace("selected because", "")
    for word in ("primary", "preferred", "selected", "upper"):
        assert word not in stderr, result.stderr


@pytest.mark.trace("FR-203-AC-12")
def test_a_hazard_assessment_and_an_estimate_of_its_situation_coexist(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    estimate(
        tmp_path, "EST-001", "pre_control", severity="marginal", estimates=["SIT-001"]
    )
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-204-AC-1")
def test_a_post_control_estimate_may_assume_a_control(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    control(tmp_path)
    estimate(tmp_path, "EST-001", estimates=["SIT-001"], assumes=["CTRL-001"])
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-204-AC-3")
def test_an_assumes_edge_to_a_hazard_is_disallowed_naming_hazard(tmp_path):
    hazard(tmp_path)
    estimate(tmp_path, "EST-001", assumes=["HAZ-001"])
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("EST-001:" in line and "'hazard'" in line for line in lines), lines


@pytest.mark.trace("FR-204-AC-4")
def test_strict_validate_fails_on_an_undeclared_assumes_target(tmp_path):
    estimate(tmp_path, "EST-001", assumes=["CTRL-999"])
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(findings(result, "dangling-reference")), "")
    assert "EST-001.md" in line and "assumes" in line and "CTRL-999" in line, line


@pytest.mark.trace("FR-204-AC-5")
def test_a_post_control_value_worse_than_the_pre_control_value_is_not_rejected(
    tmp_path,
):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    estimate(
        tmp_path, "EST-001", "pre_control", severity="minor", estimates=["SIT-001"]
    )
    estimate(
        tmp_path,
        "EST-002",
        "post_control",
        severity="catastrophic",
        estimates=["SIT-001"],
    )
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-205-AC-4")
def test_strict_validate_fails_on_an_undeclared_satisfies_target(tmp_path):
    requirement(tmp_path, "FR-901", "fr", "satisfies", f"{LOCAL}/CTRL-999")
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    lines = findings(result, "dangling-reference")
    assert any(
        "FR-901.md" in x and "satisfies" in x and "CTRL-999" in x for x in lines
    ), lines


@pytest.mark.trace("FR-205-AC-1", "FR-205-AC-2")
def test_requirement_and_verification_edges_resolve_to_a_declared_control(tmp_path):
    """The edges resolve to the control: dropping the control makes the same
    edges dangle, so the clean run is evidence the target was found."""
    requirement(tmp_path, "FR-901", "fr", "satisfies", f"{LOCAL}/CTRL-001")
    requirement(tmp_path, "IT-901", "it", "verifies", f"{LOCAL}/CTRL-001")

    def dangling():
        result = validate(tmp_path, "--strict")
        assert "disallowed-edge-target" not in result.stderr, result.stderr
        return [
            line
            for line in findings(result, "dangling-reference")
            if "CTRL-001" in line and ("'satisfies'" in line or "'verifies'" in line)
        ]

    assert len(dangling()) == 2
    control(tmp_path)
    assert dangling() == []


@pytest.mark.trace("FR-202-AC-9")
def test_a_cycle_through_the_chain_edges_is_reported(tmp_path):
    situation(tmp_path, "SIT-001", "HARM-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    result = validate(tmp_path)
    assert findings(result, "cyclic-arises_from"), result.stderr


def _count(result, check):
    return len(findings(result, check))


@pytest.mark.trace("FR-203-AC-9")
def test_an_estimate_with_no_estimates_edge_is_reported_once_and_the_edge_clears_it(
    tmp_path,
):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    estimate(tmp_path, "EST-001", "pre_control")
    result = validate(tmp_path)
    lines = findings(result, "estimate-without-situation")
    assert len(lines) == 1 and "EST-001" in lines[0], result.stderr
    assert lines[0].startswith("warning:") and result.returncode == 0

    estimate(tmp_path, "EST-001", "pre_control", estimates=["SIT-001"])
    assert _count(validate(tmp_path), "estimate-without-situation") == 0


@pytest.mark.trace("FR-204-AC-2")
def test_a_post_control_estimate_with_no_control_is_reported_once_and_assumes_clears_it(
    tmp_path,
):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    control(tmp_path)
    estimate(tmp_path, "EST-001", "post_control", estimates=["SIT-001"])
    result = validate(tmp_path)
    lines = findings(result, "post-control-without-control")
    assert len(lines) == 1 and "EST-001" in lines[0], result.stderr
    assert lines[0].startswith("warning:") and result.returncode == 0

    estimate(
        tmp_path, "EST-001", "post_control", estimates=["SIT-001"], assumes=["CTRL-001"]
    )
    assert _count(validate(tmp_path), "post-control-without-control") == 0


@pytest.mark.trace("FR-204-AC-7")
def test_a_pre_control_estimate_is_never_reported_for_missing_controls(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    estimate(tmp_path, "EST-001", "pre_control", estimates=["SIT-001"])
    assert _count(validate(tmp_path), "post-control-without-control") == 0


@pytest.mark.trace("FR-204-AC-8")
def test_the_post_control_finding_is_tunable_on_its_own_key(tmp_path):
    estimate(tmp_path, "EST-001", "post_control")
    assert validate(tmp_path).returncode == 0
    result = validate(
        tmp_path, "--severity", "trace:post-control-without-control=error"
    )
    assert result.returncode != 0, result.stderr
    assert _count(result, "post-control-without-control") == 1


@pytest.mark.trace("FR-204-AC-9")
def test_an_assumes_edge_to_an_undeclared_id_does_not_satisfy_the_relation(tmp_path):
    estimate(tmp_path, "EST-001", "post_control", assumes=["CTRL-999"])
    assert _count(validate(tmp_path), "post-control-without-control") == 1


# ── FR-103 / FR-106 / FR-107: residual-risk edges ───────────────────────────


def risk_chain(root):
    hazard(root)
    situation(root, "SIT-001", "HAZ-001")
    control(root)
    estimate(root, "EST-001", estimates=["SIT-001"], assumes=["CTRL-001"])
    policy(root)


@pytest.mark.trace("FR-103-AC-1")
def test_a_residual_risk_naming_an_estimate_and_a_policy_validates(tmp_path):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"])
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-103-AC-4")
def test_an_estimate_edge_to_another_type_is_disallowed_naming_the_type(tmp_path):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["HAZ-001"])
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("RR-001:" in line and "'hazard'" in line for line in lines), lines


@pytest.mark.trace("FR-103-AC-4")
def test_a_policy_edge_to_another_type_is_disallowed_naming_the_type(tmp_path):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["EST-001"])
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("RR-001:" in line and "'risk_estimate'" in line for line in lines), lines


@pytest.mark.trace("FR-103-AC-4")
def test_strict_validate_fails_on_an_undeclared_estimate(tmp_path):
    residual_risk(tmp_path, "RR-001", estimate=["EST-999"])
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(findings(result, "dangling-reference")), "")
    assert "RR-001.md" in line and "estimate" in line and "EST-999" in line, line


@pytest.mark.trace("FR-106-AC-1")
def test_a_benefit_risk_covering_two_residual_risks_validates(tmp_path):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"])
    residual_risk(tmp_path, "RR-002", estimate=["EST-001"], policy=["POL-001"])
    benefit_risk(tmp_path, "BR-001", "RR-001", "RR-002")
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-106-AC-4")
def test_strict_validate_fails_on_an_undeclared_covered_risk(tmp_path):
    benefit_risk(tmp_path, "BR-001", "RR-999")
    result = validate(tmp_path, "--strict")
    assert result.returncode != 0, result.stderr
    line = next(iter(findings(result, "dangling-reference")), "")
    assert "BR-001.md" in line and "RR-999" in line, line


@pytest.mark.trace("FR-106-AC-6")
def test_a_benefit_risk_reference_to_a_hazard_is_disallowed_naming_hazard(tmp_path):
    hazard(tmp_path)
    benefit_risk(tmp_path, "BR-001", "HAZ-001")
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("BR-001:" in line and "'hazard'" in line for line in lines), lines


@pytest.mark.trace("FR-107-AC-1")
def test_an_evaluation_considering_residual_risks_and_benefit_risks_validates(tmp_path):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"])
    benefit_risk(tmp_path, "BR-001", "RR-001")
    evaluation(tmp_path, "ORE-001", "RR-001", "BR-001")
    clean_of_edge_errors(validate(tmp_path))


@pytest.mark.trace("FR-107-AC-1")
def test_an_evaluation_reference_to_a_hazard_is_disallowed_naming_hazard(tmp_path):
    hazard(tmp_path)
    evaluation(tmp_path, "ORE-001", "HAZ-001")
    lines = findings(validate(tmp_path), "disallowed-edge-target")
    assert any("ORE-001:" in line and "'hazard'" in line for line in lines), lines


def _warns_once_then_clears(tmp_path, check, name, build_without, build_with):
    build_without()
    result = validate(tmp_path)
    lines = findings(result, check)
    assert len(lines) == 1 and name in lines[0], result.stderr
    assert lines[0].startswith("warning:") and result.returncode == 0
    build_with()
    assert _count(validate(tmp_path), check) == 0


@pytest.mark.trace("FR-103-AC-4")
def test_a_residual_risk_with_no_estimate_is_reported_once_and_the_edge_clears_it(
    tmp_path,
):
    risk_chain(tmp_path)
    _warns_once_then_clears(
        tmp_path,
        "residual-risk-without-estimate",
        "RR-001",
        lambda: residual_risk(tmp_path, "RR-001", policy=["POL-001"]),
        lambda: residual_risk(
            tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"]
        ),
    )


@pytest.mark.trace("FR-103-AC-4")
def test_a_residual_risk_with_no_policy_is_reported_once_and_the_edge_clears_it(
    tmp_path,
):
    risk_chain(tmp_path)
    _warns_once_then_clears(
        tmp_path,
        "residual-risk-without-policy",
        "RR-001",
        lambda: residual_risk(tmp_path, "RR-001", estimate=["EST-001"]),
        lambda: residual_risk(
            tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"]
        ),
    )


@pytest.mark.trace("FR-106-AC-2")
def test_a_benefit_risk_with_no_residual_risk_is_reported_once_and_the_edge_clears_it(
    tmp_path,
):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"])
    _warns_once_then_clears(
        tmp_path,
        "benefit-risk-without-risk",
        "BR-001",
        lambda: benefit_risk(tmp_path, "BR-001"),
        lambda: benefit_risk(tmp_path, "BR-001", "RR-001"),
    )


@pytest.mark.trace("FR-107-AC-1")
def test_an_evaluation_considering_nothing_is_reported_once_and_a_reference_clears_it(
    tmp_path,
):
    risk_chain(tmp_path)
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"], policy=["POL-001"])
    _warns_once_then_clears(
        tmp_path,
        "evaluation-without-considered-record",
        "ORE-001",
        lambda: evaluation(tmp_path, "ORE-001"),
        lambda: evaluation(tmp_path, "ORE-001", "RR-001"),
    )


@pytest.mark.trace("FR-103-AC-4")
def test_a_residual_risk_relation_check_is_tunable_on_its_own_key(tmp_path):
    residual_risk(tmp_path, "RR-001", policy=["POL-001"])
    result = validate(
        tmp_path, "--severity", "trace:residual-risk-without-estimate=error"
    )
    assert result.returncode != 0, result.stderr
    assert _count(result, "residual-risk-without-estimate") == 1


# ── FR-301, FR-303, FR-304: completeness relations and the cycle check ──────


def chain(root):
    hazard(root)
    situation(root, "SIT-001", "HAZ-001")
    harm(root, "HARM-001", "SIT-001")


CHAIN_CHECKS = (
    "hazard-without-situation",
    "situation-without-hazard",
    "situation-without-harm",
)


@pytest.mark.trace("FR-301-AC-1", "FR-301-AC-2")
def test_a_complete_chain_yields_no_chain_finding(tmp_path):
    chain(tmp_path)
    result = validate(tmp_path)
    assert result.returncode == 0, result.stderr
    for check in CHAIN_CHECKS:
        assert findings(result, check) == [], result.stderr


@pytest.mark.trace("FR-301-AC-3")
def test_a_hazard_with_no_situation_is_reported_by_name(tmp_path):
    hazard(tmp_path)
    harm(tmp_path, "HARM-001")
    lines = findings(validate(tmp_path), "hazard-without-situation")
    assert len(lines) == 1 and "HAZ-001" in lines[0], lines


@pytest.mark.trace("FR-301-AC-4")
def test_a_situation_with_no_harm_is_reported_and_its_hazard_is_not(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    result = validate(tmp_path)
    lines = findings(result, "situation-without-harm")
    assert len(lines) == 1 and "SIT-001" in lines[0], lines
    assert findings(result, "hazard-without-situation") == [], result.stderr


@pytest.mark.trace("FR-301-AC-5")
def test_free_text_situation_on_a_hazard_does_not_satisfy_the_relation(tmp_path):
    hazard(tmp_path)
    path = tmp_path / "HAZ-001.md"
    path.write_text(
        path.read_text().replace(
            "\n---\n<!--", "\ncontext:\n  situation: braking at speed\n---\n<!--", 1
        )
    )
    lines = findings(validate(tmp_path), "hazard-without-situation")
    assert len(lines) == 1 and "HAZ-001" in lines[0], lines


@pytest.mark.trace("FR-301-AC-6")
def test_a_harm_arising_from_an_undeclared_situation_does_not_satisfy(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-999")
    lines = findings(validate(tmp_path), "situation-without-harm")
    assert len(lines) == 1 and "SIT-001" in lines[0], lines


@pytest.mark.trace("FR-301-AC-7")
def test_the_hazard_without_situation_check_alone_is_escalated(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001")
    harm(tmp_path, "HARM-001")
    assert validate(tmp_path).returncode == 0
    for check in CHAIN_CHECKS:
        assert len(findings(validate(tmp_path), check)) == 1, check
    tuned = validate(tmp_path, "--severity", "trace:hazard-without-situation=error")
    assert tuned.returncode != 0, tuned.stderr
    for check in CHAIN_CHECKS:
        line = findings(tuned, check)
        assert len(line) == 1, check
        is_warning = line[0].startswith("warning:")
        assert is_warning == (check != "hazard-without-situation"), line


@pytest.mark.trace("FR-301-AC-8")
def test_only_the_situation_without_a_harm_is_reported(tmp_path):
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    situation(tmp_path, "SIT-002", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    lines = findings(validate(tmp_path), "situation-without-harm")
    assert len(lines) == 1 and "SIT-002" in lines[0], lines


@pytest.mark.trace("FR-301-AC-9")
def test_a_situation_with_no_hazard_is_reported_until_the_edge_is_added(tmp_path):
    situation(tmp_path, "SIT-001")
    lines = findings(validate(tmp_path), "situation-without-hazard")
    assert len(lines) == 1 and "SIT-001" in lines[0], lines
    hazard(tmp_path)
    situation(tmp_path, "SIT-001", "HAZ-001")
    assert findings(validate(tmp_path), "situation-without-hazard") == []


@pytest.mark.trace("FR-303-AC-1", "FR-303-AC-2")
def test_a_post_control_estimate_without_a_residual_risk_is_reported(tmp_path):
    estimate(tmp_path, "EST-001", "post_control")
    result = validate(tmp_path)
    assert result.returncode == 0, result.stderr
    lines = findings(result, "post-control-estimate-without-decision")
    assert len(lines) == 1 and "EST-001" in lines[0], lines


@pytest.mark.trace("FR-303-AC-3")
def test_a_pre_control_estimate_is_not_reported(tmp_path):
    estimate(tmp_path, "EST-001", "pre_control")
    lines = findings(validate(tmp_path), "post-control-estimate-without-decision")
    assert lines == [], lines


@pytest.mark.trace("FR-303-AC-4")
@pytest.mark.parametrize("decision", ["undecided", "accepted"])
def test_any_residual_risk_record_removes_the_decision_finding(tmp_path, decision):
    estimate(tmp_path, "EST-001", "post_control")
    residual_risk(tmp_path, "RR-001", estimate=["EST-001"])
    if decision == "undecided":
        path = tmp_path / "RR-001.md"
        path.write_text(path.read_text().replace("accepted", "undecided"))
    lines = findings(validate(tmp_path), "post-control-estimate-without-decision")
    assert lines == [], lines


@pytest.mark.trace("FR-304-AC-2")
def test_a_two_document_cycle_is_reported_once_naming_both(tmp_path):
    hazard_text = (SKELETONS_DIR / "hazard.md").read_text()
    (tmp_path / "HAZ-001.md").write_text(
        _with_edges(hazard_text, [("arises_from", f"{LOCAL}/SIT-001")])
    )
    situation(tmp_path, "SIT-001", "HAZ-001")
    lines = findings(validate(tmp_path), "cyclic-arises_from")
    assert len(lines) == 1, lines
    assert "HAZ-001" in lines[0] and "SIT-001" in lines[0], lines


@pytest.mark.trace("FR-304-AC-3")
def test_a_three_document_cycle_is_reported_once(tmp_path):
    hazard_text = (SKELETONS_DIR / "hazard.md").read_text()
    (tmp_path / "HAZ-001.md").write_text(
        _with_edges(hazard_text, [("arises_from", f"{LOCAL}/HARM-001")])
    )
    situation(tmp_path, "SIT-001", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    assert len(findings(validate(tmp_path), "cyclic-arises_from")) == 1


@pytest.mark.trace("FR-303-AC-5")
def test_a_phase_only_in_the_body_is_not_selected_by_the_relation(tmp_path):
    estimate(tmp_path, "EST-001", "post_control")
    assert (
        len(findings(validate(tmp_path), "post-control-estimate-without-decision")) == 1
    )
    path = tmp_path / "EST-001.md"
    text = path.read_text().replace("phase: post_control\n", "", 1)
    path.write_text(
        text.replace("## Judgement\n", "## Judgement\n\nphase: post_control\n", 1)
    )
    result = validate(tmp_path)
    assert findings(result, "post-control-estimate-without-decision") == []


@pytest.mark.trace("FR-303-AC-5")
def test_the_phase_selector_is_declared_vocabulary_in_a_bundle_with_no_estimate(
    tmp_path,
):
    hazard(tmp_path)
    advisories = findings(validate(tmp_path), "undeclared-relation-vocabulary")
    assert not [line for line in advisories if "'phase'" in line], advisories


@pytest.mark.trace("FR-205-AC-3")
def test_a_satisfied_control_with_no_verifies_edge_raises_no_missing_verification(
    tmp_path,
):
    control(tmp_path)
    requirement(tmp_path, "FR-901", "fr", "satisfies", f"{LOCAL}/CTRL-001")
    result = validate(tmp_path)
    assert result.returncode == 0, result.stderr
    assert not [x for x in result.stderr.splitlines() if "verif" in x.lower()]


@pytest.mark.trace("FR-304-AC-4")
def test_an_acyclic_chain_yields_no_cycle_finding(tmp_path):
    _write(tmp_path, "failure_mode", SKELETONS_DIR, "FM-001", "FM-001")
    _write(
        tmp_path,
        "hazard",
        SKELETONS_DIR,
        "HAZ-001",
        "HAZ-001",
        [("arises_from", f"{LOCAL}/FM-001")],
    )
    situation(tmp_path, "SIT-001", "HAZ-001")
    harm(tmp_path, "HARM-001", "SIT-001")
    assert findings(validate(tmp_path), "cyclic-arises_from") == []
