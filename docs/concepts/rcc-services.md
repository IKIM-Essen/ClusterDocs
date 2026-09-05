# RCC interfaces: where should I go?

RCC is one governed research environment with several interfaces. The same RCC
identity, project authorization, and policy follow you between them; choosing a
different interface does not create another account or another copy of the
project.

> **ClusterDocs 3 release boundary:** the new documentation will not be
> published before **RCC Home, Files, RCC Analysis, My RCC, and RCC Admin** are
> ready as one integrated browser experience. RCC Analysis is therefore a core
> release requirement, not a post-release feature.

## The five core browser surfaces

| Surface | User purpose | Release role |
|---|---|---|
| **RCC Home** | discover the RCC services enabled for your account/project | required for ClusterDocs 3 release |
| **Files** | upload, browse, select, and download project data | required for ClusterDocs 3 release |
| **RCC Analysis** | Notebook exploration and governed Workflow execution | required for ClusterDocs 3 release; currently the blocking surface |
| **My RCC** | personal account, preferences, memberships, invitations, and self-service actions | required for ClusterDocs 3 release |
| **RCC Admin** | approvals, delegated administration, and role-authorized administrative actions | required for ClusterDocs 3 release |

The user-facing distinction between **My RCC** and **RCC Admin** is authority,
not necessarily a different backend host. A normal user should see only the
self-service actions they are allowed to perform; approvers and administrators
receive additional bounded capabilities.

## The core research path

For ordinary research the intended path is:

```text
RCC Home
   -> choose project/service
   -> Files -> RCC Analysis Notebook/Workflow -> Files/results
   -> My RCC for personal/project self-service
   -> RCC Admin only when the user's role authorizes administrative actions
```

A browser-first account does **not** require an SSH public key. Slurm remains the
scientific-compute authority underneath RCC Analysis.

## Files: project data in the browser

Use **Files** to upload inputs, browse authorized project-facing data, select
inputs for analysis, and download results without opening a shell. Files does
not bypass project membership, data approval, retention, or sharing policy.

Read [RCC Files](rcc-files.md).

## RCC Analysis: Notebook and Workflow

RCC Analysis is the user-facing compute product required for the ClusterDocs 3
release.

Use **Notebook** for bounded interactive exploration, Python/R analysis, figures,
inspection, prototyping, and small-scale debugging. The default should be
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
The current release candidate remains blocked until this path is ready and its
integration with Home, Files, My RCC, and RCC Admin has passed acceptance.

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

## My RCC: self-service

My RCC is the user's personal/account/project surface. It covers the actions that
do not require broad infrastructure administration, including account settings,
project membership context, invitations, notification preferences, and other
self-service actions enabled for the user's role.

The exact set of actions remains capability-checked. Seeing an action in the UI
does not create authority to perform it.

## RCC Admin: role-aware administration

RCC Admin supports approvers, delegates, and administrators with the additional
actions their roles permit: approvals, invitations/sponsorship, delegated
project actions, and other bounded administrative workflows.

RCC Admin must not imply that every authenticated user is an administrator.
My RCC and RCC Admin may share identity and infrastructure while presenting
different capability surfaces.

Read [Projects and supported actions](projects-and-capabilities.md) and
[authentication lifecycle](../reference/authentication-lifecycle.md).

## Advanced technical access

SSH, VS Code, direct Slurm, containers, Gitea, workflow engines, and lower-level
storage interfaces remain first-class advanced tools. They are important for
software developers, workflow authors, automation, diagnostics, unusual resource
requirements, and researchers who want direct control.

They are not the ordinary browser entrance path once the integrated release is
ready.

## Separately staged services

Other RCC capabilities may remain independently staged even when the five-surface
browser bundle releases. Examples include protected project vhosts, selected
vendor integrations such as Ardia, and the RCC-to-Coscine self-service transfer
path. Their pages must continue to carry their own release status.

## One project, several interfaces

For advanced readers, the authority model is:

```text
RCC identity
    + project membership / delegated role
    + project type / data and service policy
              |
              +--> RCC Home
              +--> Files
              +--> Analysis: Notebook / Workflow
              +--> My RCC
              +--> RCC Admin (role-gated)
              +--> Assistant / agent capabilities
              +--> SSH / VS Code / Slurm
              +--> project services such as Gitea, DataLad, S3
```

The interface changes **how you ask**. It does not change **what you are allowed
to access or do**.
