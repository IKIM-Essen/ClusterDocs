# Which RCC connection name should I use?

> Use `login.ikim.uk-essen.de` as the public SSH jump service and `shellhost`
> (`shellhost.ikim.uk-essen.de`) as the normal interactive and command-line
> file-transfer destination. Do not copy a physical backend address from an old
> screenshot or a colleague's saved configuration.

## Why the names stay stable

RCC gives users stable service names even when the physical systems behind them
change. Operations may replace a `login1` or `login2` backend while preserving
`login.ikim.uk-essen.de`, and may replace shell-host machines behind the
approved shell-host service without changing the user workflow.

The names also describe different jobs:

- `login.ikim.uk-essen.de` is the public, forwarding-only SSH doorway;
- `shellhost` is where an ordinary user shell opens and where command-line file
  transfers terminate;
- Slurm workers run the scientific computation.

Do not turn the jump host into a data endpoint merely because it appears in an
SSH command.

## Setup to use now

`login.ikim.uk-essen.de` is the stable public RCC jump host and
`shellhost.ikim.uk-essen.de` is the stable shell host. A minimal OpenSSH
configuration is:

```sshconfig
Host {{ ssh_gateway_alias }} login.ikim.uk-essen.de
    HostName login.ikim.uk-essen.de
    User YOUR_RCC_USERNAME
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no

Host {{ ssh_target_alias }}
    HostName shellhost.ikim.uk-essen.de
    User YOUR_RCC_USERNAME
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump login.ikim.uk-essen.de
    ForwardAgent no

Host c? c?? c??? d?? g?-? g?-??
    HostName %h.ikim.uk-essen.de
    User YOUR_RCC_USERNAME
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump login.ikim.uk-essen.de
    ForwardAgent no
```

Connect from the workstation with `ssh {{ ssh_target_alias }}`. The login account is
forwarding-only for ordinary users and will not provide an interactive shell;
`ssh login.ikim.uk-essen.de` is therefore not a valid ordinary-user login test.
`ProxyJump` uses the gateway automatically while the user's terminal opens on
the destination. The node patterns support a node assigned by an active Slurm
interactive allocation; they do not authorize choosing a compute node or
running work outside Slurm.

Without an SSH config, the same path is explicit:

```bash
ssh -J YOUR_RCC_USERNAME@login.ikim.uk-essen.de YOUR_RCC_USERNAME@shellhost.ikim.uk-essen.de
```

See [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md) and
the current institutional RCC connection instructions before changing an
existing workstation configuration.

## File transfer uses the same route, not the same endpoint

The jump service does not contain the RCC research filesystem namespace.
`/homes`, `/groups`, and `/projects` are accessed on the downstream shell-host
tier. Therefore the remote operand of `scp`, `sftp`, or `rsync` is `shellhost`,
not `login.ikim.uk-essen.de`.

Canonical explicit example:

```bash
scp -J YOUR_RCC_USERNAME@login.ikim.uk-essen.de YOUR_RCC_USERNAME@shellhost.ikim.uk-essen.de:/groups/<group>/demo.test1 .
```

SFTP uses:

```bash
sftp -J YOUR_RCC_USERNAME@login.ikim.uk-essen.de YOUR_RCC_USERNAME@shellhost.ikim.uk-essen.de
```

With the SSH configuration above, `scp {{ ssh_target_alias }}:/groups/<group>/demo.test1 .` is
an equivalent shorter form because the `shellhost` entry already carries the
`ProxyJump` setting.

## Names you may see in a saved configuration

`login.ikim.uk-essen.de` and `shellhost.ikim.uk-essen.de` are the current,
stable names. Older saved configurations may also contain a physical
login-backend or old compute-node name, an `id_ikim` key, an `ikim` alias, or
an SSHFS tunnel on local port `6666`; do not reuse those for a new setup. The
approved `{{ ssh_target_alias }}` destination remains the normal user target.
Test the current configuration, and only then remove a superseded entry.

When reviewing a saved configuration:

1. identify which entries belong to RCC;
2. obtain the current RCC configuration through a trusted channel;
3. verify the published host identity independently;
4. test `ssh shellhost` or the explicit `ssh -J YOUR_RCC_USERNAME@login.ikim.uk-essen.de YOUR_RCC_USERNAME@shellhost.ikim.uk-essen.de` path; and
5. remove or archive superseded physical-backend entries only after the stable route works.

Do not disable host-key checking, delete unrelated `known_hosts` entries, or
replace a service alias with a physical node name.

## During a backend maintenance window

RCC may move an approved service alias between equivalent backends. An existing
SSH or VS Code session can disconnect during that change. Reconnect with the
same approved aliases; do not create separate workstation targets for physical
backend names. A diagnostic `hostname` value is not a connection name for users.

A timeout and a changed-host-key warning require different responses:

1. For a timeout, confirm the hospital network or VPN is available, then retry
   the same saved connection once.
2. For a changed-host-key warning, stop and contact RCC support through an
   official channel. Treat it as an infrastructure or security incident.

Never delete the complete `~/.ssh/known_hosts` file, run a blanket
`ssh-keygen -R` command, set `StrictHostKeyChecking no` or `accept-new`, or
accept a replacement key merely to bypass the warning.

## Transfer guidance

> **Service status:** SSH transfer (`scp`, `sftp`, `rsync`) to the shell host
> through the jump host is **ready now**. Existing instrument Samba shares are
> **in service**; RCC sets up each new share for an approved project and
> registered device on request. The RCC Files browser portal is **not yet
> released**.

For SSH-based transfer, use the shell host endpoint through the login jump
service as shown above. An approved SSH route does not make SSHFS the preferred
bulk-transfer method. Large instrument datasets should use SFTP or `rsync` to
the shell host, server-to-server transfer, Samba, or facility-managed automated
ingestion as appropriate. Use SSHFS only for light access to small files and
only with a supported client configuration that preserves the same
jump-host/shell-host separation.
