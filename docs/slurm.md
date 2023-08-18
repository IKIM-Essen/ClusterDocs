# Slurm

The entry point to the [Slurm][slurm-homepage] cluster is a set of nodes under the name `shellhost`. Before connecting, acquire the list of ssh host keys by executing:

```sh
ssh-keygen -R shellhost.ikim.uk-essen.de && \
    ssh ikim resolvectl query shellhost.ikim.uk-essen.de | \
    grep -E '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' --only-matching | \
    sed -E 's/(.*)/\1 shellhost.ikim.uk-essen.de/' | \
    ssh ikim ssh-keyscan -t ed25519 -f - >> ~/.ssh/known_hosts
```

Then connect to a submission node:

```sh
ssh shellhost
```

Jobs (inline commands or scripts) can be submitted to worker nodes from any of the submission nodes.

Worker nodes are divided in groups called _partitions_ in Slurm terminology. The default partition is made up of general-purpose CPU nodes.

This document is not a comprehensive guide on Slurm. To learn more, see the official manual.

## Client tools

This is a brief overview of the main commands available on the submission nodes. They can also be invoked from worker nodes as part of a submitted job.

### sinfo

Use `sinfo` to display a summary of the worker nodes.

### squeue

Use `squeue` to display a list of scheduled jobs. It's generally useful to execute

```sh
squeue -l
```

to display additional information such as the time limit.

### srun

Use `srun` to submit a job interactively. The output is displayed on the terminal.

#### Example: obtaining a shell on a node

The following example opens a shell on a worker node. The node is selected automatically by Slurm.

```sh
# A deadline is specified to avoid leaving a hanging session if the user doesn't terminate it.
srun --time=01:00:00 --pty bash -i
```

#### Example: requesting resources

A simple `srun` command is executed by default on a single worker node, using a single CPU core. Several options are available for configuring the allocated resources. In the following example, Slurm allocates 32 CPU cores by picking a worker node with enough free cores.

```sh
srun --cpus-per-task=32 python3 script.py
```

#### Example: environment inheritance

When Slurm executes a job, it inherits the caller's environment and current directory. Slurm also sets [several][sbatch-env] environment variables such as `SLURM_JOB_ID` and `SLURM_JOB_NAME`. The same applies to the other submission commands `sbatch` and `salloc`.

To illustrate, let's create a script called `job.sh` and execute it via `srun`.

```sh
$ pwd
/homes/alice/workdir

$ cat job.sh
#!/usr/bin/env sh
echo "my job ran on $(date)"
echo "working directory: $(pwd)"
echo "FOO=$FOO"  # this variable is not defined in the script
echo "job id: $SLURM_JOB_ID"  # this variable is defined by Slurm
echo $(hostname)

# Define an environment variable and execute the job.
$ FOO=bar srun sh job.sh
my job ran on Thu May  4 15:25:10 UTC 2023
working directory: /homes/alice/workdir
FOO=bar
job id: 340273
c5.ikim.uk-essen.de
```

### sbatch

Use `sbatch` to submit a script. The output is written to a file in the current directory. All `srun` options apply to `sbatch` as well and can be included in the script itself with the special comment syntax `#SBATCH`.

`sbatch` allocates the requested resources, then executes the script **on the first of the allocated nodes**. To use the allocated resources effectively, `srun` must be invoked within the script, otherwise only one node is used.

#### Example: submitting a job with sbatch

Let's create a script called `job.sh` with a couple of `srun` calls and execute it via `sbatch`. Slurm redirects standard output to the text file `slurm-[job_id].out`.

```sh
# Create a script which allocates 3 nodes and submits two job steps using srun.
$ cat job.sh
#!/usr/bin/env sh
#SBATCH --nodes 3
#SBATCH --time 01:00:00
srun hostname
srun echo hello

# Execute the script.
$ sbatch ./job.sh
Submitted batch job 340264

# Display the output. The jobs steps were executed simultaneously on all 3 nodes.
$ cat slurm-340264.out
c7.ikim.uk-essen.de
c23.ikim.uk-essen.de
c20.ikim.uk-essen.de
hello
hello
hello
```

