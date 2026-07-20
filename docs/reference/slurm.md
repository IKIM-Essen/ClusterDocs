# Slurm command reference

Login and submission hosts are for editing, submitting, and monitoring. Sustained
computation runs as a Slurm job.

> **Related learning:** Complete the bounded acceptance patterns in
> [Class 5](../course/class-05-slurm.md) before adapting these commands to a
> research workload.

## Discover the scheduler

```bash
sinfo
sinfo -o '%P %a %l %D %G'
squeue --me
```

Use these summaries to choose an approved partition and resource shape. Do not
copy scheduler inventories into public documents or build scripts around
physical node names.

## Choose the execution mode

| Work | Partition | Submission model | Boundary |
|---|---|---|---|
| Quick tests and batch jobs up to two hours | `cpu_short` | `sbatch` or a bounded `srun` | Keep the requested time at or below `02:00:00` |
| Active exploration, debugging, notebooks, or Shiny development | `interactive` | Bounded interactive allocation or interactive application job | The user remains present; stop it when the session ends |
| Long-running CPU analysis | `cpu_nodes` | Restartable `sbatch` job | No unattended long runner on an interactive node |
| GPU analysis | Current GPU partition, normally `gpu_nodes` | Bounded `sbatch` job with an explicit GPU request | Use only when the application can use the requested GPU |

The short queue is for genuinely short work, not for splitting a long job into
unnecessary fragments. Interactive nodes are for human-in-the-loop work. Do not
leave `tmux`, `screen`, `nohup`, notebook kernels, Shiny sessions, or other
unattended long runners there. Move sustained computation into a batch script
on the appropriate regular compute partition and add checkpointing when the
application supports it.

Partition policy can change. Confirm the live time limits with `sinfo` before
submitting, while preserving this short/interactive/batch distinction.

## Resources, allocations, and nodes

A Slurm allocation is a reservation of the resources requested by a job: CPU
cores, memory, GPUs, and time. It is **not normally an exclusive reservation of
an entire physical node**.

For a normal single-node program, request `--cpus-per-task`, `--mem`, and
`--time`; Slurm chooses a node with those resources. Adding `--nodes=1` merely
constrains placement to one node—it does not make that node exclusive. Request
multiple nodes only for software designed for multi-node execution, such as a
tested MPI application, and launch its work with `srun`. Whole-node or
exclusive allocation should be exceptional and supported by measurements or
agreed with the RCC team.

## Submit an interactive shell

```bash
srun --partition=interactive --pty --cpus-per-task=2 --mem=4G --time=00:30:00 bash -i
```

Always set a time limit and remain present. Exit the shell when finished so the
allocation is released. An interactive allocation is not a way to host an
overnight or unattended process.

## Submit a short batch job

```bash
#!/usr/bin/env bash
#SBATCH --job-name=small-analysis
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
srun python analysis.py
```

Create the output directory before submission, then run:

```bash
mkdir -p logs
sbatch job.sbatch
```

`sbatch` starts the script on the first allocated node. Use `srun` for job steps
that should use the allocated resources, especially multi-node work.

## Submit a long-running batch job

Long runners belong in a bounded, restartable batch job on regular compute—not
in a login shell, on an interactive node, or in the short queue:

```bash
#!/usr/bin/env bash
#SBATCH --job-name=long-analysis
#SBATCH --partition=cpu_nodes
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=12:00:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
srun python analysis.py
```

Twelve hours is an example request, not a default. Measure a representative
run, request a realistic limit, save checkpoints to durable storage, and make
the job safe to resume. A long job is still bounded.

## Inspect and cancel jobs

```bash
squeue --me
scontrol show job <jobid>
sacct -j <jobid> --format=JobID,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
scancel <jobid>
```

Common states include `PD` (pending), `R` (running), `CG` (completing), and
`CD` (completed). For a pending job, `squeue` or `scontrol` reports a reason;
do not repeatedly cancel and resubmit without understanding it.

## Job dependencies

Submit downstream work only after an upstream job succeeds:

```bash
first=$(sbatch --parsable preprocess.sbatch)
sbatch --dependency="afterok:$first" analysis.sbatch
```

Workflow managers such as Snakemake are preferable for larger dependency
graphs because they record files, commands, and software requirements.

## Reuse an allocation

For short development bursts, request a bounded allocation:

```bash
salloc --partition=interactive --no-shell --cpus-per-task=2 --mem=4G --time=01:00:00
srun --jobid=<allocation-id> --pty bash -i
scancel <allocation-id>
```

An allocation reserves resources even while no command is running. Cancel it
when finished. Reuse is for an attended development burst, not for reserving an
interactive node around an unattended long runner.

## GPU jobs

Use the currently documented GPU partition and resource syntax. A typical job
requests one GPU explicitly:

```bash
#SBATCH --partition=<approved-gpu-partition>
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
```

Inside the job:

```bash
nvidia-smi
python -c 'import torch; print(torch.cuda.is_available())'
```

Do not overwrite `CUDA_VISIBLE_DEVICES`; Slurm uses it to expose only the GPUs
assigned to the job. A reported driver capability does not mean every CUDA
toolkit is installed in your environment.

## Resource etiquette

- Request the CPUs, RAM, GPUs, and time the program can actually use.
- Use `cpu_short` only for work that completes within its two-hour limit.
- Keep interactive sessions attended and move long runners to batch jobs.
- Start with one representative job, measure it, and adjust.
- Avoid unbounded arrays, retry loops, and multi-day interactive shells.
- Split checkpoint-capable long work into restartable jobs.
- Keep high-I/O intermediates on job-local scratch.
- Connect directly to a worker only for monitoring or debugging an allocation
  you own, using the current supported RCC connection method.
