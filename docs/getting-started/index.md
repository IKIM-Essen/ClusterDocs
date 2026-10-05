# RCC Expedition Light: your first 15 minutes

This is the shortest route from a new computer to a safe RCC shell. You do not
need to understand the cluster before you begin.

Expedition Light is the required first-use path for new users. It deliberately
stops after safe access, the basic host and storage model, VS Code, and a small
Slurm check. The full RCC Expedition is optional deeper training and introduces
containers, Snakemake, and Nextflow later.

RCC is also preparing a browser-first experience for researchers who do not need
the command line. There are therefore two starting paths; today only Path A is
available.

## Path A — command-line access (current)

Use this path now. It gives you SSH, VS Code Remote SSH, direct Slurm commands,
workflow development, and automation.

| Computer | Follow this checklist |
|---|---|
| Current macOS | [Set up RCC on a Mac](macos.md) |
| Windows 11 | [Set up RCC on Windows](windows.md) |

Both checklists use the SSH client already supplied by the operating system.
Do not install a separate terminal, Linux virtual machine, or SSH program unless
the checklist shows that the built-in client is missing.

After terminal SSH works, follow [Use VS Code with RCC](vscode.md) for the
recommended day-to-day editor, terminal, Git, and remote-file interface.

## Path B — browser-first research (not yet released)

> **Service status — not yet released:** RCC Home, Files, and RCC Analysis
> Notebook/Workflow are not yet available. Use Path A until RCC announces them.

The intended journey is:

```text
RCC Home
   -> Files: upload or choose project data
   -> RCC Analysis: Notebook for interactive exploration
        or RCC Analysis: Workflow for repeatable analysis
   -> Files: inspect/download results
```

Once released, a browser-only account will be able to work without an SSH
public key. RCC web authentication and project membership remain the authority;
the browser service submits compute through the governed RCC/Slurm path on your
behalf.

## What most researchers should remember

1. **Your RCC account is your identity.** SSH is how you use RCC today; once
   the browser services are released, browser-only work will not require an
   SSH key.
2. **Files will be the browser data entry/exit surface** (not yet released).
   Durable project inputs and results belong in the project.
3. **RCC Analysis Notebook is for exploration.** It is planned as Jupyter in a
   bounded Slurm allocation without manual tunnels or worker selection.
4. **RCC Analysis Workflow is for repeatable work.** Long, repeated, unattended,
   or highly parallel analysis belongs in a governed workflow rather than an
   oversized notebook session.
5. **Slurm workers still do the computation.** Browser-first changes how you ask
   for compute, not where compute runs.

## The command-line connection model

The command-line connection model is:

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

Once released, Files and RCC Analysis should present authorized projects
directly, so browser users will not need to type these paths. The paths remain useful
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

- terminal SSH reaches the configured RCC target;
- VS Code reaches the same target if you use it;
- you know which project owns the work;
- a small Slurm test completes; and
- repeated analysis is recorded as code/workflow rather than remembered commands.

If you prefer guided, offline training, use
[RCC Expedition](../rcc-expedition.md). Returning users from the original IKIM
cluster should also read [what changed](what-changed.md).
