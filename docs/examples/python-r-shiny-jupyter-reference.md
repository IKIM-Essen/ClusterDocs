# Python, R, Shiny, and Jupyter on the RCC

This guide provides supported patterns for interactive exploration and scheduled analysis on the RCC. The central rule is that **computation runs through Slurm**. Login and interactive nodes are for editing, submitting, monitoring, and forwarding connections—not for sustained computation.

## Storage and environment rules

Use these locations consistently:

| Purpose | Location | Notes |
|---|---|---|
| Source code, notebooks, small configuration | project or home storage | Keep under version control where possible. |
| Input and final output | project storage | Prefer compressed, sequential formats. |
| Conda environments and package cache | `/local/conda/$USER` | Configured automatically on RCC worker nodes. |
| Job scratch | `/local/work/slurm-jobs/$USER/slurm-job-$SLURM_JOB_ID` | Created by the Slurm prolog and removed after it becomes stale. |
| Apptainer cache | `/local/apptainercache/$USER` | Node-local; do not place container caches on network storage. |

Avoid environments containing thousands of small files on shared storage. Create the environment within an allocated worker node, or build a reproducible Apptainer image and reuse it.

## Python batch analysis

Copy the example directory and create its environment from a worker allocation:

```bash
cp -a examples/user-workflows/python my-python-analysis
cd my-python-analysis
srun --partition=interactive --pty --cpus-per-task=2 --mem=4G --time=00:30:00 bash
mamba env create -f environment.yml -n rcc-python-example
conda activate rcc-python-example
python analysis.py
exit
```

Submit the same analysis as a batch job:

```bash
sbatch python.sbatch
```

The batch script stages inputs into node-local scratch and copies only final results back to the submission directory.

## R batch analysis

The supported R pattern uses a pinned Conda environment, which keeps R and compiled package dependencies reproducible:

```bash
cp -a examples/user-workflows/r my-r-analysis
cd my-r-analysis
srun --partition=interactive --pty --cpus-per-task=2 --mem=6G --time=00:45:00 bash
mamba env create -f environment.yml -n rcc-r-example
conda activate rcc-r-example
Rscript analysis.R
exit
sbatch r.sbatch
```

For larger projects, commit `environment.yml` and optionally an `renv.lock`. Do not use a shared-storage `renv/library` as the active library during computation; restore it into job-local storage or use the Conda environment shown here.

## JupyterLab notebooks

Jupyter must run inside a Slurm allocation and listen only on loopback. The supplied launcher:

```bash
cp -a examples/user-workflows/jupyter my-notebooks
cd my-notebooks
sbatch jupyter.sbatch
```

The job output reports the assigned worker node, port, and tunnel command. On your workstation, create the tunnel through the RCC SSH entry point using the exact worker and port shown in the log:

```bash
ssh -N -L 8888:127.0.0.1:<PORT> \
  -J <RCC-SSH-ENTRY> <USERNAME>@<WORKER>
```

Then open `http://127.0.0.1:8888` and paste the token printed in `jupyter-<jobid>.out`.

Security requirements:

- Jupyter binds to `127.0.0.1`, never `0.0.0.0`.
- Do not disable the token.
- Do not expose notebook ports through the firewall.
- Stop the job when finished: `scancel <jobid>`.
- Notebook kernels consume the CPU, RAM, GPU, and time requested in the Slurm script.

The example environment includes Python and an R kernel. Add packages to `environment.yml`, rebuild the environment, and keep notebooks separate from large input data.

## Shiny applications

Shiny applications also run inside a Slurm allocation and bind only to loopback:

```bash
cp -a examples/user-workflows/shiny my-shiny-app
cd my-shiny-app
sbatch shiny.sbatch
```

Read `shiny-<jobid>.out`, then create the tunnel reported there:

```bash
ssh -N -L 3838:127.0.0.1:<PORT> \
  -J <RCC-SSH-ENTRY> <USERNAME>@<WORKER>
```

Open `http://127.0.0.1:3838` locally. This pattern is intended for development, demonstrations, and bounded research sessions. It is not a production web-hosting service. A persistent or multi-user Shiny deployment requires an explicitly reviewed RCI service, authentication, reverse proxying, logging, lifecycle management, and a data-protection review.

## GPU notebooks and Python jobs

Request a GPU only when the code uses it:

```bash
#SBATCH --partition=gpu_nodes
#SBATCH --gres=gpu:1
```

Inside the allocation, first verify visibility:

```bash
nvidia-smi
```

Then verify the framework itself, for example:

```bash
python -c 'import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))'
```

Use a CUDA-enabled environment or a reviewed Apptainer image whose userspace CUDA libraries are compatible with the RCC driver. The host NVIDIA driver remains managed and tested by RCC operations.

## Resource selection

Start conservatively and measure:

- `--cpus-per-task`: threads the process can actually use.
- `--mem`: total RAM for the job.
- `--time`: realistic upper bound.
- `--gres=gpu:1`: only for GPU-enabled work.

Within Python use `psutil`, `/usr/bin/time -v`, or application profilers. Within R use `profvis`, `Rprof()`, and `peakRAM`. Slurm accounting can be inspected after completion with:

```bash
sacct -j <jobid> --format=JobID,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

## Common failures

**Environment creation is slow or causes heavy metadata I/O**
Confirm `CONDA_ENVS_PATH` and `CONDA_PKGS_DIRS` point to `/local/conda/$USER`. Build from a worker allocation, not directly on shared storage.

**The browser cannot reach Jupyter or Shiny**
Confirm the job is running, use the worker and port from the job log, and keep the SSH tunnel process open.

**The application starts on the login node**
Cancel it and submit through Slurm. Long-running Python, R, Jupyter, and Shiny processes are not permitted on login nodes.

**The job cannot find files after staging**
Use absolute paths or derive the submission directory from `SLURM_SUBMIT_DIR`. Copy final outputs back before the job exits.
