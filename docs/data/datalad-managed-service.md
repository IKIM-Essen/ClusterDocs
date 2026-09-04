# Managed DataLad on RCC

> **Release boundary:** The RCC-to-Coscine transfer path described below is
> **not yet released**. DataLad enablement does not activate that archive path.

DataLad is RCC's managed project service for reproducible datasets and large-file
content. It combines Git/DataLad dataset history with an RCC-approved storage
provider so researchers can record **which dataset state** an analysis used
without forcing large research files into ordinary Git history.

> **Availability:** DataLad is a project service, not a universal property of
> every RCC project. Provider selection, backend acceptance, and project
> entitlement are separate states. Do not assume DataLad is active for a project
> until RCC shows it as enabled/accepted.

## What problem DataLad solves

A normal project directory tells you where files are now. DataLad can additionally
record a dataset's history, identity, file-content references, and reproducible
state.

That is useful when you need to answer questions such as:

- Which exact input dataset did this analysis use?
- Which files changed between two analyses?
- Can another researcher obtain the same dataset state later?
- Can a result/provenance record point to an immutable dataset revision?

## Dataset metadata and large content are different

A DataLad dataset uses Git for small metadata/history and git-annex-compatible
storage for large content.

Conceptually:

```text
Git / DataLad history
       |
       +--> file identities / revisions / provenance
       |
       +--> large content held by an RCC storage provider
```

Do not solve large-data versioning by committing FASTQ, BAM, imaging datasets,
or other large binary trees directly into Git.

## RCC manages the provider

RCC defines reviewed DataLad storage-provider profiles. Current source supports
provider concepts including:

- **RIA/POSIX** — DataLad/RIA-style backend storage;
- **S3 annex** — object-native git-annex content in an RCC-managed S3 bucket;
- **hybrid** — a reviewed combination where the deployment supports it.

A project selects one reviewed provider as desired state. That selection alone
does not create a bucket, credential, dataset, or entitlement. RCC separately
accepts the provider backend and enables the project service.

This separation prevents a UI choice from silently creating new storage or
credential authority.

## S3-annex is not a normal user S3 bucket

The `s3-annex` provider is an object-native git-annex content store. It is not a
generic filename-oriented S3 namespace for users to browse with arbitrary S3
clients.

In particular, a healthy S3-annex provider can legitimately have:

- **no POSIX presentation**;
- **no JuiceFS presentation**; and
- **no generic user S3 API access**.

That is provider policy, not missing infrastructure.

If a project needs an ordinary user-facing S3 bucket, that is a different
storage/service requirement and should not be obtained by weakening the annex
bucket contract.

## One project can contain multiple datasets

The RCC project is the authorization/governance boundary. Inside it, several
DataLad datasets may exist, each with its own dataset identity/history.

Dataset UUIDs and revisions are dataset metadata; they do not become new LDAP
projects or new user accounts.

## DataLad does not grant project access

A dataset history cannot widen authorization. A user still needs the underlying
RCC project/service permissions required to obtain or modify content.

Likewise, enabling DataLad does not automatically authorize:

- public sharing;
- Coscine upload;
- data release outside RCC;
- a generic S3 credential; or
- access to another project.

## DataLad and RCC Analysis

RCC Analysis can use DataLad as an optional provenance binding: an analysis run
can record the immutable dataset state associated with its input or result.

That strengthens reproducibility but does not make DataLad mandatory for every
Analysis workflow.

A useful chain is:

```text
DataLad dataset revision
        -> RCC Analysis run
        -> typed results + RO-Crate provenance
        -> approved project archive / Coscine when applicable
```

## DataLad and Coscine are not the same service

DataLad manages reproducible dataset state and content placement inside the RCC
project/service model. Coscine is part of the governed external archive/custody
path.

Enabling DataLad must not be interpreted as automatic archive submission or
publication. The archive decision remains separately reviewed.

See [RCC project to Coscine](rcc-project-to-coscine.md) for the planned archive
path and [Class 17](../course/class-17-data-lifecycle.md) for the research-data
lifecycle.

## What users should record

When DataLad is enabled, retain enough information to identify the dataset state
used by an analysis, for example the dataset identity/revision and any relevant
sibling/provider state that the approved RCC tooling exposes.

Do not copy backend credentials into analysis scripts merely to make a dataset
portable. RCC should provide the governed storage/authentication path.

## What ClusterDocs intentionally hides

Normal user documentation does not need the root S3 mutation actor, Nomad
control-job topology, bucket-bootstrap receipts, or credential-handoff state
machine. Those are operator controls that protect the managed service.

The stable user contract is: **dataset identity/history is DataLad metadata;
content lives on an accepted RCC provider; project authorization remains
separate; archival remains separate.**
