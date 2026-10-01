"""Shared fixtures for the module's test suite.

Two policies are enforced here and nowhere else:

* **The engine is a hard dependency of the semantic rows.** ``quire`` is a dev
  dependency resolved from ``internal-pypi`` (``poetry install``). When it is
  absent the semantic tests **fail**; they never skip, because a skipped row
  is not coverage (FR 005 CON-3).
* **The emitted schemas are read from the committed tree**, and every ``$ref``
  to semantic-core resolves against the package the toolchain installs, so a
  record test validates against the real bytes.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_safety"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"
TYPESPEC_SOURCE = REPO_ROOT / "typespec" / "main.tsp"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
NEGATIVE_DIR = FIXTURES_DIR / "negative"
SEMANTIC_CORE_DIR = (
    REPO_ROOT
    / "node_modules"
    / "@agent-ix"
    / "semantic-core"
    / "generated"
    / "json-schema"
)

QUIRE_MISSING = (
    "the Quire wheel exposing `extract_semantic` is not installed in this "
    "environment. Run `poetry install` (quire is a dev dependency from "
    "internal-pypi). The semantic tests fail rather than skip, because a "
    "skipped row is not coverage."
)

OBJECT_TYPES = ("hazard", "failure_mode")

MODEL_OF = {"hazard": "Hazard", "failure_mode": "FailureMode"}

SUPPORT_MODELS = (
    "IdentityField",
    "HazardAssessment",
    "HazardContext",
    "FailureAnalysis",
    "Provenance",
    "EvidenceRef",
    "Severity",
    "Likelihood",
    "Exposure",
    "Controllability",
    "Detection",
    "EpistemicState",
    "LifecycleStatus",
)

KERNEL_SCALARS = {
    "UUID",
    "Boolean",
    "Integer",
    "Decimal",
    "String",
    "Timestamp",
    "Duration",
    "Bytes",
    "JsonObject",
}

# The ordinal scales, and the epistemic members every one of them also admits.
SCALES = {
    "Severity": ["negligible", "marginal", "critical", "catastrophic"],
    "Likelihood": [
        "incredible",
        "improbable",
        "remote",
        "occasional",
        "probable",
        "frequent",
    ],
    "Exposure": ["E0", "E1", "E2", "E3", "E4"],
    "Controllability": ["C0", "C1", "C2", "C3"],
    "Detection": ["none", "indirect", "direct", "automatic"],
}
EPISTEMIC = ["unknown", "not_assessed", "not_applicable"]


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST_PATH.read_text())


MODULE_BASE = "https://schemas.agent-ix.org/agent-ix/spec-objects-safety/"
SEMANTIC_CORE_BASE = (
    "https://schemas.agent-ix.org/semantic-core/"
    f"{load_manifest()['semantic']['semantic_core']}/"
)


def object_types() -> list[dict[str, Any]]:
    return load_manifest()["object_types"]


def object_type(name: str) -> dict[str, Any]:
    return next(ot for ot in object_types() if ot["name"] == name)


def locators(ot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    body = ot.get("body_extraction") or {}
    return ((body.get("yield_pattern") or {}).get("match")) or {}


def frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert match, "document has no frontmatter"
    return yaml.safe_load(match.group(1))


def schema_of(model: str) -> dict[str, Any]:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


def shipped_schema_paths() -> list[pathlib.Path]:
    return sorted(SCHEMAS_DIR.glob("*.json"))


def require_quire():
    """Import quire, or fail the test naming the provisioning path."""
    try:
        import quire
    except (
        ImportError
    ) as error:  # pragma: no cover - exercised by the missing-engine test
        pytest.fail(f"{QUIRE_MISSING} (import error: {error})")
    if not hasattr(quire, "extract_semantic"):  # pragma: no cover - missing-engine path
        pytest.fail(
            f"`extract_semantic` is missing from the installed quire: {QUIRE_MISSING}"
        )
    return quire


@pytest.fixture(scope="session")
def quire_engine():
    return require_quire()


@pytest.fixture(scope="session")
def manifest() -> dict[str, Any]:
    return load_manifest()


@pytest.fixture(scope="session")
def semantic_block(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["semantic"]


@pytest.fixture(scope="session")
def semantic_module(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """The `module` block `extract_semantic` takes, derived from the manifest."""
    return {
        "contractVersion": semantic_block["contract_version"],
        "semanticCore": semantic_block["semantic_core"],
        "package": semantic_block["package"],
        "exports": semantic_block["exports"],
        "imports": semantic_block["imports"],
        "compatibilityPosture": semantic_block["compatibility_posture"],
        "legacyForms": semantic_block["legacy_forms"],
    }


@pytest.fixture(scope="session")
def skeletons() -> list[pathlib.Path]:
    return sorted(SKELETONS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def bundle_index(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """A bundle index built from the skeleton frontmatter (FR 005 AC-3)."""
    objects: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        front = frontmatter(path.read_text())
        if front["id"] in seen:
            continue
        seen.add(front["id"])
        objects.append({"id": front["id"], "names": [front["id"], front["title"]]})
    return {
        "package": semantic_block["package"],
        "objects": objects,
        "enumerations": [],
        "imports": {},
    }


@pytest.fixture(scope="session")
def schema_registry():
    """A 2020-12 validator factory over the shipped schemas plus semantic-core.

    Every `$ref` resolves locally: module models from the committed `schemas/`
    directory, grammar models from the semantic-core package the pinned
    toolchain installs.
    """
    from referencing import Registry, Resource

    if not SEMANTIC_CORE_DIR.is_dir():
        pytest.fail(
            "@agent-ix/semantic-core is not installed, so `$ref`s to the grammar "
            "cannot resolve. Run `make semantic-install` (FR 002 CON-4: `@agent-ix` "
            "resolves from GitHub Packages)."
        )
    resources = []
    for path in shipped_schema_paths():
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        uri = schema.get("$id") or f"{SEMANTIC_CORE_BASE}{path.name}"
        resources.append((uri, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def validator_for(model: str):
        from jsonschema import Draft202012Validator

        return Draft202012Validator(schema_of(model), registry=registry)

    return validator_for


@pytest.fixture(scope="session")
def hazard_record() -> dict[str, Any]:
    """The smallest hazard declaration record that validates."""
    return {
        "fields": [
            {
                "name": "hazard_id",
                "type": {
                    "target": "UUID",
                    "multiplicity": {
                        "lower": 1,
                        "upper": 1,
                        "ordered": False,
                        "unique": False,
                    },
                },
                "identity": True,
            }
        ]
    }


@pytest.fixture(scope="session")
def failure_mode_record() -> dict[str, Any]:
    """The smallest failure-mode declaration record that validates."""
    return {
        "fields": [
            {
                "name": "failure_mode_id",
                "type": {
                    "target": "UUID",
                    "multiplicity": {
                        "lower": 1,
                        "upper": 1,
                        "ordered": False,
                        "unique": False,
                    },
                },
                "identity": True,
            }
        ]
    }
