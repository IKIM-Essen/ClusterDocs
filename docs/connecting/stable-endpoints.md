# Which RCC connection name should I use?

> Use the current RCC connection settings supplied through a trusted
> institutional channel. `{{ ssh_gateway_alias }}` is the forwarding gateway;
> `{{ ssh_target_alias }}` is the normal workstation target. Do not copy a
> server address from an old screenshot or a colleague's saved configuration.

## Why the name stays the same

RCC aims to give users stable service aliases even when the physical or virtual
systems behind them change. Operations may replace backends, storage gateways,
jump hosts, or proxies while preserving an approved user-facing alias.

Stable service names must never be replaced in user documentation with physical
infrastructure hostnames. Verify the approved RCC host identity through the
current institutional connection instructions rather than accepting a changed
key or copying an old configuration from a colleague.

## Setup to use now

`login.ikim.uk-essen.de` is the stable public RCC jump host and
`shellhost.ikim.uk-essen.de` is the stable shell host. The gateway block
alone is not a complete user connection: the destination block must route the
shellhost and allocation-backed interactive nodes through the gateway.

```sshconfig
Host {{ ssh_gateway_alias }}
    HostName login.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no

Host {{ ssh_target_alias }} c? c?? c??? d?? g?-? g?-??
    HostName %h.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump {{ ssh_gateway_alias }}
    ForwardAgent no
```

Connect from the workstation with `ssh {{ ssh_target_alias }}`. The
`{{ ssh_gateway_alias }}` account is forwarding-only and will not provide an
interactive shell; `ssh {{ ssh_gateway_alias }}` is not a valid login test.
`ProxyJump` uses the gateway automatically while the user's terminal opens on
the destination. The node patterns support a node assigned by an active Slurm
interactive allocation; they do not authorize choosing a compute node or
running work outside Slurm.

See [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md) and
the current institutional RCC connection instructions before changing an
existing workstation configuration.

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
4. test the approved alias with one bounded connection attempt; and
5. remove or archive superseded entries only after the replacement works.

Do not disable host-key checking, delete unrelated `known_hosts` entries, or
replace a service alias with a physical node name.

## During a backend maintenance window

RCC may move an approved connection alias between equivalent backends. An
existing SSH or VS Code session can disconnect during that change. Reconnect
with the same approved alias; do not create separate workstation targets for
physical backend names. A diagnostic `hostname` value is not a connection name
for users.

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

An approved SSH alias does not make SSHFS the preferred bulk-transfer method.
Large instrument datasets should use SFTP or `rsync` to the shell host,
server-to-server transfer, Samba or facility-managed automated ingestion as
appropriate. Use SSHFS only for light access to small files.
