#!/usr/bin/env python3
"""Fail closed unless the integrated ClusterDocs release bundle is ready."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/public.yml"


def audit() -> tuple[list[str], list[str]]:
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    blockers: list[str] = []
    ready: list[str] = []

    bundle = config.get("release_bundle")
    if not isinstance(bundle, dict):
        return ["release_bundle configuration is missing"], ready

    if bundle.get("policy") != "all_required_surfaces_ready_before_publication":
        blockers.append("release_bundle policy is missing or not fail-closed")

    required = bundle.get("required_surfaces")
    if not isinstance(required, list) or not required:
        blockers.append("release_bundle required_surfaces is missing or empty")
        return blockers, ready

    expected = ["rcc_home", "files", "rcc_analysis", "rcc_admin", "my_rcc"]
    if required != expected:
        blockers.append(
            "release_bundle required_surfaces must be exactly: " + ", ".join(expected)
        )

    statuses = config.get("feature_status")
    if not isinstance(statuses, dict):
        blockers.append("feature_status registry is missing")
        return blockers, ready

    not_ready = [surface for surface in expected if statuses.get(surface) != "ready"]
    if not_ready:
        blockers.append(
            "integrated RCC release bundle is not ready: "
            + ", ".join(f"{surface}={statuses.get(surface, 'missing')}" for surface in not_ready)
        )
    else:
        ready.append(
            "RCC Home, Files, RCC Analysis, RCC Admin, and My RCC are all recorded ready"
        )

    return blockers, ready


def main() -> None:
    blockers, ready = audit()
    print("ClusterDocs integrated release-bundle gate")
    for item in ready:
        print(f"READY: {item}")
    for item in blockers:
        print(f"BLOCKER: {item}")
    if blockers:
        raise SystemExit(1)
    print("RESULT: READY")


if __name__ == "__main__":
    main()
