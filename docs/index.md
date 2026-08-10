# RCC ClusterDocs NG

Welcome to the staged RCC learning site for medical professionals, biomedical researchers, research software developers, and technical project staff. If you are new to RCC or preparing a new computer, start with [RCC Expedition](rcc-expedition.md), the self-contained onboarding course for Windows 11 and macOS, then return here for current cluster guidance.

The course is designed so that a new user can progress without needing an administrator beside them. Each class has a small practical exercise and a gate that checks readiness without exposing credentials or generating significant cluster load.

<section class="expedition-callout" aria-labelledby="expedition-title">
  <p class="expedition-kicker">Standalone onboarding · Windows 11 and macOS</p>
  <h2 id="expedition-title">Start with RCC Expedition</h2>
  <p>If you are new to RCC or setting up a new workstation, take the self-contained local course covering workstation security, SSH, Linux, Slurm, storage, data transfer, and reproducible workflows.</p>
  <div class="expedition-actions">
    <a class="expedition-primary" href="rcc-expedition.md">Open RCC Expedition →</a>
    <a href="assets/downloads/RCC-Expedition-USB-v1.0.0.zip">Download v1.0.0 for offline use</a>
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
- Use the [course overview](course/index.md) when you want the complete seventeen-class sequence.
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
