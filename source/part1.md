---
title: "RCC Onboarding - Part 1"
subtitle: "Browser identity, optional SSH access, data transfer, and the first Slurm job"
author: "IKIM RCC documentation"
date: "5 September 2026"
---

# Contents

- About Part 1 and who needs it
- RCC identity, web credentials, and password managers
- 1. Cluster architecture and the local/remote mental model
- 2. Browser-first access and the optional advanced SSH path
- 3. Local software: OpenSSH and Visual Studio Code
- 4. SSH keys and server identity
- 5. SSH configuration and the gateway route
- 6. Terminal connection and verification
- 7. VS Code Remote - SSH and remote editing
- 8. Storage, browser transfer, and checksums
- 9. Slurm, batch scripts, resources, and the first job
- 10. Connection persistence and tmux
- 11. Layered troubleshooting
- 12. Completion checklist
- 13. What comes in Part 2

# About Part 1

ClusterDocs 3 is browser-first for ordinary researchers. If RCC Home, Files, and
the browser analysis capabilities cover your work, you do not need to create an
SSH credential merely because you have an RCC account.

Part 1 therefore has two purposes:

1. explain the common RCC identity/project/data boundaries used by every user;
2. provide the advanced SSH, VS Code, and direct Slurm path for users who need it.

By the end of the advanced path, you can:

- explain the difference between web credentials, SSH keys, and server host keys;
- create and safely handle the RCC SSH key when SSH is required;
- connect to the RCC shell host through the forwarding gateway;
- use Visual Studio Code Remote - SSH as an advanced development interface;
- transfer a small non-sensitive test file through the RCC files service; and
- submit, monitor, and inspect a small Slurm batch job.

Part 1 does **not** install scientific software or introduce Snakemake. Later
parts cover reproducible workflows, performance, and Apptainer.

## How to use this guide

Do not copy commands without understanding where they run. For each command ask:

1. Which computer am I controlling?
2. Where are the files?
3. Does this run directly in the shell or through Slurm?
4. What happens if the connection closes?

The browser-first interface hides many of these details. The advanced path makes
them explicit because direct SSH/Slurm users are responsible for using the
correct execution boundary.

# RCC identity, web credentials, and password managers

One RCC human identity is used across several interfaces, but the credentials
are not interchangeable.

- **RCC web sign-in** may use a password, passkey, and/or another enrolled factor.
- **Recovery/step-up** may use separate recovery codes, passkeys, or an approved authenticator.
- **SSH** uses a registered SSH public key only when the user needs the advanced command-line path.
- **Project membership** is authorization, not a shared credential.

For RCC web passwords, passkeys, and appropriate recovery material, use the
credential/password-manager facilities already provided by the supported Windows
or macOS environment and browser, or another institutionally approved password
manager. Do not store those credentials in project data, Git repositories,
notes alongside research data, scripts, or chat.

That recommendation does **not** mean the RCC SSH key should have a passphrase.
RCC does not recommend a passphrase on the normal software-backed RCC SSH key.

# RCC connection values and support

RCC connection targets and SSH host identities can change during maintenance.
Obtain the current SSH configuration and fingerprints through the approved RCC
instructions. Do not reconstruct them from an old screenshot, email, or a
colleague's configuration.

Browser-based project transfer is available through the RCC Files service. Sign
in through the institutional web flow and open the project assigned to you.
The files service exposes project-facing storage; it is not a separate shared
account and does not broaden project membership.

For help, use the approved RCC support route without posting credentials,
private keys, or sensitive project data.

# 1. Understand the basic layout

RCC is a shared research platform, not one large personal computer. Different
systems have different responsibilities.

```text
Browser-first research
    -> RCC Home / Files / Analysis
    -> governed project + Slurm-backed execution

Advanced command-line path
    -> local workstation
    -> forwarding gateway (ProxyJump; no working shell)
    -> RCC shell host (edit, Git, submit, inspect)
    -> Slurm allocation (scientific computation)
```

- **Your workstation:** local browser, terminal, and optional VS Code.
- **Forwarding gateway:** guarded network entry; not a place to work.
- **Shell host:** light editing, Git, job submission, workflow control, logs.
- **Slurm worker/allocation:** CPU, memory, GPU, notebook, and scientific work.
- **Project storage:** durable approved project inputs and results.
- **Job-local scratch:** temporary high-I/O work inside an allocation.

Do not run sustained analysis on the gateway or shell host.

# 2. Browser-first access and the optional advanced SSH path

An RCC account does not automatically require SSH.

Use browser-first access when the released RCC services cover the task. Use SSH
when you need direct Slurm commands, VS Code Remote SSH, workflow development,
SFTP/public-key automation, or another capability that explicitly requires it.

