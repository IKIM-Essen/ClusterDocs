# Which RCC connection name should I use?

> Use the RCC connection settings supplied through the rollout page or another
> trusted institutional channel. In these instructions, the connection name is
> `{{ ssh_alias }}`. Do not copy a server address from an old screenshot or a
> colleague's saved configuration.

## Why the name stays the same

RCC aims to give users stable service aliases even when the physical or virtual
systems behind them change. Operations may replace backends, storage gateways,
jump hosts, or proxies while preserving an approved user-facing alias.

Stable service names must never be replaced in user documentation with physical
infrastructure hostnames. Verify the approved RCC host identity through the
current institutional connection instructions rather than accepting a changed
key or copying an old configuration from a colleague.

## Setup to use now

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
the current institutional RCC connection instructions before changing an
existing workstation configuration.

## Names you may see in a saved configuration

Some saved workstation configurations contain `login.ikim.uk-essen.de`,
`shellhost`, or `shellhost.ikim.uk-essen.de`. If you see one of these names,
do not reuse it for a new connection. Get the RCC connection settings you
should use now, test them, and only then remove the saved entry.

When reviewing a saved configuration:

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
