# RCC Analysis: notebooks and governed workflows

> **Service status:** RCC Analysis is **not yet released to users**. This page
> documents the planned browser-first product model. Current RCC workers, Slurm,
> managed Snakemake/Nextflow, SSH-tunneled notebooks, and VS Code remain the
> supported paths until RCC Analysis is explicitly announced as available.

RCC Analysis is the planned **user-facing compute product** for researchers who
should not need to become HPC operators merely to use RCC.

It combines two related ways of working:

1. **Notebook** — interactive Jupyter-based exploration and bounded analysis;
2. **Workflow** — repeatable, scalable, governed scientific execution.

The two modes share identity, project data, execution authority, results, and
resource governance. “Workbench” remains an internal/advanced term for the
interactive session machinery behind Notebook mode rather than a separate
primary product.

## The browser-first model

The canonical simple path is:

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
optional advanced credential for command-line access.

## Notebook mode

Use **Notebook** when the main question is “help me work with these data
interactively.” The preferred interface is Jupyter in the browser, backed by a
bounded Slurm allocation.

Typical uses include:

- inspecting a sample or subset of a dataset;
- Python or R exploratory analysis;
- statistics and visualisation;
- examining workflow results and intermediate objects;
- prototyping transformations or model code;
- small-scale debugging; and
- developing an analysis before making it repeatable.

The normal user should not need to choose a worker, copy a cluster path, submit
an `sbatch` command, create an SSH tunnel, copy a Jupyter token, or expose a
network port. RCC owns those operational details.

### Notebook resource rule

A notebook is still real computation. Browser convenience does not make CPU,
memory, GPU, scratch, or scheduler capacity free.

RCC should therefore:

- start with a modest notebook profile;
- reclaim idle sessions;
- bound concurrent interactive sessions;
- make large CPU/GPU profiles clearly exceptional;
- recommend smaller resources when repeated measured use is low; and
- encourage conversion to Workflow mode when computation becomes repeated,
  long-running, unattended, or highly parallel.

A GPU notebook is appropriate only when the measured workload benefits from the
GPU. A GPU allocation is not a general “faster notebook” setting.

## Workflow mode

Use **Workflow** when the question is “run this scientific analysis reliably.”
The researcher chooses the data, scientific workflow, and scientifically
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

Do not require normal users to choose Nextflow versus Snakemake, Slurm
partitions, CPU counts, raw memory values, QOS, reservations, container flags,
or arbitrary scheduler arguments unless a setting is genuinely part of the
scientific method.

## Moving from Notebook to Workflow

Notebook and Workflow are deliberately adjacent. A successful exploratory
notebook often reveals the repeatable analysis that should become a governed
workflow.

Move work out of Notebook mode when it is:

- repeated across samples or cohorts;
- long-running or unattended;
- important enough to rerun for a paper or reviewer;
- composed of many dependent tasks;
- using large CPU/GPU resources;
- producing an official project result; or
- easier to review as a declared workflow than as notebook state.

RCC should make this transition visible in the product rather than forcing the
user to learn a second service.

## Start from a project and its data

An Analysis notebook or workflow belongs to an RCC project. Inputs and durable
outputs stay within the same project authorization model used by Files.

A user should normally choose project files through a browser selector rather
than paste an absolute RCC filesystem path. Deep links from Files may carry a
project/object selection, but navigation never grants new authority.

Workflow run results use the existing create-only Analysis result model,
conceptually:

```text
/projects/<project>/rcc-analysis/<run-id>/
```

An existing run is never silently replaced.

Notebook-created durable work should likewise be saved in project storage rather
than treated as durable merely because a browser session is still open.

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

### Exact reproduction

Use this when a paper, reviewer, benchmark, or validation exercise requires a
specific implementation. RCC keeps the required workflow/source identity fixed
and does not silently substitute a different scientific method.

### Adapt for RCC

Use this when the scientific goal matters more than preserving one
cluster-specific implementation. RCC may recommend a more efficient operational
plan or a reviewed alternative, while keeping scientific choices explicit.

## Hardware fit and bad computing patterns

Before a workflow is submission-ready, RCC checks whether its execution pattern
fits the current deployment. The same resource-governance principles also inform
Notebook profile recommendations.

RCC should detect and correct patterns such as:

- thousands of very short scheduler jobs;
- repeated large reads from shared project storage;
- excessive controller/scheduler overhead;
- 16 CPUs reserved for effectively single-threaded work;
- memory reservations far above observed peak RSS;
- GPU allocations with little meaningful GPU use;
- long-idle interactive sessions;
- repeated manual notebook runs that should be a workflow;
- locality-sensitive work with no scratch strategy; or
- workflow controllers consuming GPU resources unnecessarily.

When enough recent measurements exist, RCC can use aggregate utilization to
right-size CPU, memory, scratch, concurrency, and GPU recommendations. A resource
reservation is not evidence that the resource was useful.

The optimization evidence should be privacy-minimized: allocated/used CPU,
requested/peak memory, GPU utilization where available, elapsed/idle time, and
terminal state are useful. Commands, notebook contents, research filenames,
patient data, and host identities are not required for ordinary right-sizing.

## Review and run

Before starting a governed workflow, show a plain-language summary of:

- project and selected inputs;
- exact workflow name/revision;
- scientific parameters;
- expected outputs;
- relevant warnings or conditions;
- approximate resource/time expectation when evidence supports one; and
- any exact-reproduction exception.

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
session IDs are secondary diagnostics.

If a submission outcome is uncertain, RCC reconciles before retrying. A browser
network error must not create duplicate scientific runs.

## Results and provenance

A successful workflow produces declared result objects beneath the project run
root. The completion view should provide a concise result summary where the
workflow supports one, provenance/reproducibility details, and **Open results in
Files**.

The run can retain an RO-Crate research object containing exact workflow
identity, inputs/outputs, scientific parameters, citations, RCC adaptations,
hardware/efficiency evidence, and explicit retained-inefficiency decisions.

RCC Analysis does not create a private result store disconnected from project
data. Files remains the normal browser entry/exit surface, while governed
Coscine/DataLad paths remain part of the wider data lifecycle.

## Where “Workbench” fits technically

The interactive session broker that was previously presented as RCC Workbench
is still valuable machinery. It authenticates the browser, authorizes the
project, obtains a bounded Slurm allocation, starts Jupyter or an advanced IDE
inside that allocation, and brokers a safe browser attachment.

That architecture should be mostly invisible to Notebook users. Read
[Workbench execution layer](../concepts/workbench-interfaces.md) only when you
need the advanced session/security model.

## Zero-SSH browser acceptance

Before broad production promotion, pilot users with **no SSH public key enrolled**
should be able to complete an end-to-end browser journey:

1. sign in to RCC;
2. open Files;
3. upload/select project input;
4. open RCC Analysis;
5. open a Notebook without typing project IDs, paths, hostnames, or Slurm terms;
6. produce and save a small project result;
7. optionally select a supported Workflow using the same project data;
8. run with safe defaults;
9. leave and return without losing owned run/session state;
10. open the result in Files;
11. download the result; and
12. sign out.

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
   and
6. retain code, parameters, environments, checksums, logs, and job IDs so current
   runs remain reproducible.

When RCC Analysis is released, ClusterDocs should make Analysis/Notebook the
normal data-analysis starting point while retaining direct SSH/Slurm material as
an advanced/reference path.
