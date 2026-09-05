# ClusterDocs 3 integration and promotion plan

`clusterdocs-3` is the future release line in the existing
`IKIM-Essen/ClusterDocs` repository. Do not recreate the retired separate-NG
promotion model and do not publish production from `clusterdocs-ng`.

## Integration principle

Keep one coherent candidate and integrate changes in small, reviewable waves.
Every wave must preserve:

- task-first/browser-first onboarding for ordinary researchers;
- complete advanced capability discovery for experienced users;
- explicit release-state truth for staged features;
- project-scoped identity/authorization across browser, CLI, API, and agents;
- the data-blind-by-default coding-agent boundary;
- Slurm as the governed compute authority;
- safe instrument/project/lifecycle boundaries; and
- fail-closed publication from the exact `clusterdocs-3` commit.

## Recommended change waves

1. **Research front door and navigation** — Files, Analysis, account/project
   actions, advanced path, and capability overview.
2. **Analysis and workflow model** — Notebook/Workflow convergence, provenance,
   idempotent submission, and resource-efficiency guidance.
3. **AI/agent model** — data-blind default, synthetic fixtures, bounded
   diagnostics, explicit data-near exceptions, and capability authorization.
4. **Instrument/storage/lifecycle model** — sequencers/microscopes/other devices,
   project POSIX/S3/DataLad, scratch, Coscine status, and domain applications
   such as SeqLab.
5. **Release and operations** — deterministic shell, governed service endpoints,
   v3 review receipts, accessibility, media, exact-source deployment, and
   rollback.

Each wave should update regression tests with the product contract rather than
retaining assertions whose only purpose was to preserve the previous NG mental
model.

## Acceptance closure before broad exposure

The candidate is not broadly promotable until all of the following are recorded:

- fresh ClusterDocs 3 adversarial expert review;
- zero-SSH naive-user browser acceptance against the staged candidate;
- separate advanced-user acceptance for SSH/VS Code/Slurm/containers/GPU and
  workflow development;
- institutional/privacy/accessibility/operational checklist closure;
- required media review and online verification; and
- a final release-version decision and production-status change.

A small controlled pilot may precede closure to generate real evidence. It does
not substitute for the acceptance gates.

## Production source contract

The manually dispatched Gitea production workflow accepts only
`refs/heads/clusterdocs-3`, verifies the exact source SHA and clean worktree,
runs the fail-closed gates, generates the site and release receipt, and updates
`gh-pages` without force. GitHub Actions remains manual validation fallback only.

The final release should be represented by the exact source commit and generated
`assets/release.json`; historical checksum/audit artifacts from earlier NG work
must not be mistaken for the ClusterDocs 3 source-of-truth receipt.
