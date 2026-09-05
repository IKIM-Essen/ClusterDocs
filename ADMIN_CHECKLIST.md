# ClusterDocs 3 production checklist

`clusterdocs-3` is the temporary future-release integration line. Complete these
checks on the exact staged candidate before broad exposure. **Production
publication remains main-only.** Merging this candidate into `main` requires a
separate explicit authorization; this checklist does not authorize that merge.
A small controlled pilot may prove the deployment works in principle but does
not replace the expert, zero-SSH novice, advanced-user, accessibility, media, or
operational acceptance gates.

## Browser-first product and identity

- [ ] Verify RCC Home, Files, Account & projects, Documentation, and staged RCC Analysis links against the actual deployment.
- [ ] Verify a test account with no SSH public key can sign in and use every browser capability intended for ordinary researchers.
- [ ] Verify project selection and authorization are consistent across Files, Analysis, Assistant/agent capabilities, and account/project actions.
- [ ] Verify stale deep links, guessed run/object identifiers, and role changes cannot broaden project access.
- [ ] Verify self-service project/account actions cannot be confused with infrastructure-administrator authority.
- [ ] Confirm the support route and escalation process shown to users.

## Zero-SSH novice acceptance

- [ ] Run `meta/NOVICE_REVIEW_GUIDE.md` against the exact staged candidate before broad exposure.
- [ ] Verify Files -> Analysis Notebook -> durable project result -> Files/download without facilitator shell intervention.
- [ ] Verify the reviewer can distinguish Notebook from Workflow and find the support route.
- [ ] Verify the reviewer can explain the data-blind agent pattern without being taught RCC internals first.
- [ ] Record and resolve every blocker/major novice finding.

## Advanced-user acceptance

- [ ] Complete the advanced path on supported Windows and macOS clients.
- [ ] Verify OpenSSH, host identity, ProxyJump, the **no-passphrase normal RCC software-key policy**, VS Code Remote SSH, and the forwarding-only gateway model.
- [ ] Verify built-in Windows/macOS/browser password/passkey-manager guidance is limited to web/account credentials and recovery material rather than being presented as an SSH-key passphrase requirement.
- [ ] Verify direct Slurm, interactive allocations, GPU selection, accounting, cancellation, and current scheduler limits.
- [ ] Verify Conda/Mamba, Snakemake, Nextflow, rootless Apptainer, Gitea, local scratch, and efficient I/O guidance.
- [ ] Verify every command states or clearly implies the correct execution location and requires no unapproved privilege.

## RCC Analysis and workflow governance

- [ ] Verify the user-facing release status of RCC Analysis; documentation must not make an unreleased service appear live.
- [ ] Verify Notebook allocations are bounded and idle/repeated work is steered toward more appropriate execution modes.
- [ ] Verify Workflow uses governed Slurm execution and does not expose raw scheduler/workflow-engine argument injection through the ordinary browser path.
- [ ] Verify uncertain submission/retry behavior cannot create duplicate scientific runs.
- [ ] Verify durable results, workflow identity, scientific parameters, software identity, and provenance remain project-scoped.

## AI and agent boundary

- [ ] Verify ordinary off-site/general-purpose agent use works from documentation, public code, schemas, synthetic fixtures, and bounded diagnostics without real protected project data.
- [ ] Verify agent/MCP/API interfaces cannot create project membership, administrator authority, data approval, or scheduler authority.
- [ ] Verify separately approved RCC-local data-near agent capabilities are explicit exceptions with their own authorization boundary.
- [ ] Verify support and agent troubleshooting never asks users to paste secrets, unrestricted logs, complete datasets, patient data, or unnecessary filenames.

## Instrument ingestion, storage, and lifecycle

- [ ] Verify project Samba ingestion for approved registered devices and its **ready now** wording.
- [ ] Verify server-to-server and recurring-instrument guidance for sequencers, microscopes, mass spectrometers, and other acquisition systems.
- [ ] Verify personal laptops and home directories are not presented as the normal recurring instrument-data landing zone.
- [ ] Verify project POSIX storage, S3/object storage where separately enabled, DataLad, job-local scratch, and sharing guidance remain project-scoped.
- [ ] Verify Ardia integration is still marked **not yet released** until the deployment owner activates it.
- [ ] Verify the RCC-to-Coscine transfer path is marked **not yet released** until online end-to-end archive verification is complete.
- [ ] Verify archive guidance distinguishes a verified preservation transfer from an ordinary copy.
- [ ] Review SeqLab/domain-application wording so archive submission capabilities remain governed by the deployed application and destination-specific review.

## Architecture and platform boundaries

