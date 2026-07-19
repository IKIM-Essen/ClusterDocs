# RCC Onboarding Class 8 narration: R for large datasets

**Estimated duration:** 8-9 minutes

R is widely used in biomedical research, statistics, and visualization. On RCC the same principle applies as in Python: use interactive tools to inspect and explain, and use Slurm for computation.

The example for this class includes an R script, a Slurm batch file, a Conda environment, and an R notebook. The goal is not to teach all of R. The goal is to teach a pattern that is safe, reproducible, and realistic on a shared cluster.

Start by checking the input format and size. With larger tabular data, `data.table`, DuckDB, and Arrow can avoid unnecessary memory pressure. Use `ggplot2` for clear figures, but sample when a plot does not need every row.

For reproducibility, record package versions. Conda environments are used in these exercises because they can be rebuilt on a worker. `renv` can also be useful, but active package libraries with many small files should not be used on shared storage during computation.

The class is complete when you can run the R batch example once and explain how the same logic could be explored in a notebook first and then moved into Slurm.
