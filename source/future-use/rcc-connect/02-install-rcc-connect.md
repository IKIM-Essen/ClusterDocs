# Connect your macOS or Windows laptop

> **Future pilot.** Follow these steps after RCC approves your participation
> and supplies a platform-signed installer through its authenticated site
> channel. Keep any source-review ZIP for [offline review](07-operator-acceptance.md#verify-the-source-review-zip).

## Before installation

You need an RCC account with a registered SSH public key, an approved laptop
and network route, and access to an authorized RCC project. Follow the RCC
account/device enrollment and 2FA process when it becomes available. Before
running the installer, follow site instructions to verify and provision the
**independently signed RCC SSH host-key registry** in the SSH directory under
your user profile, at `.ssh/rcc/known_hosts`. The registry digest must match
the signed site release. If you have only a list of fingerprints or a review
ZIP, ask RCC support for the approved pilot package and registry.

Install **VS Code + Remote-SSH** for Python/shell use or **Positron desktop**
for R. You can use both. OpenSSH must be installed; Windows requires the system
OpenSSH Client optional feature.

## macOS

Install using the instructions supplied with the approved macOS package.
Then open Terminal and check the installed launcher:

```sh
~/.local/bin/rcc-open doctor
```

The installer runs under your own account. It adds one `Include` at the start of your
user SSH config, installs dedicated `rcc-login` / `rcc-shellhost` aliases and
places a launcher in `~/.local/bin`. Existing SSH keys are not modified.

## Windows

Install using the instructions supplied with the approved Windows package.
Then open PowerShell under your own account and check the installed launcher:

```powershell
powershell.exe -NoProfile -File "$HOME\.rcc\bin\rcc-open.ps1" doctor
```

If Windows refuses the installer under its normal security policy, contact
RCC support for the approved release path.

## Verify SSH trust, then connect

`doctor` checks the local SSH configuration. To verify the connection, use
the installed aliases with their strict host-key policy:

```sh
ssh rcc-login
ssh rcc-shellhost
```

Disconnect from those lightweight hosts; **do not start substantial analysis
there**. A Slurm worker must also have an entry in the approved registry
before you open it in either editor. If SSH reports a missing or changed key,
stop and ask RCC support to verify the host and provide any approved registry
update. Continue only after the strict SSH check succeeds.

## Launch a project session

macOS:

```sh
~/.local/bin/rcc-open positron YOUR_PROJECT
~/.local/bin/rcc-open vscode YOUR_PROJECT
```

Windows PowerShell:

```powershell
powershell.exe -NoProfile -File "$HOME\.rcc\bin\rcc-open.ps1" positron YOUR_PROJECT
```

Both examples **submit a Slurm allocation**. Use one, not both, unless you
intentionally need separate sessions. The launcher prints its Slurm job ID
and editor SSH alias; record that ID so you can reconnect. Slurm may queue
the request. See [recovery commands](06-troubleshooting.md).

No IDE settings file can enforce compute restrictions on its own. RCC's
Slurm jobs, host resource limits, project permissions and storage policy are
the enforcing boundaries.
## Project-bound reconnect (v2.2)

When attaching to an existing allocation, RCC Connect verifies the Slurm job's exact `WorkDir=/projects/PROJECT` before generating an SSH alias. Selecting a different project fails closed and does not submit a replacement job. If the scheduler cannot confirm the work directory, run `rcc-open list` and ask RCC support; do not repeat `start` blindly.

This is a client-side protection only: RCC server-side permissions and admission remain authoritative.
