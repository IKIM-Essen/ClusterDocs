# Workbench execution layer behind RCC Analysis

> **Service status:** the browser Notebook path is **not yet released to users**.
> This page documents the staged execution/security model. For the planned
> user-facing product, start with
> [RCC Analysis: notebooks and governed workflows](../analysis/rcc-analysis.md).

“RCC Workbench” remains an internal engineering term, not a separate primary
researcher product. It is the execution/session machinery that turns an
authenticated RCC Analysis Notebook request into a bounded Slurm-backed Jupyter
session.

For the normal user, the intended action is:

```text
RCC Analysis -> Notebook -> Open notebook
```

not:

```text
choose Workbench -> start web shell -> understand Slurm session details
```

RCC does **not** plan to provide a browser IDE as part of this release. Developers
who need a full IDE can continue to use a local editor such as VS Code through
the separately governed SSH path. A terminal may be available from JupyterLab as
an advanced tool, but it runs inside the same Notebook allocation and does not
create a second login, worker route, or security class.

## What the execution layer does

The retained Workbench machinery:

- accepts an authenticated RCC user and authorized project;
- selects a bounded RCC-owned Notebook resource profile;
- creates a Slurm allocation under that user's governed authority;
- starts Jupyter inside the allocation;
- puts the Jupyter server, kernels, subprocesses, and terminal in the same
  networkless user/PID namespace;
- exposes Jupyter only through a private mode-0600 job Unix socket;
- uses a separate per-job outbound mTLS agent as the browser transport;
- keeps the private Jupyter token out of the browser-facing management plane;
- records/reconciles session state; and
- stops or reclaims sessions according to policy.

It does not create a new RCC identity, widen project membership, grant generic
scheduler authority, or turn a Regular project into a Controlled Data
environment.

## Jupyter is arbitrary code, not the sandbox

Jupyter notebooks, Python/R kernels, subprocesses, and Jupyter terminals can all
execute arbitrary code as the authenticated user. Hiding a terminal would not
turn Jupyter into a security sandbox.

The security boundary is therefore the RCC execution environment around
Jupyter: Unix identity and project permissions, the constrained Slurm
allocation, network/user/PID isolation, the private Unix socket, authenticated
proxy/agent transport, and fresh project authorization checks.

The staged configuration also keeps XSRF protection enabled, disables remote
Jupyter listening, and keeps the Jupyter extension manager read-only. Runtime
extension/package mutation is not part of the accepted release path.

## Canonical Analysis route

The planned researcher-facing management origin is
`analysis.ikim.uk-essen.de`. Workflow remains at the Analysis root and Notebook
management is namespaced below `/notebook/`.

That does **not** mean the staged URL is live today. Publication remains an
explicit deployment gate. The Notebook management router is intentionally
narrow: it may proxy the Notebook launcher/static/API surface, but Jupyter
workspace/session traffic remains on the separately hardened workspace origin.

The Analysis-to-Notebook management hop also uses its own mTLS client identity.
Disabling that capability removes its credential and system-service drop-in;
Workflow does not need to acquire Notebook-broker authority merely because both
modes share one product page.

## When a notebook should become a workflow

Interactive convenience must not turn into poor cluster use. Notebook is for
exploration and bounded attended computation. Move work to **RCC Analysis ->
Workflow** when it becomes long-running, unattended, repeated across samples,
many-task, resource-intensive, provenance-critical, or something another
researcher should rerun reliably.

```text
Files -> Analysis: Notebook -> explore / prototype
                           |
                           +-> Analysis: Workflow -> repeat / scale / reproduce
                                                      |
                                                      +-> Files: results
```

## Resource guardrails

Interactive sessions are deliberately conservative by default. RCC selects the
normal Notebook profile; browser users do not choose partitions, CPU/RAM/GPU
amounts, walltime, or arbitrary scheduler options. Idle sessions are reclaimed,
concurrency is bounded, and repeated/scalable work should move to Workflow.

RCC can use privacy-minimized scheduler/accounting evidence such as allocated
versus used CPU, requested versus peak memory, GPU utilization where available,
idle duration, aggregate I/O where defensible, and terminal state. Notebook
contents, terminal commands, research filenames, and patient-related data are
not required for ordinary right-sizing.

## Where computation actually runs

```text
RCC Analysis browser
        |
        v
Notebook management broker (internal Workbench machinery)
        |
        v
      Slurm
        |
        v
approved RCC worker
        |
        +-> JupyterLab + optional Jupyter terminal
              inside one isolated allocation
```

The interactive runtime is not a replacement scheduler and the browser never
receives Slurm signing credentials.

## Existing interfaces remain valid

Until RCC Analysis Notebook is explicitly activated, follow the current released
guidance:

- [Class 9: Python notebooks](../course/class-09-python-notebooks.md) for the
  current Jupyter-through-Slurm/tunnel procedure;
- [VS Code with RCC](../getting-started/vscode.md) for current Remote SSH
  development; and
- [Class 5: Slurm](../course/class-05-slurm.md) for current direct scheduler use.

Those remain advanced alternatives after browser notebooks arrive; they simply
stop being prerequisites for ordinary researchers.
