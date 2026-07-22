# Class 1: safe access to RCC

## Learning objectives

By the end of this class you can:

- explain the difference between your SSH private key and the server host key;
- verify that an SSH client is installed;
- identify a suitable RCC public key without displaying the private key;
- validate the RCC SSH configuration before connecting;
- make one controlled login test;
- install VS Code and the Remote - SSH extension;
- use the browser transfer service without sharing an account.

## Security model in plain language

Your **private key stays on your computer**. RCC receives only the public key. The server's **digital identity** lets your computer verify that it reached an approved RCC service. RCC is moving to certificates signed by one RCC host certification authority, so clients can verify the cluster without accepting every machine individually. A changed identity is not fixed by disabling checking; follow the published transition instructions.

Do not email private keys, copy a colleague's key, register one key for several human accounts, or share a browser session. When a colleague needs access, add their own account to the project.

## First-time client setup

Create a dedicated Ed25519 key protected by a strong passphrase.

If you have a compatible FIDO2 hardware authenticator, prefer `ssh-keygen -t ed25519-sk -f ~/.ssh/id_rcc`. The private material remains on the authenticator and normally requires your physical presence.

On macOS or Linux:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_rcc
```

On Windows PowerShell:

```powershell
ssh-keygen -t ed25519 -f "$HOME\.ssh\id_rcc"
```

Register only `id_rcc.pub` through the approved RCC account workflow. The file
without `.pub` is the private key and stays on your computer.

Use the SSH configuration supplied through the RCC rollout page. During migration, RCC Connect provides a separate configuration and trust file that do not replace your ordinary SSH files. Until the rollout notice activates RCC Connect, use the current approved configuration. Its safe shape is:

```sshconfig
Host {{ ssh_alias }}
  HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
  User YOUR_RCC_USERNAME
  IdentityFile ~/.ssh/id_rcc
  IdentitiesOnly yes
  ForwardAgent no
```

Inspect the effective configuration without connecting:

```bash
ssh -G {{ ssh_alias }}
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

First verify the RCC host-CA fingerprint on the rollout page or another independent institutional channel. Then run exactly one attempt:

```bash
bash exercises/readiness/rcc-readiness.sh --live
```

The test uses strict host-key checking, disables password prompts, permits one connection attempt, and times out quickly. Stop after repeated failures and use the troubleshooting page rather than creating a retry loop.

## Gate 1C: VS Code

The same readiness script checks whether VS Code and the Microsoft Remote - SSH extension are present. Terminal SSH must work before VS Code is tested. When RCC Connect becomes active, its repair action selects the dedicated RCC SSH configuration for VS Code.

## Web data transfer

Inside the hospital network, use your individual RCC username and normal sign-in flow. External access may require an additional factor. Do not solve access problems by using a shared project account.

The transfer portal exposes project data, not arbitrary server filesystems. Confirm the selected project and destination before uploading.

> **Reference companion:** Use [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md)
> for account-request details, diagnostics, Remote SSH, and light SSHFS mounts.
> Use [Storage and transfer](../reference/storage-transfer.md) for larger data
> movement, archives, checksums, and object-storage boundaries.

## Knowledge check

<details><summary>Why is accepting every changed host key unsafe?</summary>

It removes the check that distinguishes the intended server from an unexpected system. Verify a planned transition through an independent institutional channel.
</details>

<details><summary>What should I do when RCC reports an identity change?</summary>

Do not approve the warning or delete `known_hosts` entries. Close VS Code, run RCC Connect's connection test and repair action, and report its support code if the repair fails.
</details>

<details><summary>Can two researchers use the same SSH key?</summary>

No. Each human account should have individually attributable credentials. Project access is granted through membership, not credential sharing.
</details>

## Completion gate

- The local readiness gate reports SSH and configuration as ready.
- A single live test succeeds.
- VS Code can open the same configured RCC target.
- You can explain where your private key is stored without showing it.
