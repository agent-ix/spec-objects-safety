"""Skeleton fixture tests (FR 005): the skeletons as executable typed fixtures,
and the negative fixtures that pin what the schemas and the engine refuse.

Two resolution paths are exercised and are kept distinct: `validate_document`
runs the module's own registry over one document, while `extract_semantic` runs
under a bundle index built from the skeleton frontmatter.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from tests.conftest import (
    KERNEL_SCALARS,
    NEGATIVE_DIR,
    PACKAGE_ROOT,
    REPO_ROOT,
    SKELETONS_DIR,
    frontmatter,
    locators,
    object_type,
    object_types,
)

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

ALTERNATES = ("hazard", "failure_mode")

# The columns of each type's scored table. A Properties row may not restate one
# of them: the table is the authored home of that fact, and a second home drifts.
SCORED_COLUMNS = {
    "hazard": {"severity", "likelihood", "rationale"},
    "failure_mode": {"effect", "cause", "detection"},
}

NAMED_NEGATIVE_CASES = {
    "hazard-no-identity-row.md",
    "failure_mode-no-identity-row.md",
    "properties-both-forms.md",
    "type-token-not-identifier.md",
    "hazard-no-assessment-table.md",
    "hazard-clause-without-fence.md",
    "failure_mode-analysis-missing-column.md",
}


def skeleton_paths() -> list:
    return sorted(SKELETONS_DIR.glob("*.md"))


def extract(quire_engine, module, bundle, path):
    text = path.read_text()
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": module,
            "path": str(path),
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-safety/{frontmatter(text)['id']}"
            ),
            "bundle": bundle,
        }
    )


@pytest.mark.trace("TC-048", "FR-005-AC-1")
def test_every_skeleton_validates_with_no_error(quire_engine, skeletons):
    assert len(skeletons) == 4
    for path in skeletons:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic.record-invalid" in e["message"]
        ], path.name


@pytest.mark.trace("TC-049", "FR-005-AC-2", "FR-005-CON-2")
def test_table_and_sysml_skeletons_extract_to_identical_fields(
    quire_engine, semantic_module, bundle_index
):
    for name in ALTERNATES:
        table = extract(
            quire_engine, semantic_module, bundle_index, SKELETONS_DIR / f"{name}.md"
        )
        fence = extract(
            quire_engine,
            semantic_module,
            bundle_index,
            SKELETONS_DIR / f"{name}.sysml.md",
        )
        assert table["fieldsForm"] == "table", name
        assert fence["fieldsForm"] == "fence", name
        assert table["fields"] == fence["fields"], name
        assert table["clauses"] == fence["clauses"] or [
            c["clauseId"] for c in table["clauses"]
        ] == [c["clauseId"] for c in fence["clauses"]], name


@pytest.mark.trace("TC-050", "FR-005-AC-3")
def test_under_the_bundle_index_every_skeleton_extracts_clean(
    quire_engine, semantic_module, bundle_index
):
    for path in skeleton_paths():
        record = extract(quire_engine, semantic_module, bundle_index, path)
        diagnostics = record.get("diagnostics", [])
        assert not [d for d in diagnostics if d.get("severity") == "error"], (
            path.name,
            diagnostics,
        )
        assert not [
            d for d in diagnostics if d.get("code") == "semantic.unresolved-type"
        ], (path.name, diagnostics)
        for decl in record.get("fields") or []:
            target = decl["type"]["target"]
            if target in KERNEL_SCALARS:
                continue
            assert target.startswith("ix://agent-ix/spec-objects-safety/"), (
                path.name,
                target,
            )


@pytest.mark.trace("TC-051", "FR-005-AC-4")
def test_availability_states_match_each_type(
    quire_engine, semantic_module, bundle_index
):
    for path in skeleton_paths():
        record = extract(quire_engine, semantic_module, bundle_index, path)
        actual = {
            kind: record["availability"][kind]["state"]
            for kind in ("fields", "clauses", "operations")
        }
        # Neither safety type declares operations: a hazard is a state and a
        # failure mode is a behaviour, and neither invokes anything.
        assert actual == {
            "fields": "available",
            "clauses": "available",
            "operations": "not_applicable",
        }, (path.name, actual)


@pytest.mark.trace("TC-052", "FR-005-AC-5")
def test_every_negative_fixture_fails_for_its_own_reason(quire_engine):
    fixtures = sorted(NEGATIVE_DIR.glob("*.md"))
    assert {p.name for p in fixtures} == NAMED_NEGATIVE_CASES
    seen: set[str] = set()
    for path in fixtures:
        text = path.read_text()
        front = frontmatter(text)
        assert front["because"], f"{path.name} does not say why it must fail"
        seen.add(front["expect"])
        result = quire_engine.validate_document(front["type"], str(PACKAGE_ROOT), text)
        assert not result["is_valid"], path.name
        messages = [e["message"] for e in result["errors"]]
        assert any(front["expect"] in m for m in messages), (path.name, messages)
        # The fixture must fail for its own reason, not merely with its token:
        # several of the seven surface as `semantic.record-invalid`.
        hit = next(m for m in messages if front["expect"] in m)
        assert len(hit) > len(
            front["expect"]
        ), f"{path.name}: the error carries no detail"
    assert (
        len(seen) >= 5
    ), f"the negative set exercises too few distinct refusals: {seen}"


@pytest.mark.trace("TC-053", "FR-005-AC-6")
def test_every_skeleton_heading_is_asserted_and_every_required_heading_is_present():
    for path in skeleton_paths():
        text = path.read_text()
        name = frontmatter(text)["object"]

        def heading_of(loc):
            return loc.get("after_heading") or loc.get("under_section")

        declared = locators(object_type(name))
        asserted = {heading_of(loc) for loc in declared.values() if heading_of(loc)}
        required = {
            heading_of(loc)
            for loc in declared.values()
            if loc.get("required") and heading_of(loc)
        }
        body = re.sub(r"^```.*?^```\s*$", "", text, flags=re.DOTALL | re.MULTILINE)
        headings = {
            m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.MULTILINE)
        }
        assert headings <= asserted, (path.name, headings - asserted)
        assert required <= headings, (path.name, required - headings)


@pytest.mark.trace("TC-054", "FR-005-AC-7")
def test_every_skeleton_is_placeholder_free():
    tokens = ("TODO", "TBD", "{{", "}}", "XXX", "FIXME", "lorem ipsum")
    for path in skeleton_paths():
        body = re.sub(
            r"^---\n.*?\n---\n", "", path.read_text(), count=1, flags=re.DOTALL
        )
        body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        for token in tokens:
            assert token.lower() not in body.lower(), (path.name, token)
        assert len(body.strip()) > 200, path.name


@pytest.mark.trace("TC-055", "FR-005-AC-8")
def test_skeleton_titles_are_distinct_identifiers_and_object_equals_type():
    titles: dict[str, str] = {}
    for path in skeleton_paths():
        front = frontmatter(path.read_text())
        title = front["title"]
        assert IDENTIFIER.match(title), (path.name, title)
        assert title not in KERNEL_SCALARS, (path.name, title)
        assert front["object"] == front["type"], path.name
        stem = path.stem.removesuffix(".sysml")
        owner = titles.setdefault(title, stem)
        assert owner == stem, f"{title} is used by both {owner} and {stem}"
    declared = {ot["name"] for ot in object_types()}
    assert set(titles.values()) == declared


@pytest.mark.trace("TC-056", "FR-005-AC-9")
def test_no_properties_row_restates_a_scored_column():
    """One fact, one home.

    The scored axes are authored in the `## Assessment` / `## Analysis` table
    and typed by `HazardAssessment` / `FailureAnalysis`. A Properties row with
    the same name would be a second place to write the same judgement, and the
    two would drift — the exact defect the module's own `traceability` model
    avoids by authoring the mitigation edge from one end only.
    """
    for path in skeleton_paths():
        text = path.read_text()
        name = frontmatter(text)["object"]
        section = re.search(r"^## Properties$(.*?)^## ", text, re.DOTALL | re.MULTILINE)
        assert section, f"{path.name} has no Properties section"
        declared = {
            row.split("|")[1].strip().lower()
            for row in section.group(1).splitlines()
            if row.startswith("|") and row.count("|") >= 5
        } | {
            line.split(":")[0].split()[-1].strip().lower()
            for line in section.group(1).splitlines()
            if line.strip().startswith(("attribute ", "ref item "))
        }
        clash = declared & SCORED_COLUMNS[name]
        assert not clash, f"{path.name}: Properties restates {sorted(clash)}"


@pytest.mark.trace("TC-057", "FR-005-AC-10", "FR-005-CON-3")
def test_a_missing_engine_fails_the_suite_and_nothing_skips(monkeypatch):
    """A skipped row is not coverage.

    The helper every semantic test goes through must FAIL when the engine is
    absent, naming the provisioning path and the issue that will remove the
    need for it — never `pytest.skip`, which reports a gate green while running
    nothing.
    """
    import builtins

    from tests import conftest

    real_import = builtins.__import__

    def refuse_quire(name, *args, **kwargs):
        if name == "quire":
            raise ImportError("no module named 'quire'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", refuse_quire)
    with pytest.raises(pytest.fail.Exception) as error:
        conftest.require_quire()
    monkeypatch.undo()
    message = str(error.value)
    assert "make dev-quire" in message
    assert "agent-ix/quire-rs#392" in message
    assert "skipped row is not coverage" in message

    # And no test in this suite reaches for a skip of its own. The tokens are
    # assembled rather than written out, so this scan does not trip over the
    # literal in its own source.
    banned = ("pytest." + "skip(", "@pytest.mark." + "skip", "skip" + "if")
    for path in sorted((REPO_ROOT / "tests").rglob("*.py")):
        source = path.read_text()
        for token in banned:
            assert token not in source, f"{path.name} carries `{token}`"


@pytest.mark.trace("TC-058", "FR-005-CON-2")
def test_a_properties_section_with_both_forms_is_refused(quire_engine):
    path = NEGATIVE_DIR / "properties-both-forms.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert not result["is_valid"]
    assert any(
        "semantic.properties-both-forms" in e["message"] for e in result["errors"]
    )


@pytest.mark.trace("TC-059", "FR-005-CON-1")
def test_the_branch_edits_no_corpus_repository_or_vendored_fixture():
    diff = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode != 0:  # pragma: no cover - a detached clone has no origin/main
        pytest.fail(f"cannot read the branch diff: {diff.stderr.strip()}")
    changed = [line for line in diff.stdout.splitlines() if line]
    assert changed, "the branch changes nothing"
    for path in changed:
        assert not path.startswith("corpus/"), path
        assert "fixtures/semantic-module" not in path, path
        assert "/vendor/" not in path, path
