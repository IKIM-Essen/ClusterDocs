# Data analysis path

Use this path when your main goal is to explore research data, run statistical
analyses, train or evaluate models, create figures, or build a reproducible
result pipeline.

> **Service status:** RCC workers and Slurm analysis are **ready now**. RCC
> Analysis Notebook/Workflow is **not yet released**. Until it is activated,
> use the current Jupyter/SSH, Snakemake, Nextflow, and direct Slurm guidance.

## The target user journey

RCC data analysis is converging on one browser product with two compute modes:

```text
Files -> RCC Analysis
           |      |
           |      +-> Workflow: repeat / scale / reproduce
           +--------> Notebook: explore / visualize / prototype
        -> Files: results
```

A browser-first researcher should not need an SSH key, worker hostname, Slurm
partition, Jupyter token, or SSH tunnel merely to perform ordinary interactive
analysis once Notebook mode is released.

## 1. Build the scientific foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 3](../course/class-03-performance.md) | CPU, RAM, GPU, and efficient I/O | Avoid slow or disruptive analysis patterns |
| [Class 9](../course/class-09-python-notebooks.md) | Python/Jupyter analysis | Explore and prototype safely |
| [Class 10](../course/class-10-r-analysis.md) | R analysis | Build statistical and reporting workflows |
| [Class 13](../course/class-13-biomedical-data-privacy.md) | Biomedical-data governance | Confirm the project and data are suitable for RCC |
| [Class 14](../course/class-14-efficient-io.md) | Local staging and safe publication | Keep active I/O off shared storage when measurement supports it |
| [Class 16](../course/class-16-wet-lab-data-workflows.md) | Wet-lab instrument handoff | Preserve authoritative acquisition data and verify transfer |
| [Class 17](../course/class-17-data-lifecycle.md) | Research data lifecycle | Keep data, results, archive, and disposition governed |

SSH/VS Code and direct Slurm remain important advanced skills, but they are not
intended to be prerequisites for every future browser-first researcher.

## 2. Choose Notebook or Workflow

### Notebook — explore and understand

Choose a notebook when you need to inspect data, calculate summaries, create
figures, test code, or understand an intermediate result interactively.

Use [Class 9: Python notebooks](../course/class-09-python-notebooks.md) for Python,
pandas, Polars, DuckDB, Arrow, numerical analysis, visualization, machine
learning, and AI exploration. Use [Class 10: R analysis](../course/class-10-r-analysis.md)
for statistical workflows and reproducible R environments.

The planned RCC Analysis Notebook experience is Jupyter-first and Slurm-backed.
The interactive allocation should be modest, attended, and automatically
reclaimed when idle.

### Workflow — repeat and scale

Choose a workflow when the analysis becomes repeated, many-sample, long-running,
unattended, provenance-critical, or resource-intensive.

Use [Class 6](../course/class-06-snakemake.md) for the current managed Snakemake
path and [Class 7](../course/class-07-nextflow.md) for managed Nextflow/nf-core.
These execution engines remain underneath the future RCC Analysis Workflow mode.

Read [RCC Analysis: notebooks and governed workflows](../analysis/rcc-analysis.md)
for the planned product model.

## 3. Use resources responsibly

The browser should simplify RCC, not hide bad computing patterns. Before scaling,
measure what the analysis actually needs.

Avoid:

- choosing a GPU because it sounds faster;
- reserving many CPUs for single-threaded code;
- requesting far more memory than observed peak use;
- leaving interactive notebook allocations idle;
- repeating the same manual notebook analysis across many samples;
- producing thousands of tiny scheduler jobs; and
- rereading large shared files repeatedly when batching or local scratch is
  appropriate.

A useful progression is:

```text
small notebook experiment
    -> measure CPU / memory / GPU / I/O behavior
    -> choose realistic resources
    -> move repeated/scalable work to a workflow
```

For resource selection and I/O, use [Class 3](../course/class-03-performance.md),
[Class 14](../course/class-14-efficient-io.md), and
[AI and data science](../reference/ai-data-science.md).

## 4. Make the analysis reproducible

Use [Class 2](../course/class-02-workflows.md) to organise the project and
[Class 4](../course/class-04-containers.md) when an immutable runtime is more
appropriate than a mutable environment.

If the analysis currently exists as notebook state, shell history, scripts, or a
document of commands, follow the
[script-to-workflow conversion guide](from-shell-scripts.md) before scaling it.

Keep durable inputs and final outputs in approved project storage. Stage high-I/O
intermediates into job-local scratch and retain code, environments, parameters,
checksums, logs, benchmarks, and run/job identifiers needed for reproduction.

## 5. Share an approved result

- Use [Class 11](../course/class-11-shiny.md) for bounded Shiny development.
- Use [Class 12](../course/class-12-notebook-to-service.md) when converting a
  notebook, model, or analysis into a governed service.
- Use [Class 8](../course/class-08-vhosts.md) to plan a protected project
  website. Project vhosts are not yet released.

An analysis result, model, or AI prediction remains a research output unless the
applicable clinical validation and governance processes explicitly approve
another use.

## Current versus planned access

Until RCC Analysis Notebook is activated, the current Class 9 procedure still
uses a Slurm Jupyter job and SSH tunnel. When the browser notebook path is
released, that manual tunnel procedure becomes an advanced/fallback method, not
the default onboarding experience.
