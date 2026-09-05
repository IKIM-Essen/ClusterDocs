# RCC Expedition Light: your first 15 minutes

RCC is moving toward a browser-first experience for researchers who do not need
the command line. You do **not** need to become an SSH user merely because you
have an RCC account.

There are therefore two legitimate starting paths.

## Path A — browser-first research

Use this path when the RCC Home page shows the required browser services as
enabled for your account/project.

The intended normal journey is:

```text
RCC Home
   -> Files: upload or choose project data
   -> RCC Analysis: Notebook for interactive exploration
        or RCC Analysis: Workflow for repeatable analysis
   -> Files: inspect/download results
```

A browser-first account can work without an SSH public key. RCC web
authentication and project membership remain the authority; the browser service
submits compute through the governed RCC/Slurm path on your behalf.

> **Current release note:** RCC Analysis Notebook/Workflow is documented before
> activation. Until the RCC landing page explicitly shows it as available, use
> Path B for compute and the current Files service where appropriate.

## Path B — command-line / developer access

Use this path when you need SSH, VS Code Remote SSH, direct Slurm commands,
workflow development, automation, or when browser Analysis has not yet been
activated.

| Computer | Follow this checklist |
|---|---|
| Current macOS | [Set up RCC on a Mac](macos.md) |
| Windows 11 | [Set up RCC on Windows](windows.md) |

Both checklists use the SSH client already supplied by the operating system.
Do not install a separate terminal, Linux virtual machine, or SSH program unless
the checklist shows that the built-in client is missing.

After terminal SSH works, follow [Use VS Code with RCC](vscode.md) when you need
the advanced editor/terminal/Git path.

## What most researchers should remember

1. **Your RCC account is your identity; SSH is optional.** Browser capabilities
   do not require an SSH key unless the service explicitly says so.
2. **Files is the browser data entry/exit surface.** Durable project inputs and
   results belong in the project.
3. **RCC Analysis Notebook is for exploration.** It is planned as Jupyter in a
   bounded Slurm allocation without manual tunnels or worker selection.
4. **RCC Analysis Workflow is for repeatable work.** Long, repeated, unattended,
   or highly parallel analysis belongs in a governed workflow rather than an
   oversized notebook session.
5. **Slurm workers still do the computation.** Browser-first changes how you ask
   for compute, not where compute runs.

## If you use the advanced SSH path

The command-line connection model remains:

```text
Mac or Windows
  -> jump host (automatic forwarding; no working shell)
  -> shell host (prepare and control work)
  -> Slurm allocation (perform computation)
```

You normally type only `ssh {{ ssh_target_alias }}`. The `ProxyJump` line in
your SSH configuration takes care of the middle step.

[Read the jump-host and shell-host explanation](../concepts/jump-shell-compute.md)
if you need the full command-line mental model.

## Where your work belongs

| What you have | Where it belongs |
|---|---|
| Personal settings and small private files | `/homes/<user>/` |
| Material only for your organizational group | `/groups/<primary-group>/` |
| Shared research data, code, and durable results | `/projects/<project>/` |
| Temporary, high-I/O files for one job | Job-local `/local` or `$TMPDIR` |

Browser users do not need to type these paths during normal work; Files and RCC
Analysis should present authorized projects directly. The paths remain useful
reference for developers and reproducibility documentation.

Your **primary group** records your organizational home. A **project** is the
research collaboration: it has the approved members, data, services, purpose,
and lifecycle. Add collaborators to the project; do not move them into another
primary group merely to share data.

## Turn exploration into reliable analysis

Do not keep an important analysis only in notebook state or shell history.
When interactive work becomes repeated, long-running, many-sample, or
provenance-critical, turn it into an RCC Analysis Workflow (when released) or
use the current [script-to-workflow guide](../paths/from-shell-scripts.md).

The resource rule is simple: **interactive notebooks should be modest and
attended; repeatable/scalable work should become workflows.** Requesting more
CPU, memory, GPU, or time is not a substitute for measuring what the analysis
actually uses.

## You are ready when

For the browser-first path:

- you can sign in to RCC without an SSH key;
- Files shows the correct project;
- you understand Notebook versus Workflow mode;
- you can save durable work back into the project; and
- you know that large/repeated work should leave the notebook path.

For the advanced SSH path:

- terminal SSH reaches the configured RCC target;
- VS Code reaches the same target if you use it;
- you know which project owns the work;
- a small Slurm test completes; and
- repeated analysis is recorded as code/workflow rather than remembered commands.

If you prefer guided, offline training, use
[RCC Expedition](../rcc-expedition.md). Returning users from the original IKIM
cluster should also read [what changed](what-changed.md).
