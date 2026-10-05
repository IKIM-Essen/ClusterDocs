# Regular and Controlled Data projects

RCC is a governed research-computing environment, but not every RCC project has
the same data-release model. RCC defines two project types:

- **Regular Project** — the current RCC project model;
- **Controlled Data Project** — a separately admitted protected execution and
  release model.

> **Current status:** Regular projects are the active project type. Controlled
> Data projects are defined in RCC source but **creation/runtime admission is not
> yet released**.

## Why the distinction exists

A Regular project controls who may work with project data and which RCC services
are enabled. It is appropriate when the project's approved governance allows the
normal RCC compute and transfer model.

A Controlled Data project is intended for data where ordinary direct export
must not be available to analysts. The protected data stays behind a stricter
execution boundary, and any output that leaves that boundary requires a
separate governed release decision.

This is not just “Regular, but with another checkbox.” It changes the expected
movement of data and results.

## The two models

| | Regular Project | Controlled Data Project |
|---|---|---|
| Project membership | required | required |
| Ordinary RCC compute | according to normal project policy | not automatically the protected runtime |
| Ordinary Files/transfer | according to normal project policy | protected data must not escape through ordinary transfer surfaces |
| Output release | normal approved project-sharing rules | separate reviewed release workflow |
| User chooses individual export channels | no; services follow project policy | no; the project type defines a restriction ceiling |
| Current user availability | **available** | **not yet released** |

## “RCC is controlled” does not mean “Controlled Data Project”

ClusterDocs often describes RCC as a controlled research-computing enclave. That
is a general security/governance description.

**Controlled Data Project** is a specific RCC product term with additional
anti-exfiltration and release semantics. Do not infer that an existing Regular
project has those semantics merely because it contains biomedical data.

## What Controlled Data is intended to prevent

The protected-data design requires that sensitive source data cannot simply be
copied out through ordinary user paths. In particular, the protected namespace
must not become reachable through an ordinary login mount, ordinary Files/SFTP,
ordinary S3 credentials, or another application/network route that bypasses the
release boundary.

The analyst can compute on the protected data, but a result becomes exportable
only through the separately approved release workflow.

## Workbench is not the Controlled Data sandbox

The planned RCC Workbench is an ordinary interactive project service. It is not
an anti-exfiltration environment and should not be described as the future
Controlled Data runtime.

Likewise, ordinary DataLad/S3 project services are not evidence that protected
Controlled Data can be exported.

## Project type is not a menu of protocols

A project lead should not have to design a security policy by choosing a custom
mixture of SSH, Files, SFTP, S3, Globus, or network toggles.

The project type expresses the stable data-handling model. RCC then enforces the
allowed service boundary consistently.

## Can an existing project be converted?

Project-type conversion is not intended to be an ordinary project-lead action.
Moving an established project between Regular and Controlled Data semantics can
change storage, execution, and release assumptions and therefore requires a
separately reviewed administrative migration.

## What should users do now?

For current work:

1. treat existing/current projects as **Regular** unless RCC explicitly tells
   you otherwise;
2. follow the project's approved biomedical-data governance;
3. do not assume an unreleased Controlled Data feature creates permission to
   ingest or release additional data; and
4. use [RCC biomedical-data admission](../security/rcc-biomedical-data-admission.md)
   and [How to share data safely](../reference/data-sharing.md) for current
   decisions.

When Controlled Data projects are released, ClusterDocs should add the exact
user journey for deposit, analysis, result review, release, and audit evidence.
