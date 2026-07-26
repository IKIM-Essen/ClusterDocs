# How to share data safely

Start by deciding **who should receive the data** and **why they are allowed to
receive it**. The right mechanism differs for members of your project, another
RCC group, and someone outside RCC.

| Audience | Recommended route | Avoid |
|---|---|---|
| Members of the same project | Project directory controlled by the project's Unix group | Copies in several personal home directories |
| RCC users outside the current group | Request a project or project membership that creates one shared group for all approved members | Making files readable or writable by every RCC user |
| External collaborators or the public | Approved files portal, governed project service, Coscine or an appropriate repository, depending on purpose and data class | Opening a server port, emailing restricted data, or publishing a project directory |

Before sharing biomedical or otherwise controlled data, confirm that the
project governance, consent or other legal basis, and recipient authorization
cover the disclosure. Technical access does not by itself authorize sharing.

## The recommended model: a project with a shared Unix group

Ask RCC Admin or support for a project that identifies the responsible owner,
purpose, approved members, storage location, and a **shared Unix group**. RCC
adds each named member to that group. Members can then work in the supplied
project path, normally under:

```text
/projects/<project>/
```

This is better than using one person's home directory for durable research
data. The project remains attributable when somebody changes role or leaves,
membership can be reviewed centrally, storage and retention have an owner, and
large shared workloads do not consume a personal quota or depend on one
account.

Never share an RCC password, SSH key, token, or account. Give each person an
individual account and grant access through project membership.

## How Unix group membership works

Every RCC user has exactly one primary group and may have several
**supplementary groups**. An external user's primary group is `collab`; access
to a collaboration's data still comes from explicit project membership, not
from `collab` itself. Belonging to multiple groups is normal: alongside the
primary group, one person may be a member of several supplementary project
groups at the same time.

Check the groups in the current session with:

```bash
id
groups
```

New membership may require a new login session before it appears. Do not try to
work around missing membership by sharing credentials or opening permissions.
If the expected group is absent after reconnecting, ask RCC support to check
the project membership.

An ordinary Unix file has one owner and one owning group. It does not acquire
several owning groups merely because its creator belongs to several groups.
When two organizational groups need the same data, request a project group
whose membership includes the approved people from both groups. For more
complex exceptions, ask RCC whether a reviewed access-control list is
appropriate.

## What setgid means on a shared directory

The set-group-ID bit, or **setgid**, has a useful meaning on a directory: new
files and subdirectories inherit the directory's owning group instead of the
creator's primary group. This keeps a project tree consistently associated
with the project group.

For a project owner or administrator, the intended directory state is
equivalent to:

```bash
shared=/projects/<project>/shared
project_group=<project-group>

chgrp "$project_group" "$shared"
chmod 2770 "$shared"
```

In `2770`, the leading `2` enables setgid, owner and group receive full
directory access, and other RCC users receive no access. The same bit can be
shown symbolically with `chmod g+s DIRECTORY`.

Setgid controls **group inheritance**; it does not automatically make files
group-writable. The project also needs an agreed creation mode or a default ACL
so collaborators can edit new files. RCC may configure this centrally. Do not
recursively change a populated project tree unless the project owner or RCC
support has reviewed the effect on existing permissions and controlled data.

Inspect a path without changing it:

```bash
ls -ld /projects/<project>/shared
namei -l /projects/<project>/shared/path/to/file
getfacl /projects/<project>/shared
```

A setgid **directory** is a collaboration mechanism. This guide does not
recommend setgid executable programs, which have a different and much more
sensitive security meaning.

## Sharing with people in your project

1. Confirm that every recipient appears in the approved project membership.
2. Put the authoritative or shared copy in the supplied project directory.
3. Confirm that the directory owns the project group and has setgid or the
   RCC-provided equivalent.
4. Use a dedicated `incoming`, `shared`, or `results-for-review` directory
   rather than exposing the entire project tree.
5. Check access using names and permissions; never test by asking someone to
   use your account.

For active computation, keep durable inputs and results in the project and
stage high-I/O temporary work to job-local scratch. Shared access does not make
network project storage a suitable scratch disk.

## Sharing with RCC users outside your current group

If the collaboration has an approved research purpose, request either:

- membership for the named people in the existing project; or
- a new cross-group project with its own owner, membership, Unix group and
  storage path.

This is safer and easier to audit than copying files between home directories.
Do not use `chmod o+r`, `chmod 777`, or another “everyone on RCC” permission as
a substitute for project membership. Do not add an entire broad group when
only a few named people need the data.

## A bounded handoff from a home directory

For a small, temporary and appropriately classified handoff, RCC may permit a
group-controlled directory such as:

```text
/homes/<username>/data-for-others/
```

The owner can assign the approved project group and setgid directory mode when
the parent path and RCC policy allow it:

```bash
handoff=/homes/<username>/data-for-others
project_group=<project-group>

mkdir -p "$handoff"
chgrp "$project_group" "$handoff"
chmod 2770 "$handoff"
```

Do not loosen the permissions of the whole home directory. If recipients
cannot traverse the path, ask RCC support for the approved configuration
rather than adding access for all users.

This handoff location remains owned by one person, consumes personal quota,
and may become inaccessible when that account changes. It is therefore not the
authoritative location for instrument data, durable research inputs, shared
analysis, retention, or archival. Move accepted material into the project and
remove the temporary handoff copy according to the agreed retention rule.

## Sharing outside RCC or with the outside world

Filesystem permissions stop at the RCC boundary. Use a service designed for
the intended recipient and data class:

- use the approved RCC files portal or institutional transfer service for a
  named external recipient when that capability and disclosure are approved;
- use a governed project website or application for curated, authenticated
  access—not a direct view of `/projects`;
- use Coscine for a governed retained package when it fits the project's data
  management and planned RCC-to-Coscine flow; and
- use an appropriate public or controlled-access repository for publication,
  with the required metadata, licence, review, and persistent identifier.

Create a deliberate sharing package rather than exporting a working tree.
Include only approved files, remove secrets and unnecessary identifiers, add a
manifest and README, record checksums, and have the responsible project member
review the exact package. Public sharing is an irreversible disclosure; a
world-readable Unix mode is neither a publication workflow nor an approval.

See [Storage and transfer](storage-transfer.md) for transfer commands and
[Class 15](../course/class-15-data-lifecycle.md) for retention and the planned
Coscine path.
