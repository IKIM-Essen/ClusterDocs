# RCC ClusterDocs NG

Welcome to RCC guidance for medical professionals, biomedical researchers,
research software developers, and technical project staff.

RCC is designed for two access styles:

- **advanced command-line/developer access**, using SSH, VS Code, and direct
  Slurm tools — this is **how you use RCC today**; and
- **browser-first research**, centered on Files and the planned RCC Analysis
  Notebook/Workflow experience — **not yet released**.

Start with [RCC Expedition Light](getting-started/index.md), the required
first-use path, to set up SSH access on Windows 11 or macOS. If you prefer a
guided local course, use [RCC Expedition](rcc-expedition.md).

The course is designed so that a new user can progress without needing an
administrator beside them. Each class has a small practical exercise and a gate
that checks readiness without exposing credentials or generating significant
cluster load.

<section class="expedition-callout" aria-labelledby="expedition-title">
  <p class="expedition-kicker">Start here</p>
  <h2 id="expedition-title">Set up safe RCC access in 15 minutes</h2>
  <p>Today you use RCC through SSH, VS Code, and Slurm. A browser-first experience (Files → RCC Analysis Notebook or Workflow → Files) is planned but not yet released.</p>
  <div class="expedition-actions">
    <a class="expedition-primary" href="getting-started/index.md">Start Expedition Light →</a>
    <a href="analysis/rcc-analysis.md">See planned RCC Analysis</a>
    <a href="rcc-expedition.md">Open RCC Expedition</a>
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

The underlying compute model remains Slurm-backed, but users should not all have
to interact with the scheduler directly. The planned (not yet released)
user-facing model is:

```text
Files -> RCC Analysis
           |      |
           |      +-> Workflow: repeat / scale / reproduce
           +--------> Notebook: explore / visualize / prototype
        -> Files: durable results
```

The interactive session machinery previously described as **RCC Workbench** is
now treated as an implementation/advanced execution layer behind Analysis
Notebook mode rather than a separate primary research product.

RCC supports statistics, visualization, Python and R data science, machine
learning, GPU-accelerated AI, and distributed data processing. These techniques
remain part of a reproducible research workflow: computation runs through
Slurm, data stays within its project governance, and model evaluation includes
validation, uncertainty, bias, and scientific limitations.

Not sure which surface to use? Read
[RCC services: where should I go?](concepts/rcc-services.md). It also records
which newer browser surfaces are documented before release.

## Choose your path

<section class="path-grid" aria-label="Choose an RCC learning path">
  <article class="path-card analysis-path">
    <span class="path-number">01</span>
    <p class="path-label">Data analysis</p>
    <h3>Move from research data to a reproducible result</h3>
    <p>Use notebooks for bounded exploration and governed workflows for repeated or scalable analysis; learn Python, R, statistics, AI, efficient I/O, GPUs, validation, and result sharing.</p>
    <a class="path-action" href="paths/data-analysis.md">Follow the data analysis path →</a>
  </article>
  <article class="path-card development-path">
    <span class="path-number">02</span>
    <p class="path-label">Software development</p>
    <h3>Build reviewable workflows and protected services</h3>
    <p>Use advanced SSH/VS Code tools when needed; learn Git, Snakemake, Slurm, Conda, Apptainer, Python/R applications, Shiny, APIs, and governed deployment.</p>
    <a class="path-action" href="paths/software-development.md">Follow the software development path →</a>
  </article>
</section>

## Shared foundation

- Need the complete short version first? Read the
  [ClusterDocs NG TL;DR](tldr.md).
- Unsure which RCC surface to use? Start with the
  [RCC service map](concepts/rcc-services.md).
- Planning browser-based analysis? Read
  [RCC Analysis: notebooks and governed workflows](analysis/rcc-analysis.md).
- Need SSH/VS Code or direct Slurm? Those remain available as advanced/current
  paths in the [reference](reference/index.md).
- Use the [course overview](course/index.md) when you want the complete eighteen-class sequence.
- Working with human biomedical data: complete [Class 13](course/class-13-biomedical-data-privacy.md) before transfer or analysis.
- Connecting a laboratory instrument or acquisition workstation: see
  [how the lab network and RCC fit together](resources/how-it-all-works.md).
- Moving data from an instrument into analysis: complete
  [Class 16](course/class-16-wet-lab-data-workflows.md).
- Planning retention, Coscine archiving (not yet released), or defensible cleanup: complete
  [Class 17](course/class-17-data-lifecycle.md).
- Questions or feedback: [meet the RCC team and find the best contact route](team.md).
