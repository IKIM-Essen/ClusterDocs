# Class 1: safe access to RCC

!!! tip "New workstation or first RCC experience?"
    Complete [RCC Expedition Light](../getting-started/index.md) for the
    browser-first first-use path. Use this class when you need the advanced
    SSH/VS Code route. [RCC Expedition](../rcc-expedition.md) remains a
    self-contained local course covering workstation security/patching,
    SSH/Linux basics, the research/clinical network boundary, Slurm, storage,
    data transfer, and reproducible workflows.

    The course is **datensparsam** and does not report learner progress to RCC.
    This page remains the conventional step-by-step SSH reference tutorial.

Before configuring SSH, read the one-page explanation of the
[jump host, shell host, and Slurm workers](../concepts/jump-shell-compute.md).

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Advanced SSH path · video requires v3 regeneration</p>
  <h2>Written guidance is authoritative for the v3 candidate</h2>
  <p>The existing Part 1 video predates the current RCC SSH-key policy and must be regenerated and re-reviewed before release. Use the written page below for the current key, host-verification, VS Code, transfer, and Slurm guidance.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/part1.png" src="{{ media_base_url }}/RCC_Onboarding_Part_1_Video_Enhanced.mp4?v=a536afc0">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Part_1_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

## Learning objectives

By the end of this class you can:

- explain the difference between your SSH private key and the server host key;
- explain why an RCC browser passkey and an SSH key are different credentials;
- verify that an SSH client is installed;
- identify a suitable RCC public key without displaying the private key;
- validate the RCC SSH configuration before connecting;
- make one controlled login test;
- install VS Code and the Remote - SSH extension for advanced coding and analysis preparation;
- open a narrowly scoped remote project and configure safe search exclusions;
- use the browser transfer service without sharing an account.

## Security model in plain language

Your **private key stays on your computer**. RCC receives only the public key.
The server's **digital identity** lets your computer verify that it reached an
approved RCC service. Use the host-verification information in the current RCC
instructions. A changed identity is not fixed by disabling checking; stop and
confirm it through an independent institutional channel.

Do not email private keys, copy a colleague's key, register one key for several human accounts, or share a browser session. When a colleague needs access, add their own account to the project.

### Browser sign-in and SSH are separate credentials

Your RCC username is one human identity, but RCC can authenticate that identity
in different ways:

- **web services** use the RCC sign-in/SSO flow and may use a password, passkey,
  or another enrolled factor;
- **SSH and VS Code Remote SSH** use your registered SSH public key;
- **account recovery or sensitive account actions** may use separate step-up or
  recovery credentials.

For RCC web passwords, passkeys, and appropriate recovery material, use the
password/passkey manager already provided by the supported Windows or macOS
environment, or another institutionally approved password manager. Do not turn
that recommendation into an SSH-key passphrase requirement: the normal RCC
software-backed SSH key is intentionally created without a passphrase.

A YubiKey can hold more than one kind of credential. A browser/WebAuthn passkey
and an OpenSSH `*-sk` key are not the same credential merely because they are on
the same physical key.

Read [How RCC authentication fits together](../reference/authentication-lifecycle.md)
before adding, replacing, or deleting passkeys, YubiKey credentials, recovery
codes, or SSH keys.

## First-time client setup

Create a dedicated Ed25519 key using the RCC command below. The empty `-N ""` is
intentional: RCC does **not** recommend a passphrase on the normal software-backed
SSH key. Protect the endpoint, keep the private key local, and never share it.

If you have a compatible FIDO2 hardware authenticator, prefer a hardware-backed
key where appropriate:

```bash
ssh-keygen -t ed25519-sk -N "" -f ~/.ssh/id_rcc
```

On macOS or Linux:

```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_rcc
```

On Windows PowerShell:

```powershell
ssh-keygen -t ed25519 -N "" -f "$HOME\.ssh\id_rcc"
```

Register only `id_rcc.pub` through the approved RCC account workflow. The file
without `.pub` is the private key and stays on your computer.

Use the current SSH configuration supplied through an approved RCC channel.
Do not reconstruct it from an old screenshot or a colleague's saved settings.
Its safe shape includes both the gateway and the destination:

