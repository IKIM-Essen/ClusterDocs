# RCC Expedition Light: your first 15 minutes

This is the shortest route from a new computer to a safe RCC shell. You do not
need to understand the cluster before you begin.

Need an account first? Enrollment is currently an **invite-only pilot**. Follow
[Request and activate an RCC account](account-enrollment.md) before this
connection checklist.

Expedition Light is the required first-use path for new users. It deliberately
stops after safe access, the basic host and storage model, VS Code, and a small
Slurm check. The full RCC Expedition is optional deeper training and introduces
containers, Snakemake, and Nextflow later.

## Choose your computer

| Computer | Follow this checklist |
|---|---|
| Current macOS | [Set up RCC on a Mac](macos.md) |
| Windows 11 | [Set up RCC on Windows](windows.md) |

Both checklists use the SSH client already supplied by the operating system.
Do not install a separate terminal, Linux virtual machine, or SSH program
unless the checklist shows that the built-in client is missing.

After terminal SSH works, follow [Use VS Code with RCC](vscode.md) for the
recommended day-to-day editor, terminal, Git, and remote-file interface.

If you prefer guided, offline training, use
[RCC Expedition](../rcc-expedition.md). You can open the course directly after
extracting it; installing its optional Desktop shortcut is not required.

Already used the original IKIM cluster? Read
[what changed from the old ClusterDocs](what-changed.md) before reusing a saved
SSH configuration, storage habit, or submission script.

## The four things to remember

1. **Your computer starts the connection.** Your private SSH key stays there.
2. **The jump host is the guarded doorway.** SSH crosses it automatically; it
   is not a computer where you work.
3. **The shell host is your RCC desk.** You edit small files, use Git, prepare
   jobs, and start workflow controllers there.
4. **Slurm workers do the computation.** Submit analysis rather than running it
   in the shell-host terminal.

The normal connection therefore looks like this:

```text
Mac or Windows
  -> jump host (automatic forwarding; no working shell)
  -> shell host (prepare and control work)
  -> Slurm allocation (perform computation)
```

You normally type only `ssh {{ ssh_target_alias }}`. The `ProxyJump` line in
your SSH configuration takes care of the middle step.

[Read the jump-host and shell-host explanation](../concepts/jump-shell-compute.md)
if you want the full mental model.

## Where your work belongs

| What you have | Where it belongs |
|---|---|
| Personal settings and small private files | `/homes/<user>/` |
| Material only for your organizational group | `/groups/<primary-group>/` |
| Shared research data, code, and durable results | `/projects/<project>/` |
| Temporary, high-I/O files for one job | Job-local `/local` or `$TMPDIR` |

Your **primary group** records your organizational home. A **project** is the
research collaboration: it has the approved members, data, services, purpose,
and lifecycle. Add collaborators to the project; do not move them into another
primary group merely to share data.

For a large team, use the
[large-team project layout](../reference/users-groups-projects.md#organise-storage-for-a-large-science-team)
rather than inventing another top-level storage path.

## Turn a successful command into a reliable analysis

Do not keep an important analysis only in shell history. Start with the
[script-to-workflow guide](../paths/from-shell-scripts.md). It shows how to:

- record inputs, outputs, parameters, software, and resources;
- choose Snakemake or Nextflow;
- turn a Conda environment declaration into a pinned Apptainer runtime;
- run every scientific task through Slurm; and
- test with synthetic or non-sensitive data before scaling.

## You are ready when

- terminal SSH reaches the configured RCC target;
- VS Code reaches the same target and opens a narrow project directory;
- you can explain why the jump host does not give you a shell;
- you know which project owns the work;
- a small Slurm test completes; and
- repeated analysis is recorded as code rather than remembered commands.
