# Start here: your first 15 minutes

Start with the research task you need to complete. You do **not** need an SSH key
or command-line expertise merely because you have an RCC account.

> **Release-candidate note:** ClusterDocs 3 will not be published until the core
> browser bundle—**RCC Home, Files, RCC Analysis, My RCC, and RCC Admin**—is ready
> and accepted together. RCC Analysis is part of the minimum release, not a later
> enhancement.

## Browser-first research

The ordinary ClusterDocs 3 path is:

| Step | What you do | What RCC handles |
|---|---|---|
| 1 | Open **RCC Home**, sign in, and choose the project/service | identity, project authorization, service discovery |
| 2 | Open **Files** and choose/upload approved data | governed project data access |
| 3 | Open **RCC Analysis**: Notebook to explore or Workflow to repeat/scale | Slurm placement, session/workflow execution, resource controls |
| 4 | Save durable results and open them in **Files** | project result location and provenance |
| 5 | Use **My RCC** for personal/project self-service | account preferences, membership/invitation context, permitted self-service |
| 6 | Use **RCC Admin** only when your role provides approval/admin capabilities | role-gated approvals and administration |

A browser-first account can work without an SSH public key. Browser services use
RCC web authentication and project membership; compute still runs through the
governed RCC execution path behind the interface.

The release candidate remains blocked until this entire path can be completed
against the deployed services. A successful Files or SSH path alone is not
sufficient release evidence.

### Notebook or Workflow?

Use **Notebook** for attended exploration, visualization, statistics, prototyping,
and bounded interactive analysis. Use **Workflow** when work is repeated,
long-running, many-sample, unattended, provenance-critical, or needs to scale.

Interactive convenience does not make compute free: start modestly, avoid idle
GPU/CPU reservations, and move repeatable work into a workflow.

## Advanced compute path

Use the advanced path when you need SSH, VS Code Remote SSH, direct Slurm
commands, workflow development/automation, or lower-level diagnostics.

| Computer | Follow this checklist |
|---|---|
| Current macOS | [Set up RCC on a Mac](macos.md) |
| Windows 11 | [Set up RCC on Windows](windows.md) |

After terminal SSH works, use [VS Code with RCC](vscode.md) if you need the
advanced editor, terminal, Git, and remote-file workflow.

### Optional technical model

Advanced users may find the connection model useful:

```text
Mac or Windows
  -> jump host (automatic forwarding; no working shell)
  -> shell host (prepare and control work)
  -> Slurm allocation (perform computation)
```

You normally type only `ssh {{ ssh_target_alias }}`. `ProxyJump` handles the
gateway. The jump host is not a workstation and compute does not belong on the
shell host.

Read [jump host, shell host, and workers](../concepts/jump-shell-compute.md) only
when you need that model.

## What most researchers should remember

1. **Your account is your identity; SSH is optional.**
2. **The project is the research boundary.** People, data, compute, services,
   results, and lifecycle decisions stay connected to it.
3. **RCC Home is the browser front door.**
4. **Files is the browser entry/exit surface for project data.**
5. **Notebook is for exploration; Workflow is for repeatable/scalable work.**
6. **My RCC is self-service; RCC Admin is role-gated administration.**
7. **Agents can help without receiving the dataset.** Prefer documentation,
   schemas, synthetic fixtures, public code, and bounded diagnostics; let RCC
   execute against real data inside the governed boundary.
8. **Advanced controls remain available.** SSH, VS Code, Slurm, containers, and
   direct workflow tooling are there when the research or development task needs
   them.

## Where data belongs

Browser users normally choose a project rather than type cluster paths. For the
advanced path, the underlying locations remain important:

| What you have | Where it belongs |
|---|---|
| Personal settings and small private files | `/homes/<user>/` |
| Material only for your organizational group | `/groups/<primary-group>/` |
| Shared research data, code, and durable results | `/projects/<project>/` |
| Temporary, high-I/O files for one job | Job-local `/local` or `$TMPDIR` |

Your primary group records your organizational home. A project is the research
collaboration. Add collaborators to the project rather than changing primary
group membership merely to share research data.

## You are ready when

For the browser-first release path:

- RCC Home opens and exposes the correct role/project-aware services;
- you can sign in without enrolling an SSH key;
- Files shows the correct project and can hand selected data into the analysis
  journey;
- RCC Analysis Notebook and Workflow both operate through governed Slurm-backed
  execution;
- durable results return to the project and are visible through Files;
- My RCC exposes only the user's self-service actions;
- RCC Admin exposes additional actions only to authorized roles; and
- you know where to ask for help without exporting protected research data.

For advanced access:

- SSH reaches the configured RCC target;
- VS Code reaches the same target if you use it;
- you know which project owns the work;
- a small Slurm test completes; and
- repeated analysis is recorded as code/workflow rather than remembered commands.

For the complete platform picture, read [What RCC can do](../concepts/what-rcc-can-do.md).
Returning users from the original IKIM cluster should also read
[what changed](what-changed.md).

Prefer guided, self-contained training? Use [RCC Expedition](../rcc-expedition.md).
