# Users, groups, and projects

RCC separates a user's organizational affiliation from access to shared
research data. A **primary group** says where a user belongs; a **project**
brings selected users together so they can exchange data across group
boundaries.

> **Service status:** RCC workers, project storage, and project Unix groups are
> **ready now**; RCC support creates projects and memberships on request. The
> RCC Admin self-service portal is **not yet released**. Existing instrument
> Samba shares are **in service**, and RCC sets up each new share on request.
> Project vhosts, Ardia integration, and RCC-to-Coscine transfer are **not yet
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

## Smaller shared areas within your primary group

Some RCC groups have separate working areas for **staff**, **students**, **guests**, or people who maintain an **archive**. Your group lead and RCC support decide which of these are needed. They are not separate organizations or research projects.

A typical example (using the DS group as an illustration, **not a claim about your group's current setup**) is:

```text
/groups/ds/                    common entry point for DS members
  ds-staff/                    DS staff working area
  ds-students/                 DS student working area
  ds-guests/                   DS guest working area
  ds-archive/                  archive maintenance area
```

The name of your actual area may differ, especially for groups that have older folder names. You will only see or enter the folders your membership permits. Ask your group lead or RCC support for your group's current approved paths.

**Your account still has just one Unix primary group.** For example, the person in the DS group retains primary group `ds`. RCC can also grant that person supplementary Unix groups such as `ds-students`, or a separate research project's group. Staff supervising students may have both `ds-staff` and `ds-students` access. Archive membership is an additional permission, not a fourth kind of person.

Your primary group is not a grant to see everything belonging to that organization. A restricted student, staff, or guest area has its *own* Unix group and directory permissions. When you leave a group or a project, RCC updates membership under the appropriate approved workflow.

### Why files normally stay shareable without you changing permissions

RCC configures group-owned working directories with the Unix **setgid** bit. It makes a newly created file inherit the *folder's* Unix group, even when the creator has several groups. Alongside RCC's ordinary collaborative `umask 0002`, this normally means new files can be edited by the intended group without everyone learning `chmod` and `chgrp`.

You can inspect your current login and a shared folder without changing anything:

```bash
id
groups
ls -ld /groups/<your-group>
ls -ld /groups/<your-group>/<your-approved-area>
```

An example listing might include `drwxrws---`. The **s** indicates the directory inherits its Unix group for newly created entries. Only the approved group can normally enter it. Setgid does **not** repair old file permissions, override other access controls, or make an archive read-only.

**Do not run `chmod -R`, `chmod 777`, or change an entire group directory's ownership to fix “Permission denied.”** A missing membership, an old login session, the wrong working folder, or a path that is deliberately restricted is much more likely. Reconnect once after an approved membership change; if it still fails, send RCC support the exact path and the output of `id` and `ls -ld` (do not send restricted file contents).

### Group working area or project?

Use your subgroup's working area for ongoing **small organizational** tasks and material shared within that specific cohort. **Do not use `/groups` or `/homes` for large-volume research data or data to be computed on at scale.** Use a **project** when work has a defined scientific purpose, team, datasets, results, responsibility or lifecycle, even if everyone currently belongs to the same primary group. The project has its own membership and lives under `/projects/<project>/`. For high-I/O analysis, use temporary job-local scratch and keep durable inputs and outputs in the project.

See [Storage and transfer](storage-transfer.md) before moving existing datasets or choosing a large-data workflow.

An archive *working area* is not automatically a frozen or retained scientific archive. Ask the project lead for the approved retention and archival process.

### Your group's rollout

RCC introduces the revised group/project experience **one primary group at a time**. Your group's leads review who belongs, who should have staff/student/guest area access, which old groups are really projects, and which people need another organizational home. Until that review is completed and the relevant features are accepted, your existing Unix groups and ordinary access remain in place; there is no cluster-wide forced conversion.

### For group leads: what the onboarding meeting decides

RCC will bring an up-to-date membership overview and review it with you. We will ask five practical questions:

1. **Who belongs here?** Confirm current people and identify accounts that have moved, left, are guests, or belong to another primary group.
2. **Who can see which working area?** Classify staff, students and guests, and name anyone who additionally needs archive or another restricted area.
3. **Which older groups are actually research projects?** Keep their existing members and data access while reviewing who will lead each project and where its project data should live.
4. **Which access must be restricted?** Confirm that a guest cannot read staff files, and that future shared files inherit the correct Unix group automatically.
5. **Which new RCC features should the group use?** Agree a phased rollout rather than changing every person's work routine at once.

The meeting records decisions; RCC staff apply changes only after checking their effects. You need not understand LDAP group entries, numeric Unix GIDs, or `chmod` to take part.

If the membership list is wrong, ask the group lead or RCC support to correct it using the reviewed membership editor. **Do not change another user's account or move data yourself as a substitute for the review.** A saved review decision does not necessarily mean LDAP membership or directory access has changed yet.

For further detail on directory permissions and sharing, see [How to share data safely](data-sharing.md).

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
