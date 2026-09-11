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

A minimal OpenSSH configuration is:

```sshconfig
Host login.ikim.uk-essen.de
    HostName login.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no

Host shellhost
    HostName shellhost.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump login.ikim.uk-essen.de
    ForwardAgent no

Host c? c?? c??? d?? g?-? g?-??
    HostName %h.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump login.ikim.uk-essen.de
    ForwardAgent no
```

Connect from the workstation with `ssh shellhost`. The login account is
forwarding-only for ordinary users and will not provide an interactive shell;
`ssh login.ikim.uk-essen.de` is therefore not a valid ordinary-user login test.
`ProxyJump` uses the gateway automatically while the user's terminal opens on
the destination. The node patterns support a node assigned by an active Slurm
interactive allocation; they do not authorize choosing a compute node or
running work outside Slurm.

Without an SSH config, the same path is explicit:

```bash
ssh -J login.ikim.uk-essen.de shellhost
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
scp -J login.ikim.uk-essen.de shellhost:/groups/blubb/demo.test1 .
```

SFTP uses:

```bash
sftp -J login.ikim.uk-essen.de shellhost
```

With the SSH configuration above, `scp shellhost:/groups/blubb/demo.test1 .` is
an equivalent shorter form because the `shellhost` entry already carries the
`ProxyJump` setting.

## Names you may see in a saved configuration

Some saved workstation configurations contain physical login-backend names such
as `login1`, `login2`, `is-2`, or `is2-2`. Do not create new workstation targets
for those physical names. Use the stable `login.ikim.uk-essen.de` service as the
jump path and `shellhost` as the ordinary destination.

When reviewing a saved configuration:

1. identify which entries belong to RCC;
2. obtain the current RCC configuration through a trusted channel;
3. verify the published host identity independently;
4. test `ssh shellhost` or the explicit `ssh -J login.ikim.uk-essen.de shellhost` path; and
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

> **Service status:** project Samba shares are **ready now** for approved
> projects and registered devices.

For SSH-based transfer, use the shellhost endpoint through the login jump
service as shown above. An approved SSH route does not make SSHFS the preferred
bulk-transfer method. Large instrument datasets should use the RCC files portal,
approved shellhost SFTP/SCP/rsync route, server-to-server transfer, Samba, or
facility-managed automated ingestion as appropriate. Use SSHFS only for light
access to small files and only with a supported client configuration that
preserves the same jump-host/shell-host separation.
