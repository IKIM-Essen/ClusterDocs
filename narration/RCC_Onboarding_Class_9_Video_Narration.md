# Class 9: Python notebooks for large datasets — video narration

## Slide 1: Class 9: Python notebooks for large datasets

Welcome to Class 9: Python notebooks for large datasets. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning goals

After this class, you can: start JupyterLab only inside a Slurm allocation; tunnel the notebook to your workstation without exposing it to the network; inspect a large dataset by sampling and summarising instead of loading everything blindly; choose between pandas, Polars, DuckDB, Arrow, NumPy, SciPy, and Matplotlib; distinguish descriptive analysis, statistical modeling, machine-learning training, validation, and inference; measure memory and runtime; move expensive work from a notebook into a Slurm batch script.

## Slide 3: The RCC notebook rule

A notebook kernel is a normal process. It consumes CPU, memory, local scratch space, and sometimes a GPU. Therefore, on RCC it must run under Slurm: Read the job output file. It shows the worker, the selected loopback port, and the tunnel command. Open only the local address shown by the tunnel. Do not bind a notebook to a public interface and do not disable the token. The connection sequence is always: submit the Jupyter job; wait for the job to report its worker, loopback port, token, and tunnel; run that tunnel command on your workstation; open the local 127.0.0.1 address; stop the Slurm job.

## Slide 4: Large-data pattern

Use this sequence before writing a full analysis: Describe the question in one sentence. Inspect the file size and format. Load a small sample or a small set of columns. Summarise groups before plotting. Check memory use. Save a small reproducible notebook. Move full-scale work into a Slurm script. For tabular data, prefer columnar or chunked access. CSV is portable, but slow for repeated analysis. Parquet, Arrow, DuckDB, or an indexed database table are usually better for repeated interactive work.

## Slide 5: Copyable example

The course includes: examples/interactive-workflows/notebooks/python-large-data.ipynb examples/interactive-workflows/python/analysis.py examples/interactive-workflows/python/python.sbatch examples/interactive-workflows/python/environment.yml The notebooks use synthetic data so that you can practice safely. Their RiboSnake-inspired section builds a Bray--Curtis PCoA and a ranked waterfall plot in both Python and R. Run the cells to render the figures; committed notebook outputs stay empty so that results or restricted data cannot be published accidentally. The batch script shows the same idea as a scheduled Slurm job.

## Slide 6: Good security and reproducibility habits

Do not paste patient identifiers, tokens, private keys, or passwords into notebooks. Do not commit notebook outputs containing restricted data. Keep notebooks small enough that another person can review the reasoning. Put package versions in environment.yml. Use project membership rather than sharing another user account. Shut down the Slurm job when you are finished.

## Slide 7: Completion gate

Run the local structure check before using the example on RCC: Then start one Jupyter job and confirm three things: The job output says the notebook binds to 127.0.0.1. You can connect through the SSH tunnel. You can stop the job with scancel. Do not run more than one notebook job for this class.
