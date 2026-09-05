# Start here: your first 15 minutes

Start with the research task you need to complete. You do **not** need an SSH key
or command-line expertise merely because you have an RCC account.

## Browser-first research

Use the browser-first path when RCC Home shows the required services as enabled
for your account and project.

| Step | What you do | What RCC handles |
|---|---|---|
| 1 | Sign in and choose the project | identity and project authorization |
| 2 | Open **Files** and choose/upload approved data | governed project access |
| 3 | Open **RCC Analysis**: Notebook to explore or Workflow to repeat/scale | Slurm placement, session/workflow execution, resource controls |
| 4 | Save durable results and open them in Files | project result location and provenance |

A browser-first account can work without an SSH public key. Browser services use
RCC web authentication and project membership; compute still runs through the
governed RCC execution path behind the interface.

> **Current release note:** RCC Analysis Notebook/Workflow is documented before
> activation. Until RCC Home explicitly shows it as available, use the current
> Files service for data tasks and the advanced/current compute path below.

### Notebook or Workflow?

Use **Notebook** for attended exploration, visualization, statistics, prototyping,
and bounded interactive analysis. Use **Workflow** when work is repeated,
long-running, many-sample, unattended, provenance-critical, or needs to scale.

Interactive convenience does not make compute free: start modestly, avoid idle
GPU/CPU reservations, and move repeatable work into a workflow.

## Advanced/current compute path

Use this path when you need SSH, VS Code Remote SSH, direct Slurm commands,
workflow development/automation, or when browser Analysis has not yet been
activated.

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
3. **Files is the normal browser entry/exit surface for project data.**
4. **Notebook is for exploration; Workflow is for repeatable/scalable work.**
5. **Agents can help without receiving the dataset.** Prefer documentation,
   schemas, synthetic fixtures, public code, and bounded diagnostics; let RCC
   execute against real data inside the governed boundary.
6. **Advanced controls remain available.** SSH, VS Code, Slurm, containers, and
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

For browser-first research:

- you can sign in without enrolling an SSH key;
- Files shows the correct project;
- you can explain Notebook versus Workflow mode;
- you know how durable work returns to the project; and
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
