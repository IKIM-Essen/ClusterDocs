# How shared compute works

Most users do not need to choose a special resource-sharing option. Submit work
to the normal CPU, GPU, short, or interactive partition described in the
[Slurm reference](../reference/slurm.md), and Slurm will find suitable capacity.

Some compute resources were contributed by individual research groups. RCC
protects those groups' access while allowing other researchers to use spare
capacity for suitable restartable work.

## What this means for you

- **Running ordinary research jobs?** Use the normal shared partition. Nothing
  else changes for you.
- **Your group contributed compute resources?** Use the owner submission path
  shown for your RCC account. Your eligible work receives priority on the
  capacity your group contributed.
- **Your job is short and safe to restart?** You may use spare group-owned
  capacity when the borrowing option is shown for your account.
- **Working interactively?** Use a bounded interactive allocation. RCC may use
  otherwise idle interactive capacity for restartable batch work without
  allowing that work to delay a real interactive request.

Borrowed work can be stopped and returned to the queue when the owner needs the
capacity. It starts again from the beginning unless the application has a
working checkpoint. Do not use borrowed capacity for work that cannot tolerate
that interruption.

## Which option should I use?

| What are you doing? | Use | What to expect |
|---|---|---|
| Normal CPU or GPU analysis | Shared CPU or GPU partition | Normal queue priority and fair-share |
| Work for a group that contributed hardware | Owner path supplied for the account | Priority on that group's contributed capacity |
| Short, restartable batch work | `group_borrow`, when shown for the account | The job may be requeued |
| Shell, notebook, or debugging session | `interactive` | Stay present and release it when finished |

If you are unsure, use the normal shared partition. Choose borrowed capacity
only when you understand how your application behaves after interruption.

## Is my job suitable for spare capacity?

Before borrowing capacity, answer yes to all of these questions:

1. Can the job start again without corrupting or duplicating results?
2. Are authoritative inputs and completed outputs on durable storage?
3. Does the job use atomic outputs, unique job directories, or checkpoints?
4. Is the job explicitly time-limited and submitted with `--requeue`?

Good candidates include short workflow steps, independent array elements,
compilation, validation, and stateless transformations. Databases, instrument
control, real-time services, and non-restartable calculations are not suitable.

## Technical policy details

RCC combines institutionally shared compute resources with group-contributed
resources. The scheduler protects the contributing group's access without
leaving useful hardware idle.

All names below are fictional examples. `group-alpha`, `compute-alpha-01`, and
the example users do not identify real RCC groups, people, or machines.

> A contributing group owns a reclaimable compute entitlement, not an idle
> machine.

When an owning group has work, its eligible jobs receive priority on the
resources it contributed. When the owner does not need those resources, other
RCC users may run short, restartable jobs there. These borrowed jobs may be
requeued when owner demand appears.

### Shared capacity

Most RCC resources are shared by all authorized projects. Jobs in normal CPU,
GPU, short, and interactive partitions follow ordinary queue priority and
fair-share. Owning hardware elsewhere does not allow a group to displace jobs
on community-funded shared resources.

Example:

```bash
sbatch --partition=cpu_nodes analysis.sbatch
```

### Owner capacity

A fictional `group-alpha` might have a dedicated owner partition associated
with nodes such as `compute-alpha-01`. Only the owning Slurm account and its
approved child projects can use that owner path. The scheduler assigns the
owner QOS automatically; users do not select protected QOS names manually.

Illustrative example:

```bash
sbatch \
  --account=group-alpha \
  --partition=group_owned_group_alpha \
  analysis.sbatch
```

The exact account and partition names available to a project are shown by RCC
account documentation and Slurm commands. The public site does not publish the
private node-to-group mapping.

### Borrowed capacity

When the borrowing partition is enabled for an account, idle group-owned CPU
resources may be used through `group_borrow`:

```bash
sbatch \
  --partition=group_borrow \
  --time=00:30:00 \
  --requeue \
  analysis.sbatch
```

Borrowed jobs must be batch jobs, must have an explicit time limit, and must be
safe to restart. They can be requeued before completion when an owner job needs
the same capacity.

### Interactive use

Interactive computation also runs through Slurm. Login services are for
editing, submission, monitoring, file inspection, and starting an allocation;
they are not unmanaged compute nodes.

Example:

```bash
salloc \
  --partition=interactive \
  --cpus-per-task=4 \
  --mem=16G \
  --time=02:00:00
```

Where the `interactive_backfill` partition is advertised, idle interactive
nodes may run short batch work there. A real interactive request can requeue
that backfill work. This improves utilization while preserving responsive
interactive access.

Interactive-backfill jobs have the same basic requirements as borrowed jobs:
they are batch-only, explicitly time-limited, requeue-enabled, and restartable.

### What requeue means

Requeue does not continue a process from the exact instruction where it stopped.
The job returns to the queue and starts again unless the application provides a
working checkpoint-and-restart mechanism.

A robust workflow should therefore:

1. keep authoritative input and completed output on durable project storage;
2. use node-local storage for temporary work;
3. write outputs atomically or into unique job directories;
4. record checkpoints where the application supports them;
5. detect already completed steps when it starts again;
6. avoid treating a partial file as a valid final result.

Snakemake is well suited to this pattern when rules have declared inputs and
outputs and incomplete files are handled correctly.

### Fair-share and accounting

Using a group's contributed resources does not give that group control over the
rest of the cluster. Shared-pool work remains subject to normal fair-share.
Borrowed use, owner use, preemptions, requeues, interactive wait time, and
resource utilization are accounted separately so the policy can be reviewed.

### User responsibilities

- Request realistic CPU, memory, GPU, and time limits.
- Use `--requeue` for opportunistic jobs.
- Keep borrowed and backfill jobs restartable.
- Use checkpointing for long calculations.
- Do not run heavy computation outside a Slurm allocation.
- Use `sacct` after completion to compare requested and observed resources.
- Contact RCC support when a workflow cannot tolerate interruption; do not hide
  that limitation in a borrowed job.

The policy minimizes idle resources while preserving predictable access for
contributing groups and responsive interactive work for the wider RCC
community.
