# ClusterDocs 3 integrated release-bundle decision

Decision date: 5 September 2026

## Decision

ClusterDocs 3 will **not** be released before RCC Analysis is ready.

The minimum browser product released together with ClusterDocs 3 is:

1. **RCC Home**;
2. **Files**;
3. **RCC Analysis** — Notebook and Workflow;
4. **My RCC**; and
5. **RCC Admin**.

These surfaces form one product boundary. The same RCC identity, project
membership/delegated role, and project policy must follow the user across them.
RCC Analysis is not a post-release feature and the advanced SSH/VS Code path is
not a substitute for it.

## Current candidate consequence

`config/public.yml` records `rcc_analysis: not_yet_released`, so the current
candidate is intentionally blocked from production by
`tools/release_bundle_gate.py`.

The release gate becomes green only when all five required surfaces are recorded
`ready` and the corresponding end-to-end acceptance has been completed.

## Acceptance path

The representative ordinary-user acceptance is:

```text
RCC Home
  -> Files / select or upload project input
  -> RCC Analysis Notebook
  -> promote/repeat through RCC Analysis Workflow where appropriate
  -> durable result back to project / Files
  -> My RCC for user self-service
  -> RCC Admin only for roles with approval/admin capabilities
```

The release must verify that switching surfaces does not change project authority
and that My RCC and RCC Admin remain clearly separated by capability.

## What can remain staged after ClusterDocs 3

The release-bundle decision does **not** require every documented RCC capability
to be live. Separately governed services may remain marked not yet released,
including for example:

- RCC-to-Coscine self-service transfer;
- protected project vhosts; and
- selected vendor integrations such as Ardia.

Their own pages remain authoritative for release status.

## Media remains Stage 2

This decision does not change the two-stage media plan. Stage 1 is the integrated
RCC product plus the written ClusterDocs site with video links fail-closed.
Stage 2 later regenerates, reviews, verifies, and activates the videos.

## Promotion and branch policy

The accepted candidate still requires separate explicit authorization before
merge into `main`. Production publication remains main-only. Neither this
decision nor a green candidate authorizes the merge.
