# RCC services: where should I go?

RCC is one research-computing environment with several user-facing surfaces. The
same RCC identity and project authorization follow you between them; choosing a
surface does not create a second account or a second copy of your project.

> **Release status matters (October 2026).** Today the supported routes are
> SSH through the jump host to the shell host, VS Code Remote SSH, Slurm on RCC
> workers, and this documentation site. The RCC browser services below — Home,
> Files, Admin / My RCC, the Assistant, and RCC Analysis (Notebook and
> Workflow) — are **not yet released**; their earlier internal pilot was
> withdrawn and RCC is re-establishing them in a staged rollout. A service
> described in ClusterDocs is not automatically released. Follow the status
> note on each service page.

## The short version

| Service | Use it when you want to... | Current documentation status |
|---|---|---|
| **SSH / VS Code** | work in a shell or editor and submit Slurm jobs | **ready now** |
| **Documentation** | learn RCC and look up procedures | **ready now** (this site) |
| **Home** | find RCC services and account entry points | **not yet released** |
| **Files** | upload, browse, or download approved project data in a browser | **not yet released**; use `scp`, `sftp`, or `rsync` to the shell host |
| **RCC Analysis** | explore data in a notebook or run a repeatable governed workflow | **not yet released** |
| **Assistant** | ask for explanations or bounded RCC help | **not yet released** |
| **Admin / My RCC** | manage your account, project membership, and authorized project actions | **not yet released**; RCC support handles requests |

Open OnDemand is retired from the current RCC product model. Do not use old OOD
screenshots or bookmarks as current connection instructions.

## Files: the browser data entry and exit point

When released, use **Files** when the task is primarily about project data:

- upload an input file;
- inspect project-facing folders;
- download a result; or
- move a bounded amount of data without opening a shell.

The intended browser-first journey is:

```text
Files -> RCC Analysis -> Files
          |       |
          |       +-> Workflows: repeatable/scalable analysis
          +----------> Notebooks: interactive exploration
```

Files is not a general server filesystem browser and it does not replace project
membership or data-release approval. Read
[RCC Files: browse and transfer project data](rcc-files.md).

## RCC Analysis: one product, two ways to compute

RCC Analysis is the planned user-facing compute product. It has two primary modes.

### Notebooks

Use **Notebooks** for interactive exploration, figures, Python/R analysis,
inspection of intermediate results, and bounded development. The planned default
is a browser Jupyter environment backed by a Slurm allocation. The user should
not have to create an SSH tunnel, choose a worker, expose a port, or know Slurm
syntax merely to open a notebook.

### Workflows

Use **Workflows** when the analysis should be repeatable, scalable, governed, or
run without keeping an interactive browser session open. RCC chooses the
operational execution plan and runs reviewed Nextflow/Snakemake tasks through
Slurm where appropriate.

A useful rule is:

```text
explore / inspect / prototype -> Analysis: Notebook
repeat / scale / reproduce    -> Analysis: Workflow
```

Moving from a notebook to a workflow should feel like changing mode inside one
analysis product, not switching to a different cluster product.

Read [RCC Analysis: notebooks and governed workflows](../analysis/rcc-analysis.md).
RCC Analysis is documented before activation and is not yet a live user service.

## What happened to “RCC Workbench”?

**Workbench remains an internal/advanced execution term, not a primary user
product.** It is the session-broker and interactive-compute machinery that can
place a notebook or advanced development environment on Slurm and attach the
browser safely.

For most researchers the visible action should be **Open notebook**, not “start
a Workbench session” or “open a web shell”. A browser shell may remain an
advanced interface for developers, but it should not dominate the normal
data-analysis path. RCC does not plan a browser-based VS Code IDE; use local
VS Code with Remote - SSH.

Read [Workbench execution layer](workbench-interfaces.md) only when you need the
advanced architecture and session-boundary explanation.

## Resource use is part of the product

A browser interface must not make inefficient computation easier to ignore.
RCC Analysis should steer work toward the right mode:

- keep interactive notebook allocations modest and reclaim idle sessions;
- do not reserve GPUs merely because they are available;
- move long or repeated work out of a notebook and into a workflow;
- avoid oversized CPU/RAM requests unsupported by measurement;
- batch tiny tasks when scheduler overhead dominates; and
- use job-local scratch when repeated shared-storage I/O would be wasteful.

RCC may use privacy-minimized accounting evidence to recommend a better resource
profile. Scientific data, commands, filenames, and notebook contents are not
required to decide that a job requested far more CPU, RAM, GPU, or idle time than
it used.

## Assistant: explain and help, not bypass policy

The RCC Assistant is **not yet released**. When enabled, it may explain documentation, help interpret failures, or support
bounded actions when those capabilities are enabled. It does not gain a second
identity, project access, or scheduler authority simply because the request is
made in natural language.

For coding-agent boundaries, read [RCC-internal coding agents](agents-and-mcp.md)
and [coding agents and your data](how-rcc-works.md).

## Admin / My RCC: identity and project governance

Admin / My RCC is **not yet released**; until it is, RCC support handles
account and membership requests. When released, use the account/project surface
for actions such as account security, project membership, and project-service
requests that your role is authorized to make. Finding an action in the
interface does not mean every user may execute it.

Once the browser services are released, a browser-only RCC account will not need
an SSH public key. Until then, SSH through the jump host is the supported way to
use RCC, so register an SSH public key with your account.

Read [Projects and supported actions](projects-and-capabilities.md) and
[How RCC authentication fits together](../reference/authentication-lifecycle.md).

## Supporting project/developer services

### Gitea: source code and software artifacts

Use RCC Gitea for code, workflow source, documentation, tests, and reviewed
software artifacts. Repository permissions remain separate from project data
membership, and secrets/research datasets do not belong in Git history.

Read [RCC Gitea: source control inside RCC](rcc-gitea.md).

### Managed DataLad: versioned large-dataset state

When enabled for a project, DataLad can bind dataset history/identity to an
RCC-managed storage provider without putting large content into ordinary Git.
DataLad service enablement does not imply public sharing or Coscine archival.

Read [Managed DataLad on RCC](../data/datalad-managed-service.md).

### Usage: approximate capacity/storage governance

Authorized RCC administrators/approvers may have a read-only Usage view showing
capacity, waiting demand, storage growth, inodes, and pressure signals. It is
approximate operational evidence, not billing or an entitlement system.

Read [RCC Usage reporting](../reference/usage-accounting.md).

## Two concepts follow you across every surface

### Your authentication method is not your authorization

RCC may use SSO/passkeys for web sign-in and SSH public keys for command-line
access. Those credentials prove who you are; they do not independently grant
project or administrator rights.

Read [How RCC authentication fits together](../reference/authentication-lifecycle.md).

### Project type changes the data-movement model

Current projects use the Regular project model. RCC also defines a future
Controlled Data Project type in which protected data cannot simply leave through
ordinary user transfer paths and results require a governed release boundary.
Controlled Data project runtime admission is not yet released.

Read [Regular and Controlled Data projects](project-types.md).

## One project, several interfaces

Changing interface does not change authorization:

```text
RCC identity
    + project membership / delegated role
    + project type / data and service policy
              |
              +--> Files
              +--> RCC Analysis
              |       +--> Notebook
              |       +--> Workflow
              +--> SSH / VS Code (current supported path)
              +--> Assistant
              +--> Admin
              +--> Gitea / DataLad when separately entitled
```

The interface changes **how you ask**. It does not change **what you are allowed
to access or do**.
