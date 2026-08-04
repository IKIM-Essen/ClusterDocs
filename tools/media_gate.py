#!/usr/bin/env python3
"""Fail closed unless every ClusterDocs video matches the publication manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config/media-manifest.yml"
CHUNK_SIZE = 1024 * 1024


def asset_url(base_url: str, filename: str) -> str:
    return base_url.rstrip("/") + "/" + urllib.parse.quote(filename)


def sha256_stream(stream) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    while chunk := stream.read(CHUNK_SIZE):
        digest.update(chunk)
        size += len(chunk)
    return digest.hexdigest(), size


def sha256_file(path: Path) -> tuple[str, int]:
    with path.open("rb") as stream:
        return sha256_stream(stream)


def probe_local_video(path: Path) -> dict[str, object]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,channels",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def validate_probe(probe: dict[str, object], expected_duration: float) -> list[str]:
    errors: list[str] = []
    streams = probe.get("streams", [])
    videos = [item for item in streams if item.get("codec_type") == "video"]
    audio = [item for item in streams if item.get("codec_type") == "audio"]
    if len(videos) != 1:
        errors.append(f"expected one video stream, found {len(videos)}")
    elif (videos[0].get("codec_name"), videos[0].get("width"), videos[0].get("height")) != (
        "h264",
        1280,
        720,
    ):
        errors.append("video stream is not H.264 1280x720")
    if len(audio) != 1:
        errors.append(f"expected one audio stream, found {len(audio)}")
    elif (audio[0].get("codec_name"), audio[0].get("channels")) != ("aac", 2):
        errors.append("audio stream is not stereo AAC")
    duration = float(probe.get("format", {}).get("duration", 0))
    if abs(duration - expected_duration) > 0.75:
        errors.append(
            f"duration {duration:.3f}s differs from manifest {expected_duration:.3f}s"
        )
    return errors


def validate_range_response(status: int, headers) -> list[str]:
    errors: list[str] = []
    if status != 206:
        errors.append(f"byte-range request returned HTTP {status}, expected 206")
    if not headers.get("Content-Range", "").lower().startswith("bytes 0-"):
        errors.append("byte-range response lacks a valid Content-Range header")
    content_type = headers.get("Content-Type", "").split(";", 1)[0].lower()
    if content_type != "video/mp4":
        errors.append(f"content type is {content_type or 'missing'}, expected video/mp4")
    return errors


def verify_local(directory: Path, assets: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    expected = {str(item["video"]) for item in assets}
    actual = {path.name for path in directory.glob("*.mp4")}
    for name in sorted(expected - actual):
        errors.append(f"{name}: missing local file")
    for name in sorted(actual - expected):
        errors.append(f"{name}: unmanifested local MP4")
    for item in assets:
        name = str(item["video"])
        path = directory / name
        if not path.is_file():
            continue
        digest, size = sha256_file(path)
        item_errors: list[str] = []
        if digest != item["sha256"]:
            item_errors.append(f"SHA-256 {digest} does not match manifest")
        if size != item.get("size_bytes"):
            item_errors.append(f"size {size} does not match manifest {item.get('size_bytes')}")
        try:
            item_errors.extend(validate_probe(probe_local_video(path), float(item["duration_seconds"])))
        except (FileNotFoundError, subprocess.CalledProcessError, ValueError, TypeError) as exc:
            item_errors.append(f"ffprobe failed: {exc}")
        if item_errors:
            errors.extend(f"{name}: {message}" for message in item_errors)
        else:
            print(f"LOCAL PASS {digest} {size} {name}")
    return errors


def verify_online(base_url: str, assets: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for item in assets:
        name = str(item["video"])
        url = asset_url(base_url, name)
        item_errors: list[str] = []
        try:
            range_request = urllib.request.Request(url, headers={"Range": "bytes=0-1023"})
            with urllib.request.urlopen(range_request, timeout=30) as response:
                item_errors.extend(validate_range_response(response.status, response.headers))
                response.read()
            with urllib.request.urlopen(url, timeout=60) as response:
                content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
                if response.status != 200:
                    item_errors.append(f"full download returned HTTP {response.status}")
                if content_type != "video/mp4":
                    item_errors.append(
                        f"full download content type is {content_type or 'missing'}, expected video/mp4"
                    )
                digest, size = sha256_stream(response)
            if digest != item["sha256"]:
                item_errors.append(f"downloaded SHA-256 {digest} does not match manifest")
            if size != item.get("size_bytes"):
                item_errors.append(
                    f"downloaded size {size} does not match manifest {item.get('size_bytes')}"
                )
        except Exception as exc:  # Network and TLS failures are publication blockers.
            item_errors.append(f"request failed: {exc}")
        if item_errors:
            errors.extend(f"{name}: {message}" for message in item_errors)
        else:
            print(f"ONLINE PASS {digest} {size} {url}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--local-dir", type=Path)
    source.add_argument("--base-url")
    args = parser.parse_args()

    assets = yaml.safe_load(MANIFEST.read_text()).get("assets", [])
    if len(assets) != 17:
        raise SystemExit(f"media manifest must contain 17 assets, found {len(assets)}")
    required = {"video", "sha256", "size_bytes", "duration_seconds"}
    incomplete = [str(item.get("video", "<unnamed>")) for item in assets if required - item.keys()]
    if incomplete:
        raise SystemExit("manifest entries lack required fields: " + ", ".join(incomplete))

    errors = (
        verify_local(args.local_dir.resolve(), assets)
        if args.local_dir
        else verify_online(args.base_url, assets)
    )
    if errors:
        print("\n".join(f"FAIL {message}" for message in errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"media publication gate: PASS ({len(assets)} videos)")


if __name__ == "__main__":
    main()
