# Class 15: manage the research data lifecycle

Research data needs a plan before an instrument creates the first file. This
class follows data from instrument acquisition into an approved RCC project,
through analysis and validation, and into a verified Coscine archive set. It
connects every technical copy to ownership, access, retention, reuse, and
defensible deletion decisions.

It is for researchers, project owners, data stewards, laboratory staff, and
technical staff who need to decide what happens to data when active RCC work
slows down or a project ends.

## Learning objectives

After this class, you should be able to:

- identify the lifecycle stage of a dataset;
- explain why instrument and research data belongs to an approved project and
  not a user's home directory;
- distinguish authoritative data, reproducible intermediates, durable results,
  records, and disposable temporary files;
- assign an owner, retention basis, access model, and review date;
- prepare data and metadata for reuse or archiving;
- explain when Coscine may be an appropriate archive option;
- follow the planned RCC-project-to-Coscine flow without treating it as a live
  self-service transfer; and
- require verification and acceptance before removing an RCC copy.

## 1. The lifecycle is a set of decisions

```text
plan
  -> instrument creates or acquires data
  -> approved RCC project receives and verifies it
  -> job-local workspace supports active analysis
  -> RCC project receives validated results and records
  -> project owner selects a documented archive set
  -> Coscine receives and verifies the approved archive set
  -> RCC copies are retained or removed by recorded decision
```

The arrows are not a one-way conveyor belt. Published data may be reused and
analysed again. An archived dataset may need a controlled correction. A
retention decision may change when consent, law, contracts, funder rules, or
scientific value change.

At every stage, record:

- the accountable project owner;
- the approved purpose and governance basis;
- where the authoritative copy lives;
- who may access it;
- the metadata and provenance needed to interpret it;
- the retention period or review date; and
- the event that permits archival or deletion.

For this course, Coscine is the planned endpoint for an eligible retained
archive set. It is not the destination for every temporary file, failed run, or
unreviewed project directory, and it is not available until the project and
transfer route have been approved.

## 2. Classify before moving

| Data class | Typical treatment |
|---|---|
| Authoritative raw or acquired data | Preserve under the approved retention plan; never infer that derived files replace it |
| Curated analysis input | Retain with provenance linking it to its source and transformation |
| Reproducible intermediate | Recreate when practical; retain only when cost, risk, or policy justifies it |
| Validated result | Retain with code, parameters, environment, logs, and review evidence |
| Publication or sharing package | Preserve the exact released version, metadata, licence, and persistent identifier where applicable |
| Project record | Retain decisions, approvals, manifests, access history, and disposal evidence as required |
| Cache, scratch, or failed-run output | Remove through a bounded cleanup process after confirming it is not the only useful copy |

File age alone is not a classification. A large old raw dataset may still be
the authoritative scientific record, while yesterday's multi-terabyte scratch
directory may already be disposable.

## 3. Match storage to the lifecycle stage

RCC project storage supports active, governed computation and durable project
results. Job-local storage supports temporary high-I/O work. A publication
repository supports a released dataset. An archive supports retained data that
is no longer actively changing.

### Why project data must not live in a user's home directory

A home directory is attached to an individual account. It is suitable for
personal configuration, small source files, and limited working material. It
must not become the authoritative landing area for instrument output, shared
research input, or durable results.

From a governance and legal-compliance perspective, approved project storage:

- ties processing to the project's documented purpose, responsible owner, and
  applicable approvals;
- applies project membership as the access boundary;
- supports reviewable stewardship when staff, students, or collaborators
  change;
- gives retention, archival, legal-hold, and deletion decisions a project
  context; and
- avoids relying on an individual's account to demonstrate who controls the
  data and why it is retained.

This does not make every project directory legally suitable for every dataset.
Consent, data-protection classification, contracts, funder rules, and other
project-specific requirements still decide whether RCC and Coscine are
permitted destinations.

From a performance and operational perspective:

- large instrument datasets and recurring ingestion can exhaust personal
  quotas and create excessive filesystem metadata work;
- team workflows need stable paths that do not depend on one user account;
- durable shared storage should hold inputs and validated outputs, not the
  random I/O of an active computation; and
- high-I/O intermediates should be staged to job-local storage and removed
  after required results return to the project.

The intended placement is therefore:

| Lifecycle point | Storage role |
|---|---|
| Instrument acquisition | Instrument or approved facility storage until the run is complete |
| RCC ingestion | Named approved project area, with manifest and transfer verification |
| Active computation | Job-local storage for temporary high-I/O work |
| Durable analysis record | RCC project inputs, validated outputs, code, metadata, and provenance |
| Retained end state | Verified, approved Coscine archive set |
| Personal setup | Home directory only for configuration, small source files, and non-authoritative working material |

