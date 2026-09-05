# Why RCC does not run everything on Kubernetes

Experienced infrastructure users often ask why RCC does not simply put every
service and scientific workload onto Kubernetes, or put all shared data behind a
single general-purpose distributed storage platform such as Ceph. The short
answer is: **RCC is designed around scientific I/O behavior first, then uses the
scheduler and storage semantics that fit each workload.**

This is not an argument that Kubernetes or Ceph are bad. Both are excellent,
widely used platforms. The RCC question is whether making either one the
universal substrate would improve the actual research workload enough to justify
another control plane, another translation layer, or another shared-I/O path.

## I/O patterns were the most important design constraint

For RCC, the decisive observation is that scientific workloads do not merely
consume bytes. They create very different **I/O patterns**:

- a few very large sequential FASTQ/BAM/CRAM/image/model objects;
- millions of metadata operations across tiny files;
- Conda/package trees with tens of thousands of files;
- workflow engines repeatedly checking paths and timestamps;
- temporary databases and random-access indexes;
- hundreds of jobs simultaneously reading the same reference data; and
- temporary intermediate data that does not need to cross the storage network at
  all.

A platform can advertise enormous aggregate bandwidth and still perform badly
when the useful work consists of millions of tiny opens, stats, seeks, directory
walks, locks, or synchronous metadata updates. This is why RCC documentation
repeatedly emphasizes **streaming versus random I/O, metadata pressure, local
scratch, caching, and workflow shape**.

This is also why the preferred pattern for I/O-intensive work is:

```text
durable project input
      -> Slurm allocation
      -> stage active working set to node-local scratch
      -> compute and temporary/random I/O locally
      -> validate declared outputs
      -> return durable results to the project
```

The point is not that shared storage is slow. The point is that no shared
filesystem can make an adversarial access pattern free.

## Why a different storage platform alone would not solve it

Ceph, object stores, distributed POSIX layers, and other mature storage systems
have different strengths and operational tradeoffs. RCC can and does use object
semantics where they fit. Project S3 exists for workloads that genuinely benefit
from object access.

But changing the storage backend does not remove the workload-level problem:

- 500,000 tiny files still create far more metadata work than one large object;
- repeated directory scans still create repeated metadata work;
- a workflow that rewrites temporary files over shared storage still creates
  unnecessary network traffic;
- thousands of clients starting identical software environments can still cause
  synchronized metadata/cache pressure; and
- random temporary I/O still belongs closer to the process when possible.

The RCC design therefore tries to **shape I/O before scaling infrastructure**.
Storage technology matters, but access pattern usually matters first.

See [Class 14: efficient I/O](../course/class-14-efficient-io.md) and
[Class 15: storage architecture](../course/class-15-storage-architecture.md).

## Two workload classes have different scheduling needs

RCC deliberately separates two broad execution classes.

### Scientific jobs: Slurm + Apptainer

Scientific work is usually finite, resource-declared computation: batch jobs,
workflow tasks, interactive allocations, notebooks, GPU jobs, arrays, and
large-memory or other specialized jobs. Slurm already owns the queue, resource
allocation, accounting, cancellation, scheduling policy, and the relationship
between interactive and batch work.

Apptainer provides the container boundary used by scientific jobs without
requiring a Docker daemon or turning the container runtime into another
scheduler.

For these workloads the important questions include:

- how many CPUs, how much RAM, how long, and whether a GPU is required;
- which jobs are waiting and why;
- how shared capacity is scheduled fairly;
- how workflow tasks map onto allocations;
- how high-I/O work uses job-local scratch; and
- how the exact computation can be reproduced later.

Wrapping those jobs in a second general-purpose orchestrator would not remove
Slurm's responsibilities. It would usually add another scheduler that must be
kept consistent with them.

### Long-lived services: the RCC service plane

Web applications, databases, brokers, control services, and other processes that
should stay up for days, weeks, or months have a different lifecycle. They need
service placement, restart/health behavior, bounded network/service identities,
and controlled rollout rather than a scientific batch queue.

RCC uses **Nomad for parts of this service plane**. Service-side control
components can live on Nomad while user computation they request is still
submitted to Slurm. That preserves one compute authority for scientific work
instead of allowing a web service to become a second way to acquire cluster
resources.

## Why not replace Nomad with Kubernetes just because Kubernetes is popular?

Popularity is valuable: Kubernetes has a large ecosystem, strong tooling, and a
large operator community. But replacing a working service scheduler is not free.
RCC would gain another API surface, certificate/identity system, upgrade path,
networking model, policy layer, storage integration, monitoring surface, and
failure mode.

If Kubernetes-native capabilities solve a concrete RCC problem, that can be a
good trade. If they merely duplicate an existing service plane, they increase
operational complexity without changing what the researcher can accomplish.

The same principle applies in the other direction: Nomad is not used to replace
Slurm merely because RCC already operates Nomad.

## The important design rule: one authority per capability

RCC tries to avoid split authority.

- **Slurm** owns scientific compute allocation and accounting.
- **Nomad/service orchestration** owns the long-lived service workloads assigned
  to the RCC service plane.
- **RCC identity/project policy** decides who may request an action and for which
  project.
- **Storage systems** own their storage semantics rather than letting a scheduler
  invent a second source of truth.
- **Workflow and application design** is responsible for avoiding pathological
  I/O patterns that no backend can cheaply absorb.

A browser, workflow UI, agent, API, or service may request scientific compute,
but the request still becomes governed Slurm work. A convenient interface does
not create a parallel scheduler.

## Containers still provide portability

Using more than one scheduler does not mean every workload needs a different
software packaging model. Service containers can use the service plane, while
scientific software can be built/reviewed as container artifacts and executed
through Apptainer under Slurm. The goal is portability of software without
confusing portability with scheduling authority.

## When Kubernetes could make sense

RCC should reconsider Kubernetes when a concrete workload or upstream platform
requires Kubernetes-native capabilities that materially improve safety,
operability, or scientific usefulness—for example a mature supported operator or
service ecosystem that would otherwise have to be reimplemented.

The decision should compare the real benefit with the cost of adding or
replacing a control plane **and** with the I/O behavior of the workload. “It is
the popular platform” is useful input, but not sufficient architecture
justification by itself.

## What users should take away

Ordinary researchers should not need to know which service scheduler is behind a
button. Advanced users should know that the split is intentional:

```text
browser / workflow / agent request
             |
             +--> long-lived RCC service -> service plane
             |
             +--> scientific computation -> Slurm -> local scratch / project storage
```

RCC is trying to hide unnecessary infrastructure mechanics from the user while
keeping the underlying authority and I/O boundaries explicit and supportable.

See [What RCC can do](what-rcc-can-do.md),
[RCC services](rcc-services.md),
[How shared compute works](../reference/how-shared-compute-works.md), and the
[VS Code low-I/O defaults](../getting-started/vscode.md#rcc-safe-vs-code-defaults).