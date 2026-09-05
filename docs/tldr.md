# ClusterDocs 3 TL;DR

This is the short operational model for the future RCC experience. Start with
your research task. Most researchers should not have to learn cluster topology,
SSH, or Slurm syntax before they can move data, run an approved analysis, inspect
results, or manage project membership.

> **Starting now:** use [Start here: your first 15 minutes](getting-started/index.md)
> for the browser-first path and the current advanced fallback. For guided,
> self-contained training, use [RCC Expedition](rcc-expedition.md).

## RCC in one minute

RCC is organised around people and projects:

- your **individual account** is your personal badge and must not be shared;
- every user has **exactly one primary group**, meaning their home department or
  organisational affiliation; and
- a user can join **one or more projects**, so **people from different primary
  groups** can work with the same approved data without changing affiliation.

The primary group says where you belong. The project says which research data,
services, compute, collaborators, and lifecycle actions you may use. The project
is the durable boundary regardless of whether you arrive through Files,
Analysis, an agent-assisted action, VS Code, SSH, or a domain application.

## The normal research path

For ordinary browser-first research:

1. sign in and choose the approved project;
2. use **Files** or a managed ingestion path to bring/select data;
3. use **RCC Analysis Notebook** for attended exploration or **Workflow** for
   repeatable/scalable execution when Analysis is released;
4. keep durable results, code, parameters, and provenance in the project; and
5. preserve/share/publish through the project-approved lifecycle.

RCC Analysis is **not yet released** in the current candidate, so current
SSH/VS Code, Slurm, managed Snakemake/Nextflow, and SSH-tunnel notebook paths
remain the supported compute alternatives until RCC Home activates Analysis.

## Instruments and project storage

A sequencer, microscope, mass spectrometer, acquisition workstation, or facility
server should normally feed the project rather than a researcher's laptop or
home directory.

For approved registered devices, an **approved Samba share for its project** is
a familiar Windows-style landing path, and **project Samba shares are ready
now**. A **future Ardia integration** remains **not yet released** and must use
the vendor-supported integration/export route when activated.

Project storage can include shared POSIX data plus separately enabled S3/object
storage where object semantics fit the workload. DataLad/git-annex can support
versioned large-data state where appropriate. High-I/O temporary work belongs in
**job-local storage** inside the allocation, not in a permanently busy shared
folder.

## Notebook, Workflow, and advanced HPC

Use **Notebook** for bounded, attended exploration and **Workflow** for work that
is repeated, long-running, many-sample, unattended, highly parallel, or important
enough to reproduce exactly.

Advanced users retain direct Slurm, GPU, SSH, VS Code, Conda/Mamba, rootless
Apptainer, Snakemake, Nextflow, Gitea, and lower-level diagnostics. Those tools
remain powerful; they are no longer the conceptual entrance exam for ordinary
research use.

**Managed Nextflow-to-Slurm support is ready now.** The managed controller runs
on an RCC **shellhost** or allocation-backed **interactive node** and submits the
scientific tasks through Slurm. Resume-critical state stays in shared project
storage while explicit temporary task I/O can use node-local scratch.

## AI assistance without exporting the dataset

The preferred coding-agent pattern is **data-blind by default**. Give an
external/general-purpose agent documentation, schemas, public code, synthetic
fixtures, and carefully bounded sanitized diagnostics. Let it explain, design,
test, refactor, or debug the workflow. RCC then checks the user's identity,
project/capability, and runs the resulting code against real project data inside
the governed environment.

Natural language, MCP, or an API does not create a second identity or additional
authority. Separately reviewed RCC-local data-near agent capabilities are
explicit exceptions, not the default coding-agent assumption.

Read [AI and coding agents without exposing project data](concepts/agents-and-mcp.md).

## Self-governance without giving everyone admin

Users and project leads can manage appropriate account/project actions through
the role-aware self-service surface. Named project capabilities can be delegated
without granting general LDAP, storage, Slurm, or root administration.

The interface changes how you ask; it does not change what your identity and
project role authorize.

