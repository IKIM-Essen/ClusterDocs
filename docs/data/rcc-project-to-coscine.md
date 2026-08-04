# Planned RCC project to Coscine archive flow

> **Service status — not yet released.** This page describes intended control
> points. It is not a live self-service transfer procedure, and it does not
> authorize users to copy governed RCC data to Coscine.

Use this flow when a project is considering Coscine for a stable archive set.
The RCC team must confirm when the supported transfer mechanism, eligibility
rules, and operational ownership are available.

## Intended flow

```text
instrument or facility produces authoritative data
  -> approved RCC project receives and verifies the data
  -> job-local workspace supports active analysis
  -> validated results return to the RCC project
  -> RCC project owner proposes a frozen archive set
  -> governance and destination eligibility reviewed
  -> files frozen; metadata, manifest, and checksums prepared
  -> Coscine project and suitable resource confirmed
  -> RCC-supported transfer is authorised and run
  -> destination file count, bytes, checksums, metadata, and access verified
  -> project owner and archive owner record acceptance
  -> Coscine archive state applied when appropriate
  -> RCC retention or cleanup decision executed separately
```

## 1. Request and scope

The project owner supplies:

- RCC project identifier and responsible principal investigator;
- scientific purpose and reason for archiving;
- data-protection and governance classification;
- approximate bytes, file count, and largest files;
- requested retention period;
- proposed Coscine project and resource type;
- required metadata profile and intended users; and
- any publication, funder, consent, contract, or repository obligations.

The source must be the approved RCC project area. Do not use a user's home
directory as an ingestion target, archive staging area, or substitute project
boundary.

Do not include credentials, direct identifiers, re-identification keys, or
research data in the request.

## 2. Eligibility decision

Before transfer, the responsible governance and service owners confirm:

- the data is permitted in both RCC and the selected Coscine resource;
- the resource stores the actual data when data archival is required, rather
  than metadata or links alone;
- its protection level and access model match the project;
- allocation and retention are sufficient;
- project membership is correct and attributable; and
- the proposed archive does not conflict with another required repository or
  records-retention process.

No decision should be inferred from technical connectivity alone.

## 3. Freeze and describe the archive set

Create a read-only or otherwise controlled candidate set. Record a manifest,
checksums, file count, total bytes, formats, provenance, software dependencies,
ownership, access class, and retention basis.

Exclude caches, job-local scratch, failed-run output, secrets, and undocumented
duplicates. Preserve enough code, parameters, environment information, and
documentation to interpret validated results.

## 4. Transfer control point

The exact RCC-to-Coscine mechanism remains to be implemented and documented.
Until the service is announced:

- do not guess an endpoint or copy credentials into scripts;
- do not launch unattended bulk transfers from login nodes;
- do not bypass project or Coscine approval; and
- do not describe a manual experiment as the supported production flow.

When available, the supported mechanism must use bounded retries, attributable
credentials, protected logs, resumable behavior where appropriate, and a
transfer report suitable for verification.

## 5. Verify and accept

Compare source and destination using:

- file count and total bytes;
- per-file or package checksums;
- a manifest diff;
- metadata completeness;
- representative format-open tests; and
- an access test performed by an authorised project member.

Record the transfer identifier, time, tool or service version, source snapshot,
destination project and resource, verification result, exceptions, and the
people accepting responsibility for the archive.

## 6. Archive state and RCC disposition

Applying Coscine's archive state and cleaning RCC are separate decisions.
Follow the current official
[Coscine archiving documentation](https://docs.coscine.de/en/resources/archiving/)
for the selected resource.

Keep the RCC source until destination verification, acceptance, archive status,
and the RCC retention decision are all recorded. Then execute only the approved
RCC action: retain, reduce, move, or delete. Record the result and the location
of the remaining authoritative copy.

## Failure rule

If eligibility, transfer, verification, access, or acceptance fails, preserve
the RCC source and stop. Record the failure and resume only through the
supported flow.

Continue with [Class 15: manage the research data lifecycle](../course/class-15-data-lifecycle.md)
for the complete lifecycle exercise.
