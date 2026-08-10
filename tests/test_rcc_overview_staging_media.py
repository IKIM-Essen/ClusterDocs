from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media" / "staging" / "rcc-overview"
MANIFEST = MEDIA / "manifest.yml"


def test_rcc_overview_media_is_not_in_published_docs_tree() -> None:
    assert MEDIA.exists()
    assert "docs" not in MEDIA.relative_to(ROOT).parts
    forbidden = list((ROOT / "docs").rglob("rcc-login-*.png")) if (ROOT / "docs").exists() else []
    assert forbidden == []


def test_rcc_overview_manifest_is_staging_only_and_hashes_match() -> None:
    data = yaml.safe_load(MANIFEST.read_text())
    assert data["schema_version"] == 1
    assert data["status"] == "staging-only"
    assert data["publication"]["linked_from_docs"] is False
    assert data["publication"]["publication_review_required"] is True

    assets = data["assets"]
    assert len(assets) == 5
    for asset in assets:
        assert asset["publish_directly"] is False
        path = MEDIA / asset["file"]
        assert path.is_file()
        assert path.stat().st_size == asset["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == asset["sha256"]
