# RCC interfaces: where should I go?

RCC is one governed research environment with several interfaces. The same RCC
identity, project authorization, and policy follow you between them; choosing a
different interface does not create another account or another copy of the
project.

> **Release status matters.** A capability described in ClusterDocs is not
> automatically live. Staged services must be marked explicitly and RCC Home is
> the final user-facing source for what is enabled for your account/project.

## Choose by task

| I want to... | Start with | Status guidance |
|---|---|---|
| upload, browse, or download project data | **Files** | current user path |
| explore data interactively | **RCC Analysis · Notebook** | documented before activation |
| run a repeatable/scalable analysis | **RCC Analysis · Workflow** | documented before activation |
| manage my account or project membership/actions | **My RCC / Admin** | role-aware current surface |
| ask for explanations or bounded help | **Assistant** | availability depends on project/service |
| develop directly with shell/editor/scheduler tools | **SSH / VS Code / Slurm** | current advanced path |
| understand the platform beyond the front door | **What RCC can do** | capability and status overview |

Open OnDemand is retired from the current RCC product model. Do not use old OOD
screenshots or bookmarks as current instructions.

## Files: project data in the browser

Use **Files** to upload inputs, browse authorized project-facing data, and
download results without opening a shell. Files does not bypass project
membership, data approval, retention, or sharing policy.

Read [RCC Files](rcc-files.md).

## RCC Analysis: Notebook and Workflow

RCC Analysis is the planned user-facing compute product.

Use **Notebook** for bounded interactive exploration, Python/R analysis, figures,
inspection, prototyping, and small-scale debugging. The intended default is
Jupyter in the browser backed by a bounded Slurm allocation; ordinary users
should not have to choose workers, create tunnels, expose ports, or know Slurm
syntax merely to open a notebook.

Use **Workflow** when the analysis should be repeatable, scalable, governed, or
run without keeping a browser session open. RCC can run reviewed
Nextflow/Snakemake tasks through Slurm while keeping scientific inputs,
parameters, expected outputs, and provenance visible to the researcher.

Move repeated, long, many-sample, highly parallel, or official project work from
Notebook into Workflow mode rather than growing an interactive session without
bounds.

Read [RCC Analysis: notebooks and governed workflows](../analysis/rcc-analysis.md).
RCC Analysis is documented before activation and is not yet a live user service.

## Assistant and agents: help without a policy bypass

The RCC Assistant and coding agents may explain documentation, help interpret
failures, design code/workflows, work from synthetic fixtures, and support
bounded actions when enabled. Natural language does not create a new identity or
new authority.

The preferred external/general-purpose agent pattern is **data-blind by
default**: keep real protected project data inside RCC, give the agent only the
minimum non-sensitive context needed to develop or debug the analysis, and let
RCC execute the resulting workflow against the real data.

Read [AI and coding agents without exposing project data](agents-and-mcp.md).

## My RCC / Admin: self-governance and delegation

Use the account/project surface for account security, membership, invitations,
approvals, delegated project capabilities, and project-service requests your
role is authorized to make. Self-service and administrative functions can share
a platform without implying that every user has administrator authority.

A browser-first account does **not** require an SSH public key.

Read [Projects and supported actions](projects-and-capabilities.md) and
[authentication lifecycle](../reference/authentication-lifecycle.md).

## Advanced technical access

SSH, VS Code, direct Slurm, containers, Gitea, workflow engines, and lower-level
storage interfaces remain first-class advanced tools. They are important for
software developers, workflow authors, automation, diagnostics, unusual resource
requirements, and researchers who want direct control.

They should not be a prerequisite for a user whose task is simply to move data,
run an approved analysis, inspect results, or manage project membership.

## Project and developer services

RCC can expose project-scoped supporting services such as Gitea, DataLad-backed
large-data state, object/S3 storage where enabled, databases, protected project
services, usage/capacity views, instrument-ingestion paths, and lifecycle
services. Each remains separately governed and may have a different release
status.

Read [What RCC can do](what-rcc-can-do.md) for the end-to-end platform view.

## One project, several interfaces

For advanced readers, the authority model is:

```text
RCC identity
    + project membership / delegated role
    + project type / data and service policy
              |
              +--> Files
              +--> Analysis: Notebook / Workflow
              +--> Assistant / agent capabilities
              +--> My RCC / Admin
              +--> SSH / VS Code / Slurm
              +--> project services such as Gitea, DataLad, S3
```

The interface changes **how you ask**. It does not change **what you are allowed
to access or do**.
