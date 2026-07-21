# Upcoming RCC changes: Slurm-first computing

!!! important "What users need to know"
    The RCC cluster is moving to a **Slurm-first operating model**. Long-running or resource-intensive work must be submitted through Slurm rather than started directly on shared login, submission, CPU, or GPU nodes.

    The rollout will happen incrementally. Some features described below may not be available on the first day, but the required usage pattern is changing now: **request resources through Slurm, set realistic limits, and release resources when work is idle.**

## Why the cluster is changing

RCC is a shared scientific computing environment. Directly occupying a server, keeping an interactive session alive for long periods, or reserving GPUs while they are mostly idle prevents other researchers from using the same hardware.

This is particularly important for GPU systems. Current usage patterns leave allocated or user-controlled GPU nodes underutilized for substantial periods while the nodes remain unavailable to others. Moving GPU work into Slurm makes resource use visible, schedulable, auditable, and fair.

The change is not intended to reduce legitimate access. It is intended to make more of the existing CPU, RAM, GPU, and storage performance available to everyone.

## What will change

### Slurm becomes the normal execution path

Use submission nodes to:

- log in;
- edit code and configuration;
- prepare environments and workflows;
- submit jobs;
- inspect logs and results; and
- perform short, lightweight diagnostics.

Use Slurm allocations, including bounded interactive allocations, for:

- CPU-intensive analysis;
- high-memory jobs;
- GPU workloads;
- long-running scripts;
- Jupyter, RStudio, Shiny, or similar compute sessions;
- workflow execution; and
- interactive debugging that requires compute resources.

Do not start substantial work directly on a shared server and leave it running outside Slurm.

### GPU access will be scheduled

GPU jobs must explicitly request GPU resources. Confirm the currently available GPU partition with `sinfo` and replace `<approved-gpu-partition>` below with its name:

```bash
srun \
  --partition=<approved-gpu-partition> \
  --gpus=1 \
  --cpus-per-gpu=4 \
  --mem=32G \
  --time=04:00:00 \
  --pty bash -i
```

For batch work, use `sbatch` and include the resource request in the script:

```bash
#!/usr/bin/env bash
#SBATCH --job-name=gpu-test
#SBATCH --partition=<approved-gpu-partition>
#SBATCH --gpus=1
#SBATCH --cpus-per-gpu=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x-%j.out

srun python train.py
```

Create the output directory before submitting the job:

```bash
mkdir -p logs
sbatch gpu-test.sbatch
```

Do not override `CUDA_VISIBLE_DEVICES`; Slurm uses it to expose only the GPU resources assigned to the job.

### Direct server use and idle allocations

The following patterns interfere with fair access and must be replaced:

- logging into a compute or GPU server and running work directly;
- keeping a GPU allocated while code is being edited, data is being prepared, or no process is using it;
- requesting all CPUs, RAM, or GPUs "just in case";
- leaving detached `tmux`, Jupyter, Python, R, or shell sessions running indefinitely;
- running long jobs on submission nodes or in interactive allocations; and
- using one very long allocation when checkpointed or staged jobs would release resources between steps.

`tmux` remains useful for protecting a lightweight controller, monitoring session, or submission workflow. It is not a substitute for Slurm resource allocation.

## New and improved capabilities

The RCC update is expected to provide a more consistent environment across the cluster. Planned or staged improvements include:

- a larger and more uniform Slurm-managed CPU fleet;
- scheduled access to GPU nodes;
- clearer CPU, GPU, RAM, and runtime requests;
- improved interactive jobs and node access tied to active allocations;
- better job accounting and visibility into resource use;
- standard Snakemake execution through Slurm;
- Apptainer support for reproducible containerized software;
- Miniforge/Mamba-based environment management;
- improved node-local temporary storage for I/O-intensive work;
- updated storage and data-transfer services;
- more consistent user identity and access across nodes; and
- improved documentation, examples, and acceptance testing.

Not every item will necessarily be complete at the initial rollout. The documentation will be updated as individual services become production-ready.

## What users should do now

1. Read the existing [Slurm guide](slurm.md).
2. Convert recurring commands and long-running analyses into `sbatch` scripts.
3. Add realistic `--time`, CPU, RAM, and GPU requests.
4. Check whether a GPU job is actually using the assigned GPU with `nvidia-smi`.
5. Add checkpoints to long workflows where supported.
6. Use Snakemake or another workflow system for multi-step analyses rather than holding one server for the entire project.
7. Stop or migrate long-lived direct sessions before enforcement begins.

A useful first check is:

```bash
squeue -u "$USER"
```

For completed jobs, inspect actual use with:

```bash
sacct -u "$USER" --starttime today \
  --format=JobID,JobName,Partition,State,Elapsed,AllocCPUS,ReqMem,MaxRSS
```

GPU utilization should also be observed during representative runs:

```bash
watch -n 2 nvidia-smi
```

## Rollout expectations

The transition will be phased. During the rollout:

- some nodes or services may move at different times;
- documentation may describe features that are still being validated;
- temporary interruptions or changed host availability may occur;
- legacy access patterns may continue briefly but should not be treated as permanent; and
- users should report workflows that cannot yet be expressed reasonably through Slurm.

The target state is clear even if individual components arrive incrementally: shared compute resources will be managed through Slurm rather than through informal ownership of servers.

## Friday Computing Club discussion

We will hold a **Friday Computing Club meeting at the end of July** to explain the transition, demonstrate the intended Slurm workflow, and discuss concerns in person.

Please bring examples of workloads that are difficult to schedule, especially:

- interactive GPU development;
- long model-training runs;
- Jupyter or RStudio sessions;
- workflows with large temporary data;
- jobs requiring several GPUs or unusually large memory; and
- analyses currently tied to a specific server.

The meeting date, time, and room will be announced separately.

## Questions and migration help

Please raise concerns early. The goal is to move valid scientific workloads into a fair and reproducible execution model, not to block them. Concrete examples—commands, expected runtime, CPU/GPU/RAM needs, and data-access patterns—will help us provide appropriate Slurm templates and identify missing functionality.