The following example shows the effect of an equivalent script without `srun`.

```sh
# Create a script which allocates 3 nodes, then executes two commands without srun.
$ cat job.sh
#!/usr/bin/env sh
#SBATCH --nodes 3
#SBATCH --time 01:00:00
hostname
echo hello

# Execute the script.
$ sbatch ./job.sh
Submitted batch job 340266

# Display the output. The commands were simply executed on the first assigned node.
$ cat slurm-340266.out
c7.ikim.uk-essen.de
hello
```

#### Example: monitor a job

It can be useful to request a shell on a specific node, for example to monitor the resource usage of a running job.

```sh
# Step 1: discover your allocated node with squeue.
squeue -l

# Step 2: start an interactive shell on that node.
# In this example, the job runs on node c120.
srun --nodelist=c120 --time=01:00:00 --pty bash -i

# Step 3: run your diagnosis tools (e.g, htop, nvidia-smi, etc.)
```

Since any job requires at least one CPU core, this method doesn't work if all CPU cores on the target node have already been requested.

### salloc

`salloc` allocates resources that can be used by subsequent invocations of `srun` or `sbatch`. By default, after allocating the resources `salloc` opens a shell **on the current node**: any `srun` or `sbatch` commands issued in this shell will use the allocated resources. When the user terminates the shell, the allocation is relinquished.

```sh
$ salloc --nodes=3 --time=01:00:00
salloc: Granted job allocation 340227

$ srun hostname
c5.ikim.uk-essen.de
c6.ikim.uk-essen.de
c7.ikim.uk-essen.de

$ exit
salloc: Relinquishing job allocation 340227
salloc: Job allocation 340227 has been revoked.
```

If a command is supplied to `salloc`, it is executed instead of opening a shell. The command runs on the current node, therefore it should include `srun` or `sbatch`.

The assigned nodes are not allocated exclusively unless specified, for example by requesting all available CPU cores.

### scontrol

Use `scontrol` to display detailed information about a job such as the allocated resources and the times of submission/start.

```sh
scontrol show jobid -dd [job_id]
```

### scancel

Use `scancel [job_id]` to cancel or terminate a job. Use `squeue` to display job IDs.

## Targeting GPU nodes

GPU nodes are available in a non-default partition named after the corresponding NVIDIA GPU architecture. The `--partition` option must be specified to target them.

When executing GPU workloads, the `--gpus N` option should always be specified to let slurm assign `N` GPUS automatically. More specifically, Slurm automatically selects a suitable worker node, picks the specified number of GPUs randomly among the unassigned ones and sets the environment variable `CUDA_VISIBLE_DEVICES` accordingly.

```sh
# In this example, 2 GPUs from a node in the GPUampere partition are exposed via CUDA_VISIBLE_DEVICES.
# A deadline of 1 day and 12 hours is specified to let other users know when the GPUs will be available again.
srun --partition GPUampere --gpus 2 --time=1-12 train.py
```

By specifying `--gpus 0` or omitting the option, slurm does not set the `CUDA_VISIBLE_DEVICES` variable, but it does **not** mean that GPUs are hidden. The job will have access to all GPUs on the node, even the ones assigned to other slurm jobs. This is useful when monitoring the usage of resources on specific nodes:

```sh
srun --partition GPUampere --nodelist=g2-1 nvidia-smi
```

## Job submission etiquette

If a job is expected to run continuously for many hours, a deadline should be specified with the option `--time`, even if just an overestimation. This information is especially valuable when all worker nodes are occupied as it allows other users to predict when their job will be scheduled. Accepted time formats include `minutes`, `minutes:seconds`, `hours:minutes:seconds`, `days-hours`, `days-hours:minutes` and `days-hours:minutes:seconds`.

It's good practice to always specify a deadline when opening a shell (`srun --pty bash`). This avoids the "hanging session" issue that occurs if the user forgets to log out or loses the connection abruptly.

[slurm-homepage]: https://slurm.schedmd.com
[sbatch-env]: https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES
