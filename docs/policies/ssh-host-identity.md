# RCC SSH host-identity policy

> **Status:** This page documents the planned SSH host-identity architecture and migration. Until the rollout page says RCC Connect is active, use the currently published RCC SSH configuration. Do not build a CA entry from examples on this page.

## Decision

RCC will use:

- a unique Ed25519 private host key on every server;
- one RCC SSH host certification authority (CA);
- an RCC host certificate on every server; and
- certificate principals for all approved short names, fully qualified domain names and service aliases.

The single RCC identity presented to users is the **public host CA**, not a private key copied to every machine. A shared fleet-wide private host key is prohibited: compromise of one node would otherwise permit impersonation of every other node and make individual revocation and incident containment impossible.

Host authentication and user authentication are separate. The host certificate proves that a client reached an approved RCC service. A user's SSH key proves which RCC account is connecting.

## Dedicated RCC trust

RCC trust must not depend on the user's ordinary `known_hosts` file. That file can contain stale RCC keys, hashed names, unrelated systems and records written by several SSH clients.

RCC Connect keeps its configuration under a user-owned directory:

- macOS and Linux: `$HOME/.rcc-ssh/`
- Windows: `%USERPROFILE%\.rcc-ssh\`

The dedicated `rcc_known_hosts` file contains the public RCC host-CA entry and approved hostname patterns. The generated configuration selects that file only for RCC hosts and requires strict verification:

```sshconfig
Host rcc-shell shellhost shellhost.ikim.uk-essen.de c??? d?? g?-??
  UserKnownHostsFile ~/.rcc-ssh/rcc_known_hosts
  StrictHostKeyChecking yes
  IdentitiesOnly yes
  ForwardAgent no
```

This leaves GitHub, other clusters and unrelated trust records untouched. The stable `rcc-shell` entry resolves to the RCC submission service. Generated compute-node entries use it as their jump host, keeping worker nodes from direct external exposure.

## RCC Connect

The primary client distribution is a portable ZIP that needs no installation, administrator access or PowerShell execution. A release is expected to include:

```text
RCC-Connect/
|-- README-FIRST.txt
|-- RCC-Connect.cmd
|-- RCC-Test.cmd
|-- RCC-Repair.cmd
|-- ssh_config
|-- rcc_known_hosts
|-- rcc-host-ca.pub
|-- fingerprints.txt
`-- vscode-settings.json
```

A Windows kit may include a maintained OpenSSH client to avoid conflicts among Windows OpenSSH, Git for Windows, PuTTY-derived clients and SSH programs inserted into `PATH`. RCC must promptly update any client it distributes.

Launchers explicitly select the kit configuration. They must not depend on the user's existing SSH configuration, system-wide configuration, administrator privileges or machine-wide environment variables. A user-scoped installed mode may add shortcuts and automated repair, but the portable mode remains supported when endpoint policy removes or rewrites installed files.

## VS Code integration

RCC Connect supplies VS Code Remote SSH with its dedicated configuration file. A Windows kit that bundles SSH also selects that executable. Equivalent settings are:

```json
{
  "remote.SSH.configFile": "C:\\Users\\USERNAME\\.rcc-ssh\\ssh_config",
  "remote.SSH.path": "C:\\Users\\USERNAME\\.rcc-ssh\\bin\\ssh.exe"
}
```

On macOS:

```json
{
  "remote.SSH.configFile": "/Users/USERNAME/.rcc-ssh/ssh_config",
  "remote.SSH.path": "/usr/bin/ssh"
}
```

The connection test checks these values because endpoint policy may reset them. Recovery is exposed as **Repair VS Code connection**, not as a requirement for users to edit JSON manually.

## Independent trust bootstrap

A checksum inside a downloaded ZIP cannot authenticate that ZIP. RCC publishes the host-CA fingerprint and package-signing information through several independent RCC-controlled channels, including:

- RCC Admin over HTTPS;
- the public RCC documentation site;
- account-enrolment material;
- an enrolment card or QR code;
- the RCC helpdesk verification procedure; and
- a notice at the RCC support office.

The kit displays the same fingerprint during installation and testing. No fingerprint may be added to this site until it has been independently verified and formally published by RCC.

Signed packages improve distribution integrity, but they cannot make a compromised endpoint trustworthy. A local administrator may still replace its trust store, SSH executable or downloaded program.

## User credentials and endpoint trust

Where possible, users should prefer FIDO-backed SSH keys such as `ed25519-sk`. Private material remains in the hardware authenticator and normally requires explicit user presence. RCC client configuration uses `IdentitiesOnly yes` and `ForwardAgent no`. Users must not copy long-lived private keys between machines.

| Endpoint class | Appropriate RCC access |
|---|---|
| Personally controlled endpoint | Normal SSH, VS Code and file transfer; RCC Connect and a FIDO-backed key are recommended |
| Institutionally managed endpoint with restrictive policy | Portable RCC Connect, user-scoped files and rerunning repair after policy changes |
| Endpoint administered by an untrusted or actively hostile party | Not suitable for sensitive RCC work; use an RCC-controlled workstation, virtual desktop, thin client, terminal or another trusted endpoint |

SSH encryption does not protect an active session from an endpoint administrator who can replace the SSH client, record input, alter commands or capture displayed and downloaded data.

## Migration sequence

### 1. Prepare servers

RCC retains each existing identity during transition, generates or retains a unique Ed25519 host key, signs it with the RCC host CA, includes every supported hostname as a certificate principal and validates every alias. Old and certified identities coexist initially.

### 2. Publish RCC Connect

RCC publishes portable Windows and macOS kits, optional user-scoped installers, the independently verifiable CA fingerprint, the repair utility, support documentation and a connection-test service.

### 3. Run a coexistence period

Coexistence lasts at least eight weeks and longer if significant active users have not migrated. Testing covers Windows, macOS, VS Code, command-line SSH and users returning after a long absence.

### 4. Retire old identities

After adoption is sufficient, RCC removes old server identities, retains unique certified host keys, keeps the portable repair kit permanently available and maintains a staffed support path. Users with the CA configuration see no warning. Others receive a hard failure and are directed to RCC Connect; they are never instructed to accept a changed identity manually.

## Repair and support behavior

The repair utility:

1. verifies its package version;
2. displays the RCC host-CA fingerprint;
3. tests the selected SSH client;
4. installs or refreshes the CA file and dedicated configuration;
5. tests `rcc-shell` and VS Code;
6. leaves the ordinary `known_hosts` file untouched; and
7. produces a support report without private keys or passwords.

Failures provide a short support code so users can ask for help without interpreting low-level SSH diagnostics.
