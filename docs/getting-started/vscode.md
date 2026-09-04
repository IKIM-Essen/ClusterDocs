# Use VS Code with RCC

VS Code with Microsoft's **Remote - SSH** extension is the recommended
day-to-day interface for most RCC users. It gives you an editor, terminal, Git
tools, and a small remote file view in one window.

VS Code is the interface. It does not create a compute allocation. Use it to
prepare and inspect work on the shell host; submit computation through Slurm.

## Before installing VS Code

Make terminal SSH work first:

```bash
ssh {{ ssh_target_alias }}
```

Follow the [macOS](macos.md) or [Windows 11](windows.md) checklist if this does
not work. VS Code uses the same SSH key, configuration, jump host, and shell
host. The editor cannot repair an incorrect SSH setup.

## 1. Install the editor and one extension

1. Install the current stable **Visual Studio Code** from Microsoft's official
   distribution for macOS or Windows.
2. Open the Extensions view.
3. Install Microsoft's **Remote - SSH** extension.
4. Do not install a large extension collection at first. Add only what the
   project needs after reviewing its publisher and permissions.

On a managed workstation, use the institution's approved software route when
one is provided. Do not disable Gatekeeper, SmartScreen, antivirus, or other
endpoint controls to install the editor.

## 2. Connect to the shell host

1. Open the Command Palette with F1 or Shift-Command-P on macOS, or F1 or
   Ctrl-Shift-P on Windows.
2. Choose **Remote-SSH: Connect to Host…**.
3. Select `{{ ssh_target_alias }}`.
4. Confirm only the expected, independently verified RCC host identity.
5. Wait for the lower-left connection indicator to show the remote target.

Do not select the jump-host alias. `ProxyJump` crosses that forwarding gateway
automatically and opens VS Code on the shell host.

## 3. Open one useful directory

Open the smallest project subdirectory that contains the code you need, for
example:

```text
/projects/<project>/workflows/<workflow>/
```

Do not open `/projects`, `/groups`, `/homes`, an entire large project, a raw
data tree, or a workflow cache as the VS Code workspace. Broad file watching,
Git discovery, search, and language indexing can turn a convenient editor into
a large shared-storage workload.

## 4. Exclude data and generated trees

Add project-specific exclusions to `.vscode/settings.json` only after review.
A useful starting shape is:

```json
{
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/.snakemake/**": true,
    "**/.nextflow/**": true,
    "**/work/**": true,
    "**/results/**": true,
    "**/data/**": true,
    "**/envs/**": true
  },
  "search.exclude": {
    "**/.snakemake": true,
    "**/.nextflow": true,
    "**/work": true,
    "**/results": true,
    "**/data": true,
    "**/envs": true
  }
}
```

Adjust this list to the repository. Do not exclude workflow definitions,
configuration, tests, logs needed for diagnosis, or other source that the team
expects to review.

## 5. Use the integrated terminal correctly

Good shell-host activities in the VS Code terminal include:

- editing and testing small pieces of code;
- using Git;
- running a Snakemake dry run;
- starting the managed Snakemake or `rcc-nextflow` controller;
- submitting a batch job with `sbatch`;
- checking `squeue`, `sacct`, and small text logs; and
- opening a documented interactive allocation.

Do not run sustained Python, R, genomics, model, GPU, large-memory, or high-I/O
analysis directly in the VS Code terminal on the shell host. Do not assume a
Python or Jupyter extension has allocated compute resources.

## 6. Treat the remote workspace as executable

VS Code extensions, repository tasks, debug configurations, notebook kernels,
and workspace settings can execute commands with your RCC account. Before
granting Workspace Trust to an unfamiliar repository:

- inspect `.vscode/`, task definitions, launch configurations, and notebooks;
- review extension recommendations;
- remove secrets and protected identifiers from settings and logs; and
- confirm that tasks submit sustained work through Slurm.

Never enable SSH agent forwarding, paste a private key into VS Code, or bypass
a changed host-key warning to make Remote - SSH connect.

## 7. Edit a repeatable workflow

A useful project window normally contains small, reviewable files such as:

```text
README.md
config/
workflow/ or main.nf
scripts/
envs/
tests/
```

Use the [script-to-workflow guide](../paths/from-shell-scripts.md) when the
starting point is shell history or a command collection. Keep large inputs,
outputs, installed Conda environments, container caches, and workflow work
directories outside Git and outside editor-wide search.

## Common failures

| Symptom | First check |
|---|---|
| Target is absent from Remote-SSH | Confirm the correct local SSH `config` file contains `{{ ssh_target_alias }}`. |
| VS Code cannot connect, but Terminal can | Inspect the Remote - SSH log and selected local SSH client. |
| Terminal also cannot connect | Return to the platform checklist; this is not a VS Code problem. |
| Gateway says no interactive shell | Select the shell-host target, not the forwarding gateway. |
| Remote window is very slow | Open a smaller directory and exclude data, caches, environments, and results. |
| Python or notebook uses the shell host | Start the kernel or analysis inside a bounded Slurm allocation. |
| Host identity changed | Stop and contact RCC support through the approved channel. |

## You are ready when

- terminal SSH and Remote - SSH reach the same configured target;
- VS Code opens only the relevant project or repository directory;
- data and generated trees are excluded from watching and search;
- the integrated terminal submits computation through Slurm; and
- you can explain that the jump host forwards, the shell host controls, and a
  Slurm worker computes.

For screenshots and deeper settings, continue with the
[complete SSH and VS Code reference](../reference/access-ssh-vscode.md).
