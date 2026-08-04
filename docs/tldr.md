# ClusterDocs NG TL;DR

This page is the shortest useful introduction to RCC. Read it before connecting
for the first time, or use it to find the right detailed guide.

## RCC in one minute

RCC is organised around people and projects:

- your **individual account** is your personal badge and must not be shared;
- every user has **exactly one primary group**, meaning their home department
  or organisational affiliation; and
- a user can join **one or more projects**, which are the shared workrooms where
  named people from different primary groups can work with the same approved
  data.

The primary group says where you belong. The project says which research data,
services, and collaborators you may work with. Do not change somebody's primary
group merely to share project data; add their individual account to the project.

### What is available now?

| Capability | Status |
|---|---|
| RCC Admin, including self-administration and primary approval | **Ready now** |
| RCC workers and Slurm jobs | **Ready now** |
| Project Samba shares for approved Lab-network instruments | **Ready now** |
| Managed Nextflow-to-Slurm support | **Not yet released** |
| Project vhosts | **Not yet released** |
| Ardia integration with RCC | **Not yet released** |
| RCC-to-Coscine archive transfer | **Not yet released** |

The unreleased entries are included so teams can plan safely. They are not
instructions to start using those services.

```text
person -> individual RCC account -> exactly one primary group (affiliation)
                              \-> one or more projects (collaboration)

Lab-network instrument
    -> approved Samba share for its project [ready]
       or future Ardia integration [not yet released]
    -> RCC project storage -> Slurm analysis -> project results
    -> optional protected vhost for that project [not yet released]
    -> reviewed archive set -> Coscine later [not yet released]
```

**Samba** is the technology behind a Windows-style network folder. For a
registered Lab-network instrument or acquisition computer, RCC can approve a
project-scoped Samba share so completed data arrives in the project rather than
in one person's home directory. **Ardia integration is not yet released.** Its
future mass-spectrometry data flow must use a vendor-supported integration or
export path instead of treating Ardia as an ordinary folder.

**Project vhosts are not yet released.** When the service is released, a
project that needs an easier browser interface will be able to request its own
protected **vhost** (virtual host). The vhost will belong to that project and
use individual identities plus project membership; it will not be a shared
account or a way to expose the whole project directory.

Computation runs through Slurm. Interactive tools such as Jupyter and Shiny
also run inside bounded allocations and are reached through protected local
connections. A selected final dataset may later move to Coscine after project
review and verification. **RCC-to-Coscine transfer is not yet released**; it
remains planned and not yet a live self-service transfer.

**Managed Nextflow-to-Slurm support is not yet released.** The planned service
will run the Nextflow controller only on an approved submission host and send
each analysis task to a worker through Slurm. Resume-critical work state will
stay in shared project storage; node-local storage will be used only for
explicit temporary task work. Until RCC announces the `rcc-nextflow` launcher,
use the ready managed Snakemake path or ask support instead of installing an
unmanaged Nextflow controller on a login host.

For most users, **VS Code with Remote - SSH is the suggested everyday route**
for coding and preparing data analysis. It combines the editor, remote file
view, Git tools, and terminal in one window. VS Code is the interface; Slurm is
still where computation runs, and the RCC transfer service is still the route
for large data movement.

```text
workstation
    -> approved RCC SSH or files entry point
    -> project storage for durable input, code, metadata, and results
    -> Slurm allocation
    -> job-local storage for active high-I/O work
    -> validated results back to the project
```

Instrument data follows the same project boundary and can eventually become a
reviewed Coscine archive set:

![Laboratory instruments use the protected Lab network and approved services to move data into an RCC project for analysis](assets/lab-network-flow.svg)

```text
instrument -> RCC project -> job-local analysis -> RCC project results
           -> verified Coscine archive -> recorded RCC disposition
```

## Ten rules that prevent most problems

1. Use only your own RCC account. Keep your one primary group as your
   affiliation and use approved project membership for collaboration.
2. Never send a private SSH key, password, token, passkey export, or
   re-identification key to another person.
3. Verify the approved RCC endpoint and host identity; do not bypass an SSH
   warning merely to make a connection work.
4. Put authoritative research data and durable results in the approved project,
   not a user's home directory.
5. Submit computation through Slurm; do not run analysis on login or submission
   hosts.
