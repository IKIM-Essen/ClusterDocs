# Research Objects, RO-Crate, and FAIR data

## Optional, not universal

Research Objects are not required for every RCC project or workflow run.

Use them when they add value, for example for:

- an important reproducible workflow checkpoint;
- publication;
- dataset release;
- collaborator handoff;
- archival snapshot; or
- project closure.

## Live project versus portable snapshot

> **The RCC project is the live institutional object. A Research Object is a
> portable, versioned projection of selected project state.**

A project may produce several Research Objects over its lifetime.

## RO-Crate

RO-Crate is the standards-based representation used when an RCC Research Object
is required. It can package or reference data, software, workflows, people,
organizations, instruments, provenance, licences, publications, and access
conditions.

## Thin crates for protected data

A crate does not need to contain every byte it describes. For protected medical
research it can contain metadata, provenance, software/workflow references,
dataset identifiers, access conditions, and references to protected objects.

Creating or receiving the crate does not authorize access to those payloads.

## FAIR does not mean public

FAIR means Findable, Accessible, Interoperable, and Reusable as permitted by the
scientific, ethical, and legal context.

For protected data, accessibility may still require authentication,
authorization, and purpose limitation.

## Coscine

The RCC-to-Coscine transfer is **not yet released**. When Coscine becomes the
archive target, RCC will map canonical project/provenance metadata into the
required Coscine metadata profile. RO-Crate may accompany the handoff when
selected, but RCC archiving does not depend on RO-Crate.

```text
RCC project model = institutional source of meaning
RO-Crate          = optional portable representation
Coscine           = one preservation target
```
