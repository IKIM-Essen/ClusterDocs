# RCC Analysis: from data to a reproducible run

> **Service status:** RCC Analysis is **not yet released to users**. This page
> documents the planned RCC 23 user workflow so researchers can understand the
> product before activation. Current RCC workers and Slurm remain the supported
> execution path; use the existing Snakemake, Nextflow, notebook, and Slurm
> guidance until RCC Analysis is explicitly announced as available.

RCC Analysis is the user-facing layer for running governed scientific workflows
without having to design the Slurm execution plan by hand.

The researcher chooses the **data, scientific workflow, and scientific
parameters**. RCC then proposes a deployment-appropriate execution plan for the
hardware that is actually available, submits the work through Slurm, and records
what was run so the result can be reproduced.

In short:

```text
project data
    -> choose a workflow
    -> choose parameters
    -> review hardware fit and execution plan
    -> run through Slurm
    -> inspect typed results
    -> retain provenance / rerun / archive
```

RCC Analysis does not replace Slurm, Nextflow, Snakemake, project storage, or
RCC Workbench. It coordinates those components behind one governed analysis
workflow.

## RCC Analysis or RCC Workbench?

Use **RCC Workbench** when your main goal is interactive work: a shell, notebook,
VS Code session, exploratory analysis, or development and debugging.

Use **RCC Analysis** when your main goal is to run a repeatable scientific
analysis with a defined workflow, inputs, parameters, outputs, and provenance.

| | RCC Workbench | RCC Analysis |
|---|---|---|
| Main question | “Give me an interactive environment.” | “Run this analysis.” |
| Best for | Exploration, development, debugging | Repeatable production analysis |
| You choose | Interactive environment and what you do inside it | Data, workflow, scientific parameters |
| RCC chooses | Secure session placement | Operational execution and task placement |
| Typical result | Files you create interactively | Governed run, typed outputs, provenance |

A common pattern is to **develop in Workbench and run routinely in Analysis**.

## The RCC Analysis workflow

### 1. Start from a project and its data

An Analysis run belongs to an RCC project. You select the input data objects the
workflow should consume. Examples include a microscopy acquisition, an image
set, paired FASTQ reads, a metagenome read set, a BAM file, or another supported
data type.

RCC uses the project boundary for authorization and for durable results. The
normal result location is conceptually:

```text
/projects/<project>/rcc-analysis/<run-id>/
```

An existing run is never silently replaced.

### 2. Choose a scientific workflow

RCC Analysis presents compatible workflows for the selected data. A workflow is
not just a directory containing scripts: it has an exact version, an immutable
source snapshot, declared inputs and outputs, parameters, citations, and an
ownership scope.

Workflows may belong to:

- an individual user;
- a group;
- a project;
- a facility; or
- RCC itself.

A workflow may also carry review or operational information such as
**unreviewed**, **approved**, **supported**, or **preferred**. These labels help
with discovery and operations; they do not grant project access and they do not
claim that a scientific result is correct.

### 3. Choose scientific parameters

You provide the parameters that affect the scientific analysis: for example a
reference database, threshold, model, sample grouping, or workflow option.

You do **not** normally choose raw Slurm partitions, nodes, QOS, reservations,
or arbitrary Nextflow/Snakemake scheduler arguments in the Analysis interface.
Those are operational details owned by RCC.

This distinction is deliberate: the scientific intent belongs to the
researcher; machine placement belongs to the compute platform.

### 4. Choose between exact reproduction and adaptation

Imported or externally developed workflows can be used in two important modes.

#### Exact reproduction

Choose this when a paper, reviewer, benchmark, or validation exercise requires a
specific implementation or configuration.

RCC keeps the required source/version fixed and does not silently substitute a
different scientific workflow. It may still use safe operational mechanisms such
as RCC-managed Slurm submission or local scratch when those do not change the
scientific computation.

#### Adapt for RCC

Choose this when the scientific goal matters more than preserving one cluster-
specific implementation.

RCC may recommend a more efficient operational plan or identify a better-suited
reviewed workflow. You remain responsible for choosing whether to use the
imported workflow or an alternative.

### 5. Review hardware fit and task efficiency

Before a run is submission-ready, RCC checks the workflow against the current
RCC deployment rather than assuming that resource requests copied from another
cluster are appropriate.

The review can detect patterns such as:

- thousands of very short scheduler jobs;
- repeated large reads from shared project storage;
- excessive workflow-controller or scheduler overhead;
- poor CPU or memory utilisation;
- GPU allocations with little measured GPU use;
- locality-sensitive work with no local-scratch strategy; or
- a GPU workflow that unnecessarily runs the workflow controller on a GPU.

When enough recent measurements exist, RCC can use observed utilisation to
right-size CPU, memory, scratch, or concurrency recommendations. A resource
reservation is not treated as proof that the resource was useful.

The user-facing decision should be understandable rather than scheduler-centric:

```text
RCC recommends a more efficient plan

[ Use RCC recommendation ]

[ Keep the requested configuration ]
  reason required
```

Keeping an inefficient configuration remains possible when there is a genuine
scientific or reproduction reason; that decision becomes part of the run
provenance.

### 6. Review the exact run before submission

