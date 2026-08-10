# Data lifecycle TL;DR

This is the short version for anyone who creates, transfers, analyses, or
archives research data on RCC.

> **Service status:** project Samba ingestion and RCC workers are **ready now**.
> Ardia integration, project vhosts, and RCC-to-Coscine transfer are **not yet
> released**. This page marks their intended place in the lifecycle; it does
> not activate them.

## First understand people and projects

Every person uses an individual RCC account and has exactly one **primary
group**, representing their home department or organisational affiliation. A
**project** is different: it brings named, approved people from one or more
primary groups into one shared research workspace.

In plain language, your primary group says where you belong; project membership
says which collaborative data you may use. Instrument data and shared analysis
inputs and results belong to the project, not to one person's home directory.
Future project vhosts and later archive decisions will use the same project
boundary after those services are released.

## The whole path

```text
registered Lab-network instrument
    -> approved project Samba share [ready]
       or future Ardia integration [not yet released]
    -> approved RCC project/incoming
    -> job-local analysis workspace
    -> approved RCC project/results
    -> reviewed and frozen archive set
    -> future verified Coscine archive [not yet released]
    -> recorded RCC retention or deletion
```

The most important rule is simple:

> Research data belongs to a governed project, not a user's home directory.
> Temporary high-I/O work belongs on job-local storage. An approved, documented
> final set can move to Coscine after the transfer service is released and the
> destination is verified.

## 1. Start with the project

Before moving instrument data, identify:

- the approved RCC project;
- the responsible project owner;
- the permitted purpose and data classification;
- who needs access;
- the authoritative source;
- expected size and file count;
- retention or review requirements; and
- who will verify the transfer.

Instrument data must land in the named project area. Do **not** put it in
`/home/<user>`, even temporarily as the routine transfer path.

### Consider the Lab network for the device

A suitable registered instrument or acquisition workstation can be connected
to the **Lab network**. This removes general direct Internet connectivity and
reduces exposure while preserving:

- direct access to explicitly approved server endpoints and services, such as
  an approved project Samba share or managed acquisition service; and
- limited outbound web access through an explicit HTTP proxy, for example for
  approved software or vendor updates.

The proxy does not make the device reachable from the Internet, and access to
one server does not grant general RCC access. RCC must review the device owner,
updates, licensing, vendor support, server dependencies, credentials, and data
flow before connection. Do not plug in an unregistered device or guess proxy
settings. See [how RCC and the Lab network work together](../resources/how-it-all-works.md).

For non-technical users, a **Samba share** looks like a normal network folder
on an instrument or Windows acquisition computer. Behind the scenes it is
restricted to the approved project. RCC provides the exact connection; do not
reuse another project's share or put the data in a personal folder. Wait for a
run or supported export to complete before transfer unless RCC and the facility
have approved a purpose-built continuous-ingestion workflow. **Ardia
integration is not yet released**; its future mass-spectrometry flow will use a
vendor-supported integration or export path.

Project storage matters for governance and legal compliance because it connects
the data to an approved purpose, an accountable owner, managed membership, and
project-specific retention and deletion decisions. A personal directory makes
one account the accidental owner and creates problems when staff, students, or
collaborators change roles or leave.

Project storage also matters for performance. Home storage is intended for
personal configuration, small source files, and limited working material—not
large recurring transfers or instrument trees containing hundreds of thousands
of files. Those workloads can exhaust personal quota and create filesystem
metadata load that affects interactive use.

## 2. Protect acquisition and verify ingestion

Wait until the instrument run or supported export is complete. Preserve the
authoritative original according to facility policy. Do not assume that a
derived FASTQ, TIFF export, spreadsheet, or analysis result replaces raw data.

For each handoff:

1. freeze or clearly identify the completed source;
2. record file count, total bytes, and important completion markers;
3. create checksums or use a validated transfer report;
4. transfer directly to the approved RCC project where possible;
5. verify the destination; and
6. record who accepted the handoff.

