# ClusterDocs integration and promotion plan

`clusterdocs-3` is the temporary future-release integration line in the existing
`IKIM-Essen/ClusterDocs` repository. It is **not** intended to become the
permanent production branch. The long-term publication source is `main`.

This plan records the desired end state but does **not** authorize merging
`clusterdocs-3` into `main`, deleting branches, or publishing production.

## Integration principle

Keep one coherent candidate and integrate changes in small, reviewable waves.
Every wave must preserve:

- task-first/browser-first onboarding for ordinary researchers;
- complete advanced capability discovery for experienced users;
- explicit release-state truth for staged features;
- project-scoped identity/authorization across browser, CLI, API, and agents;
- the data-blind-by-default coding-agent boundary;
- Slurm as the governed scientific-compute authority;
- clear long-lived service-plane authority rather than a second scientific scheduler;
- safe instrument/project/lifecycle boundaries; and
- fail-closed candidate validation before promotion to `main`.

## Recommended change waves

1. **Research front door and navigation** — Files, Analysis, account/project actions, advanced path, and capability overview.
2. **Analysis and workflow model** — Notebook/Workflow convergence, provenance, idempotent submission, and resource-efficiency guidance.
3. **AI/agent model** — data-blind default, synthetic fixtures, bounded diagnostics, explicit data-near exceptions, and capability authorization.
4. **Instrument/storage/lifecycle model** — sequencers/microscopes/other devices, project POSIX/S3/DataLad, scratch, Coscine status, and domain applications such as SeqLab.
5. **Credential model** — OS/password-manager guidance for web credentials, no-passphrase RCC software SSH keys, and FIDO-backed SSH where appropriate.
6. **Architecture rationale** — explain why Slurm owns scientific compute while the service plane handles long-lived services rather than forcing Kubernetes or any other orchestrator onto every workload.
7. **Release and operations** — deterministic shell, governed service endpoints, v3 review receipts, accessibility, media, main-only production deployment, and rollback.

Each wave should update regression tests with the product contract rather than
retaining assertions whose only purpose was to preserve the previous NG mental
model.

## Acceptance closure before promotion

The candidate is not promotable until all of the following are recorded:

- fresh ClusterDocs 3 adversarial expert review;
- zero-SSH naive-user browser acceptance against the staged candidate;
- separate advanced-user acceptance for SSH/VS Code/Slurm/containers/GPU and workflow development;
- institutional/privacy/accessibility/operational checklist closure;
- required media review and online verification, including regenerated Part 1 media after the SSH-key policy correction; and
- a final release-version decision.

A small controlled pilot may precede closure to generate real evidence. It does
not substitute for the acceptance gates.

## Promotion to main

After acceptance closure, the next action is **not** direct publication from
`clusterdocs-3`. The candidate must first be promoted into `main` through the
normal repository merge path. That promotion requires explicit authorization
at the time; nothing in this plan grants it in advance.

After the authorized merge:

1. identify the exact resulting `main` commit;
2. rerun repository/build/readiness validation on that exact main commit;
3. confirm no unreviewed changes entered between candidate acceptance and main;
4. set/confirm the production release state only on the accepted main commit;
5. dispatch the main-only production workflow; and
6. verify `assets/release.json` records `source_branch: main` and the exact commit.

## Branch retirement

`clusterdocs-ng` and `clusterdocs-3` are temporary lineage/integration branches.
Do not delete them during review or merely because the candidate was merged.
Retire them only after the main-based production deployment and rollback evidence
have been verified, and only through the repository's approved branch-retirement
procedure.

After retirement, normal ClusterDocs development should branch from and return
to `main`; future production publication should continue to originate from
`main`, not from a permanently named release-development branch.
