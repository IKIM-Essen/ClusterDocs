# Jump host, shell host, and compute worker

RCC uses three different roles so that the Internet-facing doorway, the place
where users prepare work, and the machines that perform computation do not
have to be the same system.

## The short explanation

| Role | Think of it as | What you do there |
|---|---|---|
| Jump host | Guarded doorway | Nothing interactively; SSH forwards through it. |
| Shell host | Your RCC desk | Edit small files, use Git, submit jobs, inspect logs, and control workflows. |
| Compute worker | Scheduled laboratory bench | Run analysis inside a Slurm allocation. |

Your SSH configuration joins the first two steps. You normally run:

```bash
ssh {{ ssh_target_alias }}
```

SSH reads `ProxyJump {{ ssh_gateway_alias }}`, crosses the gateway, and opens
your terminal on the destination shell host. You do not need to open one
terminal on the jump host and then SSH again.

```text
workstation
  -> jump host: verify and forward
  -> shell host: prepare and supervise
  -> Slurm: allocate a worker
  -> worker: calculate
```

## Why the jump host refuses a shell

The jump host is deliberately forwarding-only for ordinary users. It reduces
the exposed surface and prevents the public entry point from becoming a place
where data, tools, or long-lived processes accumulate. A refused interactive
shell on the gateway is therefore expected behavior, not an account failure.

Test the configured destination, not the gateway:

```bash
ssh {{ ssh_target_alias }}
```

Do not use physical backend names such as `login1` or `login2`. Operations can
replace backends while the approved service aliases remain stable.

## What belongs on the shell host

Appropriate shell-host work is light control-plane activity:

- editing a script or workflow definition;
- using Git and inspecting small text logs;
- running a Snakemake dry run;
- starting the managed Snakemake or `rcc-nextflow` controller;
- using `sbatch`, `squeue`, `sacct`, and `scancel`; and
- keeping a workflow controller alive in `tmux` when documented.

The shell host is not a free compute node. Do not run sustained analysis,
large-memory work, GPU work, or high-I/O processing in its terminal.

## What belongs on a compute worker

Slurm workers perform the scientific tasks. A job requests bounded CPU,
memory, time, and optional GPU resources. Slurm chooses the worker and starts
the task there. Temporary high-I/O files may use the job's `$TMPDIR` or
approved `/local` path; declared results must return to project storage before
the allocation ends.

Snakemake and Nextflow preserve the same separation:

| Component | Runs where |
|---|---|
| Workflow definition and durable state | Project storage |
| Snakemake or Nextflow controller | Shell host or documented interactive allocation |
| Each scientific rule or process | Slurm worker |
| Temporary task files | Worker-local scratch |
| Validated outputs and provenance | Project storage |

## A common misconception

“I connected through the login service, so my command is running on a compute
node” is incorrect. SSH provides access; Slurm provides compute. Unless a
documented interactive allocation moved your shell to an assigned worker,
submit the program with the supported Slurm or workflow command.

Continue with [Class 1](../course/class-01-safe-access.md) for setup or
[Class 5](../course/class-05-slurm.md) for job submission.
