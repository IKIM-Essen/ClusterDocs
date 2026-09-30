# Mac files and encrypted RCC backups

> **Service status: not yet released.** RCC Remote Files and network Time Machine
> are being prepared. Keep the existing backup disk at your work desktop until
> RCC accepts the encrypted work backup. Keep the separate backup disk at home
> for full Mac replacement. This page does not announce a live endpoint.

RCC Remote Files is intended to give your Mac access to your Home folder, your
approved primary working group's folder, and a separate encrypted Time Machine
backup destination. Project datasets and results stay in governed project storage.
A mounted Home or Groups folder is not itself a backup of your Mac.

The RCC Admin page will show three distinct Finder destinations on the issued
server: **My home folder** (`/Home`), **My working group** (`/Groups`) and
**Mac backup** (`/TimeMachine`). Working-group access requires approval;
Mac backup remains marked pending until its own acceptance. Use the full address
shown by RCC Admin rather than adding these paths to a guessed server name.

## Before joining the pilot

RCC supplies the accepted server address and enrollment instructions. Do not use
an address copied from an example or expose SMB port 445 to the Internet.
You need an RCC account with strong two-factor authentication, FileVault enabled,
and a way to recover the RCC Time Machine encryption password without the work
Mac. Confirm that the separate home backup disk is also encrypted,
and keep it and its password in their normal secure home location. Never put either password in a support ticket, Git repository,
screenshot or test report.

Enrollment, credential rotation and recovery enrollment require strong 2FA.
Scheduled backups reconnect using the enrolled device and a separate Files
credential stored in Keychain. They cannot prompt for a second factor on every
scheduled run. This is a persistent device session, not fresh interactive 2FA
for each backup. The first-backup encryption admission workflow is still a
release prerequisite; RCC does not require management of your Mac.

## Connect and make the first backup

1. Follow the RCC Admin Remote Files enrollment instructions using strong 2FA.
2. Connect the approved Tailscale client to the RCC Headscale service. Follow the
   issued configuration; do not enable subnet routes or inbound services.
3. In Finder, choose **Go → Connect to Server**. Use the exact Home or Groups
   SMB address issued by RCC and the separate Files credential, not your RCC
   account password. An unapproved group is intentionally unavailable.
4. Add the issued TimeMachine destination in macOS Time Machine settings and
   enable **Encrypt Backups**. Store the encryption password in the approved
   recovery system. It is separate from the Files credential.
5. Complete the initial backup. RCC storage is already encrypted while it is
   created, but **your first RCC backup is not yet accepted**. An operator checks
   that the Mac's backup bundle is encrypted on the exact RCC destination. If
   encryption was missed, keep your existing work-desktop backup disk and make
   a new encrypted RCC backup with RCC's help; do not delete a backup yourself.
   RCC also checks an incremental backup, sleep/wake reconnection, capacity
   limits and a selected-file restore with you.

RCC will ask you to repeat the short encryption check every 90 days. If the
reviewed result is missing or older than 90 days, RCC shows the worksite backup
health as **Unknown** until a new check is reviewed. This does not erase your
backup or disconnect your Mac. It also does not replace normal monitoring that
the backup is recent and restorable.

Network encryption, server disk encryption and encrypted Time Machine backups
are different protections. RCC requires all three. A successful upload or a
checked checkbox alone does not establish that the recovery test passed.

## Restore a file

Connect to the RCC overlay and your backup destination, open Time Machine,
choose the date and file, and restore it. Open the restored file to check it.
For an important recovery, preserve the current file separately first.
Report a failed or stale backup to RCC; do not delete the backup bundle to
"repair" it.

## Recover after a lost, replaced or erased Mac

1. Contact RCC and revoke the old Mac's Remote Files access if it is lost or
   untrusted.
2. Use the **separate backup disk kept at home** as the source for full Mac
   replacement. On the replacement Mac, use Migration Assistant and select
   **From a Mac, Time Machine or startup disk**. You need that disk's own
   encryption password. Do not depend on the RCC overlay being available during
   macOS Recovery or initial Setup Assistant.
3. Open representative restored files and applications. Confirm FileVault is on.
4. Sign in to RCC Admin using strong 2FA and enroll the replacement Mac. Rejoin
   the RCC overlay and use the newly issued Files credential for Home and any
   approved Groups share. The old Mac must remain revoked.
5. If you need an older work file from the RCC backup, connect to the RCC
   TimeMachine share and use its **separate** encryption password. Keep the
   previous Mac's RCC backup bundle until RCC approves its retention/disposal.
6. Start a new encrypted RCC backup from the replacement Mac. RCC verifies its
   encryption, a later incremental backup and a small file restore.

Apple documents [restoring a Mac with Migration Assistant](https://support.apple.com/102551).
The encrypted home disk remains the full-machine recovery path. Losing the RCC backup
password can make that additional copy unusable; RCC cannot bypass its encryption.
Keep the RCC password available away from the work Mac.

## Working-group folders

Only your reviewed primary working group is exposed. Before publication, the
group lead and RCC must identify project datasets, intermediate files, research
results and controlled data, and arrange their reviewed migration to the correct
project. Group documents and small common resources may remain when their access
boundary is appropriate. Do not move or delete other people's data yourself.
New project data must not accumulate in the shared group folder after approval.

## When can the desktop backup disk be retired?

Only after RCC confirms the service is released and your initial/incremental
worksite backups, encrypted-bundle checks, selected-file restore, home-disk
recovery route and replacement-Mac re-enrollment have passed. RCC must also
accept server recovery, monitoring, capacity and lost-device revocation. Keep
the home backup disk as the independent full-Mac recovery source. Until the
worksite service is accepted, retain the existing disk at the work desktop.