Only create/register an SSH key when that advanced capability is needed.

# 3. Install the required advanced-path software

## Windows 11

Open PowerShell and verify the built-in OpenSSH client:

```powershell
ssh -V
```

If it is missing, install the Microsoft OpenSSH Client optional feature through
the supported Windows mechanism. You do not need WSL merely to connect to RCC.

Install Visual Studio Code and Microsoft's Remote - SSH extension only if you
need the advanced editor/developer path.

## macOS

Open Terminal and verify OpenSSH:

```bash
ssh -V
```

OpenSSH is supplied with current macOS. Install Visual Studio Code and Remote -
SSH only when you need the advanced path.

# 4. Create your RCC SSH key

## 4.1 Private key, public key, and host key

An SSH key pair contains:

- a **private key**, which remains on the workstation or compatible hardware authenticator;
- a **public key**, which RCC registers to the individual RCC account.

The server's **host-key fingerprint** is a different thing: it lets the client
verify that the expected RCC server answered.

Never email, upload, paste, or commit the private SSH key. Project membership is
never granted by sharing a credential.

## 4.2 RCC SSH-key policy

For the normal software-backed RCC key, create the key **without a passphrase**.
The empty `-N ""` is intentional RCC policy, not a missing tutorial step.

Security comes from keeping the private key on a protected endpoint, using
individual attributable accounts, disabling agent forwarding, verifying the RCC
server identity, promptly responding to lost devices, and preferring a
hardware-backed FIDO SSH key where appropriate.

Do not add an SSH-key passphrase merely because a generic SSH tutorial recommends
one. Password-manager guidance in ClusterDocs applies to RCC web/account
credentials and recovery material.

## 4.3 Windows software-backed key

```powershell
New-Item -ItemType Directory -Force "$HOME\.ssh" | Out-Null
ssh-keygen -t ed25519 -N "" -f "$HOME\.ssh\id_rcc" -C "$env:USERNAME@rcc"
```

The files are normally:

```text
C:\Users\YOUR_WINDOWS_NAME\.ssh\id_rcc
C:\Users\YOUR_WINDOWS_NAME\.ssh\id_rcc.pub
```

Register only the `.pub` file/content.

## 4.4 macOS software-backed key

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_rcc -C "$USER@rcc"
chmod 600 ~/.ssh/id_rcc
```

Register only `~/.ssh/id_rcc.pub`.

## 4.5 Hardware-backed FIDO SSH key

Where a compatible authenticator and current RCC/client support are available,
prefer a hardware-backed key:

```bash
ssh-keygen -t ed25519-sk -N "" -f ~/.ssh/id_rcc
```

A browser/WebAuthn passkey and an OpenSSH `*-sk` credential are separate
credentials even when both live on the same physical security key.

# 5. Configure the SSH connection

Use the current host blocks supplied through the approved RCC channel. Their
safe shape is:

```sshconfig
Host rcc-login
    HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
    User <RCC_USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host shellhost c? c?? c??? d?? g?-? g?-??
    HostName %h.ikim.uk-essen.de
    User <RCC_USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump rcc-login
    ForwardAgent no