Do not delete the instrument or facility copy merely because an upload command
finished. Verification must happen first.

## 3. Compute locally, keep durable data in the project

RCC project storage is the durable team location for approved inputs, code,
metadata, provenance, and validated results. It is not the best place for every
temporary read and write made by an active job.

For I/O-intensive work:

1. submit the computation through Slurm;
2. copy or stage the required input subset to job-local storage;
3. run temporary, random, or metadata-heavy I/O locally;
4. validate the output;
5. copy required results, logs, parameters, and provenance back to the project;
6. verify the published result; and
7. allow temporary job-local data to be cleaned up.

Never rely on job-local storage after the job ends. Never leave the only useful
result there. Do not solve shared-storage performance problems by moving
authoritative research data into home storage.

## 4. Decide what should survive

Before archiving, classify the project content:

| Content | Default decision |
|---|---|
| Authoritative raw or acquired data | Retain when required by the approved plan |
| Curated inputs | Retain with provenance to the source |
| Validated results | Retain with code, parameters, environment, and review evidence |
| Publication package | Preserve the exact released version and metadata |
| Reproducible intermediates | Recreate unless cost, risk, or policy justifies retention |
| Scratch, caches, and failed runs | Remove after confirming they are not the only useful copy |
| Credentials or re-identification keys | Never include in the archive set |

Do not archive the entire project tree merely because selection is difficult.
Create a deliberate, reviewable archive set containing data, documentation,
metadata, provenance, checksums, and the retention decision.

## 5. Prepare for a future verified Coscine archive

Coscine is the planned final lifecycle point for an eligible retained dataset.
The RCC-to-Coscine integration is **not yet released; it is planned and not yet
a live self-service transfer**. Project approval, Coscine eligibility, a
suitable resource type, and an announced supported transfer route must be
confirmed before real data moves.

After the service is released, the intended archive handoff is:

1. the project owner proposes a frozen archive set;
2. governance and destination eligibility are reviewed;
3. metadata, a manifest, and checksums are completed;
4. the suitable Coscine project and resource are confirmed;
5. the authorised RCC-supported transfer runs;
6. files, bytes, checksums, metadata, and access are verified;
7. project and archive owners record acceptance; and
8. RCC retention or cleanup is decided and recorded separately.

Different Coscine resource types may preserve data plus metadata, or metadata
and links only. Confirm what the selected resource actually retains. Archiving
in Coscine is not a substitute for project approval, data-protection review,
backup, or a repository required by a funder or publication.

Keep the RCC source until verification, archive acceptance, and the RCC
disposition decision are all recorded.

## Stop and ask for help when

- the approved project or accountable owner is unclear;
- the data contains direct identifiers or re-identification keys;
- consent, contracts, legal obligations, or repository requirements are
  uncertain;
- an instrument is still writing;
- the dataset is unusually large, contains many small files, or recurs often;
- a vendor appliance or managed system such as Ardia is the source;
- the authoritative copy or required retention period is disputed;
- the Coscine resource type or protection level is unclear; or
- anybody proposes deleting a source before verification and acceptance.

## Five checks before you finish

- [ ] The authoritative data and validated results are in the approved project,
      not a home directory.
- [ ] Temporary high-I/O computation used job-local storage and required results
      returned to the project.
- [ ] The archive set is intentional, documented, checksummed, and approved.
- [ ] After service release, Coscine contains what the project expects, and an
      authorised person tested access.
- [ ] Archive acceptance and the RCC retention or deletion decision are recorded.

For training and the full rationale, read
[Class 16: wet-lab instrument data](../course/class-16-wet-lab-data-workflows.md)
and [Class 17: research data lifecycle](../course/class-17-data-lifecycle.md).
For operational control points, use the
[planned RCC project to Coscine flow](rcc-project-to-coscine.md).
