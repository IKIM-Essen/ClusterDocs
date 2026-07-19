# RCC Onboarding Class 7 narration: Python notebooks for large datasets

**Estimated duration:** 8-9 minutes

## Chapter 1 — What notebooks are for

In this class we use Python notebooks for what they are good at: looking at data, checking assumptions, calculating summaries, and making figures that explain what is happening.

A notebook is not a magic lightweight tool. The Python kernel is a real process. It uses CPU, memory, temporary disk space, and sometimes a GPU. On RCC that means the kernel must run inside a Slurm allocation.

The safe pattern is simple. You submit a Jupyter job. The notebook listens only on the worker itself. You create an SSH tunnel from your laptop. Then your browser talks to your local address while the computation remains inside the scheduled allocation.

## Chapter 2 — Start small, then scale

Large-data work should not begin by loading everything. First ask what the question is. Then inspect the file size, format, and columns. Load a small sample. Summarise groups before plotting. Measure memory. Only after that should you decide whether pandas is enough or whether you need DuckDB, Arrow, Polars, or a batch workflow.

This habit protects the cluster and saves your time. A mistake that is invisible on a small laptop example can become a long-running job or a memory failure when applied to real project data.

## Chapter 3 — The provided example

The course contains a synthetic Python notebook and a matching Slurm batch script. The notebook is for inspection. The script is for repeatable execution. Both use safe sample data and avoid real project identifiers.

Open the notebook, run the group summary, and look at the sampled plot. Then inspect the batch script. Notice that it stages work into local scratch and copies final results back. That separation is one of the most important RCC habits.

## Chapter 4 — Security and attribution

Do not paste passwords, tokens, private keys, patient identifiers, or restricted sample sheets into notebooks. Do not share a notebook containing hidden output cells with sensitive data. Do not use another person’s account to access a project. If somebody needs access, ask for named project membership.

A notebook should explain the analysis. It should not become an unreviewed archive of secrets and patient data.

## Chapter 5 — Completion

The class is complete when you can start one Jupyter job, connect through one tunnel, run the synthetic example, and stop the job. You should also be able to explain when work belongs in the notebook and when it belongs in a Slurm batch job.