```

The gateway is forwarding-only. Do not try to use it as a working shell. The
worker/node patterns are only for a node assigned by an active Slurm allocation;
they are not permission to choose arbitrary compute nodes.

Do not add `ForwardAgent yes` and do not disable host-key checking to make a
connection work.

# 6. Test the SSH connection in a terminal

Inspect the effective configuration first:

```bash
ssh -G shellhost
```

Then make one bounded connection attempt:

```bash
ssh shellhost
```

Compare every first-use or changed host-key fingerprint with the current value
published through an independent institutional channel. Stop on an unexpected
identity warning; do not delete all `known_hosts` entries.

After login:

```bash
whoami
hostname
pwd
```

Then disconnect with:

```bash
exit
```

If a client unexpectedly prompts for a password/passphrase when the configured
RCC key was generated with `-N ""`, first verify that the correct key and host
configuration are being used. Do not solve the problem by adding another secret
or weakening authentication checks.

# 7. Connect with Visual Studio Code

Use Visual Studio Code Remote - SSH only after terminal SSH works.

1. Start VS Code.
2. Open **Remote-SSH: Connect to Host...**.
3. Select the approved RCC shell-host alias.
4. Verify the remote indicator and `hostname`.
5. Open only the smallest useful code/project subdirectory.

A VS Code remote window does not create a Slurm allocation. Its terminal runs on
the RCC shell host. Use it for light commands, Git, job submission, monitoring,
and logs; submit scientific computation through Slurm.

Exclude data, results, package trees, workflow caches, and large environments
from workspace-wide search and file watching. Review Workspace Trust and remote
extensions because they can execute code with the RCC account's permissions.

# 8. Transfer a test file with RCC Files

Use the browser Files service for the small first transfer rather than dragging
research data through VS Code.

Create a local non-sensitive file such as:

```text
rcc-transfer-test.txt
```

Upload it to the exact approved project destination. Then on RCC calculate:

```bash
sha256sum rcc-transfer-test.txt
```

Compare with the local checksum:

Windows PowerShell:

```powershell
Get-FileHash .\rcc-transfer-test.txt -Algorithm SHA256
```

macOS:

```bash
shasum -a 256 rcc-transfer-test.txt
```

Matching hashes provide strong evidence that the bytes match. They do not prove
that a file is scientifically correct, permitted, or in the correct project.

Keep large/recurring instrument transfers on their reviewed project ingestion
path rather than using a laptop as an intermediate copy.

# 9. Submit your first Slurm job

Scientific computation is scheduled by Slurm. The first job should be small and
synthetic.

Create:

```bash
mkdir -p ~/rcc-introduction/{scripts,logs,results}
cd ~/rcc-introduction
```

Create `scripts/first-job.sh`:

```bash
#!/usr/bin/env bash
#SBATCH --job-name=rcc-first
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=256M
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail

echo "User: ${USER}"
echo "Slurm job ID: ${SLURM_JOB_ID}"
echo "Compute node: $(hostname)"
printf "value\n1\n2\n3\n4\n5\n" > results/numbers.csv
awk 'NR > 1 {sum += $1; n += 1} END {printf "n=%d\nmean=%.2f\n", n, sum/n}' \
    results/numbers.csv > results/summary.txt
```

Submit:

```bash
sbatch scripts/first-job.sh
```

Inspect current work:

```bash
squeue -u "$USER"
```

After completion:

```bash
sacct -j <JOB_ID> --format=JobID,JobName,State,Elapsed,AllocCPUS,ExitCode
cat results/summary.txt
```

Expected result:

```text
n=5
mean=3.00
```

The Slurm log should identify a compute node, not the shell host.

# 10. Connections, long-running control processes, and tmux

A submitted Slurm batch job continues after the laptop disconnects because
Slurm owns the job.

`tmux` preserves a remote terminal session and may be useful for a lightweight
workflow controller or monitoring session:

```bash
tmux new -s my-workflow
tmux ls
tmux attach -t my-workflow
```

`tmux` does not allocate compute resources and does not make heavy analysis on
the shell host acceptable.

# 11. Troubleshooting

Classify the failure before changing configuration:

1. local tool;
2. network route;
3. user authentication/key selection;
4. server identity;
5. remote host/role;
6. storage/path/permissions;
7. scheduler/allocation;
8. scientific application.

Useful bounded diagnostics include:

```bash
ssh -G shellhost
ssh -vvv shellhost
squeue -j <JOB_ID> -o "%.18i %.9T %.30R"
```

Remove usernames, local paths, tokens, research identifiers, and unnecessary
file names before sharing diagnostics. Never send the private key.

If SSH unexpectedly asks for a passphrase/password, remember that the current
normal RCC software key was created without a passphrase. Verify key selection
and configuration rather than adding a passphrase or disabling checks.

# 12. Completion checklist

You have completed the advanced Part 1 path when:

- [ ] you know which file is the private SSH key and have never shared it;
- [ ] you can explain that the normal RCC software-backed SSH key is generated without a passphrase;
- [ ] you use the supported Windows/macOS/browser credential manager for RCC web/account credentials where appropriate;
- [ ] `ssh shellhost` works through the forwarding gateway;
- [ ] you verified the RCC host fingerprints;
- [ ] VS Code can open the shell host if you use the advanced editor path;
- [ ] you transferred a non-sensitive file into the correct project and matched its checksum;
- [ ] Slurm accepted your batch script; and
- [ ] the job log proves the scientific work ran on a compute node.

# 13. What comes next

The RCC onboarding series continues with:

- **Part 2:** reproducible workflows, Conda declarations, Snakemake/Nextflow, statistics, and synthetic sequence examples;
- **Part 3:** CPU, GPU, memory, storage, I/O, bottleneck diagnosis, and node-local scratch; and
- **Part 4:** Apptainer containers and reproducible runtime patterns.

Do not pre-install an unrelated software stack merely because another HPC guide
uses it. Follow the current RCC software/runtime guidance so the project remains
reviewable and reproducible.
