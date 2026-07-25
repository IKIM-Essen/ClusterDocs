# Class 15: manage the research data lifecycle — video narration

## Slide 1: Class 15: manage the research data lifecycle

Welcome to Class 15: manage the research data lifecycle. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this class, you should be able to: identify the lifecycle stage of a dataset; explain why instrument and research data belongs to an approved project and not a user's home directory; distinguish authoritative data, reproducible intermediates, durable results, records, and disposable temporary files; assign an owner, retention basis, access model, and review date; prepare data and metadata for reuse or archiving; explain when Coscine may be an appropriate archive option; follow the planned RCC-project-to-Coscine flow without treating it as a live self-service transfer; and require verification and acceptance before removing an RCC copy.

## Slide 3: The lifecycle is a set of decisions

The arrows are not a one-way conveyor belt. Published data may be reused and analysed again. An archived dataset may need a controlled correction. A retention decision may change when consent, law, contracts, funder rules, or scientific value change. At every stage, record: the accountable project owner; the approved purpose and governance basis; where the authoritative copy lives; who may access it; the metadata and provenance needed to interpret it; the retention period or review date; and the event that permits archival or deletion. For this course, Coscine is the planned endpoint for an eligible retained archive set. It is not the destination for every.

## Slide 4: Classify before moving

File age alone is not a classification. A large old raw dataset may still be the authoritative scientific record, while yesterday's multi-terabyte scratch directory may already be disposable.

## Slide 5: Match storage to the lifecycle stage

RCC project storage supports active, governed computation and durable project results. Job-local storage supports temporary high-I/O work. A publication repository supports a released dataset. An archive supports retained data that is no longer actively changing. ### Why project data must not live in a user's home directory A home directory is attached to an individual account. It is suitable for personal configuration, small source files, and limited working material. It must not become the authoritative landing area for instrument output, shared research input, or durable results. From a governance and legal-compliance perspective, approved project storage: ties processing to the project's documented purpose, responsible owner, and.

## Slide 6: Build the minimum archive package

Select data intentionally rather than copying an entire project tree by default. A reviewable package should include: The manifest should record at least the relative path, byte size, checksum, data class, source, format, responsible owner, access class, retention basis, and relationship to other files. Use meaningful metadata that remains useful after current team members leave. Do not place secrets, credentials, direct identifiers, or re-identification keys in README files, manifests, filenames, or general metadata fields.

## Slide 7: Coscine as an archive option

Coscine is a research-data management platform that can associate project data with structured metadata. Its available resource types do not all retain the same thing: some can hold data and metadata, while others represent or retain metadata about data held elsewhere. Confirm the selected resource type, allocation, protection level, retention period, and institutional approval before transfer. Coscine is the planned final lifecycle point for an eligible completed or stable research dataset that needs: an accountable project and membership model; descriptive metadata for discovery and reuse; a stable retained package rather than active RCC computation; and an archive period supported by the selected Coscine resource. It.

## Slide 8: Archive acceptance comes before RCC cleanup

A successful command or upload is not archive acceptance. Before changing or removing the RCC source, record evidence that: the intended archive set was frozen; file count, total bytes, and checksums match; metadata is complete enough for an independent project member; the destination resource contains data as well as metadata when required; access has been tested by an authorised person; retention and archive state are recorded; the project owner and archive owner accepted the transfer; and the RCC retention or deletion action was separately approved. When any check fails, preserve the RCC copy, record the failure, and resume from a known state. Do not repeatedly.

## Slide 9: Review instead of forgetting

Set a review date even when the archive has a defined retention period. Review: ownership and contact continuity; access membership; consent, legal, contractual, and funder obligations; whether formats and documentation remain usable; whether a persistent identifier or publication link is still correct; whether the data remains in scope for the selected archive; and what must happen at the end of retention. Record deletion as an accountable lifecycle event. The record should identify what was removed, under whose authority, when, from which locations, and which retained or published copies remain.

## Slide 10: Completion gate

Produce a synthetic lifecycle and archive plan that identifies the data classes, authoritative copy, owner, governance basis, retention decision, metadata, verification evidence, destination acceptance, and permitted RCC cleanup action. The plan must trace instrument data through project storage and job-local analysis to Coscine, explain why home storage is excluded, and state that the RCC-to-Coscine flow is planned and requires service confirmation.
