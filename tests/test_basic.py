"""The pack exposes its manifest as importable resource data."""

from __future__ import annotations

from spec_objects_safety import MANIFEST_PATH, PACK_ROOT


def test_manifest_path_resolves() -> None:
    assert PACK_ROOT.is_dir()
    assert MANIFEST_PATH.is_file()
    assert MANIFEST_PATH.parent == PACK_ROOT
