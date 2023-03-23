# Slurm

The entry point to the [Slurm][slurm-homepage] cluster is the job submission node:

```sh
ssh slurmq
```

From the submission node, jobs (inline commands or scripts) can be submitted to worker nodes.

Worker nodes are divided in groups called _partitions_ in Slurm terminology. The default partition is made up of CPU nodes. GPU nodes are available in a non-default partition named after the corresponding NVIDIA GPU architecture.

See [Slurm quickstart][slurm-quickstart] for an introduction.

## Client tools

This is a brief overview of the main commands available on the submission node. They can also be invoked from worker nodes as part of a submitted job.

### sinfo

Use `sinfo` to display a summary of the worker nodes.

### squeue

Use `squeue` to display a list of scheduled jobs. It's generally useful to execute

```sh
squeue -l
```

to display additional information such as the time limit.

### srun, sbatch

Use `srun` to submit a job interactively. The output of the job is displayed on the terminal.

Use `sbatch` to submit a script. The output is written to a file in the current directory. All `srun` options apply to `sbatch` as well and can be included in the script itself with the special comment syntax `#SBATCH`.

When you submit a job, the environment variables of your current shell are inherited to the job. Slurm also sets [several][sbatch-env] environment variables such as `SLURM_JOB_ID` and `SLURM_JOB_NAME`.

### scontrol

Use `scontrol` to display detailed information about a job such as the allocated resources and the times of submission/start.

```sh
scontrol show jobid -dd [job_id]
```

### scancel

Use `scancel [job_id]` to cancel or terminate a job. Use `squeue` to display job IDs.

## Job submission etiquette

If the job is expected to run continuously for more than a work day, specify a deadline using `--time`, even if just an overestimation. This information becomes especially valuable when all worker nodes are occupied as it allows other users to predict when their job will be scheduled.

When targeting GPU nodes, always request a specific amount of GPUs using `--gpus N` so that slurm can automatically assign different GPUs to concurrent jobs. More specifically, Slurm automatically selects a worker node with the specified amount of unassigned GPUs and sets the environment variable `CUDA_VISIBLE_DEVICES` accordingly.

The following example requests 2 GPUs and executes a script in batch mode with a deadline of 1 day and 12 hours:

```sh
sbatch --partition GPUampere --gpus 2 --time=1-12 job.sh
```

Acceptable time formats include `minutes`, `minutes:seconds`, `hours:minutes:seconds`, `days-hours`, `days-hours:minutes` and `days-hours:minutes:seconds`.

## Basic Example

To illustrate basic usage, we create below `job.sh`. The output will be written to a file `slurm-[job_id].out`.

```sh
#!/bin/bash
echo "my job ran at $(date)"
echo "working directory = $(pwd)"
echo "FOO=$FOO"
echo "job id = $SLURM_JOB_ID"
echo $(hostname)
```

```sh
# Submit the job
$ export FOO=bar
$ sbatch job.sh
Submitted batch job 300451

# Show output file
$ cat slurm-300451.out
my job ran at Thu Mar 23 09:39:13 AM UTC 2023
working directory = /homes/jan/tmp
FOO=bar
job id = 300451
c120.ikim.uk-essen.de
```

## Monitor a running job

You may want to monitor a running job, for instance to check how well it makes use of GPU/CPU resources. To do that, you can start an interactive shell on the node your job is running on. This needs at least one free cpu core to work.

```sh
# Step 1: discover your allocated node with squeue.
squeue -l

# Step 2: start an interactive shell on that node.
# In this example, the job runs on node g2-1 in partition `GPUampere`
srun --partition GPUampere -w g2-1 --time=01:00:00 --pty bash -i

# Step 3: run your diagnosis tools (e.g, htop, nvidia-smi, etc.)
```

[slurm-homepage]: https://slurm.schedmd.com
[slurm-quickstart]: https://slurm.schedmd.com/quickstart.html
[sbatch-env]: https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES
