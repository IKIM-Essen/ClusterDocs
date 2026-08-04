# Windows: recognize an existing SSHFS setup

> **Service status:** project Samba shares are **ready now**. Ardia integration
> is **not yet released**. This historical SSHFS page is not a setup guide for
> either service.

> **Setting up access now? Skip this page.** Follow
> [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md) and use
> the RCC connection settings you were given. This page is only for people who
> already have an SSHFS setup on their Windows computer and need to identify or
> replace it.

This type of setup used WinFsp, SSHFS-Win, SSHFS-Win Manager, an SSH tunnel,
and optionally Windows Task Scheduler.

If you see `login.ikim.uk-essen.de`, `shellhost`, or local port `6666` in a
saved configuration, do not copy those values into a new setup. Ask RCC for
the connection settings to use now.

## SSH settings you may find on an existing computer

Location:

```text
C:\Users\<WINDOWS-USERNAME>\.ssh\config
```

Pattern:

```sshconfig
Host ikim
    HostName login.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_ikim

Host shellhost
    HostName shellhost.ikim.uk-essen.de
    User <RCC-USERNAME>
    IdentityFile ~/.ssh/id_ikim
    ProxyJump ikim
```

Do not reuse this unchanged. Obtain the current RCC configuration and key
instructions from [Account access, SSH, and VS Code](../reference/access-ssh-vscode.md).

## Tunnel command you may find

```powershell
Start-Process ssh -WindowStyle Hidden `
  -ArgumentList "-fN", "-L", `
  "6666:shellhost.ikim.uk-essen.de:22", "shellhost"
```

The SSHFS-Win Manager connection used the forwarded local port.

## How this setup was installed

1. Install a supported WinFsp release.
2. Install a compatible SSHFS-Win release.
3. Install SSHFS-Win Manager.
4. Configure and test SSH.
5. Add the SSHFS connection.
6. Optionally use Task Scheduler to start the tunnel.
7. Test with a small non-sensitive file.

The setup may refer to `/homes/<username>/`, `/groups/<group>/`, or
`/project/<project>/`. Confirm your project path with RCC before transferring
data.

### Recognize the installed software

> **Do not copy values from these screenshots.** They help you recognize an
> existing installation. For a new connection, use the software versions,
> server name, path, and port supplied by RCC.

The WinFsp installer selected the core filesystem component rather than the
developer components:

![WinFsp installer with the Core component selected and developer components disabled](../assets/WinFSP_download.png)

The SSHFS-Win Manager example used a local forwarded connection and a group
path. Do not copy its localhost port, key path, remote path, or automatic-start
choice into a new setup:

![SSHFS-Win Manager basic and advanced connection screens from an existing setup](../assets/sshfs_win_manager.png)

The former optional automation used Windows Task Scheduler. These screenshots
are retained so an existing task can be recognized and removed or migrated:

![Historical Windows Task Scheduler General tab for the background SSH task](../assets/sshfs_win_manager_details1.png)

![Historical Windows Task Scheduler network-event trigger for the background SSH task](../assets/sshfs_win_manager_details2.png)

![Historical Windows Task Scheduler Conditions tab limiting the task to an available network connection](../assets/sshfs_win_manager_conditions.png)

![Historical Windows Task Scheduler Settings tab for the background SSH task](../assets/sshfs_win_manager_settings.png)

Do not create an unattended background tunnel merely because it appears in the
walkthrough. Before changing or recreating it, ask RCC to confirm the server
name, host identity, credential handling, need for automatic mounting, and safe
stop behavior.

## Appropriate use

Use the mount to inspect a report, edit a small text file, copy a sample sheet,
or browse completed results.

Do not use it for complete sequencing runs, live Nanopore output, Ardia exports,
large microscopy datasets, analysis, or hundreds of thousands of files.

Prefer the current RCC transfer portal, SFTP service, server-to-server transfer,
or facility-managed ingestion for instrument data.

Return to [Choosing an instrument-data transfer path](instrument-data-options.md)
before selecting a current transfer method.
