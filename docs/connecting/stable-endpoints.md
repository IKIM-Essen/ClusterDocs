# RCC endpoint compatibility and legacy names

> **Current configuration wins:** Use the RCC alias and host configuration
> published through the rollout page or another trusted institutional channel.
> In this documentation the configured alias is `{{ ssh_alias }}`. Do not infer
> a current endpoint from a historical example.

## Stable names and replaceable backends

RCC aims to give users stable service aliases even when the physical or virtual
systems behind them change. Operations may replace backends, storage gateways,
jump hosts, or proxies while preserving an approved user-facing alias.

Stable service names must never be replaced in user documentation with physical
infrastructure hostnames. The current host-identity policy also requires users
to verify the approved RCC host identity rather than accepting a changed key or
copying an old configuration from a colleague.

## Current SSH pattern

Use only values supplied by the approved RCC configuration:

```sshconfig
Host {{ ssh_alias }}
    HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no
```

See [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md) and
the [SSH host-identity policy](../policies/ssh-host-identity.md) before changing
an existing workstation configuration.

## Historical names

Older ClusterDocs and workstation setups may contain names such as
`login.ikim.uk-essen.de`, `shellhost`, or `shellhost.ikim.uk-essen.de`. The
legacy Windows and macOS pages retain those strings only so an existing setup
can be identified and migrated. These historical names are not a statement
that they are the current production route.

When reviewing a historical configuration:

1. identify which entries belong to RCC;
2. obtain the current RCC configuration through a trusted channel;
3. verify the published host identity independently;
4. test the approved alias with one bounded connection attempt; and
5. remove or archive superseded entries only after the replacement works.

Do not disable host-key checking, delete unrelated `known_hosts` entries, or
replace a service alias with a physical node name.

## Transfer guidance

An approved SSH alias does not make SSHFS the preferred bulk-transfer method.
Large instrument datasets should use the RCC files portal, approved SFTP,
server-to-server transfer, Samba or facility-managed automated ingestion as
appropriate. Use SSHFS only for light access to small files.
