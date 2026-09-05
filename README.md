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

## Architecture principle: I/O first

The single most important architectural lesson behind the current RCC design is
that **I/O access pattern usually matters more than headline storage bandwidth**.
Many-small-file metadata traffic, directory scans, package environments,
workflow work directories, temporary random I/O, synchronized reference reads,
and editor/indexer activity can dominate elapsed time and shared-service load.

RCC therefore tries to shape I/O before simply scaling infrastructure:

- durable project inputs/results stay on governed shared storage;
- active random/temporary/high-I/O working sets move to node-local scratch when
  useful;
- workflows declare/stage data deliberately;
- caches use stable identities; and
- developer tools such as VS Code are configured not to crawl large shared-data
  trees automatically.

This is a major reason RCC does **not** assume that moving everything onto one
popular substrate such as Ceph or Kubernetes would solve the research workload.
Changing backend technology cannot make a hostile metadata/random-I/O pattern
free.

Scientific jobs remain under Slurm and Apptainer. Long-lived managed services
use the RCC service plane, including Nomad where deployed. A browser, workflow
UI, or agent can request work, but it does not create a second scientific
scheduler. See `docs/concepts/why-not-kubernetes-everywhere.md` and
`docs/course/class-14-efficient-io.md`.

## Credential principle

For RCC web passwords, passkeys, and appropriate recovery material, users should
use the built-in credential/password-manager facilities provided by supported
Windows/macOS/browser environments or another institutionally approved manager.

That guidance is **not** an SSH-key passphrase policy. RCC does not recommend a
passphrase on the normal software-backed RCC SSH key. The v3 workstation,
advanced-access, canonical Part 1 source, narration, and caption text make the
no-passphrase policy explicit; hardware-backed FIDO SSH keys remain preferred
where appropriate.

The existing generated Part 1 audio/video predates this correction. It is not a
Stage-1 dependency and must remain unlinked until regenerated/re-reviewed in the
Stage-2 media wave.

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
- an I/O-first architecture rationale for storage and Slurm/service-plane/
  Kubernetes tradeoffs;
- prominent RCC-safe VS Code search/watcher defaults;
- RCC Analysis, Files, identity/project, agent, storage, lifecycle, and service
  documentation;
- an eighteen-class English-language RCC course for deeper optional training;
- advanced SSH/VS Code/Slurm/Snakemake/Nextflow/Apptainer reference material;
- instrument-ingestion, biomedical-data, efficient-I/O, and research-data
  lifecycle material; and
- the versioned offline RCC Expedition package.

## Two-stage release

The media pipeline is intentionally **not** on the critical path for the first
ClusterDocs 3 publication.

### Stage 1 — written site

After text/product/operational acceptance and explicit promotion into `main`,
publish the complete written site with `preview_links` disabled. The renderer
must replace video players with the fail-closed “Video not yet released” state.
Human approval of the old generated videos does not block Stage 1.

### Stage 2 — videos

Once the written/narration sources are stable, regenerate media on the approved
workstation, update exact hashes/sizes/durations, perform human review and online
media verification, then enable video links through the governed media state.

Stage 2 includes a proposed **3–4 minute “What changed from the old cluster?”**
video for returning users. Its prepared narration lives at
`narration/RCC_What_Changed_From_Old_Cluster_Narration.md`.

## Stage-1 release state

The candidate is not broadly promotable until it has:

1. passed repository/build/link validation;
2. completed the fresh ClusterDocs 3 adversarial expert review;
3. completed zero-SSH naive-user browser acceptance before broad exposure;
4. completed separate advanced-user acceptance including the low-I/O VS Code
   profile;
5. completed institutional/privacy/accessibility/operational checks;
6. kept all video links fail-closed for Stage 1;
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

With media links disabled, the readiness gate treats video regeneration/review
as deferred Stage-2 work rather than a Stage-1 blocker. Once links are enabled,
media verification and human approval become hard gates.

## Deployment authority

Gitea is the manually dispatched production deployment authority. The production
workflow accepts only `refs/heads/main`, verifies the exact checked-out commit,
runs the active-stage fail-closed gates, generates `assets/release.json` with
`source_branch: main`, and publishes the exact generated tree as a normal
non-forced update to GitHub Pages. GitHub Actions remains a manual validation
fallback and has no deployment credential.

After a verified main-based Stage-1 publication, the temporary `clusterdocs-ng`
and `clusterdocs-3` branches can be retired through the approved repository
process. Stage-2 video work should then use an ordinary branch from `main` and
return to `main`.

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