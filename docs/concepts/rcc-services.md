# RCC services: where should I go?

RCC is one research-computing environment with several user-facing surfaces. The
same RCC identity and project authorization follow you between them; choosing a
surface does not create a second account or a second copy of your project.

> **Release status matters.** RCC Analysis and its browser notebook mode are
> documented before user activation. A service described in ClusterDocs is not
> automatically released. Follow the status note on the service page and the
> current RCC landing page.

## The short version

| Service | Use it when you want to... | Current documentation status |
|---|---|---|
| **Home** | find RCC services and account entry points | current RCC surface |
| **Files** | upload, browse, or download approved project data | current user path |
| **RCC Analysis** | explore data in a notebook or run a repeatable governed workflow | **not yet released** |
| **Documentation** | learn RCC and look up procedures | current user path |
| **Assistant** | ask for explanations or bounded RCC help | availability depends on the current RCC service/project |
| **Admin / My RCC** | manage your account, project membership, and authorized project actions | current RCC surface |
| **SSH / VS Code** | use an advanced command-line or development path | current advanced path |

Open OnDemand is retired from the current RCC product model. Do not use old OOD
screenshots or bookmarks as current connection instructions.

## Files: the browser data entry and exit point

Use **Files** when the task is primarily about project data:

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
a Workbench session” or “open a web shell”. A shell or VS Code-style browser IDE
may remain an advanced interface for developers, but it should not dominate the
normal data-analysis path.

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

The RCC Assistant may explain documentation, help interpret failures, or support
bounded actions when those capabilities are enabled. It does not gain a second
identity, project access, or scheduler authority simply because the request is
made in natural language.

For coding-agent boundaries, read [RCC-internal coding agents](agents-and-mcp.md)
and [coding agents and your data](how-rcc-works.md).

## Admin / My RCC: identity and project governance

Use the account/project surface for actions such as account security, project
membership, and project-service requests that your role is authorized to make.
A browser-first RCC account does **not** require an SSH public key. SSH is an
optional credential for users who need the command-line path.

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
              +--> SSH / VS Code (optional advanced capability)
              +--> Assistant
              +--> Admin
              +--> Gitea / DataLad when separately entitled
```

The interface changes **how you ask**. It does not change **what you are allowed
to access or do**.
