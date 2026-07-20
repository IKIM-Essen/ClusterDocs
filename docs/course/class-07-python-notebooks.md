# Class 7: Python notebooks for large datasets

This class teaches a safe pattern for interactive Python analysis on RCC. A notebook is useful for inspection, statistics, and figures. It is **not** the place to run an overnight computation or keep many gigabytes in memory without limits.

## Learning goals

After this class, you can:

- start JupyterLab only inside a Slurm allocation;
- tunnel the notebook to your workstation without exposing it to the network;
- inspect a large dataset by sampling and summarising instead of loading everything blindly;
- choose between pandas, Polars, DuckDB, Arrow, NumPy, SciPy, and Matplotlib;
- distinguish descriptive analysis, statistical modeling, machine-learning training, validation, and inference;
- measure memory and runtime;
- move expensive work from a notebook into a Slurm batch script.

## Before you start

Complete the Class 1 SSH gate and the Class 5 Slurm gate. You need a working SSH client, a valid RCC account, and the ability to submit one small Slurm job.

## The RCC notebook rule

A notebook kernel is a normal process. It consumes CPU, memory, local scratch space, and sometimes a GPU. Therefore, on RCC it must run under Slurm:

```bash
cp -a examples/interactive-workflows/jupyter my-jupyter-session
cd my-jupyter-session
sbatch jupyter.sbatch
```

Read the job output file. It shows the worker, the selected loopback port, and the tunnel command. Open only the local address shown by the tunnel. Do not bind a notebook to a public interface and do not disable the token.

The connection sequence is always:

1. submit the Jupyter job;
2. wait for the job to report its worker, loopback port, token, and tunnel;
3. run that tunnel command on your workstation;
4. open the local `127.0.0.1` address;
5. stop the Slurm job with `scancel <jobid>` when finished.

> **Reference companions:** [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md)
> contains connection diagnostics. [Slurm commands](../reference/slurm.md)
> explains how to inspect and stop the notebook allocation.

## Large-data pattern

Use this sequence before writing a full analysis:

1. Describe the question in one sentence.
2. Inspect the file size and format.
3. Load a small sample or a small set of columns.
4. Summarise groups before plotting.
5. Check memory use.
6. Save a small reproducible notebook.
7. Move full-scale work into a Slurm script.

For tabular data, prefer columnar or chunked access. CSV is portable, but slow for repeated analysis. Parquet, Arrow, DuckDB, or an indexed database table are usually better for repeated interactive work.

## Copyable example

The course includes:

- `examples/interactive-workflows/notebooks/python-large-data.ipynb`
- `examples/interactive-workflows/python/analysis.py`
- `examples/interactive-workflows/python/python.sbatch`
- `examples/interactive-workflows/python/environment.yml`

The notebook uses synthetic data so that you can practice safely. The batch script shows the same idea as a scheduled Slurm job.

## Python tool choices

| Task | Suggested tool | Notes |
|---|---|---|
| Small to medium tables | pandas | Good default for teaching and quick work. |
| Larger local tables | Polars or DuckDB | Useful when memory becomes tight. |
| Numerical arrays | NumPy | Keep arrays typed and avoid unnecessary copies. |
| Statistics | SciPy, statsmodels | Record versions and assumptions. |
| Static plots | Matplotlib | Reliable for publication-oriented figures. |
| Interactive exploration | Notebook widgets sparingly | Avoid building long-running web apps in a notebook. |

## AI and data science techniques

Use notebooks to inspect data, establish baselines, compare techniques, and
explain results. Move full training, large hyperparameter searches, embedding
generation, and production inference into bounded batch workflows.

A reviewable machine-learning workflow includes:

- data-quality and missingness checks;
- a subject-safe or time-safe split into training, validation, and test data;
- preprocessing and feature engineering inside the versioned pipeline;
- a simple statistical or machine-learning baseline;
- an evaluation measure chosen before tuning;
- calibration, uncertainty, subgroup behavior, and leakage checks;
- fixed seeds where deterministic behavior is possible; and
- versioned code, environment, parameters, metrics, and model artifacts.

Tree models and regularized regression are often strong tabular baselines.
Neural networks and transformers are appropriate when the data type, sample
size, and research question justify their complexity. Unsupervised techniques
such as clustering, dimensionality reduction, and representation learning need
stability checks and scientific interpretation; visual separation alone is not
validation.

Use GPUs only when measurement shows that the framework and workload benefit.
For larger-than-memory tables, try column selection, Parquet, Arrow, DuckDB,
Polars, and chunked processing before introducing distributed computation.
Spark-style processing is useful only when its parallelism outweighs network,
serialization, scheduling, and operational overhead.

> **Reference companion:** [AI and data science on RCC](../reference/ai-data-science.md)
> covers technique selection, model development, training versus inference,
> distributed processing, reproducibility, and responsible-use boundaries.

## Good security and reproducibility habits

- Do not paste patient identifiers, tokens, private keys, or passwords into notebooks.
- Do not commit notebook outputs containing restricted data.
- Keep notebooks small enough that another person can review the reasoning.
- Put package versions in `environment.yml`.
- Use project membership rather than sharing another user account.
- Shut down the Slurm job when you are finished.

## Completion gate

Run the local structure check before using the example on RCC:

```bash
python3 exercises/interactive/validate-interactive-examples.py
```

Then start one Jupyter job and confirm three things:

1. The job output says the notebook binds to `127.0.0.1`.
2. You can connect through the SSH tunnel.
3. You can stop the job with `scancel`.

Do not run more than one notebook job for this class.

## Self-check questions

1. Why is a notebook kernel a Slurm workload?
2. Why is a sampled plot safer than loading every row at once?
3. What should move from a notebook into a batch script?
4. Why should notebook ports bind only to loopback?
5. Which files should not be committed to a repository?
