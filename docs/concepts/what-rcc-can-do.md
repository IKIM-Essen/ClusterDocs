# What RCC can do

RCC is a research platform, not only a login host and batch scheduler. Its goal
is to connect the full research lifecycle while keeping data, identity,
execution, provenance, and governance coherent.

This page is intentionally aimed at experienced researchers, facility staff,
research software engineers, and technical project leads who want to see the
complete platform.

> **Status rule:** “RCC can support” does not mean every capability is already
> enabled for every project. Follow the status on the linked page and RCC Home.
> In particular, RCC Analysis, project vhosts, Ardia integration, and the
> RCC-to-Coscine transfer path are **not yet released** in the current candidate.

## The architecture starts with I/O behavior

The most important technical constraint behind the current RCC platform is
**I/O access pattern**, not simply advertised storage capacity or bandwidth.
Scientific workloads can generate millions of small-file metadata operations,
repeated directory scans, package/environment lookups, workflow temporary state,
random database/index access, synchronized reference reads, and editor/indexer
traffic.

That is why RCC combines governed shared project storage with **node-local
scratch**, deliberate staging, caching, immutable/reusable artifacts, and
workflow guidance that distinguishes streaming from random/metadata-heavy I/O.
It is also why RCC does not assume that putting everything on Ceph, Kubernetes,
or any other single popular substrate would automatically solve the workload.
A different backend cannot make an inefficient access pattern free.

Advanced users should read
[Why RCC does not run everything on Kubernetes](why-not-kubernetes-everywhere.md),
[Class 14: efficient I/O](../course/class-14-efficient-io.md), and the
[RCC-safe VS Code defaults](../getting-started/vscode.md#rcc-safe-vs-code-defaults).

## Connect instruments and acquisition systems

RCC can accept data from sequencers, microscopes, mass spectrometers, acquisition
workstations, facility servers, and other scientific devices through reviewed
project ingestion paths.

For current approved projects, **project Samba shares are ready now** and provide
a familiar managed landing path for suitable registered devices. Large recurring
or automated sources can use server-to-server or dedicated ingestion patterns.
Vendor-specific integrations are enabled only after their own review; Ardia
integration is **not yet released**.

The important property is that instrument data lands in the **project**, not in
a researcher's laptop or personal home directory.

Read [Choosing an instrument-data transfer path](../data/instrument-data-options.md).

## Use the storage model that fits the science

A project can use different storage semantics for different needs:

- shared POSIX project storage for ordinary collaborative files and workflow
  inputs/outputs;
- **project S3/object storage** where object semantics, scale, or an application
  require it and the capability is enabled;
- DataLad/git-annex backed state for versioned large-data workflows where
  appropriate;
- job-local scratch for high-I/O temporary computation; and
- governed preservation rather than treating primary compute storage as a
  permanent archive.

Storage choice is part of the project/service contract, not something every
user must configure from raw infrastructure components.

## Explore interactively, then make the work reproducible

RCC Analysis is designed around two adjacent modes:

- **Notebook** — Jupyter-first exploration, visualization, statistics,
  prototyping, and bounded interactive work;
- **Workflow** — repeatable, scalable, governed execution with declared inputs,
  parameters, outputs, software identity, and provenance.

A successful notebook should be able to graduate into a workflow without making
the researcher learn a different cluster product. RCC keeps Slurm as the compute
authority underneath the browser interface.

RCC Analysis is **not yet released**. Until it is activated, current SSH/VS Code,
Slurm, managed Snakemake/Nextflow, and SSH-tunnel notebook routes remain the
supported compute path.

## Keep the advanced HPC capabilities

Browser-first does not mean “beginner-only.” Advanced users retain direct access
to **Slurm, GPUs**, shell tools, VS Code Remote SSH, Conda environments, rootless
Apptainer, Snakemake, Nextflow, Gitea, efficient local scratch patterns, and
lower-level diagnostics.

The improvement is that those mechanics are **available when useful rather than
mandatory before science can begin**.

Advanced infrastructure users may reasonably ask why RCC does not simply put
all of this onto Kubernetes. The split is deliberate: scientific compute stays
under Slurm, while long-lived managed services use the RCC service plane. Read
[Why RCC does not run everything on Kubernetes](why-not-kubernetes-everywhere.md).

## Let projects govern themselves within bounded authority

RCC projects combine membership, data, compute, services, results, and lifecycle
under one authorization boundary. Project leads can delegate named capabilities
such as membership approval, storage/compute requests, lifecycle actions, or
archive preparation without granting general LDAP, Slurm, storage, or root
administration.

Automation and agents use the same capability model. They do not acquire hidden
administrator authority merely because an action is requested programmatically
or in natural language.

## Use AI assistance without exporting the dataset

A major RCC design goal is to separate **AI assistance** from **data disclosure**.
The preferred pattern is **data-blind by default**. An external or general-purpose
coding agent can help with:

- RCC documentation and explanations;
- workflow and software design;
- public code;
- synthetic test fixtures;
- schemas and data contracts that contain no protected records;
- generic or carefully bounded diagnostics; and
- code review, refactoring, testing, and reproducibility work.

The agent does **not** need the real project rows, reads, images, patient-derived
records, or filenames merely to be useful. It proposes code/workflows; RCC
validates authorization and executes those against the real data inside the
governed environment; only permitted results or bounded diagnostics leave that
execution boundary.

Some separately reviewed RCC-local agent capabilities may be authorized to work
near data. That is an explicit governed capability, not the default assumption
for coding-agent use.

Read [AI and coding agents without exposing project data](agents-and-mcp.md).

## Make resource efficiency part of the workflow

RCC can use privacy-minimized utilization evidence to identify wasteful patterns
without inspecting scientific content: oversized CPU/RAM requests, GPUs with
little GPU use, long-idle interactive sessions, thousands of tiny jobs, or
shared-storage I/O patterns that should use local scratch.

The purpose is to improve throughput and user experience, not to turn approximate
usage data into billing, punishment, or a scientific entitlement system.

## Build project and domain services on top of RCC

RCC can support project-scoped databases, protected web applications, Gitea,
DataLad, object storage, workflow services, and domain applications. Project
vhosts are **not yet released** in the current candidate. These capabilities let
a research group or facility build a reproducible service on the same identity,
project, data, and compute foundation rather than creating another isolated
infrastructure stack.

**SeqLab** is the useful mental model for a domain application: sequencing data
can move from acquisition into project storage, through analysis and review,
retain provenance and metadata, and then support submission to the appropriate
international sequence archives when the SeqLab/deployment path enables that
function. The user should not have to assemble separate identity, scheduler,
storage, and archive machinery to achieve that lifecycle.

The same pattern can support microscopy, imaging, mass spectrometry, and other
domain-specific applications.

## Preserve research beyond the compute project

Primary RCC storage is not the archive. The planned governed RCC-to-Coscine path
connects a reviewed project archive set to durable research-data preservation,
with checksums, ownership, retention, and disposition remaining explicit.

That RCC-to-Coscine transfer route is **not yet released** in the current
candidate. Read [the planned RCC project to Coscine archive flow](../data/rcc-project-to-coscine.md).

## The platform promise

The researcher should be able to describe the scientific intent—bring these
instrument data into the project, explore them, run this validated workflow,
share with these collaborators, preserve this result, submit this domain output—
while RCC translates that intent into the appropriate identity, storage,
execution, resource, provenance, and governance mechanisms.

Simplifying the front door must never mean hiding the platform's capability from
advanced users. It means infrastructure knowledge becomes **progressively
disclosed** rather than a prerequisite.
