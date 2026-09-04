#!/usr/bin/env python3
"""Validate the public RCC Expedition archive and its release checksum."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import re
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs/assets/downloads/RCC-Expedition-USB-v1.0.1.zip"
CHECKSUM = ARCHIVE.with_suffix(".sha256")
PRESERVED_RELEASES = (
    ROOT / "docs/assets/downloads/RCC-Expedition-USB-v1.0.0.zip",
)
PRODUCTION_DOCS = "https://ikim-essen.github.io/ClusterDocs/"
FORBIDDEN_DOCS = (
    "https://ikim-essen.github.io/clusterdocs-ng/",
    "https://docs.ikim.uk-essen.de/",
)
REQUIRED_FUTURE_PAGES = (
    PRODUCTION_DOCS + "course/class-04-containers/",
    PRODUCTION_DOCS + "course/class-09-python-notebooks/",
    PRODUCTION_DOCS + "reference/access-ssh-vscode/",
)
TEXT_SUFFIXES = {".cmd", ".command", ".css", ".html", ".js", ".sh", ".txt"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_checksum_lines(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError(f"invalid SHA256SUMS line: {line!r}")
        parsed[match.group(2)] = match.group(1)
    return parsed


def main() -> None:
    expected_downloads = {ARCHIVE.name, CHECKSUM.name}
    for preserved in PRESERVED_RELEASES:
        expected_downloads.update({preserved.name, preserved.with_suffix(".sha256").name})
    actual_downloads = {path.name for path in ARCHIVE.parent.iterdir() if path.is_file()}
    if actual_downloads != expected_downloads:
        raise SystemExit("RCC Expedition downloads directory contains an unexpected file set")

    for preserved in PRESERVED_RELEASES:
        preserved_checksum = preserved.with_suffix(".sha256")
        preserved_outer = parse_checksum_lines(preserved_checksum.read_text())
        if preserved_outer != {preserved.name: digest(preserved.read_bytes())}:
            raise SystemExit(f"preserved RCC Expedition checksum failed: {preserved.name}")

    expected_outer = parse_checksum_lines(CHECKSUM.read_text())
    archive_digest = digest(ARCHIVE.read_bytes())
    if expected_outer != {ARCHIVE.name: archive_digest}:
        raise SystemExit("RCC Expedition outer checksum does not match the archive")
    for public_record in (
        ROOT / "docs/rcc-expedition.md",
        ROOT / "docs/maintainers/rcc-expedition-release.md",
    ):
        if archive_digest not in public_record.read_text():
            raise SystemExit(f"RCC Expedition checksum is stale in {public_record.name}")

    with zipfile.ZipFile(ARCHIVE) as bundle:
        names = bundle.namelist()
        normalized_names = [name.replace("\\", "/") for name in names]
        if len(normalized_names) != len({name.casefold() for name in normalized_names}):
            raise SystemExit("RCC Expedition archive contains duplicate paths")
        for name, normalized in zip(names, normalized_names):
            path = PurePosixPath(normalized)
            if (
                path.is_absolute()
                or ".." in path.parts
                or not path.parts
                or ":" in path.parts[0]
            ):
                raise SystemExit(f"unsafe RCC Expedition archive path: {name}")

        inner = parse_checksum_lines(bundle.read("SHA256SUMS").decode("utf-8"))
        expected_names = set(names) - {"SHA256SUMS"}
        if set(inner) != expected_names:
            raise SystemExit("RCC Expedition SHA256SUMS does not cover the exact payload")
        for name, expected in inner.items():
            if digest(bundle.read(name)) != expected:
                raise SystemExit(f"RCC Expedition inner checksum failed: {name}")

        visible = []
        for name in names:
            if PurePosixPath(name).suffix.lower() in TEXT_SUFFIXES:
                visible.append(bundle.read(name).decode("utf-8"))
        text = "\n".join(visible)
        for legacy in FORBIDDEN_DOCS:
            if legacy in text:
                raise SystemExit(f"RCC Expedition contains legacy ClusterDocs URL: {legacy}")
        if PRODUCTION_DOCS not in text:
            raise SystemExit("RCC Expedition does not link to the production ClusterDocs site")
        missing_pages = [url for url in REQUIRED_FUTURE_PAGES if url not in text]
        if missing_pages:
            raise SystemExit(
                "RCC Expedition lacks future-page links: " + ", ".join(missing_pages)
            )

    print(f"RCC Expedition release: PASS ({archive_digest})")


if __name__ == "__main__":
    main()
