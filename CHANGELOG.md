# Changelog

## v1.0.2 — deployment-state sync (5–6 October 2026)

Reconciled ClusterDocs with the RCC deployment state recorded in RCC `main`
`c000a582` (18.3.2) and the Essen site overlay on 5 October 2026.

- Named the live public jump host `login.ikim.uk-essen.de` in every SSH
  configuration example instead of a placeholder, and stopped telling users
  that the current `login` and `shellhost` names are stale.
- Marked RCC Admin / My RCC, RCC Files, the RCC home page, and the help
  assistant **not yet released**: the internal browser pilot was withdrawn on
  3 October 2026. Account and membership requests go to RCC support, and
  transfers use `scp`, `sftp`, or `rsync` to the shell host.
- Removed the site-shell links to the withdrawn Home, Files, and RCC Admin
  endpoints.
- Downgraded managed Nextflow-to-Slurm from ready to **validating**: the pinned
  launcher is deployed on some shell hosts, but end-to-end acceptance is
  pending.
- Narrowed Samba wording to existing instrument shares that are in service,
  with new shares set up by RCC on request.
- Marked opportunistic capacity, owner partitions, and `group_borrow` as staged
  and not yet enabled; corrected GPU request syntax to `gpu_nodes` with
  `--gpus-per-node` and the `rtx_a6000` type; noted that `ai_top_atom` and
  `interactive_gpu` currently have no schedulable capacity.
- Replaced the unsupported personal-quota claim with shared-capacity wording.

### Integrated pending documentation PRs

- Clarified shell-host transfers through the login bastion with complete
  `-J user@login… user@shellhost…` examples (#87).
- Distinguished the JuiceFS backend S3 layer from direct project S3, which is
  not yet released (#88).
- Added the planned encrypted Mac work-backup and home-disk recovery guide, not
  yet released (#89).
- Required the EMCP infrastructure citation for RCC-enabled publications (#86).
- Added the RCC Journey page, not yet released (#85).
- Documented the planned RCC Admin enrollment flow, not yet released (#82).
- Made markdown validation reproducible with `.markdownlint.yml` (#83).
- Rendered the Expedition and Class 1 onboarding notes as blockquotes instead of
  unsupported MkDocs admonitions (#91).
- Analysis and Workbench convergence (#84):
  - Reframed RCC Analysis as the planned user-facing compute product with two
    primary modes: Jupyter-first **Notebook** for interactive exploration and
    **Workflow** for repeatable/scalable governed analysis.
  - Demoted “RCC Workbench” from a peer user product to the advanced/internal
    interactive execution layer behind Analysis Notebook mode while preserving
    its documentation URL for architecture/reference use.
  - Documented a planned browser-first path (not yet released) beside the current
    SSH/VS Code path, which remains the required Expedition Light route today;
    once the browser services are released, an RCC account will no longer imply
    an SSH key.
  - Connected Files directly to the planned `Files -> Analysis -> Files` journey.
  - Added notebook-to-workflow resource guidance to discourage idle interactive
    allocations, CPU/RAM/GPU over-requesting, repeated manual analyses, tiny-job
    fan-out, and inefficient shared-storage I/O.
  - Preserved current-release accuracy: until RCC Analysis Notebook is explicitly
    activated, the existing Slurm + SSH-tunnel Jupyter procedure remains the
    supported notebook path.
- Listed every `mkdocs.yml` page in the published site menu (RCC services,
  Managed DataLad, authentication, Workbench, Usage, and publication pages) and
  added a test that keeps the two menus identical; set `VERSION` to 1.0.2.
- Added the remaining standalone pages (coding agents, project actions and
  delegated governance, data lifecycle, FAIR research objects, help and
  Guardians, Expedition maintenance) to both menus, with a test that every
  docs page outside `classes/examples/` is in the site menu.
- Flagged the Class 15 video for re-rendering: its narration gained the
  backend-S3 versus direct-project-S3 boundary after rendering. The readiness
  gate now blocks media release until it is re-rendered on macOS, and the
  class page notes that the written text is authoritative.

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

- Added Classes 7-10 for Python notebooks, R analysis, Shiny applications, and notebook-to-service workflows.
- Imported and adapted Python, R, Jupyter and Shiny examples from RCC user-workflow material.
- Added synthetic Python and R notebook examples.
- Added two instructor slide decks covering interactive large-data work and Shiny/Jupyter service patterns.
- Extended publication linting and validation to cover public examples.

## v0.1.1

- Expanded the governed vhost class and narration.
