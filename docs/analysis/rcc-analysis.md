# RCC Analysis: notebooks and governed workflows

> **Service status:** RCC Analysis is **not yet released to users**. This page
> documents the staged browser-first product model. Current RCC workers, Slurm,
> managed Snakemake/Nextflow, SSH-tunneled notebooks, and local VS Code remain
> the supported paths until RCC Analysis is explicitly announced as available.

RCC Analysis is the planned **user-facing compute product** for researchers who
should not need to become HPC operators merely to use RCC.

It combines two related ways of working:

1. **Notebook** — interactive Jupyter-based exploration and bounded analysis;
2. **Workflow** — repeatable, scalable, governed scientific execution.

The two modes share RCC identity, project data, results, and resource governance.
“Workbench” remains an internal engineering term for the interactive session
machinery behind Notebook mode rather than a separate primary product.

## The browser-first model

```text
Files: upload or choose project data
        |
        v
RCC Analysis
   |          |
   |          +-> Workflow -> run reviewed repeatable analysis
   |
   +-> Notebook -> explore, visualize, prototype
                         |
                         +-> promote repeatable work to Workflow
        |
        v
Files: inspect/download project results
```

A browser-first user can have a valid RCC account without enrolling an SSH key.
Project membership and RCC web authentication are sufficient for browser
capabilities that have been enabled for that user/project. SSH remains an
optional advanced credential for command-line and local-editor access.

## Notebook mode

Use **Notebook** when the main question is “help me work with these data
interactively.” The preferred interface is JupyterLab in the browser, backed by
a bounded Slurm allocation selected by RCC.

Typical uses include inspecting data, Python/R exploratory analysis, statistics
and visualisation, examining workflow results, prototyping transformations or
model code, and small-scale debugging.

The normal user should not need to choose a worker, paste a cluster path, submit
an `sbatch` command, create an SSH tunnel, copy a Jupyter token, expose a port,
or select CPU/RAM/GPU/partition settings.

### Jupyter and terminal security

Jupyter is arbitrary user-code execution, not a sandbox. Kernels, subprocesses,
and an optional Jupyter terminal all execute as the authenticated user.
Therefore hiding a terminal would not be the RCC security boundary.

The staged Notebook architecture instead places Jupyter Server, kernels,
subprocesses, and terminal in the same networkless user/PID namespace inside the
same Slurm allocation. Jupyter listens on a private job-local Unix socket, the
extension manager is read-only, remote access is disabled, and browser transport
uses a separate authenticated outbound agent.

The terminal is an advanced tool **inside Notebook**, not a second service,
login path, SSH substitute, or separate authority class.

RCC does **not** provide a browser IDE in this release. Users who need a full IDE
can continue to use a local editor such as VS Code through the separately
governed SSH path.

### Notebook resource rule

A notebook is still real computation. RCC therefore starts with a modest
interactive profile, reclaims idle sessions, bounds concurrent sessions, keeps
large/GPU allocations exceptional, and directs repeated or scalable work to
Workflow mode. Browser users do not choose raw scheduler resources.

A GPU notebook is appropriate only when the measured workload benefits from the
GPU; it is not a general “faster notebook” setting.

## Workflow mode

Use **Workflow** when the question is “run this scientific analysis reliably.”
The researcher chooses project data, a scientific workflow, and scientifically
meaningful parameters. RCC chooses the deployment-appropriate execution plan,
submits through Slurm, and records what ran so the result can be reproduced.

```text
project data
    -> choose supported workflow
    -> choose scientific parameters
    -> review important warnings and expected outputs
    -> RCC selects efficient execution plan
    -> run through Slurm
    -> typed results + provenance
    -> open results in Files
```

Normal users should not choose Nextflow versus Snakemake as a deployment detail,
Slurm partitions, CPU counts, raw memory values, QOS, reservations, container
flags, or arbitrary scheduler arguments unless a setting is genuinely part of
the scientific method.

The browser request is not scheduler authority. Before execution, RCC recompiles
the scientific intent against trusted server-side workflow/project evidence and
re-checks current authorization. The privileged Slurm submission path then
independently constrains the project/account, controller profile, engine,
partition, resources, run paths, and generated controller shape.

## Moving from Notebook to Workflow

Notebook and Workflow are deliberately adjacent. Move work out of Notebook when
it is repeated across samples or cohorts, long-running or unattended,
provenance-critical, composed of many dependent tasks, resource-intensive,
producing an official project result, or important for another researcher to
rerun.

The user changes mode inside Analysis rather than learning a second RCC product.

## Start from a project and its data

An Analysis notebook or workflow belongs to an RCC project. Inputs and durable
outputs stay within the same project authorization model used by Files.

For a user with one eligible project, RCC should use it implicitly. A user with
multiple eligible projects chooses from a server-generated list. Normal browser
users should not type project identifiers or `/projects/...` paths.

Deep links from Files may carry project/object context, but navigation never
grants new authority; Analysis re-checks authorization server-side.

Workflow run results use the create-only Analysis result model:

```text
/projects/<project>/rcc-analysis/<run-id>/
```

Existing runs are never silently replaced. Notebook-created durable work should
also be saved in project storage rather than treated as durable merely because a
browser session is still open.

## Canonical staged browser route

The planned researcher-facing Analysis origin is:

```text
https://analysis.ikim.uk-essen.de/
```