## Services, domain applications, and preservation

RCC can support project-scoped databases, Gitea, DataLad, S3/object storage,
workflow services, and domain applications on the same identity/project/compute
foundation.

SeqLab is a useful example: sequencing can move from acquisition into project
storage, analysis, review, provenance/metadata, and onward submission to the
appropriate international archive when that deployed SeqLab function is enabled.
The same platform pattern can support microscopy, imaging, mass spectrometry,
and other domain workflows.

An **optional protected vhost for that project** remains **not yet released** in
the current candidate. Project vhosts must not be treated as a route to expose an
entire project filesystem.

Primary RCC storage is not the archive. A reviewed archive set can eventually
move to a **verified Coscine archive**, but **RCC-to-Coscine transfer is not yet
released**; it remains **planned and not yet a live self-service transfer**.
Verification, metadata, checksums, ownership, and disposition remain separate
from merely copying files.

## Ten rules that prevent most problems

1. Use your own RCC account; use project membership for collaboration.
2. Never share private keys, passwords, tokens, passkey exports, or
   re-identification keys.
3. Keep authoritative data and durable results in the **approved project**.
4. Keep direct identifiers/re-identification keys outside RCC and follow the
   project biomedical-data approval.
5. Use Notebook for bounded exploration and Workflow/batch execution for
   repeated or scalable work.
6. Use Slurm for substantial computation; do not turn gateways/submission hosts
   into compute nodes.
7. Use job-local storage for active high-I/O temporary work when appropriate and
   copy validated results back before the allocation ends.
8. Request measured CPU/RAM/GPU/time rather than treating larger reservations as
   inherently faster.
9. Let agents help from non-sensitive context; do not export protected project
   data merely to get coding assistance.
10. Verify important transfers and archives before deleting a source.

## Biomedical-data boundary

Complete [Class 13: biomedical data privacy](course/class-13-biomedical-data-privacy.md)
before transferring or analysing biomedical data. Filenames, manifests,
notebooks, logs, plots, and support requests can reveal sensitive information as
well as the primary dataset.

When uncertain, stop before disclosure/transfer and use the
[biomedical-data admission guide](security/rcc-biomedical-data-admission.md).

## Lab network

Suitable registered instruments can use the protected **Lab network** and
explicitly approved ingestion/service routes. The Lab network reduces exposure;
it does not make an instrument trusted or turn an acquisition workstation into a
compute node.

Read [Class 16: instrument data](course/class-16-wet-lab-data-workflows.md) and
[how RCC and the Lab network work together](resources/how-it-all-works.md).

## Advanced connection path

When you actually need shell/developer access, use
[Access, SSH, and VS Code](reference/access-ssh-vscode.md). The approved
`{{ ssh_gateway_alias }}` gateway is forwarding-only; the normal user target is
`{{ ssh_target_alias }}`. SSH provides access while Slurm provides compute.

Do not copy hostnames from old screenshots or accept a host-identity warning just
to make a connection work.

## When something fails

Do not respond by disabling verification, opening ad-hoc listeners, sharing
credentials, recursively changing permissions, scanning hosts, or repeatedly
launching duplicate jobs/transfers.

Use the [troubleshooting guide](reference/troubleshooting.md), capture the
smallest useful diagnostic, remove secrets/research identifiers, and ask through
the approved support route.

## Choose the next page

- Browser-first start: [first 15 minutes](getting-started/index.md).
- Complete platform: [What RCC can do](concepts/what-rcc-can-do.md).
- Data analysis: [data-analysis path](paths/data-analysis.md).
- Software/workflow development: [development path](paths/software-development.md).
- Commands and deep technical detail: [day-to-day reference](reference/index.md).
- Instrument ingestion: [transfer-path decision guide](data/instrument-data-options.md).
- Lifecycle/preservation: [Class 17](course/class-17-data-lifecycle.md).
- Guided optional training: [RCC Expedition](rcc-expedition.md).
- Human support: [RCC team/contact route](team.md).
