#!/usr/bin/env python3
"""Rebuild RCC Expedition deterministically with canonical ClusterDocs links."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ARCHIVE = ROOT / "docs/assets/downloads/RCC-Expedition-USB-v1.0.0.zip"
ARCHIVE = ROOT / "docs/assets/downloads/RCC-Expedition-USB-v1.0.1.zip"
OVERLAY_DIR = ROOT / "expedition-overlays"
OVERLAYS = {
    "READ ME FIRST.txt": OVERLAY_DIR / "READ ME FIRST.txt",
    "START HERE.html": OVERLAY_DIR / "START HERE.html",
}
CANONICAL_BASE = "https://ikim-essen.github.io/ClusterDocs/"
ALTERNATE_BASE = "https://docs.ikim.uk-essen.de/"
REPLACEMENTS = (
    (ALTERNATE_BASE + "course/", CANONICAL_BASE + "course/"),
    (ALTERNATE_BASE + "reference/", CANONICAL_BASE + "reference/"),
    (ALTERNATE_BASE, CANONICAL_BASE),
    (CANONICAL_BASE + "apptainer/", CANONICAL_BASE + "course/class-04-containers/"),
    (CANONICAL_BASE + "vs-code-setup/", CANONICAL_BASE + "reference/access-ssh-vscode/"),
    (CANONICAL_BASE + "jupyter/", CANONICAL_BASE + "course/class-09-python-notebooks/"),
    (
        "Mutable RCC facts belong in current ClusterDocs master.",
        "Mutable RCC facts belong in the current ClusterDocs site:\n" + CANONICAL_BASE,
    ),
)
TEXT_SUFFIXES = {".cmd", ".command", ".css", ".html", ".js", ".sh", ".txt"}
FIXED_TIME = (2026, 8, 9, 12, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    with zipfile.ZipFile(SOURCE_ARCHIVE) as source:
        infos = source.infolist()
        payload: dict[str, bytes] = {}
        for info in infos:
            if info.filename == "SHA256SUMS":
                continue
            overlay = OVERLAYS.get(info.filename)
            data = overlay.read_bytes() if overlay else source.read(info.filename)
            if Path(info.filename).suffix.lower() in TEXT_SUFFIXES:
                text = data.decode("utf-8")
                for old, new in REPLACEMENTS:
                    text = text.replace(old, new)
                data = text.encode("utf-8")
            payload[info.filename] = data

    sums = "".join(f"{sha256(data)}  {name}\n" for name, data in payload.items())
    payload["SHA256SUMS"] = sums.encode("utf-8")
    order = [info.filename for info in infos]
    info_by_name = {info.filename: info for info in infos}

    handle = tempfile.NamedTemporaryFile(
        prefix=ARCHIVE.name + ".", suffix=".tmp", dir=ARCHIVE.parent, delete=False
    )
    temporary = Path(handle.name)
    handle.close()
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as target:
            for name in order:
                original = info_by_name[name]
                info = zipfile.ZipInfo(name, FIXED_TIME)
                info.create_system = original.create_system
                info.external_attr = original.external_attr
                info.flag_bits = original.flag_bits
                info.compress_type = zipfile.ZIP_DEFLATED
                target.writestr(info, payload[name])
        os.replace(temporary, ARCHIVE)
    finally:
        temporary.unlink(missing_ok=True)

    print(sha256(ARCHIVE.read_bytes()))


if __name__ == "__main__":
    main()
