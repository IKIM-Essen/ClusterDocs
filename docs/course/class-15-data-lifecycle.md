# Class 15: manage the research data lifecycle

Research data needs a plan before it needs an archive. This class connects the
decisions made during acquisition and analysis with retention, reuse,
publication, archiving, and defensible deletion.

It is for researchers, project owners, data stewards, laboratory staff, and
technical staff who need to decide what happens to data when active RCC work
slows down or a project ends.

## Learning objectives

After this class, you should be able to:

- identify the lifecycle stage of a dataset;
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
  -> create or acquire
  -> organise and document
  -> analyse and validate
  -> share or publish
  -> retain, archive, or dispose
  -> review
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

Coscine may be an option when a completed or stable research dataset needs:

- an accountable project and membership model;
- descriptive metadata for discovery and reuse;
- a stable retained package rather than active RCC computation; and
- an archive period supported by the selected Coscine resource.

It is not automatically appropriate merely because data currently fits on
RCC. Biomedical-data governance, consent, contracts, intellectual-property
rules, export controls, and repository requirements still apply. Complete
[Class 11: biomedical data privacy](class-11-biomedical-data-privacy.md) and
obtain the project-specific approvals before moving governed data.

The RCC integration is **planned, not yet a live self-service service**. Follow
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
2. name the authoritative copy and accountable owner;
3. state the governance basis and retention or review date;
4. select the files for an archive set;
5. create a manifest and checksums;
6. decide whether Coscine, another repository, continued RCC retention, or
   deletion is appropriate;
7. if choosing Coscine, walk through the planned flow without transferring
   real data; and
8. write the acceptance evidence required before any RCC cleanup.

## Take-home rule

> Archive a deliberate, documented dataset—not an unexplained directory.
> Verify the destination and record acceptance before deleting any source.

## Completion gate

Produce a synthetic lifecycle and archive plan that identifies the data
classes, authoritative copy, owner, governance basis, retention decision,
metadata, verification evidence, destination acceptance, and permitted RCC
cleanup action. If Coscine is selected, the plan must state that the RCC flow is
planned and requires service confirmation.
