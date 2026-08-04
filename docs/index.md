# RCC ClusterDocs NG

Welcome to the staged RCC learning site for medical professionals, biomedical researchers, research software developers, and technical project staff.

The course is designed so that a new user can progress without needing an administrator beside them. Each class has a small practical exercise and a gate that checks readiness without exposing credentials or generating significant cluster load.

## RCC in plain language

Think of RCC as a set of project workrooms rather than one large shared disk:

### Service availability

| Capability | Status |
|---|---|
| RCC Admin self-administration and primary-approver workflow | **Ready now** |
| RCC workers and Slurm computation | **Ready now** |
| Project Samba shares for approved projects and registered Lab-network devices | **Ready now** |
| Managed Nextflow-to-Slurm support | **Not yet released** — use the managed Snakemake path until RCC announces the `rcc-nextflow` launcher |
| Protected project vhosts | **Not yet released** — the documentation is planning and training material |
| Ardia-to-RCC integration | **Not yet released** — use no Ardia transfer route until RCC announces it |
| RCC-to-Coscine archive transfer | **Not yet released** — prepare archive sets, but do not treat the planned flow as operational |

“Ready now” still means that the user, project, data, and—where applicable—the
instrument must be approved. It does not mean that one project can access
another project's service.

| RCC term | Plain-language meaning |
|---|---|
| Your account | Your personal badge. Use your own account so actions remain attributable. |
| Your primary group | Your home department or organisational affiliation. Every user has exactly one. |
| A project | A shared workroom for named, approved people. A project can include people from different primary groups. |
| A project Samba share | A Windows-compatible network folder where an approved Lab-network instrument or acquisition computer can deliver data to the project. |
| Managed Nextflow support | A future launcher that will keep the workflow controller on an approved submission host while Slurm runs each task on an RCC worker. It is not yet released. |
| A project vhost | A future optional protected website for that project. Project-vhost hosting is not yet released. |
| Coscine | A planned later destination for a reviewed archive set. RCC-to-Coscine transfer is not yet released. |

The usual journey is:

```text
people from one or more primary groups
    -> one approved project and its shared data
Lab-network instrument
    -> approved project Samba share [ready]
       or future Ardia integration [not yet released]
    -> RCC project storage -> Slurm analysis -> project results
    -> optional project vhost [not yet released]
    -> reviewed archive set -> Coscine later [not yet released]
```

Your primary group records where you belong; it is not how cross-department
research data is shared. The project is the access and collaboration boundary.
Start with the [complete plain-language TL;DR](tldr.md) for the important limits
and links.

RCC supports statistics, visualization, Python and R data science, machine
learning, GPU-accelerated AI, and distributed data processing. These techniques
remain part of a reproducible research workflow: computation runs through
Slurm, data stays within its project governance, and model evaluation includes
validation, uncertainty, bias, and scientific limitations.

## Choose your path

<section class="path-grid" aria-label="Choose an RCC learning path">
  <article class="path-card analysis-path">
    <span class="path-number">01</span>
    <p class="path-label">Data analysis</p>
    <h3>Move from research data to a reproducible result</h3>
    <p>Learn Python, R, notebooks, statistics, AI and machine learning, efficient I/O, GPUs, validation, and governed result sharing.</p>
    <a class="path-action" href="paths/data-analysis.md">Follow the data analysis path →</a>
  </article>
  <article class="path-card development-path">
    <span class="path-number">02</span>
    <p class="path-label">Software development</p>
    <h3>Build reviewable workflows and protected services</h3>
    <p>Learn Git, Snakemake, Slurm, Conda, Apptainer, Python and R applications, Shiny, APIs, and governed deployment.</p>
    <a class="path-action" href="paths/software-development.md">Follow the software development path →</a>
  </article>
</section>

## Shared foundation

- Need the complete short version first? Read the
  [ClusterDocs NG TL;DR](tldr.md).
- Everyone begins with [Class 1: safe access](course/class-01-safe-access.md).
- Use the [course overview](course/index.md) when you want the complete fifteen-class sequence.
- Connecting now: use the [current RCC connection-name guidance](connecting/stable-endpoints.md).
- Working with human biomedical data: complete [Class 11](course/class-11-biomedical-data-privacy.md) before transfer or analysis.
- Looking up a command after training: use the [day-to-day reference](reference/index.md).
- Connecting a laboratory instrument or acquisition workstation: see
  [how the lab network and RCC fit together](resources/how-it-all-works.md).
- Moving data from an instrument into analysis: complete
  [Class 14](course/class-14-wet-lab-data-workflows.md).
- Planning retention, Coscine archiving, or defensible cleanup: complete
  [Class 15](course/class-15-data-lifecycle.md).
- Questions or feedback: [meet the RCC team and find the best contact route](team.md).
