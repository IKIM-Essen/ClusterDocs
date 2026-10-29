# Operator checklist — RCC Connect public release

> **Internal draft. No activation, rollout or release authorization.**

## Technical release gates

- [ ] Fix installer release provenance: signed, versioned packages; checksums served from official authenticated RCC infrastructure; establish installer update/revocation path.
- [ ] Verify the four shellhosts are accepted as client-only, reachable via the real jump service, with working `rcc-dev-session`, correct DNS and preserved host identity.
- [ ] Prove `pam_slurm_adopt` fails closed without a job and binds the IDE server, terminal, R/Python consoles and children to **the user's actual** Slurm job cgroup.
- [ ] Publish the authoritative SSH host-key fingerprint registry with appropriate independent signing/verification, covering jump, shellhost and selected workers. No TOFU under a non-interactive Positron session.
- [ ] Test passkey/SSH-agent, keyboard-interactive 2FA, certificate and device-onboarding flows on both OSes. Positron native OpenSSH must not depend on prompts.
- [ ] Qualify the Ubuntu worker release, editor-server binaries, extension downloads/install paths and network policy. VS Code and Positron server components must be obtainable without broad worker egress.
- [ ] Native Windows 10/11 and macOS supported-version regression suite: first install, upgrade, return to known-good, denied write, symlink/reparse, non-ASCII profile paths, OneDrive home, ACLs, shell conventions, available/missing OpenSSH.
- [ ] Integrate project/group authorization in an accepted server-side service; a user-supplied `PROJECT` path does not grant access.
- [ ] Ensure no new allocation is submitted when the previous request's outcome is ambiguous; reconcile using `sacct`/`squeue` and job ownership.
- [ ] Verify no IDE starts compute on shellhosts and no editor auto-indexing traverses all of `/projects`, `/groups` or `/homes`. Add storage metadata-rate monitoring and bounded policy.
- [ ] Determine session resource profiles and caps, including idle-time release and batch handoff; prohibit unmanaged autoSRE Slurm mutations.
- [ ] Test session loss, reconnection, timeout, server reboot, Slurm failover and partial installer rollback with durable receipts.

## Experience and documentation gates

- [ ] Pilot separately with at least one R/Positron and one Python/VS Code user on each desktop OS.
- [ ] Pilot task-based pathways: browser-first recommendation, VS Code,
  Positron and direct SSH/CLI. Every authorized interface must be selectable
  without a "beginner/expert" label, self-rating or shell-proficiency test.
- [ ] Make "Switch interface" discoverable and reversible; do not hide the
  terminal behind an advanced-user gate. Any saved interface preference must
  be explicitly chosen, changeable and separate from authorization.
- [ ] Offer simple/detailed controls inside every interface, without changing
  Slurm limits, permissions or data visibility. Test with scientists who
  know Bash but not Slurm and scientists who prefer web despite strong HPC
  experience; avoid stereotypes.
- [ ] Show transparent job queueing, project permissions, and estimated
  resource use without invented availability. On failed scheduling, suggest
  alternatives but never silently run compute on a shellhost.
- [ ] Verify a user can prepare in one interface and inspect/reattach to the
  same authorized allocation where supported, without duplicate submissions.
- [ ] Provide German and English editions, accessibility review, ClusterDocs navigation, synthetic screenshots and clear support ownership.
- [ ] Add an authenticated myRCC download page with enrollment/status and user-specific parameters; never embed private SSH material in downloads.
- [ ] Publish a clear warning that Workbench and desktop deployment have independent acceptance gates. Do not link staged features as if live.
- [ ] Retain opt-in pilot boundaries; do not include prototype changes on the Admin go-live train.

## Multi-node Slurm batch acceptance

- [ ] Test one synthetic two-node CPU batch with correct placement of
  `--nodes`, `--ntasks-per-node`, `--cpus-per-task`, per-node `--mem` and
  walltime; inspect resulting allocation and per-rank logs.
- [ ] Test an independently built MPI executable; confirm the accepted
  MPI plugin with `srun --mpi=list` rather than assuming `pmix`.
- [ ] For multi-node GPU jobs, qualify GPU counts per node, fabric,
  NCCL/distributed runtime, affinity, container compatibility and failure
  cleanup before exposing a user profile.