Workflow occupies the Analysis root. Notebook management is namespaced below
`/notebook/`. This route is **staged source configuration, not a claim of live
availability**.

The Analysis-to-Notebook management hop uses a separate mTLS identity and may be
revoked independently. Jupyter workspace/session traffic remains on its separate
hardened workspace origin rather than being tunneled through the Analysis
management page.

## Choose a scientific workflow

RCC Analysis presents compatible workflows for the selected data. A workflow
has an exact version, immutable source snapshot, declared inputs/outputs,
parameters, citations, ownership scope, and assurance state.

Workflow ownership may be user, group, project, facility, or RCC. Assurance may
include **unreviewed**, **approved**, **supported**, or deployment-specific
**preferred** state. These labels guide discovery and operations; they do not
grant project access and they are not claims that a scientific result is
clinically correct.

## Exact reproduction and adaptation

Use **exact reproduction** when a paper, reviewer, benchmark, or validation
exercise requires one exact implementation. Use **adapt for RCC** when the
scientific goal matters more than preserving cluster-specific implementation
details; RCC may recommend a more efficient operational plan while keeping
scientific choices explicit.

## Hardware fit and bad computing patterns

RCC should detect and correct patterns such as thousands of tiny jobs, repeated
large shared-storage reads, excessive controller overhead, severe CPU/RAM
over-request, idle GPU allocation, long-idle interactive sessions, repeated
manual notebook runs that should be workflows, and locality-sensitive work with
no scratch strategy.

With enough recent observations RCC can right-size CPU, memory, scratch,
concurrency, and GPU recommendations. A reservation is not evidence that a
resource was useful.

Optimization evidence should be privacy-minimized: allocated/used CPU,
requested/peak memory, GPU utilization where available, elapsed/idle time,
aggregate I/O where defensible, and terminal state are useful. Commands,
notebook contents, research filenames, and patient data are not required for
ordinary right-sizing.

## Review and run

Before a governed workflow starts, show a plain-language summary of the project,
selected inputs, exact workflow revision, scientific parameters, expected
outputs, relevant warnings/conditions, and resource/time expectation when the
evidence supports one.

The primary action is **Run analysis**. The browser never accepts raw scheduler
or workflow-engine arguments.

## Follow progress

User-facing states should answer what the researcher needs to know:

- Preparing
- Waiting for compute
- Running
- Finishing results
- Complete
- Stopped
- Needs attention

Raw Slurm job IDs, controller jobs, engine logs, child-task counts, and internal
session IDs are secondary diagnostics. If submission is uncertain, RCC
reconciles before retrying; a browser network error must not create a duplicate
scientific run.

## Results and provenance

A successful workflow produces declared result objects beneath the project run
root. The completion view should provide a concise result summary where
available, provenance/reproducibility details, and **Open results in Files**.

The run may retain an RO-Crate research object containing exact workflow
identity, inputs/outputs, scientific parameters, citations, RCC adaptations,
hardware/efficiency evidence, and explicit retained-inefficiency decisions.

RCC Analysis does not create a private result store disconnected from project
data. Files remains the normal browser entry/exit surface, while governed
Coscine/DataLad paths remain part of the wider data lifecycle.

## Files project visibility and transfer acceptance

Ordinary Files should expose every current Files-enabled **Regular** project in
which the user is a member; the primary project may affect the landing directory
but must not hide other eligible projects. Controlled Data and unpublished or
missing project directories remain intentionally absent from ordinary Files.

Browser transfer performance must be accepted on the deployed system rather
than inferred from architecture. The rollout pilot should measure multi-GiB
upload/download, checksums, representative small-file behavior, concurrent
users, retries/errors, and compare sustained performance with an accepted native
transfer reference such as SFTP. A large unexplained browser penalty is an RCC
defect to investigate, not a reason to make SSH a prerequisite again.

## Zero-SSH browser acceptance

Before broad production promotion, pilot users with **no SSH public key
enrolled** should be able to:

1. sign in to RCC;
2. open Files and upload/select project input;
3. open RCC Analysis;
4. open Notebook without typing project IDs, paths, hostnames, Slurm terms, or
   choosing a resource profile;
5. produce and save a small project result;
6. run a supported Workflow using scientific inputs/parameters only;
7. leave and return without losing owned run/session state;
8. open/download results in Files; and
9. sign out.

Passing CLI/API canaries is necessary but not sufficient. The browser product is
not prime-time until non-HPC users can complete this without facilitator shell
intervention.

## What to use before RCC Analysis is released

Until RCC Analysis is explicitly activated:

1. use [Class 9](../course/class-09-python-notebooks.md) for the current
   Jupyter-through-Slurm and SSH-tunnel notebook path;
2. use [Class 6](../course/class-06-snakemake.md) for managed Snakemake;
3. use [Class 7](../course/class-07-nextflow.md) for managed Nextflow;
4. use [Class 5](../course/class-05-slurm.md) for direct Slurm execution;
5. use [Class 14](../course/class-14-efficient-io.md) for efficient local I/O;
6. use local VS Code/other editors through the released SSH path when an IDE is
   genuinely needed; and
7. retain code, parameters, environments, checksums, logs, and job IDs so
   current runs remain reproducible.

When RCC Analysis is released, ClusterDocs should make Analysis the normal
data-analysis starting point while retaining direct SSH/Slurm material as an
advanced/reference path.
