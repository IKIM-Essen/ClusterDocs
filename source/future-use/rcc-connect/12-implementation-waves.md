# RCC Connect implementation waves and acceptance (staged)

> **Source-only pilot.** This page records implementation state as of
> 29 October 2026. It does not activate desktop remote execution or create
> a supported public download.

## Goal

Scientists choose an approved RCC project, then use a browser, VS Code,
Positron or the terminal without configuring machines or guessing resource
requests. Substantial work remains Slurm-managed. The desktop IDE stays on the
laptop, and its per-user backend stays in the selected Slurm allocation.
A shellhost serves as a client/SSH gateway, never an unscheduled compute host.

## Source waves versus live rollout

| Wave | Source objective | Current gate |
| --- | --- | --- |
| 1 — Slurm contract | Project-bound session start; job ownership and exact project verification; machine-readable running worker resolution; no blind retries | Draft RCC source; offline verification only; live Slurm acceptance missing |
| 2 — desktop client | macOS/Windows installer/launcher source, strict SSH effective settings, safe local rollback, session list/attach/stop; shared contract with the server | Offline macOS mock tests pass; native Windows and verified SSH host registry missing |
| 3 — VS Code | Connect laptop editor to allocation-backed VS Code Server; account for remote extensions, Python, shells, Jupyter and subprocesses in job cgroup | Server binary/bootstrap and live PAM/Slurm acceptance missing |
| 4 — Positron | Native OpenSSH through approved RCC gateway; backend and R process on allocated worker; plotting and package behavior | Worker Ubuntu compatibility, authentication and backend acceptance missing |
| 5 — release | Signed downloads, trusted site overlay/host-key publication, native OS matrix, real scientist pilots and translated/accessible user docs | No user-facing release authorized |

Documentation may be drafted before rollout; guides must preserve the status
labels **planned**, **source-only**, **pilot**, or **accepted** accurately.

## Local proof vs real proof

Offline tests check input validation, parse errors, file ownership, symlink
refusal, malformed Slurm receipts, unsafe SSH alias overrides and refusal to
resubmit after uncertain outcomes. They cannot demonstrate that the real
Slurm controller, scheduler, SSH host keys, workstation authentication or
VS Code/Positron backends are working on production hardware.

On one approved canary, the operator must prove the entire sequence:
`start --project` → `RUNNING` → project-bound `resolve` → independently
verified SSH worker identity → IDE Remote-SSH → actual backend/cgroup adoption
→ Python or R synthetic work → disconnect/reconnect → cancel/time out
→ zero orphaned compute. Repeat for both IDEs and supported desktop OSes.

## Experience constraints

- **Browser-first, not mandatory.** SSH, VS Code and Positron remain choices
  without an expertise test. The current project and job can be inspected
  through the permitted interface.
- **Simplify the task, not the science.** RCC can prepare environment, Slurm
  and storage defaults, but cannot silently change scientific commands,
  methods or results.
- **Fail clearly.** When a connection is lost, the user should see the
  last known job ID, how to inspect status, and an appropriate next action.
  It must never silently submit another allocation.
- **Do not invent service availability.** An unaccepted desktop canary is
  not an established production feature, even if a laptop settings file
  exists.
- **Safe performance.** Keep big searches and analyses off shellhosts.
  A small workspace is useful but is not a security or storage-rate boundary.

This guide is intended for extraction into the site-neutral `clusterdocs`
core. Essen's hostname, signed download, device registration and acceptance
details belong in the future `clusterdocs-site-essen` overlay.

See [operator acceptance](07-operator-acceptance.md),
[VS Code](03-vscode-python.md),
[Positron](04-positron-r.md),
and [the ClusterDocs site/core split](09-core-site-migration-plan.md).
