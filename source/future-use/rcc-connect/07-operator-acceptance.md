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
- [ ] Include beginner and expert workflows; show transparent job queueing, project permissions, and estimated resource use without invented availability.
- [ ] Provide German and English editions, accessibility review, ClusterDocs navigation, synthetic screenshots and clear support ownership.
- [ ] Add an authenticated myRCC download page with enrollment/status and user-specific parameters; never embed private SSH material in downloads.
- [ ] Publish a clear warning that Workbench and desktop deployment have independent acceptance gates. Do not link staged features as if live.
- [ ] Retain opt-in pilot boundaries; do not include prototype changes on the Admin go-live train.

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
