# RCC services: where should I go?

RCC is one research-computing environment with several user-facing surfaces. The
same RCC identity and project authorization follow you between them; choosing a
surface does not create a second account or a second copy of your project.

> **Release status matters.** Some services below are available now, while
> Workbench and RCC Analysis are documented before user activation. A service
> described in ClusterDocs is not automatically released. Follow the status note
> on the service page and the current RCC landing page.

## The short version

| Service | Use it when you want to... | Current documentation status |
|---|---|---|
| **Home** | find RCC services and account entry points | current RCC surface |
| **Files** | browse or transfer approved project data | current user path |
| **Documentation** | learn RCC and look up procedures | current user path |
| **Workbench** | get an interactive shell, notebook, or development session | **not yet released** |
| **Assistant** | ask for explanations or bounded RCC help | availability depends on the current RCC service/project |
| **Admin / My RCC** | manage your account, project membership, and authorized project actions | current RCC surface |
| **RCC Analysis** | run a repeatable governed scientific workflow | **not yet released; RCC 23 product** |

Open OnDemand is retired from the current RCC product model. Do not use old OOD
screenshots or bookmarks as current connection instructions.

## Files: move and inspect project data

Use **Files** when the task is primarily about data movement or browsing:

- upload or download an approved project file;
- inspect the project-facing file tree exposed by the service;
- perform a bounded transfer without opening a shell.

Files is not a general server filesystem browser and it does not replace project
membership or data-release approval. For larger or specialized transfers, use
the route documented in [Storage and transfer](../reference/storage-transfer.md).

## Workbench: interactive work

Use **Workbench** when you need an interactive environment to explore, edit,
develop, or debug. The intended interfaces include shells, notebooks, and
VS Code-style development sessions, while substantial computation still runs on
RCC workers through Slurm.

A Workbench session does not grant extra project access. It runs under your RCC
identity and project authorization.

Read [Where you can work with RCC](workbench-interfaces.md) for the complete
Workbench model and current release status.

## RCC Analysis: repeatable scientific execution

Use **RCC Analysis** when the task is already a defined scientific workflow with
known inputs, parameters, outputs, and provenance requirements. RCC Analysis
compiles the scientific request into a deployment-appropriate execution plan and
runs it through Slurm using Nextflow or Snakemake where appropriate.

A useful rule is:

```text
explore / develop / debug  -> Workbench
repeat / govern / reproduce -> RCC Analysis
```

Read [RCC Analysis: from data to a reproducible run](../analysis/rcc-analysis.md).
RCC Analysis is documented before activation and is not yet a live user service.

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
Finding an action in the interface does not mean every user may execute it.

Read [Projects and supported actions](projects-and-capabilities.md) for the
plain-language capability model.

## One project, several interfaces

Moving between Files, Workbench, Analysis, the Assistant, SSH, and Admin should
not change the fundamental authorization model:

```text
RCC identity
    + project membership / delegated role
    + data and service policy
              |
              +--> Files
              +--> Workbench
              +--> Analysis
              +--> SSH / VS Code
              +--> Assistant
              +--> Admin
```

The interface changes **how you ask**. It does not change **what you are allowed
to access or do**.
