# ClusterDocs 3 production-candidate status

Review date: 5 September 2026

## Current decision

ClusterDocs 3 is the future release candidate. The branch materially changes the
product model: browser-first use, optional SSH, RCC Analysis Notebook/Workflow,
progressive disclosure of advanced HPC controls, a broader RCC capability story,
and a stronger AI/agent boundary.

The expert review recorded for the August candidate is therefore superseded for
this release. Broad exposure is **blocked** until a fresh ClusterDocs 3 expert
review and zero-SSH naive-user browser acceptance are completed.

A very small controlled pilot is allowed before those reviews so the team can
prove the deployment works in principle and collect real browser evidence. The
pilot is not equivalent to broad production acceptance.

## What ClusterDocs 3 must communicate

- New users can begin with a research task rather than learning cluster topology.
- Browser-first research is a legitimate complete path; an RCC account does not
  imply an SSH credential.
- Advanced users can immediately discover the platform step-change: instrument
  ingestion, project storage including S3 where enabled, DataLad, Notebook,
  Workflow, Slurm/GPU/HPC, self-governance/delegation, AI assistance, project
  services, reproducibility/provenance, Coscine preservation, and domain
  applications such as SeqLab.
- Agents can help explain, design, code, test, and debug without making protected
  project-data disclosure the default workflow.
- Every staged/future capability remains status-truthful and fail-closed.

## Completed foundations retained from the previous candidate

- The 17-video media handoff, manifest, captions, publication gating, and
  separate media-endpoint model remain in place.
- Gitea remains the production deployment authority; GitHub Actions has no
  production deployment credentials.
- Rootless Apptainer, Slurm execution, storage, data-sharing, instrument,
  privacy, and lifecycle reference material remain part of the candidate.
- The visual RCC documentation shell and responsive navigation remain the base
  design rather than reverting to the legacy site.

## ClusterDocs 3 release blockers

1. Complete the fresh adversarial review in `meta/EXPERT_REVIEW_GUIDE.md` and
   resolve blocker/major findings.
2. Run `meta/NOVICE_REVIEW_GUIDE.md` with zero-SSH naive users against the exact
   staged candidate; complete the Files -> Analysis -> Files path without
   facilitator shell intervention.
3. Run a separate advanced-user acceptance for SSH, VS Code, Slurm, containers,
   workflow development, GPU use, and lower-level diagnostics.
4. Complete the institutional administrator checklist: operational endpoints,
   supported versions, identity/roles, storage/Slurm behavior, privacy/domain
   approval, accessibility, ownership, monitoring, and rollback.
5. Publish/verify the staged video assets and complete the required human media
   approval and clean-client browser checks.
6. Verify all service links and release badges against the actual deployment;
   documentation of a service must not make an unreleased service appear live.
7. Verify role separation for My RCC/self-service versus administrator actions.
8. Verify the standard agent-assisted workflow does not require exporting real
   protected project data and that agent/API/MCP interfaces do not broaden
   authority.
9. Change `site_status` to `production` only after the preceding gates pass.

## Manual review gate

Build the exact candidate and verify the review prerequisites:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The manual-review command should report that the candidate is ready to begin the
fresh expert, novice-browser, advanced-user, and media reviews. It must not reuse
the August expert receipt as ClusterDocs 3 approval.

## Production release gate

After the review evidence and institutional values are resolved:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

The full readiness gate must fail until both the ClusterDocs 3 expert review and
zero-SSH novice acceptance are explicitly recorded as completed. A controlled
pilot is not sufficient evidence for broad exposure.