- [ ] Adversarially review `docs/concepts/why-not-kubernetes-everywhere.md` against the current RCC implementation.
- [ ] Confirm Slurm remains the scientific-compute authority and Nomad/service orchestration remains the long-lived service-plane authority; user-facing browser/agent actions must not create a second scheduler.
- [ ] Confirm the architecture page does not imply Kubernetes is prohibited forever; future Kubernetes adoption requires a concrete workload/operational benefit rather than popularity alone.

## Data protection and scientific boundaries

- [ ] Confirm the local policy that direct identifiers and re-identification keys remain outside RCC while approved biomedical research data may be processed under the project policy.
- [ ] Review biomedical-data admission, genomic/imaging scenarios, defacing/pseudonymisation guidance, and external legal links with the responsible institutional office.
- [ ] Review statistical, AI, and sequence-analysis disclaimers with domain experts.
- [ ] Verify data-release/sharing language does not imply project membership alone authorizes external disclosure.

## Resource efficiency and operations

- [ ] Confirm cluster/account/partition/QOS/time/CPU/memory/GPU syntax and current supported versions.
- [ ] Confirm node-local scratch path/capacity and the documented staging patterns.
- [ ] Confirm practical file-count/directory-count guidance and representative shared-vs-local I/O behavior.
- [ ] Verify resource recommendations can use privacy-minimized utilization evidence without needing research contents.
- [ ] Confirm Usage/capacity views are advisory operational evidence rather than billing, punishment, or entitlement.

## Web shell, accessibility, and deterministic build

- [x] Configure RCC Home, Files, and Account & projects endpoints in `config/public.yml` rather than scattering service URLs through the renderer.
- [x] Remove the runtime dependency on the external UME logo from the generated site.
- [x] Replace the decorative green “Documentation online” indicator with the explicit configured documentation status.
- [ ] Complete clean-client desktop/mobile checks and keyboard/screen-reader acceptance.
- [ ] Check internal links through the generated-site link checker and perform the final external link check online.
- [ ] Verify rendering and critical workflows in the supported browser set.

## Media

- [x] Keep media publication fail-closed until the separate RCC media endpoint passes its checks.
- [ ] Reconcile `source/part1.md` with the current **no-SSH-passphrase** policy; the old canonical Part 1 source must not remain authoritative for v3 media.
- [ ] Regenerate the Part 1 video from the corrected narration/source and re-review its audio/captions before activation; the staged old audio states the retired passphrase policy.
- [ ] Promote the exact approved MP4 set into the staged publication manifest and verify hashes.
- [ ] Verify trusted HTTPS, `video/mp4`, byte-range support, expected size, and full download for every released video.
- [ ] Complete human review of every released video and caption against final narration and visuals.

## Release control

- [x] Make candidate validation branch-agnostic/manual so `clusterdocs-3` can be reviewed without becoming a permanent publication branch.
- [x] Pin the manual Gitea **production** workflow to `refs/heads/main`; reject direct production publication from `clusterdocs-3` or `clusterdocs-ng`.
- [x] Keep GitHub Actions as manual validation fallback only and deployment-credential free.
- [ ] Choose and record the final release version; do not infer it solely from the temporary branch name.
- [ ] Complete the fresh ClusterDocs 3 adversarial expert review in `meta/EXPERT_REVIEW_GUIDE.md`.
- [ ] Record the expert review as `completed` only after blocker/major findings are resolved or explicitly accepted.
- [ ] Record zero-SSH novice browser acceptance as `completed` before broad exposure.
- [ ] Record the separate advanced-user acceptance as `completed` before broad exposure.
- [ ] Provision and acceptance-test the dedicated GitHub Pages deploy key and pinned GitHub SSH host key in Gitea.
- [ ] Obtain explicit authorization to merge the accepted `clusterdocs-3` candidate into `main`. **No authorization is recorded by this checklist.**
- [ ] After the authorized merge, run validation again on the exact `main` commit and verify it contains no unreviewed post-candidate changes.
- [ ] Set `site_status: production` on the accepted main release only after all preceding gates pass.
- [ ] Run `python tools/validate_repo.py` on the exact main release commit.
- [ ] Run `python tools/build_site.py --production --output site-production` on the exact main release commit.
- [ ] Run `python tools/rollout_readiness.py` and resolve every reported blocker.
- [ ] Verify the published `assets/release.json` records `source_branch: main` and the exact main source commit.
- [ ] Verify the GitHub Pages update is a normal non-forced child commit and that rollback is documented/tested.
- [ ] Only after main-based publication is verified, retire the temporary `clusterdocs-ng` and `clusterdocs-3` branches according to repository policy; do not delete either branch as part of candidate review.