```sshconfig
Host {{ ssh_gateway_alias }}
  HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
  User YOUR_RCC_USERNAME
  IdentityFile ~/.ssh/id_rcc
  IdentitiesOnly yes
  ForwardAgent no

Host {{ ssh_target_alias }} c? c?? c??? d?? g?-? g?-??
  HostName %h.ikim.uk-essen.de
  User YOUR_RCC_USERNAME
  IdentityFile ~/.ssh/id_rcc
  IdentitiesOnly yes
  ProxyJump {{ ssh_gateway_alias }}
  ForwardAgent no
```

Use `{{ ssh_target_alias }}` for normal login. The additional node patterns
support a node assigned by an active Slurm interactive allocation; they do not
permit work outside Slurm. The `{{ ssh_gateway_alias }}` account is
forwarding-only and will not provide an interactive shell. Do not test it with
`ssh {{ ssh_gateway_alias }}`; `ProxyJump` uses it automatically when you
connect to the destination.

Inspect the effective configuration without connecting:

```bash
ssh -G {{ ssh_target_alias }}
```

## Gate 1A: local readiness

### macOS or Linux

```bash
bash exercises/readiness/rcc-readiness.sh
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File exercises/readiness/Test-RccReadiness.ps1
```

The gate checks software and configuration. It does not contact RCC unless you explicitly add `--live` or `-Live`.

## Gate 1B: one bounded SSH test

First verify the published RCC host identity through an independent
institutional channel. Then run exactly one attempt:

```bash
bash exercises/readiness/rcc-readiness.sh --live
```

The test uses strict host-key checking, disables password prompts, permits one connection attempt, and times out quickly. Stop after repeated failures and use the troubleshooting page rather than creating a retry loop.

## Gate 1C: VS Code

The same readiness script checks whether VS Code and the Microsoft Remote - SSH extension are present. Terminal SSH must work before VS Code is tested.

For users who need the advanced command-line/developer path, VS Code is a useful
day-to-day interface after the connection test passes. Open the code repository
or smallest useful project subdirectory, not an entire home, group, or
project-storage tree. VS Code does not create a Slurm allocation: use its
terminal to submit and inspect jobs, not to run a sustained analysis directly.

Before searching, exclude data, results, environments, package trees, and
workflow caches. Review extensions and Workspace Trust because remote
extensions and repository tasks can run with your RCC account's permissions.
The [VS Code reference](../reference/access-ssh-vscode.md#customize-vs-code-without-creating-performance-problems)
contains copyable settings and the restored ClusterDocs performance advice.

## Web data transfer

Inside the hospital network, use your individual RCC username and normal RCC
sign-in flow. External access may require an additional factor. Do not solve
access problems by using a shared project account.

The Files service exposes project-facing data, not arbitrary server filesystems.
Confirm the selected project and destination before uploading. Read
[RCC Files](../concepts/rcc-files.md) for the browser/SFTP distinction and
project-data boundary.

> **Reference companion:** Use [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md)
> for account-request details, diagnostics, Remote SSH, and light SSHFS mounts.
> Use [Storage and transfer](../reference/storage-transfer.md) for larger data
> movement, archives, checksums, and object-storage boundaries.

## Knowledge check

<details><summary>Why is accepting every changed host key unsafe?</summary>

It removes the check that distinguishes the intended server from an unexpected
system. Stop and verify the current identity through an independent
institutional channel.
</details>

<details><summary>What should I do when RCC reports an identity change?</summary>

Do not approve the warning or delete `known_hosts` entries. Close VS Code,
compare the configuration and host identity with the current RCC instructions,
and contact RCC support if they do not match.
</details>

<details><summary>Can two researchers use the same SSH key?</summary>

No. Each human account should have individually attributable credentials. Project access is granted through membership, not credential sharing.
</details>

<details><summary>Is my RCC browser passkey the same as my SSH key?</summary>

No. They can live on the same physical authenticator, but WebAuthn/passkey
credentials and OpenSSH keys are separate credentials used by different
protocols.
</details>

## Completion gate

- The local readiness gate reports SSH and configuration as ready.
- A single live test succeeds.
- VS Code can open the same configured RCC target if you use the advanced editor path.
- You can explain where your private SSH key is stored without showing it.
- You can explain that the normal RCC software-backed SSH key is generated without a passphrase.
- You can explain why web sign-in credentials, recovery credentials, and SSH
  keys are related to one RCC identity but are not interchangeable.
