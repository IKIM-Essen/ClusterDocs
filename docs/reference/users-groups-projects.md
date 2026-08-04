# Users, groups, and projects

RCC separates a user's organizational affiliation from access to shared
research data. A **primary group** says where a user belongs; a **project**
brings selected users together so they can exchange data across group
boundaries.

> **Service status:** RCC Admin project and membership workflows are **ready
> now**. Project Samba shares are **ready now** for approved projects. Project
> vhosts, Ardia integration, and RCC-to-Coscine transfer are **not yet
> released**.

## A simple way to remember it

- **Account = your badge.** Every person signs in with their own account.
- **Primary group = your home department.** Every user has exactly one; an
  external collaborator's primary group is `collab`.
- **Project = the shared project room.** Named people can enter even when their
  primary groups are different. A user may belong to several project rooms.

Changing the label on somebody's badge is not how a collaboration is created.
Keep the correct primary group and add the person to the approved project.

## Identity and access model

| Concept | Rule | What it is for |
|---|---|---|
| User | Every person has an individual account. | Attribution, authentication, and auditability. |
| Primary group | Every user has exactly one primary group. | The user's main organizational affiliation and group-level working area. |
| External user | An external user's primary group is `collab`. | A neutral affiliation for collaborators who do not belong to an internal RCC group. |
| Project | A user may join one or more approved projects. | A governed space where selected users from different primary groups can exchange data. |

The primary group and project memberships are independent. Sharing a primary
group does not automatically grant access to every project owned by that group.
Likewise, membership in `collab` does not allow an external user to see other
external users' projects or data. Access to project storage and services comes
from explicit project membership.

## Use a project for cross-group data exchange

Projects are the normal collaboration boundary when data must move between
groups. The project lead identifies the participants, and RCC grants each
participant's individual account membership in the project. Project members
then use the approved project storage, file-transfer service, and project
applications covered by that project's governance.

For example, a user whose primary group is `<group-a>`, a user whose primary
group is `<group-b>`, and an external user whose primary group is `collab` can
all be members of `<project-x>`. They exchange approved data in
`/projects/<project-x>/`; their unrelated group and project data remains
separate.

Use the available storage areas accordingly:

- use home storage for personal configuration and small, non-shared files;
- use group storage for material governed and shared within the primary group;
- use project storage to exchange project data among approved members,
  especially when participants have different primary groups; and
- never use shared accounts, personal home directories, or broad permissions
  as a substitute for project membership.

When a collaborator joins or leaves, ask the project lead to update project
membership. Do not change the user's primary group merely to grant access to
project data. For practical permission and sharing procedures, continue with
[How to share data safely](data-sharing.md).

## What belongs to the project

A project is more than a folder. It is the common boundary for:

- the named people allowed to work together;
- shared project storage and data-transfer access;
- an approved Samba share used by a registered Lab-network instrument or
  acquisition computer;
- a future optional protected vhost when the service is released; and
- the decision to prepare an approved archive set for the future Coscine flow.

Each future vhost will belong to one project and check individual identity plus
project membership. Do not plan one catch-all vhost for unrelated projects.
Coscine archival is a later, reviewed lifecycle step; the RCC-to-Coscine route
is not yet released and is not a live self-service transfer.
