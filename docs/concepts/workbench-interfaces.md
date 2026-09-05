# Workbench execution layer behind RCC Analysis

> **Service status:** the browser notebook/interactive path is **not yet released
> to users**. This page documents the underlying execution model. For the planned
> user-facing product, start with [RCC Analysis: notebooks and governed workflows](../analysis/rcc-analysis.md).

“RCC Workbench” remains a useful engineering term, but it should no longer be
thought of as a separate primary product for ordinary researchers. It is the
interactive execution layer that safely turns an authenticated browser request
into a bounded Slurm-backed session.

For the normal user, the important action is expected to be:

```text
RCC Analysis -> Notebook -> Open notebook
```

not:

```text
choose Workbench -> start web shell -> understand Slurm session details
```

A shell or browser IDE can remain available as an advanced interface for users
who genuinely need it, but Jupyter is the preferred interactive analysis mode.

## What the execution layer does

The Workbench machinery:

- accepts an authenticated RCC user and authorized project;
- selects a bounded RCC-owned resource profile;
- creates a Slurm allocation under that user's authority;
- starts the interactive runtime inside the allocation;
- keeps the notebook/IDE listener off the worker network;
- attaches the browser through a bounded authenticated proxy path;
- records/reconciles session state; and
- stops or reclaims sessions according to policy.

It does not create a new RCC identity, widen project membership, grant scheduler
priority, or turn a Regular project into a Controlled Data environment.

## Jupyter-first interactive computing

The first broadly useful interface should be a **Jupyter notebook**, because it
matches the work many researchers actually want to do: inspect data, calculate
summary statistics, create figures, run Python/R code, examine intermediate
results, and prototype analysis logic.

The user should not need to:

- enroll an SSH key merely to use a notebook;
- choose a worker hostname;
- run `srun`/`sbatch`;
- create an SSH tunnel;
- copy a Jupyter token;
- expose a port; or
- know which internal session broker submitted the allocation.

Those remain implementation details owned by RCC.

## When a notebook should become a workflow

Interactive convenience must not turn into poor cluster use. A notebook is the
right place for exploration and bounded attended computation. It is the wrong
place for repeated or unattended production runs.

Move work to **RCC Analysis -> Workflow** when it becomes:

- long-running or unattended;
- repeatedly executed with the same scientific intent;
- a many-sample or many-task analysis;
- dependent on substantial CPU/GPU capacity;
- provenance-critical;
- suitable for Nextflow/Snakemake; or
- important enough that another researcher should rerun it reliably.

The desired lifecycle is therefore:

```text
Files -> Analysis: Notebook -> explore / prototype
                           |
                           +-> Analysis: Workflow -> repeat / scale / reproduce
                                                      |
                                                      +-> Files: results
```

## Resource guardrails

Interactive sessions should be deliberately conservative by default:

- a modest CPU notebook profile should be the normal choice;
- large CPU or GPU sessions should be visibly exceptional;
- idle sessions should be reclaimed automatically;
- simultaneous sessions should be bounded;
- GPU sessions with no meaningful GPU use should trigger guidance;
- persistent CPU/RAM over-requesting should result in a smaller recommended
  profile; and
- repeated manual notebook execution should prompt conversion to an Analysis
  workflow.

Resource recommendations can use aggregate scheduler/accounting evidence such as
allocated CPU, observed CPU use, requested versus peak memory, GPU utilization
where available, and idle duration. RCC does not need notebook contents,
research filenames, commands, or patient-related data to detect these patterns.

## Where computation actually runs

The browser is only the interface. The computation still runs in Slurm:

```text
RCC Analysis browser
        |
        v
interactive session broker (Workbench machinery)
        |
        v
      Slurm
        |
        v
approved RCC worker
        |
        +-> Jupyter / advanced IDE inside the allocation
```

The interactive runtime is not a replacement scheduler and the browser never
receives Slurm signing authority.

## Existing interfaces remain valid

Until the RCC Analysis notebook path is explicitly activated, follow the current
released guidance:

- [Class 9: Python notebooks](../course/class-09-python-notebooks.md) for the
  current Jupyter-through-Slurm/tunnel procedure;
- [VS Code with RCC](../getting-started/vscode.md) for current Remote SSH
  development; and
- [Class 5: Slurm](../course/class-05-slurm.md) for current direct scheduler use.

Those remain valid advanced interfaces after browser notebooks arrive; they
simply stop being prerequisites for every researcher.
