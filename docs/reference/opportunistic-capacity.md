# Opportunistic RCC capacity for short CPU jobs

> **Availability:** This scheduling policy is being introduced through a
> controller-first canary. It applies only when RCC reports the capability as
> active; users must not select hidden partitions or protected QOS names.

RCC can use otherwise-idle hardware for short CPU work without changing the
normal submission workflow.

## What qualifies

A normal CPU job may use opportunistic capacity when it:

- requests no GPU;
- has an explicit wall time of at most two hours; and
- otherwise fits the available CPU and memory resources.

No special RCC partition, QOS, project flag, or ownership option is required.
Submit normally and make the resource request accurate:

```bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=24G
#SBATCH --time=01:30:00
```

## Interactive systems

Selected interactive RCC systems can run short Slurm work in the background
while retaining CPU and memory headroom for interactive allocations. Background
compute is deliberately subordinate under contention and is limited to the
resources that Slurm advertises.

Interactive access remains allocation-bound. This policy does not authorize
unmanaged computation through a direct SSH session. Resource-intensive analysis
still belongs in Slurm.

## Idle GPU servers

An otherwise-idle GPU server can provide CPU capacity to an eligible job that
does not request a GPU. RCC admits new background work only while the server is
idle.

GPU work has precedence. If a real GPU allocation needs resources held by an
already-running background CPU job, Slurm may requeue that CPU job. An explicit
`--no-requeue` request keeps a job off reclaimable GPU capacity while preserving
its eligibility for ordinary non-preemptive CPU capacity.

## Write jobs so restart is safe

Requeueing means a batch job may execute again. A robust job should:

1. keep durable inputs on approved shared storage;
2. use job-local storage only for temporary working data;
3. write results to a temporary or unique output name;
4. validate the result;
5. atomically move it into its final shared-storage location; and
6. use checkpoints when restarting from the beginning is expensive.

The practical rule remains simple: submit normally, request an accurate wall
time, and let Slurm choose the machine.
