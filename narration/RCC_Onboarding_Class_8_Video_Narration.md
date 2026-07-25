# Class 8: R notebooks and large-data analysis — video narration

## Slide 1: Class 8: R notebooks and large-data analysis

Welcome to Class 8: R notebooks and large-data analysis. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning goals

After this class, you can: run R in a controlled Conda environment; use an R kernel in JupyterLab when needed; analyse larger tables with data.table, DuckDB, Arrow, and dplyr patterns; build figures with ggplot2; separate exploratory notebooks from batch analysis; prepare R code that can be rerun by a colleague.

## Slide 3: Recommended R workflow

Start from the provided example: For an interactive R notebook, use the Jupyter example from Class 7. The environment already includes an R kernel.

## Slide 4: Handling larger tables

Do not begin by loading every file into memory. First check: file size; number of columns; expected row count; whether the file is compressed; whether the analysis needs all columns; whether the operation is streaming, grouped, or random-access. Good starting points:

## Slide 5: Reproducibility

For teaching and small examples, the course uses Conda environments because they are easy to reproduce in Slurm jobs. For larger R projects, you may also use renv, but do not keep active package libraries with many small files on shared storage while computing. Restore packages into local job storage or use a reviewed container.

## Slide 6: Copyable example

The course includes: examples/interactive-workflows/notebooks/r-large-data.ipynb examples/interactive-workflows/r/analysis.R examples/interactive-workflows/r/r.sbatch examples/interactive-workflows/r/environment.yml The notebook demonstrates group summaries and a sampled figure. The batch example writes reproducible output into a results directory.

## Slide 7: Good cluster patterns for R users

Request only the CPU and memory your script can use. Keep raw data compressed where tools support it. Avoid thousands of tiny temporary files on shared storage. Use node-local scratch for intermediate output. Save final tables and figures back to the project area. Use sacct after completion to compare requested and observed memory.

## Slide 8: Completion gate

Run: Then submit the R batch job once and verify that the result file was written. The gate is complete when you can explain how the same code could be moved from notebook exploration into the batch script.
