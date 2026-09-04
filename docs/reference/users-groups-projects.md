# Users, groups, and projects

RCC separates a user's organizational affiliation from access to shared
research data. A **primary group** says where a user belongs; a **project**
brings selected users together so they can exchange data across group
boundaries.

> **Service status:** RCC Admin project and membership workflows are an
> **invite-only pilot**. Project Samba shares are **ready now** for approved
> projects. Project
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

## Groups do have benefits—but a different purpose

A primary group is useful. It gives a stable organizational affiliation, a
home for material genuinely shared by that department or unit, and a sensible
place for group-level contacts or defaults. Those benefits do not turn it into
the access boundary for every study led by somebody in the group.

Use this decision rule:

| Question | Use |
|---|---|
| Is this about where the person organizationally belongs? | Primary group |
| Is the material only for members of that one organizational group? | `/groups/<primary-group>/` |
| Does the work have a scientific purpose, named team, data owner, or lifecycle? | Project |
| Are collaborators from different groups or institutions involved? | Project |
| Is this personal shell configuration or a small private working file? | Home |

When in doubt for research data, choose a project. It makes membership,
ownership, purpose, services, storage, retention, and handover explicit.

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

## Organise storage for a large science team

Use one project when the team shares the same approved purpose, governance,
owner, membership model, sensitivity, and retention rules. Create separate
projects when one of those boundaries is materially different. Do not create a
new project for every script, sample batch, or temporary analysis.

A large project can stay understandable with a documented internal layout:

```text
/projects/<project>/
├── README.md          # owner, purpose, contacts, layout, retention
├── incoming/          # newly received material awaiting verification
├── raw/               # verified authoritative inputs; treat as read-only
├── reference/         # named and versioned reference data
├── workflows/         # code, configuration, environments, documentation
├── analyses/          # one directory per study, release, or analysis unit
├── results/           # validated shared outputs
├── metadata/          # manifests, checksums, provenance, data dictionaries
├── shared/            # intentional team exchange, not an unowned dumping area
└── archive-staging/   # reviewed candidate set, not an automatic archive
```

This is a project-internal convention, not a new RCC top-level namespace. Keep
the user-visible shared roots limited to `/homes/<user>`,
`/groups/<primary-group>`, and `/projects/<project>`. Job-local `/local` is for
temporary compute work and is not another collaborative storage tier.

For every large project:

1. Put the accountable owner, scientific purpose, contacts, and directory
   meanings in the top-level `README.md`.
2. Define who may add data, validate incoming material, publish results, and
   approve archival or deletion.
3. Give analyses stable identifiers and keep their code and configuration in
   version control.
4. Treat `raw/` as authoritative input and avoid editing it in place.
5. Write active high-I/O intermediates to job-local scratch when appropriate,
   then return declared results and evidence to the project.
6. Review membership regularly and remove access through the project workflow,
   never through broad permission changes.
7. Separate storage cleanup from scientific or archival acceptance; a copied
   file is not automatically a verified archive.

Avoid opaque personal folders at the project root, duplicated datasets in many
team members' homes, shared human accounts, and recursive `chmod` fixes. Those
patterns obscure ownership and make departure, review, and cleanup harder.
