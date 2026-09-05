# ClusterDocs 3 production checklist

ClusterDocs 3 is the future RCC documentation release. Complete these checks on
the exact staged candidate before broad exposure. A small controlled pilot is
allowed to prove the deployment works in principle; it does not replace the
expert, zero-SSH novice, advanced-user, accessibility, media, or operational
acceptance gates.

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
- [ ] Verify OpenSSH, host identity, ProxyJump, SSH key policy, VS Code Remote SSH, and the forwarding-only gateway model.
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
- [ ] Promote the exact approved MP4 set into the staged publication manifest and verify hashes.
- [ ] Verify trusted HTTPS, `video/mp4`, byte-range support, expected size, and full download for every released video.
- [ ] Complete human review of every released video and caption against final narration and visuals.

## Release control

- [x] Pin the manual Gitea production workflow to `refs/heads/clusterdocs-3` and reject the retired `clusterdocs-ng` production source.
- [x] Keep GitHub Actions as manual validation fallback only and deployment-credential free.
- [ ] Complete the fresh ClusterDocs 3 adversarial expert review in `meta/EXPERT_REVIEW_GUIDE.md`.
- [ ] Record the expert review as `completed` only after blocker/major findings are resolved or explicitly accepted.
- [ ] Record zero-SSH novice browser acceptance as `completed` before broad exposure.
- [ ] Record the separate advanced-user acceptance as `completed` before broad exposure.
- [ ] Provision and acceptance-test the dedicated GitHub Pages deploy key and pinned GitHub SSH host key in Gitea.
- [ ] Set `site_status: production` only after all preceding gates pass.
- [ ] Run `python tools/validate_repo.py` on the exact release candidate.
- [ ] Run `python tools/build_site.py --production --output site-production` on the exact release candidate.
- [ ] Run `python tools/rollout_readiness.py` and resolve every reported blocker.
- [ ] Verify the published `assets/release.json` records `source_branch: clusterdocs-3` and the exact source commit.
- [ ] Verify the GitHub Pages update is a normal non-forced child commit and that rollback is documented/tested.