Before starting the analysis, the review page should make the important facts
visible:

- project and selected inputs;
- exact workflow name, version, and source identity;
- scientific parameters;
- expected outputs;
- exact-reproduction requirements, if any;
- RCC hardware-fit findings;
- the proposed controller and task execution classes; and
- any explicit exception you chose to retain.

RCC then seals this run plan. A later authorization change must not be hidden by
an older plan: current project/workflow authority is checked again at activation
time.

### 7. RCC runs the workflow through Slurm

Slurm remains the sole scheduler and accounting authority.

RCC Analysis separates the lightweight workflow controller from the scientific
child tasks. For example, a GPU workflow can use a normal CPU allocation for the
Nextflow or Snakemake controller while only the actual GPU tasks consume GPU
nodes.

Conceptually:

```text
RCC Analysis
    -> controller job
       -> Nextflow or Snakemake
          -> child Slurm jobs
             -> CPU / GPU / locality class selected by RCC
```

The browser does not receive a Slurm signing key and RCC Analysis does not own a
separate scheduler authority. Submission uses the shared RCC per-user Slurm
submission boundary.

### 8. Follow the run

The run view should focus on scientific progress and actionable failures rather
than requiring the researcher to reconstruct state from several systems.

Useful status includes:

- planned / waiting / running / completed / failed;
- workflow-controller state;
- task progress;
- links to useful logs;
- clear explanation of an authorization, placement, or input problem; and
- whether a submission outcome is uncertain and needs reconciliation.

RCC must not automatically submit a second copy merely because a scheduler reply
was uncertain. Recovery first determines whether the original job exists.

### 9. Inspect results and provenance

A successful run produces its declared result objects beneath the project run
root. Depending on the workflow these might include tables, reports, images,
segmentations, alignments, variant calls, or other governed outputs.

The run can also retain an RO-Crate research object containing the information
needed to understand and reproduce the result, including:

- exact workflow identity and immutable source snapshot;
- selected inputs and outputs;
- scientific parameters;
- citations or reproduction requirements;
- RCC operational adaptations;
- hardware/efficiency evidence used for the plan; and
- an explicit record when an inefficient requested configuration was retained.

This provenance stays with the project result. Optional DataLad binding can
associate the result with an immutable dataset state, and the normal RCC/Coscine
project archive path remains the custody mechanism when an approved result set
is archived.

## Importing a workflow

RCC Analysis is intended to support reviewed Nextflow and Snakemake workflows as
well as workflows imported from public HTTPS Git repositories, public HTTPS
URLs, or bounded pasted source.

Import is inspection, not execution. RCC examines the source in a data-less
sandbox and does not mount project research data merely to determine whether a
workflow can be represented safely.

An imported workflow starts as **unreviewed**. It cannot award itself RCC
approval, support, or preferred status.

Cluster-specific scheduler directives are also checked. A workflow that embeds
unmanaged queue/account placement may require adaptation before RCC can safely
compile an execution plan.

## What “preferred” means

A **preferred** workflow is stronger than a casual recommendation. It refers to
an exact workflow revision with evidence that it fits a particular RCC
deployment and has a good hardware-efficiency review.

That judgement is deployment-specific. A workflow that is preferred on one RCC
installation is not automatically preferred on another installation with
different hardware or measured behaviour.

Preferred status is operational guidance; it is not scientific validation and
it does not itself grant scheduler priority.

## What RCC Analysis changes for the system

For researchers, Analysis hides unnecessary scheduler detail. For RCC, it adds a
controlled compilation layer between scientific intent and Slurm.

Instead of accepting every workflow decomposition exactly as presented, RCC can
reason about:

```text
scientific workflow
    -> task behaviour
    -> measured utilisation
    -> available hardware
    -> efficient execution plan
    -> Slurm
```

This gives RCC a common place to enforce scheduler portability, avoid pathological
small-job fan-out, improve CPU/GPU utilisation, use local scratch appropriately,
and retain evidence about why a particular execution plan was chosen.

The important authority boundaries remain unchanged:

- Slurm schedules and accounts for compute;
- project membership governs project access;
- Nextflow and Snakemake remain workflow engines;
- Workbench remains the interactive environment;
- the Assistant may explain recommendations but does not invent measurements or
  gain scheduler authority; and
- Coscine/DataLad integration remains part of the governed data lifecycle rather
  than a new credential path inside Analysis.

## What to use before RCC Analysis is released

Until RCC Analysis is explicitly activated for users:

1. use [Class 5](../course/class-05-slurm.md) for Slurm execution;
2. use [Class 6](../course/class-06-snakemake.md) for the current managed
   Snakemake path;
3. use [Class 7](../course/class-07-nextflow.md) for Nextflow guidance and
   release status;
4. use [Python notebooks](../course/class-09-python-notebooks.md) or
   [R analysis](../course/class-10-r-analysis.md) for interactive exploration;
5. use [Class 14](../course/class-14-efficient-io.md) for efficient local I/O;
   and
6. retain code, parameters, environments, checksums, logs, and Slurm job IDs so
   today's runs remain reproducible.

When RCC Analysis is released, ClusterDocs will replace this status notice with
the live entry point and the exact user acceptance workflow.
