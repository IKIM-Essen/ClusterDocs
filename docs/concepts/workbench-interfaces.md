# RCC Workbench: interactive computing on RCC

> **Service status:** RCC Workbench is **not yet released to users**. This page
> documents the intended interactive-computing model while the existing SSH,
> VS Code, notebook, and Slurm routes remain the supported paths.

RCC Workbench is the interactive side of RCC. Use it when you want a working
session in which to explore data, edit code, use a shell or notebook, develop a
workflow, or debug a problem before turning it into a repeatable production
analysis.

The important idea is simple:

> **Workbench gives you an interactive environment. Slurm still runs substantial
> computation.**

A Workbench session does not create a new identity or a new project boundary.
It uses your RCC identity and the project access you already have.

## Workbench or RCC Analysis?

| | RCC Workbench | RCC Analysis |
|---|---|---|
| Main question | “Give me an interactive environment.” | “Run this analysis.” |
| Best for | Exploration, coding, debugging, notebooks | Repeatable governed scientific workflows |
| You control | What you do interactively | Data, workflow, scientific parameters |
| RCC controls | Secure session placement and attachment | Operational execution and task placement |
| Typical output | Files and code you create | Governed run, typed results, provenance |

A common lifecycle is:

```text
Workbench
  explore -> develop -> test -> debug
                         |
                         v
                    RCC Analysis
              repeat -> govern -> reproduce
```

Read [RCC Analysis: from data to a reproducible run](../analysis/rcc-analysis.md)
for the planned production-workflow path.

## What a Workbench session is

A Workbench session is an RCC-managed interactive session associated with your
user identity. Depending on the released interface, it may provide a shell,
notebook, or development environment such as VS Code.

The browser-facing control layer is not the compute worker itself. RCC brokers
the session, Slurm places the actual interactive work on an allowed worker, and
the browser attaches to that session through a bounded authenticated path.

You should not need to choose a physical worker or manually expose a port.

## What you should use Workbench for

Workbench is well suited to:

- inspecting a small part of a dataset;
- writing and reviewing scripts;
- using Python or R notebooks;
- developing or adapting Nextflow/Snakemake workflows;
- testing on a small example;
- examining logs and failed outputs;
- preparing a larger Slurm job; and
- deciding whether a workflow is ready for repeatable RCC Analysis execution.

It is not intended to make a long-running calculation happen inside the browser
process itself.

## Project access does not widen in Workbench

Your session receives only the project access admitted for your RCC identity.
Opening Workbench does not:

- add you to another project;
- make another user's session visible;
- turn a Regular project into a Controlled Data environment;
- grant a scheduler reservation or priority; or
- authorize data export.

If a project is not visible to your ordinary RCC account, Workbench is not a
workaround for that restriction.

## Sessions belong to one user

Workbench sessions are owner-scoped. A user should see and control their own
sessions, not another researcher's sessions. RCC may also limit the number of
simultaneous non-terminal sessions per user so abandoned browser tabs cannot
consume unbounded shared capacity.

When a session ends, durable results belong in project storage. Worker-local
scratch is temporary and should not be treated as the authoritative result
location.

## Browser reconnects are attachments, not permanent authority

The browser connection to a running workspace is deliberately bounded. A stale
browser cookie or old tab should not become indefinite permission to reattach to
compute.

In practice this means you may occasionally be asked to authenticate again when
reconnecting. That is expected security behavior, not evidence that the Slurm
job or project data disappeared.

## Where the computation actually runs

Substantial interactive computation still runs through Slurm. Workbench is a
safe way to request and attach to that allocation; it is not an alternative
scheduler.

The model is:

```text
browser / Workbench control
           |
           v
      RCC session broker
           |
           v
         Slurm
           |
           v
     approved RCC worker
```

Use [Class 5: Slurm](../course/class-05-slurm.md) when you need to understand
resource requests, queues, or batch execution.

## Existing interfaces remain valid

Until Workbench is released, use the current interfaces documented by RCC:

### VS Code

Use VS Code with the approved Remote SSH configuration when you are developing
scripts or working with a repository. Larger calculations still belong on RCC
workers.

### SSH

Use SSH for command-line work and automation. Follow the current two-hop RCC
configuration; the public login gateway is forwarding-only.

### Notebooks

Use the documented Python/R notebook workflow and submit substantial computation
to workers rather than treating the login environment as a compute node.

### RCC-internal coding agent

When available for your project, an RCC-internal coding agent can help prepare
code, submit bounded work, explain failures, and organize results under the same
project authorization. It does not become an administrator.

Read [RCC-internal coding agents](agents-and-mcp.md) for the data and authority
boundary.

## One simple rule

Use an interactive interface for **exploring, editing, understanding, and
starting work**. Use RCC workers for substantial computation. Keep durable
inputs and final results in the project rather than on temporary worker disk.

For the wider service map, read [RCC services: where should I go?](rcc-services.md).
New users can start with [RCC Expedition](../rcc-expedition.md).
