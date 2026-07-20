# Data analysis path

Use this path when your main goal is to explore research data, run statistical
analyses, train or evaluate models, create figures, or build a reproducible
result pipeline.

## 1. Build the shared foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 1](../course/class-01-safe-access.md) | Safe SSH, VS Code, and file access | Establish an attributable, verified connection |
| [Class 3](../course/class-03-performance.md) | CPU, RAM, GPU, and efficient I/O | Avoid slow or disruptive analysis patterns |
| [Class 5](../course/class-05-slurm.md) | Slurm jobs and resource requests | Run computation on managed workers |
| [Class 11](../course/class-11-biomedical-data-privacy.md) | Biomedical-data governance | Confirm the project and data are suitable for RCC |

## 2. Choose your analysis environment

Start with the optional [account starter setups](../reference/account-starter-setups.md)
if you want a reviewable Conda data-science environment, an inexpensive prompt,
or an importable Shiny template. The installer previews all changes first.

- [Class 7: Python notebooks](../course/class-07-python-notebooks.md) for pandas,
  Polars, DuckDB, Arrow, numerical analysis, visualization, machine learning,
  and AI exploration.
- [Class 8: R analysis](../course/class-08-r-analysis.md) for statistical
  workflows, larger tables, reporting, and reproducible R environments.
- [AI and data science](../reference/ai-data-science.md) for technique selection,
  validation, training, inference, GPUs, and distributed processing.

## 3. Make the analysis reproducible

Use [Class 2](../course/class-02-workflows.md) to turn repeated steps into a
versioned workflow. Use [Class 4](../course/class-04-containers.md) when an
immutable runtime is more appropriate than an environment containing many
small files.

Keep durable inputs and final outputs in approved project storage. Stage
high-I/O intermediates into job-local scratch and retain code, environments,
parameters, checksums, logs, benchmarks, and Slurm job IDs.

## 4. Share an approved result

- Use [Class 9](../course/class-09-shiny.md) for a bounded Shiny development
  workflow.
- Use [Class 10](../course/class-10-notebook-to-service.md) when converting a
  notebook, model, or analysis into a governed service.
- Use [Class 6](../course/class-06-vhosts.md) before requesting a protected
  project website.

An analysis result, model, or AI prediction remains a research output unless
the applicable clinical validation and governance processes explicitly approve
another use.
