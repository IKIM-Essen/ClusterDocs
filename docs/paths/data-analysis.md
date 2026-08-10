# Data analysis path

Use this path when your main goal is to explore research data, run statistical
analyses, train or evaluate models, create figures, or build a reproducible
result pipeline.

> **Service status:** RCC workers and Slurm analysis are **ready now**. Project
> vhosts and RCC-to-Coscine transfer are **not yet released**; the linked
> classes prepare those future publication and archive steps.

## 1. Build the shared foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 1](../course/class-01-safe-access.md) | Safe SSH, VS Code, and file access | Establish an attributable, verified connection |
| [Class 3](../course/class-03-performance.md) | CPU, RAM, GPU, and efficient I/O | Avoid slow or disruptive analysis patterns |
| [Class 5](../course/class-05-slurm.md) | Slurm jobs and resource requests | Run computation on managed workers |
| [Class 6](../course/class-06-snakemake.md) | Ready-now managed Snakemake | Submit reproducible rule jobs through Slurm |
| [Class 7](../course/class-07-nextflow.md) | Planned Nextflow and nf-core | Prepare for the not-yet-released managed service |
| [Class 13](../course/class-13-biomedical-data-privacy.md) | Biomedical-data governance | Confirm the project and data are suitable for RCC |
| [Class 14](../course/class-14-efficient-io.md) | Local staging and safe publication | Keep active I/O off shared storage when measurement supports it |
| [Class 16](../course/class-16-wet-lab-data-workflows.md) | Wet-lab instrument handoff | Preserve authoritative acquisition data and verify transfer before analysis |
| [Class 17](../course/class-17-data-lifecycle.md) | Instrument-to-Coscine data lifecycle | Keep data in governed projects, stage analysis correctly, and archive an approved set |

## 2. Choose your analysis environment

Read the optional [account setup patterns](../reference/account-starter-setups.md)
if you want guidance for a reviewable Conda data-science environment, an
inexpensive prompt, or a bounded Shiny setup.

- [Class 9: Python notebooks](../course/class-09-python-notebooks.md) for pandas,
  Polars, DuckDB, Arrow, numerical analysis, visualization, machine learning,
  and AI exploration.
- [Class 10: R analysis](../course/class-10-r-analysis.md) for statistical
  workflows, larger tables, reporting, and reproducible R environments.
- [AI and data science](../reference/ai-data-science.md) for technique selection,
  validation, training, inference, GPUs, and distributed processing.

## 3. Make the analysis reproducible

Use [Class 2](../course/class-02-workflows.md) to organise the project, then
[Class 6](../course/class-06-snakemake.md) for the ready managed workflow path.
Use [Class 7](../course/class-07-nextflow.md) when a reviewed community
workflow uses Nextflow or nf-core.
Use [Class 4](../course/class-04-containers.md) when an immutable runtime is
more appropriate than an environment containing many small files.

Keep durable inputs and final outputs in approved project storage. Stage
high-I/O intermediates into job-local scratch and retain code, environments,
parameters, checksums, logs, benchmarks, and Slurm job IDs.

Use [Class 15](../course/class-15-storage-architecture.md) when you need to
diagnose metadata, object-storage, network, or cache behavior in more detail.

## 4. Share an approved result

- Use [Class 11](../course/class-11-shiny.md) for a bounded Shiny development
  workflow.
- Use [Class 12](../course/class-12-notebook-to-service.md) when converting a
  notebook, model, or analysis into a governed service.
- Use [Class 8](../course/class-08-vhosts.md) to plan a protected project
  website. Project vhosts are not yet released.

An analysis result, model, or AI prediction remains a research output unless
the applicable clinical validation and governance processes explicitly approve
another use.
