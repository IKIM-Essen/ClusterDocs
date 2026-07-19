# Class 8: R notebooks and large-data analysis

This class teaches the same RCC pattern for R: use interactive sessions to inspect, visualise, and explain; use Slurm jobs for expensive computation.

## Learning goals

After this class, you can:

- run R in a controlled Conda environment;
- use an R kernel in JupyterLab when needed;
- analyse larger tables with `data.table`, DuckDB, Arrow, and `dplyr` patterns;
- build figures with `ggplot2`;
- separate exploratory notebooks from batch analysis;
- prepare R code that can be rerun by a colleague.

## Recommended R workflow

Start from the provided example:

```bash
cp -a examples/interactive-workflows/r my-r-analysis
cd my-r-analysis
sbatch r.sbatch
```

For an interactive R notebook, use the Jupyter example from Class 7. The environment already includes an R kernel.

## Handling larger tables

Do not begin by loading every file into memory. First check:

- file size;
- number of columns;
- expected row count;
- whether the file is compressed;
- whether the analysis needs all columns;
- whether the operation is streaming, grouped, or random-access.

Good starting points:

| Pattern | R tool | Why it helps |
|---|---|---|
| Fast delimited file input | `data.table::fread()` | Efficient and familiar. |
| Tidy transformations | `dplyr` | Clear pipelines for moderate data. |
| Larger-than-memory query | DuckDB | SQL over local files without loading everything. |
| Columnar data | Arrow | Efficient column selection and interchange. |
| Reproducible plotting | `ggplot2` | Stable, reviewable figures. |

## Reproducibility

For teaching and small examples, the course uses Conda environments because they are easy to reproduce in Slurm jobs. For larger R projects, you may also use `renv`, but do not keep active package libraries with many small files on shared storage while computing. Restore packages into local job storage or use a reviewed container.

## Copyable example

The course includes:

- `examples/interactive-workflows/notebooks/r-large-data.ipynb`
- `examples/interactive-workflows/r/analysis.R`
- `examples/interactive-workflows/r/r.sbatch`
- `examples/interactive-workflows/r/environment.yml`

The notebook demonstrates group summaries and a sampled figure. The batch example writes reproducible output into a results directory.

## Good cluster patterns for R users

- Request only the CPU and memory your script can use.
- Keep raw data compressed where tools support it.
- Avoid thousands of tiny temporary files on shared storage.
- Use node-local scratch for intermediate output.
- Save final tables and figures back to the project area.
- Use `sacct` after completion to compare requested and observed memory.

## Security habits

- Never store passwords or database credentials inside an `.RData` file.
- Do not publish notebooks with hidden patient identifiers in output cells.
- Do not reuse a colleague's RCC account to access a project.
- Use named project membership and named device accounts for instruments.

## Completion gate

Run:

```bash
python3 exercises/interactive/validate-interactive-examples.py
```

Then submit the R batch job once and verify that the result file was written. The gate is complete when you can explain how the same code could be moved from notebook exploration into the batch script.

## Self-check questions

1. When should you prefer DuckDB or Arrow over a plain data frame?
2. Why should active R package libraries avoid shared storage during computation?
3. Why does a plot usually use a sample rather than every row?
4. What information should be recorded so another person can rerun your R analysis?
