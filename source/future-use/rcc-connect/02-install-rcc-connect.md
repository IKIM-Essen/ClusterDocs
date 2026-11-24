# Connect your macOS or Windows laptop

> **Pilot only.** Download only from a future authenticated, signed myRCC
> release. The present source bundle is a prototype for review, not an
> independently signed application or a production download.

## Before installation

You need an RCC account with a registered SSH public key, an approved laptop
and network route, and access to an authorized RCC project. Follow the RCC
account/device enrollment and 2FA process when it becomes available. Obtain
**trusted SSH host-key fingerprints from an independent official RCC channel**
before connecting. RCC Connect does not generate a key or silently trust an
unknown host.

Install **VS Code + Remote-SSH** for Python/shell use or **Positron desktop**
for R. You can use both. OpenSSH must be installed; Windows requires the system
OpenSSH Client optional feature.

## macOS

Extract the entire release archive, inspect the scripts, open Terminal in the
extracted directory, and run:

```sh
bash ./Install-macOS.command YOUR_LDAP_USERNAME
~/.local/bin/rcc-open doctor
```

Alternatively, launch the `.command` file from Finder. The installer does not
require administrator privileges. It adds one `Include` at the start of your
user SSH config, installs dedicated `rcc-login` / `rcc-shellhost` aliases and
places a launcher in `~/.local/bin`. Existing SSH keys are not modified.

## Windows

Extract the archive, review the scripts and double-click `Install-Windows.cmd`
(or from PowerShell run):

```powershell
powershell.exe -NoProfile -File .\Install-Windows.ps1 -RccUser YOUR_LDAP_USERNAME
powershell.exe -NoProfile -File "$HOME\.rcc\bin\rcc-open.ps1" doctor
```

Use your normal Windows account, not Administrator. Do not disable PowerShell
security controls to force unsigned scripts to run; contact RCC support for an
approved release path. This prototype has not been natively validated on
Windows.

## Verify SSH trust, then connect

`doctor` checks local SSH alias configuration; it **does not check the authenticity
of a remote host key**. Compare the server fingerprint against the independently
obtained official RCC registry before accepting the key. After that,
initial enrollment can be done from Terminal/PowerShell:

```sh
ssh -o StrictHostKeyChecking=ask rcc-login
ssh -o StrictHostKeyChecking=ask rcc-shellhost
```

Disconnect from those lightweight hosts; **do not start substantial analysis
there**. When you request a Slurm worker, you must also verify that worker's
key before using Positron native Remote SSH. Do not accept an unfamiliar key
because it looks plausible. RCC's future signed host-key registry should
make this onboarding step simpler.

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
