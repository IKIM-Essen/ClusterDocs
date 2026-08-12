# The RCC data lifecycle

RCC treats data movement and storage as part of the project rather than as
unrelated copies.

```text
instrument / facility / collaborator
        -> governed ingest
        -> active project data
        -> scheduled analysis
        <-> approved managed transfer
        -> publication / archive
        -> restore when needed
        -> governed disposition
```

## Lab VLAN

Where direct research-instrument integration is configured, RCC uses the
dedicated campus **Lab VLAN**. It is an acquisition path, not a way to turn
instrument-control computers into general compute nodes or unrestricted storage
clients.

Instrument integration should define project destination, completion detection,
retry/resume, counts, checksums or equivalent verification, ownership,
monitoring, and retention.

## Active data and scratch

Durable inputs/results belong on approved project storage. Node-local `/local`
is temporary job-local work where documented.

## Managed transfer and Globus

Large or restartable transfers should use a managed transfer route. Globus is
part of the transfer plane where enabled.

Transfer does not remove project ownership, data classification, endpoint
policy, verification, or provenance.

## Archive

Archive is a project lifecycle transition, not "move old files somewhere."

A useful state model is:

```text
planned -> validated -> transferring -> verified -> archived
```

Finalization should not skip verification.

## Coscine

The RCC-to-Coscine transfer is **not yet released**. Once that reviewed path is
available, Coscine can be an archive target for projects using it. RCC keeps its
canonical project/provenance/archive semantics and maps metadata into the
selected target.

## Research Objects are optional

An archive does not require every project or workflow to create an RO-Crate.
Research Objects are used when they add value for publication, important
workflow checkpoints, handoff, preservation, or project closure.

See [Research Objects and FAIR data](research-objects-fair.md).
