# RCC ClusterDocs 3 release candidate

`clusterdocs-3` is the temporary integration branch for the future RCC
documentation release. It describes RCC as a governed research-computing
platform rather than primarily as a cluster that every user must learn to
operate from a shell.

The long-term publication source is **`main`**. Candidate validation may happen
on `clusterdocs-3`, but production publication is intentionally blocked until an
accepted candidate is explicitly promoted into `main`. Nothing in this branch
or README authorizes that merge.

The public product model is **task-first and browser-first** for ordinary
researchers: choose or bring project data, analyse it in a Notebook or governed
Workflow when RCC Analysis is enabled, keep durable results with the project,
and preserve or publish them through the appropriate governed lifecycle.
SSH, VS Code, Slurm, containers, workflow engines, storage internals, and lower-
level diagnostics remain first-class advanced tools.

Experienced users should see the full platform: instrument ingestion for
sequencers, microscopes and other acquisition systems; project POSIX and
S3/object storage where enabled; DataLad; Jupyter; governed workflows; GPUs/HPC;
project self-governance and delegation; privacy-preserving AI/agent assistance;
project services; Coscine preservation status; and domain applications such as
SeqLab.

## Architecture principle

RCC deliberately does **not** force every workload onto one orchestration
platform merely because it is popular. Scientific jobs remain under Slurm and
Apptainer. Long-lived managed services use the RCC service plane, including
Nomad where deployed. A browser, workflow UI, or agent can request work, but it
does not create a second scientific scheduler. See
`docs/concepts/why-not-kubernetes-everywhere.md`.

## Credential principle

For RCC web passwords, passkeys, and appropriate recovery material, users should
use the built-in credential/password-manager facilities provided by supported
Windows/macOS/browser environments or another institutionally approved manager.

That guidance is **not** an SSH-key passphrase policy. RCC does not recommend a
passphrase on the normal software-backed RCC SSH key. The v3 workstation,
advanced-access, canonical Part 1 source, narration, and caption text now make
the no-passphrase policy explicit; hardware-backed FIDO SSH keys remain
preferred where appropriate.

The **existing generated Part 1 audio/video predates this correction**. It must
be regenerated from the corrected source/narration and its captions must be
re-timed/re-reviewed against the new audio before media activation. The source
policy itself is reconciled; generated media acceptance is the remaining Part 1
credential-content gate.

## AI and agent principle

The default coding-agent pattern is **data-blind by default**. General-purpose
or off-site agents can explain RCC, develop and review code/workflows, operate on
public code and synthetic fixtures, and interpret bounded sanitized diagnostics.
RCC executes the resulting analysis against real governed project data. Any
RCC-local agent capability allowed to work near protected data is a separately
reviewed exception rather than the default assumption.

## Current advanced workflow contract

Managed Nextflow-to-Slurm support is **ready now**. Its controller runs on an RCC
`shellhost` or allocation-backed **interactive node** while scientific tasks run
through Slurm. Resume-critical state stays in shared project storage; explicit
temporary task work can use node-local scratch. This advanced path remains
available even as the ordinary research front door becomes browser-first.

## Documentation and training layers

The site includes:

- a task-first home page and short browser-first start path;
- a complete capability overview for advanced researchers and technical staff;
- an architecture rationale for Slurm/service-plane/Kubernetes tradeoffs;
- RCC Analysis, Files, identity/project, agent, storage, lifecycle, and service
  documentation;
- an eighteen-class English-language RCC course for deeper optional training;
- advanced SSH/VS Code/Slurm/Snakemake/Nextflow/Apptainer reference material;
- instrument-ingestion, biomedical-data, efficient-I/O, and research-data
  lifecycle material; and
- the versioned offline RCC Expedition package.

## Release state

The branch is intentionally **not** self-declaring as production-ready. The
release machinery is fail-closed until the exact candidate has:

1. passed repository/build/link validation;
2. completed the fresh ClusterDocs 3 adversarial expert review;
3. completed zero-SSH naive-user browser acceptance before broad exposure;
4. completed separate advanced-user acceptance;
5. completed institutional/privacy/accessibility/operational checks;
6. regenerated and re-reviewed Part 1 media from the corrected no-passphrase credential source, and completed the remaining media review/verification;
7. selected the final release version; and
8. received explicit authorization to merge the accepted candidate into `main`.

A very small controlled pilot can precede broad acceptance to prove the deployed
journey works in principle. It does not replace the release gates.

## Candidate validation commands

Check whether human review can begin while working on `clusterdocs-3`:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The full production gate is run again **after an explicitly authorized merge on
the exact resulting `main` commit**:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

The production command is expected to fail while the release remains staged or
review/media evidence is incomplete.

## Deployment authority

Gitea is the manually dispatched production deployment authority. The production
workflow accepts only `refs/heads/main`, verifies the exact checked-out commit,
runs the fail-closed gates, generates `assets/release.json` with
`source_branch: main`, and publishes the exact generated tree as a normal
non-forced update to GitHub Pages. GitHub Actions remains a manual validation
fallback and has no deployment credential.

After a verified main-based publication, the temporary `clusterdocs-ng` and
`clusterdocs-3` branches can be retired through the approved repository process.
They are not to be deleted during candidate review.

## Local website preview

The RCC-styled site generated by `tools/build_site.py` is the canonical rendered
product. `mkdocs.yml` remains useful for structure/content checks but does not
reproduce the custom visual shell.

```bash
python3 tools/build_site.py --output site-preview
python3 -m http.server 8765 --bind 127.0.0.1 --directory site-preview
```

Then open `http://127.0.0.1:8765/` locally.

## Safety boundary

Educational examples are not validated clinical pipelines and do not replace
study-design, statistical, bioinformatics, data-protection, or clinical review.
No documentation interface, agent, API, or workflow obtains authority beyond the
user's RCC identity, project membership/delegated role, data policy, and current
service release state.