6. Stage high-I/O temporary work to job-local storage and copy validated results
   back before the job ends.
7. Request realistic CPU, memory, GPU, and time limits. Start with one small
   bounded test.
8. Bind Jupyter, Shiny, and development services to loopback and reach them only
   through the documented tunnel or governed service path.
9. Keep direct identifiers and re-identification keys outside RCC. Confirm that
   project governance permits every biomedical dataset before transfer.
10. Verify every important transfer or archive before deleting a source.

## First connection

Start with [Class 1: safe access](course/class-01-safe-access.md) and the
[access, SSH, and VS Code reference](reference/access-ssh-vscode.md).

The basic sequence is:

1. request an individual account and project membership;
2. create a dedicated SSH key, preferably hardware-backed where supported;
3. register only the public key;
4. obtain the current approved RCC configuration through a trusted channel;
5. inspect the effective configuration;
6. make one bounded connection test; and
7. use the approved alias `{{ ssh_alias }}` in current instructions.

The access reference includes a visual VS Code walkthrough plus recommended
search, file-watcher, extension, and Workspace Trust settings. Do not copy a
server name from a screenshot.

## Where files belong

| Content | Correct place |
|---|---|
| Personal configuration and small source files | Home storage |
| Material shared only within your primary group | Approved primary-group storage |
| Authoritative project input | Approved project storage |
| Validated results, code, metadata, and provenance | Approved project storage |
| Active temporary and random I/O | Job-local storage inside the allocation |
| Large browser upload or ordinary download | Approved RCC files service when suitable |
| Retained final archive set | Approved repository or planned Coscine flow |

Home is not a project-data area. A project connects data to its accountable
owner, approved purpose, membership, retention, legal context, and continuity
when a team member leaves. Home capacity and filesystem behavior are also not
intended for large recurring instrument ingestion.

For collaboration across primary groups, request a project whose Unix group
contains every approved member. A setgid project directory keeps new files
associated with that project group; it does not authorize disclosure or make
files group-writable by itself. Use the
[users, groups, and projects guide](reference/users-groups-projects.md) for the
identity model and the [data-sharing guide](reference/data-sharing.md) for
colleagues in your project, other RCC groups, and external recipients.

Read [Class 12: efficient local I/O](course/class-12-efficient-io.md),
[Class 13: storage architecture](course/class-13-storage-architecture.md), and
the [storage and transfer reference](reference/storage-transfer.md).

## How to run work

Use Slurm for batch jobs, interactive shells, notebooks, GPU work, and long
analysis. The normal choices are:

- `srun` or a documented interactive allocation for short attended work;
- `sbatch` for reproducible or unattended work;
- `cpu_short` for jobs up to two hours; and
- a regular compute partition for longer bounded, restartable jobs.

Discover current partitions and resources rather than copying old hardware
names. Use `squeue` to inspect jobs, `scontrol show job` for reasons and
allocation details, and `scancel` to stop work you no longer need.

Start with [Class 5: Slurm](course/class-05-slurm.md), then keep the
[Slurm command reference](reference/slurm.md) nearby. The
[shared-compute reference](reference/how-shared-compute-works.md) explains owner,
shared, borrowed, and requeue behavior.

## Reproducible software and workflows

- Put code, configuration, parameters, and small environment definitions in
  version control.
- Use Snakemake or another workflow system for repeated dependent steps.
- Activate Conda environments inside the job rather than relying on a login
  shell state.
- Use rootless Apptainer for immutable runtimes when it is the better fit. The
  container runs with your RCC permissions—not host-root privileges—so it
  cannot bypass project access or Slurm; it can still change files your user
  can write, so bind only what the job needs.
- Keep large caches, environments with many small files, and temporary
  container writes off inappropriate shared paths.

See [Class 2: workflows](course/class-02-workflows.md),
[Class 4: Apptainer](course/class-04-containers.md), and the
[software-workflow reference](reference/software-workflows.md).

## Python, R, notebooks, AI, and Shiny

Use [Class 7](course/class-07-python-notebooks.md) for Python and Jupyter,
[Class 8](course/class-08-r-analysis.md) for R, and
[Class 9](course/class-09-shiny.md) for Shiny development.

Notebook and application processes are real workloads:

