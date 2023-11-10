# Slurm

The entry point to the [Slurm][slurm-homepage] cluster is a set of _submission_ nodes under the name `shellhost`. Submission nodes must be used exclusively to log in and submit jobs (inline commands or scripts) to _worker_ nodes.

To connect to a submission node:

```sh
ssh shellhost
```

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

It's also possible to connect to worker nodes directly via ssh. See [Example: connect to a worker node](#example-connect-to-a-worker-node).

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

#### Example: connect to a worker node

Users can connect via ssh to worker nodes on which they have at least one running job. This is typically useful for launching monitoring (`htop`, `nvidia-smi`, etc.) or debugging tools.

After launching a job, the allocated node can be quickly discovered by passing `-u username` to `squeue`. For example:

```sh
$ squeue -u alice
JOBID PARTITION   NAME    USER ST   TIME  NODES NODELIST(REASON)
 1234      IKIM   job1   alice  R   10:30      1 c11
 1245      IKIM   job2   alice  R    3:05      1 c23
```

To connect to one of the listed nodes, open a new shell on the local workstation (not on the submission node) and execute:

```sh
ssh c11
```

The ssh session is incorporated into one of the running jobs on the target node: when the job terminates, the ssh session terminates as well.

This feature is meant for monitoring and debugging. **Do not** use it for work that could be submitted via slurm instead.

Interactive shells can also be launched on any worker node using `srun`, regardless of running jobs. See [Example: obtaining a shell on a node](#example-obtaining-a-shell-on-a-node). The `srun` method allocates one CPU core on the target node, therefore it doesn't work if the node is already fully allocated.

#### Example: create a pipeline of jobs

The `--dependency` option allows creating a tree of interdependent jobs such that downstream jobs start only after upstream jobs terminate with a certain outcome.

```sh
# This example submits a job, then two parallel downstream jobs which depend on
# on successful completion of the upstream job:
#
#      Job 10
#     /      \
# Job 11    Job 12
#
# Submit the upstream job.
$ sbatch preprocess.sh
Submitted batch job 10

# Submit a downstream job configured to wait in the queue until job 10
# terminates successfully.
$ sbatch --dependency afterok:10 train1.sh
Submitted batch job 11

# Submit another downstream job.
$ sbatch --dependency afterok:10 train2.sh
Submitted batch job 12

# Check the queue.
$ squeue
    JOBID PARTITION           NAME    USER ST    TIME  NODES NODELIST(REASON)
       12      IKIM      train2.sh   alice PD    0:00      1 (Dependency)
       11      IKIM      train1.sh   alice PD    0:00      1 (Dependency)
       10      IKIM  preprocess.sh   alice  R    0:15      1 c20
```

From a resource allocation standpoint, the individual jobs are separate: they can request different resources and might be scheduled on different nodes unless specified otherwise.

For the full dependency syntax, see the [--dependency][dependencies] section in the official manual.

### salloc

`salloc` allocates resources that can be used by subsequent invocations of `srun` or `sbatch`. By default, after allocating the resources `salloc` opens a shell **on the current node**: any `srun` or `sbatch` commands issued in this shell will use the allocated resources. When the user terminates the shell, the allocation is relinquished.

The following example requests allocates a certain number of nodes for a limited amount of time. Note that the assigned nodes are not allocated exclusively unless specified, for example by requesting all available CPU cores.

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

To request only an allocation without executing a specific command right away, execute `salloc` with `--no-shell`. As soon as the allocation is granted, a job ID is displayed in the output. The allocation can then be used by invoking `srun` or `sbatch` and passing the job ID to the `--jobid` option. The allocation stays active until either the `--time` runs out or it gets terminated via `scancel`.

#### Example: allocate resources for future use

The following example allocates 3 GPUs on the same node for 8 hours. At any point within this time frame, jobs can be executed on the allocation.

```sh
$ salloc --no-shell --time=08:00:00 --partition GPUampere --nodes=1 --gpus 3
salloc: Granted job allocation 486835

# A shell or any other job can now be submitted on allocation 486835.
# This can be done as many times as desired until the session is canceled or times out.
$ srun --jobid=486835 --pty bash -i
```

This approach is helpful for executing jobs in bursts over a period of time without losing the claim on certain resources. For instance, a user planning a bug-fixing session (short runs interspersed with code changes) on a GPU-equipped node can allocate a GPU for a few hours instead of submitting each job to the queue individually.

See [Targeting GPU nodes][targeting-gpu-nodes] to learn more about requesting GPUs.

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
# In this example, Slurm exposes 2 GPUs from a node in the GPUampere partition via CUDA_VISIBLE_DEVICES.
# The script must not override CUDA_VISIBLE_DEVICES!
# A deadline of 1 day and 12 hours is specified to let other users know when the GPUs will be available again.
srun --partition GPUampere --gpus 2 --time=1-12 train.py
```

The end-user script can then refer to specific devices by using library-specific mechanisms. For example, after passing `--gpus N` to Slurm, Pytorch maps the assigned CUDA devices to indices `0` through `N-1`: `cuda:0`, `cuda:1`, etc. Since CUDA_VISIBLE_DEVICES is managed by Slurm, end-user scripts must not modify it.

If the option `--gpus` is omitted, slurm does not set the `CUDA_VISIBLE_DEVICES` variable. This does **not** mean that GPUs are hidden: the job will have access to all GPUs on the node, even the ones assigned to slurm jobs from other users.

## Job submission etiquette

### Setting a deadline

If a job is expected to run continuously for many hours, a deadline should be specified with the option `--time`, even if just an overestimation. This information is especially valuable when all worker nodes are occupied as it allows other users to predict when their job will be scheduled. Accepted time formats include `minutes`, `minutes:seconds`, `hours:minutes:seconds`, `days-hours`, `days-hours:minutes` and `days-hours:minutes:seconds`.

It's good practice to always specify a deadline when opening a shell (`srun --pty bash`). This avoids the "hanging session" issue that occurs if the user forgets to log out or loses the connection abruptly.

### Breaking up jobs at checkpoints

A large workflow that runs for multiple days occupying several CPU cores or GPUs typically has a checkpoint system that saves its state at regular intervals. Instead of implementing such a workflow as a single job, it can be broken up into a sequence of jobs that end by saving a checkpoint and start by loading the previous checkpoint. This increases the fairness of the queue by allowing other jobs to be scheduled in between. See the [pipeline][pipelines] example for details.

[slurm-homepage]: https://slurm.schedmd.com
[sbatch-env]: https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES
[dependencies]: [https://slurm.schedmd.com/sbatch.html#OPT_dependency]
[targeting-gpu-nodes]: #targeting-gpu-nodes
[pipelines]: #example-create-a-pipeline-of-jobs