An archive is not:

- a backup of live, changing project storage;
- a substitute for tested recovery;
- a place to hide undocumented files;
- automatically suitable for every data-protection class; or
- permission to delete the source immediately after upload.

Keep at least one recorded authoritative copy throughout a migration. If the
project requires backup or disaster recovery, document that separately from
archival retention.

## 4. Build the minimum archive package

Select data intentionally rather than copying an entire project tree by
default. A reviewable package should include:

```text
ARCHIVE_SET/
├── README.md
├── MANIFEST.tsv
├── CHECKSUMS.sha256
├── metadata/
├── data/
├── code-and-environments/
├── documentation/
└── approvals-and-retention/
```

The manifest should record at least the relative path, byte size, checksum,
data class, source, format, responsible owner, access class, retention basis,
and relationship to other files. Use meaningful metadata that remains useful
after current team members leave.

Do not place secrets, credentials, direct identifiers, or re-identification
keys in README files, manifests, filenames, or general metadata fields.

## 5. Coscine as an archive option

[Coscine](https://about.coscine.de/en/about/overview/) is a research-data
management platform that can associate project data with structured metadata.
Its available resource types do not all retain the same thing: some can hold
data and metadata, while others represent or retain metadata about data held
elsewhere. Confirm the selected resource type, allocation, protection level,
retention period, and institutional approval before transfer.

Coscine is the planned final lifecycle point for an eligible completed or
stable research dataset that needs:

- an accountable project and membership model;
- descriptive metadata for discovery and reuse;
- a stable retained package rather than active RCC computation; and
- an archive period supported by the selected Coscine resource.

It is not automatically appropriate merely because data currently fits on
RCC. Biomedical-data governance, consent, contracts, intellectual-property
rules, export controls, and repository requirements still apply. Complete
[Class 11: biomedical data privacy](class-11-biomedical-data-privacy.md) and
obtain the project-specific approvals before moving governed data.

The RCC integration is **planned, not yet a live self-service service**. Do not
stage the archive through a home directory. Follow
the [planned RCC project to Coscine archive flow](../data/rcc-project-to-coscine.md)
and wait for the RCC team to confirm the supported transfer route.

For current Coscine behavior and resource-specific limitations, consult the
official [Coscine archiving documentation](https://docs.coscine.de/en/resources/archiving/).

## 6. Archive acceptance comes before RCC cleanup

A successful command or upload is not archive acceptance. Before changing or
removing the RCC source, record evidence that:

1. the intended archive set was frozen;
2. file count, total bytes, and checksums match;
3. metadata is complete enough for an independent project member;
4. the destination resource contains data as well as metadata when required;
5. access has been tested by an authorised person;
6. retention and archive state are recorded;
7. the project owner and archive owner accepted the transfer; and
8. the RCC retention or deletion action was separately approved.

When any check fails, preserve the RCC copy, record the failure, and resume from
a known state. Do not repeatedly launch unbounded transfer attempts.

## 7. Review instead of forgetting

Set a review date even when the archive has a defined retention period. Review:

- ownership and contact continuity;
- access membership;
- consent, legal, contractual, and funder obligations;
- whether formats and documentation remain usable;
- whether a persistent identifier or publication link is still correct;
- whether the data remains in scope for the selected archive; and
- what must happen at the end of retention.

Record deletion as an accountable lifecycle event. The record should identify
what was removed, under whose authority, when, from which locations, and which
retained or published copies remain.

## 8. Practical exercise

Using synthetic or non-sensitive files, prepare a lifecycle decision for one
small dataset:

1. classify raw data, curated inputs, intermediates, results, and records;
2. trace the dataset from an instrument into its named RCC project;
3. explain why the home directory is not an acceptable landing point;
4. name the authoritative copy and accountable owner;
5. state the governance basis and retention or review date;
6. separate job-local intermediates from durable project records;
7. create a manifest and checksums for the Coscine archive set;
8. walk through the planned Coscine flow without transferring real data; and
9. write the acceptance evidence required before any RCC cleanup.

## Take-home rule

> Move instrument data into a governed project, not a personal home directory.
> Archive a deliberate, documented set in Coscine, verify acceptance, and only
> then apply the recorded RCC retention or deletion decision.

## Completion gate

Produce a synthetic lifecycle and archive plan that identifies the data
classes, authoritative copy, owner, governance basis, retention decision,
metadata, verification evidence, destination acceptance, and permitted RCC
cleanup action. The plan must trace instrument data through project storage and
job-local analysis to Coscine, explain why home storage is excluded, and state
that the RCC-to-Coscine flow is planned and requires service confirmation.
