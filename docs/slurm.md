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

See the Slurm website for the complete manual with additional examples.

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

### scancel

Use `scancel` to cancel or terminate a job. To target a specific job, the job ID is required. Use `squeue` to display job IDs.

## Job submission etiquette

If the job is expected to run continuously for more than a work day, specify a deadline using `--time`, even if just an overestimation. This information becomes especially valuable when all worker nodes are occupied as it allows other users to predict when their job will be scheduled.

When targeting GPU nodes, always request a specific amount of GPUs using `--gpus N` so that slurm can automatically assign different GPUs to concurrent jobs. More specifically, Slurm automatically selects a worker node with the specified amount of unassigned GPUs and sets the environment variable `CUDA_VISIBLE_DEVICES` accordingly.

The following example requests 2 GPUs and executes a script in batch mode with a deadline of 1 day and 12 hours:

```
sbatch --partition GPUampere --gpus 2 --time=1-12 job.sh
```

[slurm-homepage]: https://slurm.schedmd.com
[slurm-quickstart]: https://slurm.schedmd.com/quickstart.html
