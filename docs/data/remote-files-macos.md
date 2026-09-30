# RCC Remote Files and encrypted Time Machine on macOS

> **Service status: not yet released.** This page documents the intended RCC
> macOS service and recovery procedure. Do not remove an existing working backup
> until RCC has announced your Remote Files and Time Machine enrollment as
> accepted.

RCC Remote Files is designed to let an enrolled Mac use three separate RCC
storage surfaces through one restricted, encrypted device connection:

- **Home** — your personal RCC home directory;
- **Groups** — only primary-group folders that RCC has explicitly approved for
  Mac sharing; and
- **TimeMachine** — an optional per-user network backup target.

Project data remains in `/projects/<project>` and is **not** exposed through
Remote Files. RCC Files/SFTPGo remains the normal user-facing transfer surface
for project data.

## Why this replaces a desk-side backup disk

The goal is that an RCC user should not need a USB or desktop hard drive merely
to protect a work Mac.

For Time Machine, RCC requires all three encryption layers:

1. the Mac-to-RCC SMB connection uses mandatory SMB 3.1.1 encryption and
   signing;
2. the Time Machine backup set itself is encrypted; and
3. the RCC backup storage is encrypted at rest and quota-controlled.

RCC does not accept a Time Machine pilot merely because a backup completes.

## Authentication and 2FA

Enrollment and security-sensitive changes require fresh strong RCC
authentication / 2FA:

- enroll a Mac;
- replace a lost or retired Mac;
- rotate the Remote Files password;
- revoke a device;
- recover or re-enroll access; and
- administrative changes to the service.

Scheduled Time Machine backups and normal Finder reconnects do **not** display a
second-factor prompt every time. They use the previously enrolled device
identity plus the separate Remote Files SMB credential stored in the Mac
Keychain. Otherwise unattended Time Machine backups could not work.

If the Mac is lost, revoke it through RCC before enrolling a replacement.

## Network model

The Mac uses a Tailscale-compatible client pointed at RCC Headscale. eduroam is
only the underlying Internet connection.

RCC does **not** expose SMB port 445 directly to eduroam or the public Internet.
The enrolled Mac may reach only the dedicated Remote Files server on the SMB
port allowed by RCC policy.

RCC does not require the Mac to accept RCC DNS or subnet routes and does not
enable Tailscale SSH on the Mac.

## First-time setup

After RCC announces the service for your account:

1. Sign into RCC Admin and open **Remote Files**.
2. Complete the requested strong authentication / 2FA.
3. Enroll the Mac with the one-use overlay enrollment material shown by RCC.
4. Delete the one-use enrollment file immediately after the client has joined.
5. Return to RCC Admin and confirm the enrolled device.
6. Save the separate Remote Files password in the Mac login Keychain.

Do not put the enrollment key or Remote Files password in email, chat, tickets,
shell history, or Git.

## Connect Home and Groups

In Finder choose **Go → Connect to Server…**.

Use the exact RCC Remote Files server address shown by RCC Admin, for example:

```text
smb://<RCC-REMOTE-FILES-SERVER>/Home
smb://<RCC-REMOTE-FILES-SERVER>/Groups
```

Save the Remote Files credential in Keychain when macOS offers to remember it.

The **Groups** share contains only group folders released for Mac sharing. A
primary group must first have its group storage reviewed so project/study data
that belongs in `/projects` is moved out.

### What belongs in a group folder

Good examples are material genuinely owned by the organizational working group:

- shared group documentation;
- group-wide templates and reference material;
- non-project administrative material;
- common small resources intended for all members of that primary group.

Move material to a project when it has a scientific study purpose, named
project team, data owner, research-data lifecycle, project-specific retention,
or collaborators outside the primary group.

## Configure encrypted Time Machine

RCC Time Machine is enabled separately from Home/Groups.

When RCC has enabled it for your account:

