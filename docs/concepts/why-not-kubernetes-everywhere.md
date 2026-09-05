# Why RCC does not run everything on Kubernetes

Experienced infrastructure users often ask why RCC does not simply put every
service and scientific workload onto Kubernetes. The short answer is: **RCC uses
the scheduler that owns each problem rather than forcing one orchestration model
onto every workload.**

This is not an argument that Kubernetes is bad. Kubernetes is an excellent and
widely used platform for many service workloads. RCC's design question is
whether introducing it as the universal execution authority would improve the
research platform enough to justify another control plane and another scheduling
translation layer.

## Two workload classes have different needs

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

For these workloads the important questions are things such as:

- how many CPUs, how much RAM, how long, and whether a GPU is required;
- which jobs are waiting and why;
- how shared capacity is scheduled fairly;
- how workflow tasks map onto allocations;
- how high-I/O work uses job-local scratch; and
- how the exact computation can be reproduced later.

Wrapping those jobs in a second general-purpose orchestrator would not remove
Slurm's responsibilities. It would usually add another scheduler that has to be
kept consistent with them.

### Long-lived services: the RCC service plane

Web applications, databases, brokers, control services, and other processes that
should stay up for days, weeks, or months have a different lifecycle. They need
service placement, restart/health behavior, bounded network/service identities,
and controlled rollout rather than a scientific batch queue.

RCC uses **Nomad for parts of this service plane**. For example, service-side
control components can live on Nomad while the user computation they request is
still submitted to Slurm. That preserves one compute authority for scientific
work instead of allowing a web service to become a second way to acquire cluster
resources.

## Why not replace Nomad with Kubernetes just because Kubernetes is popular?

Popularity is valuable: Kubernetes has a large ecosystem, strong tooling, and a
large operator community. But replacing a working service scheduler is not free.
RCC would gain another API surface, certificate/identity system, upgrade path,
networking model, policy layer, storage integration, monitoring surface, and
failure mode. If those capabilities solve a concrete RCC problem, that can be a
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

The decision should then compare the real benefit with the cost of adding or
replacing a control plane. “Kubernetes is the popular platform” is useful input,
but not sufficient architecture justification by itself.

## What users should take away

Ordinary researchers should not need to know which service scheduler is behind a
button. Advanced users should know that the split is intentional:

```text
browser / workflow / agent request
             |
             +--> long-lived RCC service -> service plane
             |
             +--> scientific computation -> Slurm -> Apptainer/job runtime
```

RCC is trying to hide unnecessary infrastructure mechanics from the user while
keeping the underlying authority boundaries explicit and supportable.

See [What RCC can do](what-rcc-can-do.md),
[RCC services](rcc-services.md), and
[How shared compute works](../reference/how-shared-compute-works.md).
