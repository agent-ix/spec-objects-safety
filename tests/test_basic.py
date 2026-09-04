"""The pack exposes its manifest as importable resource data."""

from __future__ import annotations

import pytest

from spec_objects_safety import MANIFEST_PATH, PACK_ROOT


@pytest.mark.trace("TC-006", "FR-001-AC-4")
def test_manifest_path_resolves() -> None:
    assert PACK_ROOT.is_dir()
    assert MANIFEST_PATH.is_file()
    assert MANIFEST_PATH.parent == PACK_ROOT
