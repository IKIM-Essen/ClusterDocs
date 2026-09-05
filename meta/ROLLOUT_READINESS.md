# ClusterDocs 3 production-candidate status

Review date: 5 September 2026

## Current decision

`clusterdocs-3` is the temporary future-release candidate. The branch materially
changes the product model: browser-first use, optional SSH, RCC Analysis
Notebook/Workflow, progressive disclosure of advanced HPC controls, a broader
RCC capability story, a stronger AI/agent boundary, corrected credential
policy, and an explicit scheduler/service-plane architecture rationale.

The expert review recorded for the August candidate is superseded. Broad exposure
is **blocked** until a fresh ClusterDocs 3 expert review and zero-SSH naive-user
browser acceptance are completed.

A very small controlled pilot is allowed before those reviews so the team can
prove the deployment works in principle and collect real browser evidence. The
pilot is not equivalent to broad production acceptance.

Production publication is **main-only**. Validation of `clusterdocs-3` is not
merge authorization and is not permission to publish directly from the
candidate branch. After acceptance closure, promoting the candidate into `main`
requires a separate explicit authorization.

## What ClusterDocs 3 must communicate

- New users can begin with a research task rather than learning cluster topology.
- Browser-first research is a legitimate complete path; an RCC account does not imply an SSH credential.
- Advanced users can immediately discover instrument ingestion, project S3/POSIX/DataLad, Notebook, Workflow, Slurm/GPU/HPC, self-governance/delegation, AI assistance, project services, Coscine status, and domain applications such as SeqLab.
- Agents can help explain, design, code, test, and debug without making protected project-data disclosure the default workflow.
- Windows/macOS password/passkey managers are recommended for web/account credentials; the normal RCC software-backed SSH key is generated without a passphrase.
- Slurm owns scientific compute while the RCC service plane owns long-lived services; Kubernetes remains a possible future choice when a concrete workload justifies it, not a mandatory universal substrate.
- Every staged/future capability remains status-truthful and fail-closed.

## ClusterDocs 3 release blockers

1. Complete the fresh adversarial review in `meta/EXPERT_REVIEW_GUIDE.md` and resolve blocker/major findings.
2. Run `meta/NOVICE_REVIEW_GUIDE.md` with zero-SSH naive users against the exact staged candidate; complete the Files -> Analysis -> Files path without facilitator shell intervention.
3. Run a separate advanced-user acceptance for SSH, VS Code, Slurm, containers, workflow development, GPU use, and lower-level diagnostics.
4. Complete the institutional administrator checklist: operational endpoints, supported versions, identity/roles, storage/Slurm behavior, privacy/domain approval, accessibility, ownership, monitoring, and rollback.
5. Reconcile `source/part1.md` with the current no-passphrase SSH-key policy; regenerate and human-review the Part 1 video/audio/captions before media activation. The existing staged audio is not acceptable v3 evidence.
6. Publish/verify the remaining staged video assets and complete the required human media approval and clean-client browser checks.
7. Verify the Slurm/service-plane/Kubernetes rationale against the actual RCC deployment and ensure no user-facing interface creates a second scientific scheduler.
8. Verify all service links and release badges against the actual deployment; documentation of a service must not make an unreleased service appear live.
9. Verify role separation for My RCC/self-service versus administrator actions.
10. Verify the standard agent-assisted workflow does not require exporting real protected project data and that agent/API/MCP interfaces do not broaden authority.
11. Choose the final release version.
12. Obtain explicit authorization to merge the accepted candidate into `main`; this document does not provide it.
13. After the authorized merge, rerun all production gates on the exact resulting `main` commit and change `site_status` to `production` only when those gates pass.

## Manual review gate on the candidate

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The manual-review command verifies that the active v3 documentation is coherent
enough to begin human review. It must not reuse the August expert receipt as
ClusterDocs 3 approval.

## Promotion gate

Only after candidate acceptance is complete and explicit merge authorization is
given:

1. merge the accepted `clusterdocs-3` candidate into `main` through the normal repository path;
2. record the exact resulting main commit;
3. verify no unreviewed changes entered with the promotion; and
4. run the production gates on that exact main commit.

No merge has been authorized by this plan.

## Production release gate on main

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

The manually dispatched production workflow itself accepts only
`refs/heads/main`. `assets/release.json` must record `source_branch: main` and the
exact source commit.

After a verified main-based publication and rollback check, the temporary
`clusterdocs-ng` and `clusterdocs-3` branches can be retired through repository
policy. Branch retirement is not part of candidate review and is not performed
by these gates.
