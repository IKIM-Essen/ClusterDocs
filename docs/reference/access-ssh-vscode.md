# Account access, SSH, and VS Code reference

This guide collects the practical setup details from the earlier ClusterDocs
site. Complete [Class 1](../course/class-01-safe-access.md) first so that the
credential and host-verification rules are clear.

## Request an RCC account

Use the RCC Admin request flow when it is available. If your project still
uses a coordinated onboarding process, send the following to the responsible
project coordinator through the approved institutional channel:

- first and last name;
- institutional email address;
- project or working group;
- sponsor or project lead; and
- the **public** SSH key, never the private key.

Every researcher receives an individual account. Project membership replaces
shared accounts and shared credentials.

## Create an SSH key

Where a compatible FIDO2 authenticator is available, prefer a hardware-backed key. Its private material remains on the authenticator and normally requires user presence:

```bash
ssh-keygen -t ed25519-sk -f ~/.ssh/id_rcc
```

Otherwise, create the dedicated software-backed Ed25519 key described below. Do not copy either type of private credential between computers.

### macOS and Linux

Create a dedicated Ed25519 key and protect it with a strong passphrase:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_rcc
```

This creates two files:

- `~/.ssh/id_rcc` is the private key. Keep it on your workstation and never
  send or paste it anywhere.
- `~/.ssh/id_rcc.pub` is the public key. This is the file RCC registers.

Show the public key when you need to copy it:

```bash
cat ~/.ssh/id_rcc.pub
```

### Windows

Current Windows releases provide the OpenSSH client as an optional feature.
Open PowerShell and check it first:

```powershell
ssh -V
ssh-keygen -t ed25519 -f "$HOME\.ssh\id_rcc"
```

If `ssh` is unavailable, install the Microsoft OpenSSH Client optional feature
using the official Windows instructions. The private and public files are
normally stored under `C:\Users\<username>\.ssh\`.

## Configure the approved RCC target

Use the host block supplied through the RCC rollout page or another trusted institutional channel. During the host-identity migration, RCC will distribute **RCC Connect**: a portable kit with a dedicated RCC configuration, host-CA trust file and connection test. It does not modify or delete entries for unrelated services in the ordinary `known_hosts` file.

Until the rollout page says RCC Connect is active, continue using the currently approved configuration. The public alias used in this course is `{{ ssh_alias }}`. A safe client block has this shape:

```sshconfig
Host {{ ssh_alias }}
  HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
  User YOUR_RCC_USERNAME
  IdentityFile ~/.ssh/id_rcc
  IdentitiesOnly yes
  ForwardAgent no
```

Do not copy an old hostname from a colleague, disable host-key checking or enable agent forwarding merely to make a connection work. Verify the published RCC host-CA fingerprint through an independent institutional channel before migration.

Inspect the effective configuration without connecting:

```bash
ssh -G {{ ssh_alias }}
```

Then use the bounded readiness test from Class 1. For manual diagnostics, one
verbose connection attempt is usually enough:

```bash
ssh -v {{ ssh_alias }}
```

Remove key material, usernames, local paths, and tokens before sharing a debug
log with support.

During or after migration, do not approve an unexpected SSH identity warning and do not delete host records merely to make the warning disappear. Close the client, run the RCC connection test and use its repair action. Report the generated support code if repair fails.

## Use VS Code Remote SSH

1. Install Visual Studio Code and Microsoft's **Remote - SSH** extension.
2. Confirm terminal SSH works first.
3. If RCC Connect is active, run its test and repair action before opening VS Code. The kit selects its dedicated SSH configuration and, where necessary, its maintained SSH executable.
4. Open **Remote Explorer** and select the approved RCC alias from the SSH targets.
5. Open only the project or source directory you need.
6. Keep data, environment, cache, and generated-result directories out of
   workspace-wide search.

Do not manually accept an unexpected identity warning in VS Code. Close it and run the RCC connection test instead. See the [SSH host-identity policy](../policies/ssh-host-identity.md) for the architecture and rollout controls.

VS Code uses `rg` for full-text search. A recursive search over large shared
storage or an environment containing thousands of files can create substantial
metadata load. Add generated trees to `.gitignore` or `.ignore`, for example:

```gitignore
.venv/
.snakemake/
data/
results/
node_modules/
```

## End a session cleanly

Close remote editors and terminals when finished. Interactive analysis,
notebooks, and long-running commands belong in bounded Slurm jobs; they should
not depend on a laptop connection remaining open.

## Mount a small remote folder

Prefer the RCC files portal for browser-based access to approved project
folders. SSHFS is appropriate only for light interactive use such as editing a
small document. It is not a bulk-transfer or analysis filesystem.

After installing a maintained SSHFS implementation for your operating system,
create an empty mount point and use the configured RCC alias:

```bash
mkdir -p "$HOME/rcc-project"
sshfs {{ ssh_alias }}:/projects/<project> "$HOME/rcc-project" \
  -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3
```

Unmount before sleeping the computer or changing networks. The exact unmount
command depends on the operating system and SSHFS package. Do not enable an
unattended automatic mount until manual mount and unmount work reliably.

Avoid opening large directory trees in Finder, Explorer, indexing services,
backup tools, antivirus scanners, or VS Code through SSHFS. Use the
[storage and transfer reference](storage-transfer.md) for larger transfers.
