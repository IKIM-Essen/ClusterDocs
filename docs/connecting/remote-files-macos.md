# Planned macOS Remote Files and encrypted Time Machine through RCC

RCC is preparing a managed macOS Remote Files service so users can reach their
RCC home directory and an approved primary working-group directory from a Mac,
and can use encrypted network Time Machine backups instead of maintaining a
desktop USB backup disk.

> **Service status: not yet released.** Do not remove an existing backup disk or
> treat RCC as your workstation backup until RCC announces general availability
> and your Mac has passed the documented restore test.

The Mac uses a Tailscale-compatible client pointed at **RCC Headscale**. It does
not join a personal hosted Tailscale network. TCP/445 is not opened directly to
eduroam or the Internet: SMB is reachable only over the enrolled RCC overlay.

## What will be available

After release, an enrolled Mac can use:

- **Home** — the authenticated user's RCC home directory;
- **Groups** — only the user's primary working group, and only after that group
  has been reviewed for Remote Files publication;
- **TimeMachine** — a per-user network Time Machine destination when the backup
  capability has separately passed RCC acceptance.

Project storage is deliberately not exposed through Remote Files.

## Why Groups needs a review first

The primary working-group directory is not a substitute for governed project
storage. Before RCC publishes a group to Macs, the working group must review its
group directory and move project-like material to the appropriate
`/projects/<project>`.

That includes, in particular:

- raw or derived project datasets;
- durable workflow intermediates or results;
- participant, patient, or other project-governed data;
- material whose access should follow project membership rather than primary
  group membership.

The remotely published group directory should contain only material whose
authorization really is the primary working-group boundary, such as small common
resources, shared templates, internal working documents, or non-project
collaborative material.

RCC does not attempt to infer this safely from filename extensions or file size.
The group needs an explicit review before publication.

## Enrollment and two-factor authentication

Enrollment and every consequential access change require **strong RCC
two-factor authentication**: device enrollment/confirmation, Files-password
rotation, device revocation, and recovery enrollment all require a fresh RCC
strong-authentication ceremony.

Scheduled Time Machine backups and normal Finder reconnection do **not** prompt
for a user-present second factor on every SMB connection. That would make
unattended backups impossible. The unattended data path instead requires both:

1. the Mac's RCC Headscale/Tailscale device identity; and
2. the separate generated RCC Remote Files SMB credential stored in the Mac
   login Keychain.

FileVault is required on the Mac. This two-credential unattended path should not
be confused with a fresh user-present MFA ceremony.

## Connect Home and Groups

RCC Admin will display the reviewed overlay server address and a one-time Files
credential. On macOS:

1. choose **Go → Connect to Server…** in Finder;
2. connect to `smb://<RCC-overlay-address>/Home`;
3. save the separate Files credential in Keychain when prompted;
4. if your primary working group has been approved, also connect to
   `smb://<RCC-overlay-address>/Groups`.

Remote Files does not rely on Bonjour/mDNS discovery or on RCC MagicDNS. An
unapproved working group must fail closed.

## Configure encrypted Time Machine

RCC requires encryption in three places:

- the SMB connection is encrypted in transit;
- the Time Machine backup bundle itself must be encrypted by macOS;
- the RCC backing filesystem must be encrypted at rest.

When RCC enables Time Machine for your account:

1. connect in Finder to `smb://<RCC-overlay-address>/TimeMachine`;
2. open **System Settings → General → Time Machine** and select the mounted
   network disk;
3. enable Time Machine backup encryption;
4. store the Time Machine encryption password in the institutionally approved
   recovery-custody/password-manager workflow;
5. complete the first backup;
6. complete an incremental backup;
7. perform an actual restore test before retiring any local USB backup disk.

RCC does not keep a hidden bypass key for an encrypted Time Machine backup. If
the encryption password is lost and no approved recovery copy exists, that
backup is not recoverable.

## Recover files

For an ordinary deleted or damaged file, connect the Mac to the RCC overlay,
open Time Machine, and restore the required file or version.

For a network Time Machine destination, use Time Machine's **Verify Backups**
function if backup integrity is in doubt. A backup that has never been restored
is not considered sufficient evidence for replacing the previous backup method.

## Replace or reinstall a Mac

If the old Mac is lost or untrusted:

1. revoke it in RCC Admin;
2. install or recover macOS and enable FileVault;
3. use strong RCC two-factor authentication to enroll the replacement Mac;
4. connect to the RCC Headscale service and confirm the new device;
5. connect to your TimeMachine SMB destination;
6. recover the Time Machine encryption password from its approved custody;
7. use macOS Migration Assistant for full-machine recovery, or Time Machine for
   selected files;
8. complete a new backup and another small restore test.

A lost device must not remain usable merely because its old SMB password is
still present in a Keychain.

## eduroam and relay performance

On eduroam, the Tailscale-compatible client will use a direct encrypted path
when possible and can fall back to an RCC-operated DERP relay when direct
connectivity is unavailable.

An initial Time Machine backup is sustained bulk traffic. RCC will not declare
the service generally available until forced-relay testing shows that this load
does not degrade remote-console/PiKVM access and that relay capacity has adequate
headroom.

## What this service is not

- It is not a way to mount `/projects` on a Mac.
- It is not an alternative project-sharing mechanism.
- It does not expose SMB directly on eduroam.
- It does not make the Mac a trusted RCC compute node.
- It does not remove the need for project-specific retention and archival policy.
- It is not released merely because the source code exists.

Until RCC announces general availability, keep your existing verified backup
method in place.
