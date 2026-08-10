---
description: "Guide a ClusterDocs rollout using the repository runbook and readiness gates"
name: "ClusterDocs rollout"
argument-hint: "manual-review | staging | production"
agent: "agent"
---

Help me run or review a ClusterDocs rollout for the requested phase.

Use the repository guidance in [meta/PUBLICATION_RUNBOOK.md](../../meta/PUBLICATION_RUNBOOK.md), [meta/ROLLOUT_READINESS.md](../../meta/ROLLOUT_READINESS.md), and the review guides in [meta/EXPERT_REVIEW_GUIDE.md](../../meta/EXPERT_REVIEW_GUIDE.md), [meta/NOVICE_REVIEW_GUIDE.md](../../meta/NOVICE_REVIEW_GUIDE.md), and [meta/VIDEO_REVIEW_GUIDE.md](../../meta/VIDEO_REVIEW_GUIDE.md) as the authoritative workflow.

Follow this structure:
1. Identify the rollout phase from the argument or ask for it if it is missing.
2. Explain the purpose of the phase and the exact commands to run.
3. Call out the required evidence and success criteria for each gate.
4. Highlight blockers, rollback actions, and the next recommended step.

When the phase is:
- manual-review: focus on the review-guide checks, speculative rollout wording removal, canonical-source validation, and the readiness gate output.
- staging: verify the repo, build the review site, and confirm the rollout readiness checks before any production switch.
- production: verify the production build, deployment prerequisites, media publication readiness, site-status handling, and rollback conditions.

Prefer the repository’s existing commands and scripts, for example:
- python tools/validate_repo.py
- python tools/build_site.py --output site-review
- python tools/build_site.py --production --output site-production
- python tools/rollout_readiness.py --manual-review
- python tools/rollout_readiness.py

Keep the response concise, actionable, and evidence-based. If a gate fails, explain the failure clearly and propose the minimal next step to unblock the rollout.

Examples:
- /cluster-docs-rollout manual-review
- /cluster-docs-rollout staging
- /cluster-docs-rollout production