- [ ] Verify project authorization, QOS limits, worker eligibility, scheduler
  queueing, cancellation, job-array alternative and real job accounting.
- [ ] Verify request identity and durable receipt prevent automatic duplicate
  submission after ambiguous `sbatch`/transport outcome. Test malicious
  spec fields, traversal, policy ownership and mismatched resource ceilings.
- [ ] Keep interactive VS Code/Positron backend **single-node**; all distributed
  processes must run as Slurm batch steps, never from the shellhost or direct
  user-controlled SSH between compute nodes.
- [ ] Allow browser, VS Code, Positron and terminal users to choose the same
  accepted multi-node submission contract without an expert/beginner gate.
- [ ] Do not enable the example site policy or publish the multi-node option
  until the corresponding host/Slurm/MPI/GPU and documentation gates pass.

## VS Code allocation-backed server acceptance

- [ ] Start a session on an accepted worker, connect the local VS Code
  Remote-SSH client, and observe the worker-side VS Code Server, remote
  extension hosts, terminals, Python, Jupyter and language-server processes.
- [ ] Prove by cgroup inspection (not only SSH success) that every process
  belongs to the user's **actual Slurm job**. Deny connections before the
  job is running and after it ends, including attempts to use stale aliases.
- [ ] Verify a completed, cancelled and timed-out Slurm job terminates all
  associated server and child processes, including detached subprocesses and
  any lingering user service. No unscheduled compute may survive on workers.
- [ ] Prove strict host-key verification on the selected worker before
  non-interactive editor connection; changing or missing key must fail closed.
- [ ] Verify a matching VS Code Server build is delivered under reviewed
  worker network/egress policy, without broad downloads or unbounded
  metadata-heavy installation on shared project storage.
- [ ] Test idle session, disconnect, reconnect, failover, server restart,
  storage scratch cleanup and one explicit stop; never silently resubmit
  following ambiguous client transport failure.
- [ ] Test VS Code workspace `rg`, file watching and extension behavior with
  a small synthetic source tree and with bounded shared-storage telemetry.
  No production filesystem-wide scan is an acceptable test.

## Documentation core/site separation acceptance

- [ ] Classify all existing ClusterDocs pages and assets as generic, Essen,
  mixed or historical; document where the final content will live.
- [ ] Establish a distinct site-neutral `clusterdocs` source with **fresh,
  sanitized history**, a site-marker leakage test, link checks and a build
  that fails on unfilled site values.
- [ ] Pin generic source by exact revision in the Essen overlay; review
  rendered output, content license, accessibility, screenshots and media.
- [ ] Preserve the current site's production URL and deep links during the
  future `clusterdocs-site-essen` rename. Check Github Pages path, redirect
  decisions and existing media paths before any cutover.
- [ ] Confirm that generic docs make no promise of local live availability
  and contain no Essen hostnames, institutional policies or local trust facts.
- [ ] Keep all of this material out of published navigation until both
  source and site acceptance are complete. See
  [migration plan](09-core-site-migration-plan.md).

## Known prototype limitations

This prototype uses local configuration files and SSH command output; it is not
an authenticated Desktop API, an offline signer, a multi-device credential
manager, a Workbench client or an autoSRE resource recommender. CLI `--gpu`
uses the existing Slurm helper, not a scheduler learned profile. macOS tests
mock SSH only; Windows has no native runtime evidence. A user can still launch
arbitrary shell commands manually; editor configuration does not enforce
filesystem-access policy or resource quotas.

Backlog: signed host-key registry, progress/status UX, project picker, verified
binary distribution, uninstall/upgrade, session record file and safe recovery,
Windows test harness, resource-policy integration, and localized onboarding.
## Additional v2.2 acceptance checks

- Positive and negative cross-project `attach` tests: a user-owned job from another project must not be connected under the selected project.
- If `scontrol show job -o JOBID` fails or omits `WorkDir`, the client must stop and must not submit a replacement.
- Review Slurm WorkDir parsing against live Slurm 25.11.2 output, including unusual project paths.
- Confirm Windows PowerShell runtime, file ACLs, native OpenSSH, Positron transport, and editor bootstrap under supported endpoint policy.
