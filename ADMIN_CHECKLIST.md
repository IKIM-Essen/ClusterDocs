# ClusterDocs 3 production checklist

`clusterdocs-3` is the temporary future-release integration line. Complete these
checks on the exact staged candidate before broad exposure. **Production
publication remains main-only.** Merging this candidate into `main` requires a
separate explicit authorization; this checklist does not authorize that merge.

The rollout has two independent publication stages:

1. **Stage 1 — written site:** publish the complete reviewed documentation with
   video links fail-closed/disabled. Media regeneration and approval do not block
   this stage.
2. **Stage 2 — videos:** after the repository text is stable, regenerate the
   videos on the approved workstation, review/publish them, and enable player
   links through the governed media configuration.

A small controlled pilot may prove the Stage-1 deployment works in principle but
does not replace expert, zero-SSH novice, advanced-user, accessibility, or
operational acceptance.

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
- [ ] Verify the [RCC-safe VS Code defaults](docs/getting-started/vscode.md#rcc-safe-vs-code-defaults) are visible before users are encouraged to open large project trees.
- [ ] Verify `search.followSymlinks: false`, `search.useIgnoreFiles: true`, watcher exclusions, and search exclusions prevent automatic traversal of data/results/environments/work directories in the test workspace.
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

## Architecture and I/O boundaries

- [ ] Adversarially review `docs/concepts/why-not-kubernetes-everywhere.md` against the current RCC implementation.
- [ ] Confirm the documentation states that **I/O access pattern is the most important RCC architecture constraint**, rather than presenting CPU count or advertised backend bandwidth as the primary design metric.
- [ ] Confirm the Ceph/Kubernetes comparison is fair: alternative platforms may be appropriate, but changing backend/orchestrator does not make small-file, metadata-heavy, random, temporary, or editor-driven I/O free.
- [ ] Confirm Slurm remains the scientific-compute authority and Nomad/service orchestration remains the long-lived service-plane authority; browser/agent actions must not create a second scheduler.
- [ ] Confirm future Kubernetes adoption remains possible when a concrete workload and operational benefit justify it.

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

## Stage 1 — written-site release

- [ ] Confirm `config/media-manifest.yml` keeps `preview_links` disabled before Stage-1 production publication.
- [ ] Build the production site and verify every video source is replaced by the fail-closed “Video not yet released” state; no dead MP4 link may escape into Stage 1.
- [ ] Confirm the written Class 1/source/caption policy is current even though the old generated Part-1 media is not being published.
- [ ] Confirm the short “What changed from the old cluster?” video is documented as a Stage-2 plan rather than a Stage-1 dependency.

## Stage 2 — media activation

- [ ] [stage-2] Regenerate Part 1 video/audio from the corrected source/narration and re-time/re-review its captions.
- [ ] [stage-2] Generate the short 3–4 minute “What changed from the old cluster?” video from `narration/RCC_What_Changed_From_Old_Cluster_Narration.md` if it remains useful after final text acceptance.
- [ ] [stage-2] Rebuild any other course videos whose final written/narration source changed materially after the previous render.
- [ ] [stage-2] Promote the exact approved MP4 set into the staged publication manifest and update hashes/sizes/durations.
- [ ] [stage-2] Verify trusted HTTPS, `video/mp4`, byte-range support, expected size, and full download for every released video.
- [ ] [stage-2] Complete human review of every released video and caption against final narration and visuals.
- [ ] [stage-2] Set media publication to `verified_live` and enable player links only after all Stage-2 gates pass.

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
- [ ] Set `site_status: production` on the accepted main release only after all Stage-1 gates pass.
- [ ] Run `python tools/validate_repo.py` on the exact main release commit.
- [ ] Run `python tools/build_site.py --production --output site-production` on the exact main release commit.
- [ ] Run `python tools/rollout_readiness.py` and resolve every Stage-1 blocker.
- [ ] Verify the published `assets/release.json` records `source_branch: main` and the exact main source commit.
- [ ] Verify the GitHub Pages update is a normal non-forced child commit and that rollback is documented/tested.
- [ ] Only after main-based publication is verified, retire the temporary `clusterdocs-ng` and `clusterdocs-3` branches according to repository policy; do not delete either branch as part of candidate review.
