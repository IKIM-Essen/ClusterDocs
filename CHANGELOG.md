# Changelog

## Unreleased — ClusterDocs 3

- Reframed the front door around research tasks rather than cluster topology:
  project files, browser analysis, project/account actions, then advanced
  SSH/VS Code/Slurm when needed.
- Added a dedicated **What RCC can do** overview so experienced users can see
  instrument ingestion, project S3/object storage where enabled, DataLad,
  Notebook/Workflow, Slurm/GPU/HPC, delegated governance, project services,
  Coscine preservation status, and domain applications such as SeqLab.
- Recorded a dated **external-reader review** in
  `meta/EXTERNAL_READER_REVIEW_2026-09-05.md`. The subsequent release decision
  resolves its main current-versus-target ambiguity by making the integrated
  browser experience a hard release boundary rather than publishing Analysis as
  a post-release promise.
- Defined the **ClusterDocs 3 integrated release bundle** as RCC Home + Files +
  RCC Analysis + My RCC + RCC Admin. All five surfaces must be recorded `ready`
  and pass end-to-end acceptance before production publication. The current
  candidate is intentionally blocked while `rcc_analysis` is
  `not_yet_released`.
- Added `tools/release_bundle_gate.py` and wired it into the main-only production
  workflow so changing `site_status` cannot bypass the five-surface release
  requirement.
- Made **I/O access pattern the primary architecture/performance rationale**:
  shared bandwidth does not make metadata storms, many-small-file workloads,
  temporary random I/O, synchronized reads, or editor/indexer traversal free.
  The Kubernetes/Ceph discussion now starts from workload I/O rather than
  platform popularity.
- Added an advanced **Why RCC does not run everything on Kubernetes** rationale:
  Slurm remains the scientific-compute authority, long-lived managed services
  use the RCC service plane (including Nomad where deployed), and another
  orchestrator should be introduced only for a concrete supported workload or
  operational benefit rather than popularity alone.
- Promoted **RCC-safe VS Code defaults** into the first-use advanced guide,
  including `search.followSymlinks: false`, `search.useIgnoreFiles: true`, and
  explicit watcher/search exclusions for data, results, environments, package
  trees, Snakemake/Nextflow state, and workflow work directories.
- Reframed AI/coding-agent guidance around a **data-blind by default** pattern:
  agents can explain, design, test with synthetic fixtures, develop workflows,
  and interpret bounded diagnostics while RCC executes against real data inside
  the governed project boundary.
- Reframed RCC Analysis as the required user-facing compute product with two
  primary modes: Jupyter-first **Notebook** for interactive exploration and
  **Workflow** for repeatable/scalable governed analysis.
- Demoted “RCC Workbench” from a peer user product to the advanced/internal
  interactive execution layer behind Analysis Notebook mode while preserving
  its documentation URL for architecture/reference use.
- Split onboarding into a browser-first path and an advanced SSH/VS Code path;
  an RCC account no longer implies that the user must enroll an SSH key.
- Reconciled the RCC credential model: built-in Windows/macOS/browser password
  managers are recommended for web passwords, passkeys, and appropriate
  recovery material, while the normal software-backed RCC SSH key is explicitly
  generated **without a passphrase**; hardware-backed FIDO SSH keys remain
  preferred where appropriate.
- Reconciled canonical Part 1 source, active written guidance, narration, and
  caption text with the no-passphrase SSH-key policy. Existing generated Part 1
  audio/video is deferred to the media wave and must be regenerated/re-reviewed
  before activation.
- Kept a **two-stage media rollout**: Stage 1 is the integrated five-surface RCC
  browser product plus the reviewed written site with video links fail-closed;
  Stage 2 later regenerates, reviews, verifies, and enables media. Video approval
  is not a Stage-1 blocker, but RCC Analysis is.
- Added a prepared 3–4 minute **What changed from the old cluster?** returning-
  user narration for the Stage-2 media wave, centered on browser/project changes,
  I/O behavior, local scratch, and low-I/O VS Code settings.
- Connected Files directly to the `RCC Home -> Files -> Analysis -> Files`
  journey and made My RCC/RCC Admin role separation part of the release
  acceptance contract.
- Added notebook-to-workflow resource guidance to discourage idle interactive
  allocations, CPU/RAM/GPU over-requesting, repeated manual analyses, tiny-job
  fan-out, and inefficient shared-storage I/O.
- Invalidated the August expert receipt for the materially changed v3 product
  model and made fresh adversarial review, zero-SSH novice-browser acceptance,
  and separate advanced-user acceptance hard gates before broad exposure.
- Changed the long-term release model so temporary candidate branches may be
  validated/reviewed, but **production publication accepts `main` only**. An
  accepted `clusterdocs-3` candidate requires separate explicit authorization
  before merge into `main`; `clusterdocs-ng` and `clusterdocs-3` are retired
  only after verified main-based Stage-1 publication and rollback evidence.
- Preserved release-state accuracy for separately staged services such as
  RCC-to-Coscine transfer, project vhosts, and selected vendor integrations.

## v1.0.1

- Made RCC Expedition Light the required first-use route and added direct,
  installation-light setup pages for macOS and Windows 11.
- Added a dedicated VS Code Remote SSH guide with safe workspace defaults.
- Explained the jump-host, shell-host, and Slurm-worker roles as one access
  model.
- Clarified users, primary groups, collaboration projects, and storage layout
  for larger science teams.
- Added a guided path for converting shell command collections into tested,
  restartable Snakemake or Nextflow workflows with pinned Conda-derived
  Apptainer images.
- Added an old-to-new cluster migration table based on the public documentation
  at commit `8f5b2bd` from 21 July 2026.
- Published the immutable RCC Expedition USB v1.0.1 archive while preserving
  the v1.0.0 asset and checksum.
- Reconciled the course and canonical source with the ready-now managed
  Nextflow-to-Slurm support contract.

## v0.1.3

- Added Class 11 on European and German biomedical-data protection.
- Documented the RCC non-identifiable-data admission rule and the difference between anonymisation and pseudonymisation.
- Added genomic, medical-imaging, free-text, rare-cohort, and data-linkage risk guidance.
- Added a proportionate defacing decision path that favours derived or upstream-approved data when possible.
- Added official EU, German, BfDI, EDPB, and Universitätsklinikum Essen resources.
- Clarified that approved genomic and X-ray/CT/MRI research data may be processed inside RCC even though they can remain special-category or indirectly identifying data.
- Replaced machine-generated admission outcomes with scenario-based user training and human project governance.
- Clarified that defacing is a possible disclosure safeguard, not a default requirement for controlled enclave research.
- Added tests for the training boundary and official-resource links.
- Enabled validation pushes on the `clusterdocs-ng` branch.

## v0.1.2

- Added Classes 7-10 for Python notebooks, R analysis, Shiny development, and notebook-to-service workflows.
- Imported and adapted Python, R, Jupyter and Shiny examples from RCC user-workflow material.
- Added synthetic Python and R notebook examples.
- Added two instructor slide decks covering interactive large-data work and Shiny/Jupyter service patterns.
- Extended publication linting and validation to cover public examples.

## v0.1.1

- Expanded the governed vhost class and narration.
