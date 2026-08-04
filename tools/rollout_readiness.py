#!/usr/bin/env python3
"""Fail closed until ClusterDocs NG has its production decisions and assets."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
UNRESOLVED = ("TO_BE_", ".invalid", "STAGING-", "CLUSTERDOCS-", "TRANSFER-")


def unresolved_config(config: dict[str, object]) -> list[str]:
    keys = []
    for key, value in config.items():
        if isinstance(value, str) and any(marker in value for marker in UNRESOLVED):
            keys.append(key)
    return keys


def has_deployment_workflow() -> bool:
    workflow_root = ROOT / ".github/workflows"
    text = "\n".join(
        path.read_text(errors="replace").lower()
        for path in workflow_root.glob("*.y*ml")
    )
    signals = (
        "actions/deploy-pages",
        "peaceiris/actions-gh-pages",
        "aws s3 sync",
        "rclone copy",
        "rsync ",
        "netlify",
    )
    return any(signal in text for signal in signals)


def manual_review_audit() -> tuple[list[str], list[str]]:
    """Check whether the candidate is coherent enough to start human review."""
    blockers: list[str] = []
    ready: list[str] = []
    required_guides = (
        ROOT / "meta/EXPERT_REVIEW_GUIDE.md",
        ROOT / "meta/NOVICE_REVIEW_GUIDE.md",
        ROOT / "meta/VIDEO_REVIEW_GUIDE.md",
    )
    missing_guides = [path.name for path in required_guides if not path.is_file()]
    if missing_guides:
        blockers.append("manual-review guides are missing: " + ", ".join(missing_guides))
    else:
        ready.append("expert, novice, and video review guides are present")

    public_text = "\n".join(path.read_text(errors="replace") for path in (ROOT / "docs").rglob("*.md"))
    stale_terms = [term for term in ("RCC Connect", "rollout/index.md", "rollout page") if term in public_text]
    if stale_terms:
        blockers.append("speculative rollout wording remains public: " + ", ".join(stale_terms))
    else:
        ready.append("public guidance uses the current institutional connection route")

    if re.search(r"RCC_Onboarding_Part_[1-4]\.pptx", public_text):
        blockers.append("public pages still link unsynchronized Part 1–4 slide exports")
    else:
        ready.append("unsynchronized Part 1–4 office exports are withheld")

    source_part4 = (ROOT / "source/part4.md").read_text().lower()
    if "rootless execution on a shared cluster" not in source_part4:
        blockers.append("canonical Part 4 source lacks the rootless execution update")
    else:
        ready.append("canonical Part 4 explains rootless Apptainer")
    return blockers, ready


def audit() -> tuple[list[str], list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    ready: list[str] = []

    config = yaml.safe_load((ROOT / "config/public.yml").read_text())
    if config.get("site_status") != "production":
        blockers.append("config.public.yml still declares site_status as staging")
    unresolved = unresolved_config(config)
    if unresolved:
        blockers.append("unresolved production configuration: " + ", ".join(unresolved))

    manifest = yaml.safe_load((ROOT / "config/media-manifest.yml").read_text())
    assets = manifest.get("assets", [])
    classes = [item.get("class") for item in assets]
    if classes != list(range(1, 18)):
        blockers.append("media manifest does not contain exactly Classes 1–17 in order")
    else:
        ready.append("media manifest covers all 17 classes")

    not_human_reviewed = [
        str(item.get("class"))
        for item in assets
        if item.get("review_status") not in {"human_review_approved", "published"}
    ]
    if not_human_reviewed:
        blockers.append(
            "videos lack recorded human approval for classes: "
            + ", ".join(not_human_reviewed)
        )

    course_pages = sorted((ROOT / "docs/course").glob("class-*.md"))
    missing_tracks = [
        page.name for page in course_pages if 'kind="captions"' not in page.read_text()
    ]
    if missing_tracks:
        blockers.append("course videos lack in-player caption tracks: " + ", ".join(missing_tracks))
    else:
        ready.append("all 17 course pages declare in-player English captions")

    unchecked = len(re.findall(r"(?m)^- \[ \] ", (ROOT / "ADMIN_CHECKLIST.md").read_text()))
    if unchecked:
        blockers.append(f"administrator publication checklist has {unchecked} unchecked items")

    if not has_deployment_workflow():
        blockers.append("no reviewed production deployment workflow is present")

    review_blockers, review_ready = manual_review_audit()
    blockers.extend(review_blockers)
    ready.extend(review_ready)

    warnings.extend(
        (
            "external links require a final online link check",
            "the archived transition announcement needs a new operational review before reuse",
            "browser, mobile, screen-reader, and novice-user acceptance remain manual checks",
        )
    )
    return blockers, warnings, ready


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-blocked",
        action="store_true",
        help="print the audit without returning a failing status",
    )
    parser.add_argument(
        "--manual-review",
        action="store_true",
        help="check whether expert and novice manual review can begin",
    )
    args = parser.parse_args()
    if args.manual_review:
        blockers, ready = manual_review_audit()
        print("ClusterDocs NG manual-review readiness")
        for item in ready:
            print(f"READY: {item}")
        for item in blockers:
            print(f"BLOCKER: {item}")
        if blockers:
            print(f"RESULT: BLOCKED ({len(blockers)} blocker groups)")
            if not args.allow_blocked:
                raise SystemExit(1)
        else:
            print("RESULT: READY_FOR_EXPERT_AND_NOVICE_REVIEW")
        return
    blockers, warnings, ready = audit()
    print("ClusterDocs NG rollout readiness")
    for item in ready:
        print(f"READY: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in blockers:
        print(f"BLOCKER: {item}")
    if blockers:
        print(f"RESULT: BLOCKED ({len(blockers)} blocker groups)")
        if not args.allow_blocked:
            raise SystemExit(1)
    else:
        print("RESULT: READY")


if __name__ == "__main__":
    main()
