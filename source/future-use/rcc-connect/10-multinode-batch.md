# Multi-node jobs: run one analysis across several Slurm workers (pilot draft)

> **Source-only proposal, not available as an RCC Connect release.**
> Batch execution requires separate site acceptance. This is a portable
> educational explanation; actual partitions, MPI versions and allowed
> node/GPU classes come from the site's published, verified capabilities.

## Why might I need more than one node?

A node is a compute machine, not a CPU core. A job can use many CPUs on
**one** node, or it can request **several** nodes. A multi-node program must
actually coordinate parallel processes across nodes. Increasing the number of
nodes does not automatically make an ordinary R or Python script faster.

A conventional single-node analysis is often the best first choice. Consider
multi-node only for software that supports MPI ranks, distributed workers,
multi-node data processing or distributed training, after measuring one-node
performance.

| I want to do... | Suggested execution |
| --- | --- |
| Explore a dataset, debug Python, plot in R | Single-node Slurm development allocation (Workbench, VS Code or Positron) |
| Train a model on one accepted GPU | Slurm single-node GPU allocation or batch job |
| Run an MPI simulation or distributed CPU program | Multi-node Slurm **batch** job |
| Run distributed GPU training | Multi-node Slurm **batch**, only after specific GPU/fabric/runtime acceptance |
| Run many unrelated samples | Often a Slurm job array or workflow manager, not a single multi-node job |

## Choose resources by tasks, not by guessing machine names

A multi-node batch submission must describe:

- **Nodes:** how many whole machines the scheduler should allocate.
- **Tasks per node:** the number of independent ranks/processes per machine.
- **CPUs per task:** CPU threads reserved for each rank/process.
- **Memory per node:** the entire memory budget for each machine (not per rank).
- **GPUs per node:** only for an accepted GPU batch class.
- **Walltime:** the maximum duration; jobs may queue until all requested
  resources can be allocated simultaneously.
- **MPI integration:** request a site-accepted plugin only when the program
  and its MPI build require it. Do not assume PMIx support without a live
  `srun --mpi=list` acceptance test.

For example, two nodes × four tasks per node × two CPUs per task represent
**eight parallel tasks and sixteen requested CPUs across two nodes**.
A two-node job requesting 32 GiB memory per node has a separate 32 GiB
limit on each node, not one shared 64 GiB address space.

## Submitting from any RCC interface

The intended flow is the same whether you use the browser, VS Code,
Positron, or a terminal:

1. Select your project and an approved multi-node batch execution profile.
2. Describe the application command and resources, or use a reviewed workflow
   template. RCC presents a preview of the Slurm request and any warnings.
3. The scheduler validates entitlement and availability and submits one
   batch job. **Slurm**, not the editor or user, selects eligible nodes.
4. View queued/running/completed status and logs in your preferred interface.
   Closing the editor must not cancel the job.
5. Save results to the project's durable storage. Use job-local `$TMPDIR`
   for expensive temporary I/O, copying required outputs back before exit.

The source-only RCC helper `scripts/rcc-multinode-job.py` illustrates a
validated, explicit `sbatch` and `srun` path. Its example policy is
disabled. It is **not** yet a distributed computing button in RCC Connect.

Preview syntax (for developers working from the reviewed RCC source checkout):

```bash
python3 scripts/rcc-multinode-job.py plan \
  --spec config/multinode-job.example.json \
  --policy config/multinode-policy.example.json
```

The example command uses a synthetic program and an example partition; it
submits nothing. In an accepted site environment, an explicit submit would
add a job receipt and require an operator-installed, root-owned policy. A
connection loss is ambiguous: find the existing request by its unique job
name/comment before attempting any new submission.

## Important distinctions

**An interactive development session is still single-node.** VS Code Server,
Positron's backend, terminals and R/Python kernels remain attached to the
Slurm worker hosting that development allocation. A multi-node batch job is
different: it uses resources on several Slurm workers, independently of the
laptop session. Running MPI from a shellhost or creating SSH connections to
individual compute hosts is not an alternative.

**No expertise gate.** Everyone may choose how to submit supported jobs; the
site's actual resource permissions and scheduler quotas still apply. The
interface can recommend single-node, job arrays, MPI or a workflow based on the
task and resource requirements without classifying the user as a beginner or
expert. autoSRE can advise on sizing from job accounting, but cannot grant
unapproved nodes or bypass Slurm.

## Acceptance before publication

A synthetic two-node rank-placement test, per-node memory/cgroup checks, PMIx
plugin and MPI binary qualification, distributed GPU/fabric qualification if
offered, project authorization, job receipt/recovery and batch queue limits
must pass. The first pilot should cover an ordinary independent-process
job and a genuine MPI program separately. Do not claim that a multi-node
request is faster until the application has been profiled.

See [Slurm and data](05-slurm-and-data.md),
[Choose your interface](01-choose-your-environment.md), and
[operator acceptance](07-operator-acceptance.md).
