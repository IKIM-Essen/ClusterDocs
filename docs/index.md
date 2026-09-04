# RCC ClusterDocs NG

Welcome to RCC guidance for medical professionals, biomedical researchers,
research software developers, and technical project staff. If you want to
connect now, use [RCC Expedition Light](getting-started/index.md). If you
prefer a guided local course, use [RCC Expedition](rcc-expedition.md).

The course is designed so that a new user can progress without needing an administrator beside them. Each class has a small practical exercise and a gate that checks readiness without exposing credentials or generating significant cluster load.

<section class="expedition-callout" aria-labelledby="expedition-title">
  <p class="expedition-kicker">Two clear starting routes · Windows 11 and macOS</p>
  <h2 id="expedition-title">Connect quickly or learn step by step</h2>
  <p>Use the short checklist when you need a working connection. Use the self-contained local Expedition for guided workstation security, SSH, Linux, Slurm, storage, data transfer, and workflow training.</p>
  <div class="expedition-actions">
    <a class="expedition-primary" href="getting-started/index.md">Start Expedition Light →</a>
    <a href="rcc-expedition.md">Open RCC Expedition</a>
    <a href="assets/downloads/RCC-Expedition-USB-v1.0.1.zip">Download v1.0.1 for offline use</a>
  </div>
  <p class="expedition-privacy">Datensparsam by design: no learner account, analytics, telemetry, central progress database, or supervisor dashboard.</p>
</section>

## RCC in plain language

Think of RCC as a set of project workrooms rather than one large shared disk.
For definitions used throughout the documentation, see the
[RCC terminology reference](reference/terminology.md).

Your primary group records where you belong; it is not how cross-department
research data is shared. The project is the access and collaboration boundary.
Start with the [complete plain-language TL;DR](tldr.md) for the important limits
and links.

The network path is just as simple: the jump host is a guarded doorway, the
shell host is the desk where you prepare work, and Slurm workers perform the
calculation. [See the three roles on one page](concepts/jump-shell-compute.md).

Returning users can use the
[old-cluster migration table](getting-started/what-changed.md) to see which
access, storage, Slurm, Conda, and workflow habits changed.

RCC supports statistics, visualization, Python and R data science, machine
learning, GPU-accelerated AI, and distributed data processing. These techniques
remain part of a reproducible research workflow: computation runs through
Slurm, data stays within its project governance, and model evaluation includes
validation, uncertainty, bias, and scientific limitations.

Not sure whether you need Files, an interactive session, RCC Analysis, the
Assistant, or account/project management? Read
[RCC services: where should I go?](concepts/rcc-services.md). It also records
which newer surfaces are documented before release.

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

- Need an RCC account? Enrollment is currently an **invite-only pilot**; read
  [Request and activate an RCC account](getting-started/account-enrollment.md).
- Need the complete short version first? Read the
  [ClusterDocs NG TL;DR](tldr.md).
- Unsure which RCC surface to use? Start with the
  [RCC service map](concepts/rcc-services.md).
- Everyone begins with [Class 1: safe access](course/class-01-safe-access.md).
- Use the [course overview](course/index.md) when you want the complete eighteen-class sequence.
- Connecting now: use the [current RCC connection-name guidance](connecting/stable-endpoints.md).
- Working with human biomedical data: complete [Class 13](course/class-13-biomedical-data-privacy.md) before transfer or analysis.
- Looking up a command after training: use the [day-to-day reference](reference/index.md).
- Connecting a laboratory instrument or acquisition workstation: see
  [how the lab network and RCC fit together](resources/how-it-all-works.md).
- Preparing approved remote-console access: read the
  [RCC Headscale and PiKVM guide](connecting/pikvm-headscale.md). This service
  is **not yet released**.
- Moving data from an instrument into analysis: complete
  [Class 16](course/class-16-wet-lab-data-workflows.md).
- Planning retention, Coscine archiving, or defensible cleanup: complete
  [Class 17](course/class-17-data-lifecycle.md).
- Questions or feedback: [meet the RCC team and find the best contact route](team.md).