1. Connect in Finder to:

   ```text
   smb://<RCC-REMOTE-FILES-SERVER>/TimeMachine
   ```

2. Open **System Settings → General → Time Machine**.
3. Add/select the mounted RCC network disk.
4. Enable backup encryption when macOS asks for the Time Machine backup
   password.
5. Store the Time Machine encryption password in an approved password manager
   or other secure recovery location. Do not store the only copy on the Mac
   being backed up.
6. Allow the first full backup to complete while connected to a reliable
   network.

RCC acceptance checks verify that the resulting Time Machine backup set is
encrypted. An unencrypted backup is not an accepted RCC backup.

Remote Files does not rely on Bonjour/mDNS discovery across the RCC overlay;
connect to the SMB target explicitly first.

## Everyday operation

After enrollment, Finder and Time Machine should reconnect without another
browser 2FA prompt.

RCC expects the service to recover across:

- Mac sleep/wake;
- moving between eduroam access points;
- ordinary network interruption; and
- direct versus RCC-relayed overlay paths.

If Home/Groups reconnect but Time Machine does not, do not delete the existing
backup set. Check the Remote Files service state and contact RCC support.

## Restore a deleted or older file

For ordinary files protected by Time Machine:

1. Make sure the Mac is connected to the RCC overlay.
2. Confirm the RCC Time Machine network disk is reachable.
3. Open Time Machine from macOS.
4. Navigate to the required date/version.
5. Restore into the normal location or into a temporary local folder when you
   want to compare before replacing a current file.
6. Verify important restored research-support files before deleting the current
   copy.

Project research data should normally be recovered from the project/storage
recovery process, not from a user's Mac backup.

## Replace a failed or lost Mac

Do not copy the old overlay enrollment identity to another computer.

1. From a trusted device, sign into RCC Admin.
2. Complete fresh strong authentication / 2FA.
3. Revoke the lost/failed Mac.
4. Enroll the replacement Mac as a new device.
5. Connect to the RCC Time Machine target.
6. During macOS Setup Assistant / Migration Assistant, select the network Time
   Machine backup when supported by the current macOS workflow, or restore
   required files after the new Mac is configured.
7. Enter the Time Machine backup encryption password.
8. After recovery, verify Home and approved Groups access and start a new backup
   from the replacement Mac.

If the Time Machine encryption password is lost, RCC cannot treat bypassing that
encryption as a normal recovery path.

## Remote Files password rotation

A rotation changes the SMB credential used by Home, Groups, and Time Machine.

After rotation:

1. disconnect existing RCC SMB shares;
2. update/remove the old RCC Remote Files password in Keychain;
3. reconnect Home and Groups with the new password;
4. reconnect the TimeMachine share; and
5. verify a new scheduled backup succeeds.

An SMB session that stayed open across a password rotation is not proof that the
old password still works.

## Lost device or suspected compromise

From a trusted device:

1. sign into RCC Admin;
2. complete fresh strong authentication / 2FA;
3. revoke the affected Mac immediately;
4. do not reuse its old overlay identity or Remote Files credential; and
5. enroll a replacement only after the incident/recovery procedure says it is
   safe.

RCC revocation is designed to remove both the enrolled overlay device and its
Remote Files SMB access.

## What RCC still has to accept before release

The service is not considered mature merely because the source configuration
exists. RCC operations must retain successful evidence for:

- Headscale backup and isolated restore;
- RCC DERP relay and restricted-network behavior;
- exact supported Tailscale-compatible client version;
- exact supported Samba build against the current macOS Time Machine client;
- encrypted Time Machine backup-set verification;
- encrypted server-side backup storage and enforced quota;
- full backup, incremental backup, file restore and replacement-Mac recovery;
- sleep/wake and eduroam roaming;
- credential rotation and lost-device revocation; and
- no direct SMB exposure on the campus or Internet interface.

Until those checks are accepted, keep an existing approved backup method.
