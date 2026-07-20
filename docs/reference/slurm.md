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

## Submit an interactive shell

```bash
srun --pty --cpus-per-task=2 --mem=4G --time=00:30:00 bash -i
```

Always set a time limit. Exit the shell when finished so the allocation is
released.

## Submit a batch job

```bash
#!/usr/bin/env bash
#SBATCH --job-name=small-analysis
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
salloc --no-shell --cpus-per-task=2 --mem=4G --time=01:00:00
srun --jobid=<allocation-id> --pty bash -i
scancel <allocation-id>
```

An allocation reserves resources even while no command is running. Cancel it
when finished.

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
- Start with one representative job, measure it, and adjust.
- Avoid unbounded arrays, retry loops, and multi-day interactive shells.
- Split checkpoint-capable long work into restartable jobs.
- Keep high-I/O intermediates on job-local scratch.
- Connect directly to a worker only for monitoring or debugging an allocation
  you own, using the current supported RCC connection method.