- start them through Slurm;
- bind only to `127.0.0.1` during development;
- use the generated SSH tunnel;
- keep tokens out of screenshots, chat, notebooks, and Git;
- move long or expensive steps into batch workflows; and
- stop the allocation when finished.

For machine learning and AI, begin with a scientific question and a simple
baseline. Record data splits, preprocessing, versions, parameters, metrics,
uncertainty, subgroup behavior, and leakage checks. Use a GPU only when the
framework and measured workload benefit.

## Protected project websites and services

A notebook is not a production service. Use
[Class 10](course/class-10-notebook-to-service.md) to separate request handling
from expensive Slurm computation, then complete
[Class 6](course/class-06-vhosts.md) before requesting a governed protected
project website. When a project needs a browser interface, request a vhost for
that project **after the vhost service is released**. The current Class 6
material is for planning and training, not an operational request. Each future
vhost will have a named project owner, be authorised by project membership, and
expose only the approved application or curated data—not every file in project
storage. A project will not need a vhost unless it has a clear web use case.

Do not expose an ad-hoc listener, notebook, Shiny app, or development server to
the network. Authentication, authorization, proxy behavior, logs, secrets,
updates, ownership, and shutdown behavior need review.

## Biomedical-data boundary

Complete [Class 11: biomedical data privacy](course/class-11-biomedical-data-privacy.md)
before transferring or analysing biomedical data.

Do not place direct identifiers or re-identification keys in RCC. Genomic,
imaging, and other biomedical research data may be used only when the approved
project governance covers RCC and the required safeguards. Filenames,
manifests, notebooks, logs, plots, and support requests can all leak sensitive
information; inspect them before sharing.

When uncertain, stop before transfer and ask the responsible project and data
governance contacts. The
[biomedical-data admission guide](security/rcc-biomedical-data-admission.md)
contains the short decision checklist.

## Instruments and the Lab network

Suitable registered instruments and acquisition workstations can use the
protected **Lab network**. It removes general direct Internet connectivity
while retaining direct access to explicitly approved server endpoints or
services. Limited outbound web access through an explicit HTTP proxy can
support approved needs such as updates without allowing unsolicited inbound
Internet access.

For an ordinary file-producing instrument, the approved endpoint is commonly a
project-scoped **Samba share**: a Windows-style network folder that delivers a
completed run directly to the right RCC project. RCC supplies the exact share
and credentials; do not guess them or reuse another project's connection.
**Ardia integration is not yet released.** When released, the managed vendor
platform will require its supported integration or export route.

The Lab network reduces exposure; it does not make a device trusted. RCC must
review the owner, software and update needs, vendor support, licensing,
credentials, server dependencies, data flow, and target project before
connection.

Read [Class 14: instrument data](course/class-14-wet-lab-data-workflows.md) and
[how RCC and the Lab network work together](resources/how-it-all-works.md).

## Finish the data lifecycle

[Class 15](course/class-15-data-lifecycle.md) follows data from instrument
acquisition through project storage and analysis to a reviewed Coscine archive
set. The [data-lifecycle TL;DR](data/data-lifecycle-tldr.md) is the two-page
version.

Before archival:

1. classify raw data, inputs, intermediates, results, and records;
2. select a deliberate frozen archive set;
3. add useful metadata, provenance, a manifest, and checksums;
4. confirm governance and the destination resource;
5. use the supported transfer route when announced;
6. verify files, bytes, checksums, metadata, and access;
7. record acceptance; and
8. decide RCC retention or deletion separately.

## When something fails

Do not respond by disabling host verification, opening a network port, sharing
credentials, recursively changing permissions, scanning hosts, or repeatedly
launching jobs and transfers.

Use the [troubleshooting guide](reference/troubleshooting.md), capture the
smallest useful diagnostic, remove secrets and research identifiers, and ask
through the approved RCC contact route. Include the job ID or support code when
available—not private keys, passwords, tokens, patient-related filenames, or
entire unrestricted logs.

## Choose the next page

- New to RCC: [complete the fifteen-class course](course/index.md).
- Analysing data: [follow the data-analysis path](paths/data-analysis.md).
- Building software or services: [follow the development path](paths/software-development.md).
- Looking up commands: [open the day-to-day reference](reference/index.md).
- Connecting now: use the [current RCC connection-name guidance](connecting/stable-endpoints.md).
- Need a person: [meet the RCC team and find the contact route](team.md).
