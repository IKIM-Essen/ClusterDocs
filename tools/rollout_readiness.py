#!/usr/bin/env python3
"""Fail closed until ClusterDocs 3 has production decisions and review evidence."""

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
    workflow = ROOT / ".gitea/workflows/deploy-production.yml"
    if not workflow.is_file():
        return False
    text = workflow.read_text(errors="replace")
    required = (
        "workflow_dispatch:",
        "runs-on: rcc-ci",
        "/opt/rcc-ci/bin/gitea-ci-checkout",
        'refs/heads/clusterdocs-3',
        "tools/validate_repo.py",
        "tools/rollout_readiness.py",
        "tools/build_site.py --production",
        "git@github.com:IKIM-Essen/ClusterDocs.git",
        "--branch gh-pages",
        "push origin HEAD:gh-pages",
        "touch site-production/.nojekyll",
        "test ! -e site-production/CNAME",
        "StrictHostKeyChecking=yes",
    )
    forbidden = ("refs/heads/clusterdocs-ng", "pull_request:", "\n  push:", "schedule:", "uses:")
    return all(signal in text for signal in required) and not any(
        signal in text for signal in forbidden
    )


def manual_review_audit() -> tuple[list[str], list[str]]:
    """Check whether the exact v3 candidate is coherent enough for human review."""
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
        ready.append("expert, novice-browser, and video review guides are present")

    public_text = "\n".join(
        path.read_text(errors="replace") for path in (ROOT / "docs").rglob("*.md")
    )
    stale_terms = [
        term
        for term in ("RCC Connect", "rollout/index.md", "rollout page")
        if term in public_text
    ]
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

    home = (ROOT / "docs/index.md").read_text(errors="replace").lower()
    if "what do you want to do?" not in home or "what rcc can do" not in home:
        blockers.append("v3 home page is not task-first and capability-discoverable")
    else:
        ready.append("v3 home page is task-first and exposes the advanced capability overview")

    agents = (ROOT / "docs/concepts/agents-and-mcp.md").read_text(errors="replace").lower()
    if "data-blind by default" not in agents:
        blockers.append("agent guidance lacks the data-blind default boundary")
    else:
        ready.append("agent guidance records the data-blind default boundary")

    review_status = yaml.safe_load((ROOT / "config/review-status.yml").read_text())
    expert = review_status.get("expert_content_review", {})
    novice = review_status.get("novice_acceptance", {})
    if expert.get("status") not in {"required_v3_rereview", "completed"}:
        blockers.append("v3 expert-review state is missing or ambiguous")
    if novice.get("status") not in {"required_pre_broad_rollout", "completed"}:
        blockers.append("v3 novice-browser review state is missing or ambiguous")
    if novice.get("zero_ssh_required") is not True:
        blockers.append("v3 novice acceptance is not explicitly zero-SSH")
    if not blockers:
        ready.append("v3 review receipts are reset and ready to collect fresh evidence")

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
            "videos lack recorded human approval for classes: " + ", ".join(not_human_reviewed)
        )

    course_pages = sorted((ROOT / "docs/course").glob("class-*.md"))
    video_classes = set(classes)
    video_pages = [
        page
        for page in course_pages
        if int(page.name.removeprefix("class-")[:2]) in video_classes
    ]
    missing_tracks = [
        page.name for page in video_pages if 'kind="captions"' not in page.read_text()
    ]
    if missing_tracks:
        blockers.append("course videos lack in-player caption tracks: " + ", ".join(missing_tracks))
    else:
        ready.append("all 17 video-backed course pages declare in-player English captions")

    checklist_text = (ROOT / "ADMIN_CHECKLIST.md").read_text()
    unchecked_lines = re.findall(r"(?m)^- \[ \] .+$", checklist_text)
    unchecked = len(
        [line for line in unchecked_lines if "Run `python tools/rollout_readiness.py`" not in line]
    )
    if unchecked:
        blockers.append(f"administrator publication checklist has {unchecked} unchecked items")

    if not has_deployment_workflow():
        blockers.append("no reviewed ClusterDocs 3 production deployment workflow is present")
    else:
        ready.append("Gitea-only ClusterDocs 3 production deployment workflow is present")

    if not (ROOT / "meta/BRANCH_PR_AUDIT.md").is_file():
        blockers.append("ClusterDocs branch and pull-request audit is missing")
    else:
        ready.append("ClusterDocs branch and pull-request audit is present")

    review_status = yaml.safe_load((ROOT / "config/review-status.yml").read_text())
    expert = review_status.get("expert_content_review", {})
    novice = review_status.get("novice_acceptance", {})
    advanced = review_status.get("advanced_acceptance", {})

    if expert.get("status") != "completed":
        blockers.append("ClusterDocs 3 expert content review is not recorded as completed")
    else:
        ready.append("ClusterDocs 3 expert content review is recorded as completed")

    if novice.get("zero_ssh_required") is not True:
        blockers.append("ClusterDocs 3 novice acceptance is not explicitly zero-SSH")
    if novice.get("status") != "completed":
        blockers.append(
            "zero-SSH novice browser acceptance is not recorded as completed before broad exposure"
        )
    else:
        ready.append("zero-SSH novice browser acceptance is recorded as completed")

    if advanced.get("status") != "completed":
        blockers.append("advanced-user acceptance is not recorded as completed")
    else:
        ready.append("advanced-user acceptance is recorded as completed")

    review_blockers, review_ready = manual_review_audit()
    blockers.extend(review_blockers)
    ready.extend(review_ready)

    warnings.extend(
        (
            "external links require a final online link check",
            "browser, mobile, keyboard, and screen-reader acceptance remain manual checks",
            "a controlled pilot is not evidence for broad production acceptance",
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
        help="check whether the v3 expert/novice/advanced manual reviews can begin",
    )
    args = parser.parse_args()

    if args.manual_review:
        blockers, ready = manual_review_audit()
        print("ClusterDocs 3 manual-review readiness")
        for item in ready:
            print(f"READY: {item}")
        for item in blockers:
            print(f"BLOCKER: {item}")
        if blockers:
            print(f"RESULT: BLOCKED ({len(blockers)} blocker groups)")
            if not args.allow_blocked:
                raise SystemExit(1)
        else:
            print("RESULT: READY_FOR_V3_HUMAN_REVIEW")
        return

    blockers, warnings, ready = audit()
    print("ClusterDocs 3 rollout readiness")
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
