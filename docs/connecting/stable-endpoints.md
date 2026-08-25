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

Use only values supplied by the approved RCC configuration. The gateway block
alone is not a complete user connection: the destination block must route the
shellhost and allocation-backed interactive nodes through the gateway.

```sshconfig
Host {{ ssh_gateway_alias }}
    HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
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

Some saved workstation configurations contain `login.ikim.uk-essen.de` or a
physical login-backend name. Do not reuse those names for a new gateway
connection. The approved `{{ ssh_target_alias }}` destination remains the
normal user target. Get the current RCC connection settings, test them, and
only then remove a superseded gateway entry.

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

> **Service status:** project Samba shares are **ready now** for approved
> projects and registered devices.

An approved SSH alias does not make SSHFS the preferred bulk-transfer method.
Large instrument datasets should use the RCC files portal, approved SFTP,
server-to-server transfer, Samba or facility-managed automated ingestion as
appropriate. Use SSHFS only for light access to small files.
