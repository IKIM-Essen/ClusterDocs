# RCC ClusterDocs

RCC is a governed research-computing platform for taking research data from
acquisition to analysis, reproducible results, collaboration, preservation, and
where appropriate downstream publication or archive submission.

RCC supports both **browser-first research** and **advanced command-line/developer
access**. You do **not** need to become an HPC operator to use RCC. Ordinary
researchers should be able to work through the browser; SSH, VS Code, Slurm, and
the deeper technical layers remain available for people who need them.

<section class="expedition-callout" aria-labelledby="expedition-title">
  <p class="expedition-kicker">Start with the research task, not the infrastructure</p>
  <h2 id="expedition-title">What do you want to do?</h2>
  <p>Choose project data, analyse it, manage the project, or open the advanced technical path. RCC keeps the same project identity and authorization underneath each interface.</p>
  <div class="expedition-actions">
    <a class="expedition-primary" href="concepts/rcc-files.md">Work with project files →</a>
    <a href="analysis/rcc-analysis.md">Analyse data →</a>
    <a href="concepts/projects-and-capabilities.md">Manage a project →</a>
    <a href="reference/access-ssh-vscode.md">Advanced SSH / VS Code →</a>
  </div>
  <p class="expedition-privacy">Browser-first by design: having an RCC account does not imply that you need an SSH key.</p>
</section>

## The normal research journey

For a researcher, the important sequence is simple:

1. **Bring or choose project data.** Use Files, a project share, a managed
   instrument path, or another approved project ingestion route.
2. **Analyse the data.** Use an interactive Notebook for exploration or a
   governed Workflow for repeatable/scalable work in RCC Analysis.
3. **Keep durable results with the project.** Results, provenance, code, and
   relevant metadata stay tied to the project rather than to one laptop or
   browser session.
4. **Preserve or publish when appropriate.** Use the project's approved
   lifecycle, including Coscine preservation when that route is released and
   domain applications that support downstream archive submission.

RCC handles the infrastructure mechanics behind those actions. The researcher
still controls the scientific question, data, method, parameters, and decision
about what result is fit for use.

## ClusterDocs 3 release bundle

ClusterDocs 3 is **not** intended to publish before the integrated browser
experience is ready. The minimum release bundle is:

- **RCC Home** — the front door and authoritative view of enabled RCC services;
- **Files** — browser project-data entry and exit;
- **RCC Analysis** — Notebook for exploration and Workflow for repeatable or
  scalable scientific execution;
- **My RCC** — personal account, preferences, project membership, invitations,
  and self-service actions; and
- **RCC Admin** — the role-aware approval and administration surface for people
  who hold those capabilities.

These are not independent future add-ons to ClusterDocs 3. They are the core
user experience that this documentation release is meant to describe and must be
ready together before publication. The same RCC identity, project authorization,
and policy must follow the user across all five surfaces.

The current `clusterdocs-3` branch is therefore a **release candidate**, not a
public promise that the browser bundle is already live. In particular, RCC
Analysis remains a release blocker until its Notebook/Workflow path and its
integration with RCC Home, Files, My RCC, and RCC Admin pass acceptance.

Videos are separate: the written/product release can ship with video players
fail-closed, and the regenerated/reviewed videos can follow in the later media
stage.

Other capabilities such as RCC-to-Coscine self-service, protected project
vhosts, and selected vendor integrations may remain separately staged when the
core ClusterDocs 3 bundle releases; their own pages must continue to state that
truth explicitly.

## What RCC can do

The new RCC is much more than a remote shell with a web front end. Experienced
users should start with [What RCC can do](concepts/what-rcc-can-do.md), which
covers the complete platform and the release status of each capability.

Highlights include:

- **instrument-to-project ingestion** for sequencers, microscopes, mass
  spectrometers, acquisition workstations, and other research devices;
- **project storage chosen for the workload**, including ordinary shared project
  storage and S3/object storage where enabled and scientifically appropriate;
- **Jupyter-first interactive analysis** plus governed repeatable workflows;
- **Slurm, GPUs, containers, and direct HPC controls** for advanced users;
- **self-service and delegated project governance** without handing out broad
  infrastructure-administrator privileges;
- **AI and coding-agent assistance without exporting protected project data**:
  agents can explain, design, test on synthetic examples, develop workflows,
  and interpret bounded diagnostics while RCC executes against real data inside
  the governed environment;
- **reproducibility and provenance** across workflows, results, software, and
  project lifecycle decisions;
- **Coscine preservation** through the governed RCC-to-Coscine path when
  released; that transfer is **not yet released** in the current candidate; and
- **domain applications such as SeqLab**, which demonstrate how RCC can connect
  acquisition, analysis, review, provenance, and submission to appropriate
  international archives without making the researcher assemble the underlying
  infrastructure by hand.

A capability being documented does not automatically mean it is active. Pages
that describe separately staged functionality must say so explicitly.

## One project, many interfaces

Think of an RCC project as the shared research workroom. It connects the approved
people, data, compute, services, results, and lifecycle for one purpose.
Switching from Files to Analysis, an agent-assisted workflow, My RCC, RCC Admin,
VS Code, or a command line does not create a new authority boundary.

Your primary group records your organizational home. It is not the mechanism for
sharing cross-department research data. Add collaborators to the project instead
of moving them into another primary group merely to share data. For the exact
vocabulary used throughout ClusterDocs, see the
[RCC terminology reference](reference/terminology.md).

## AI assistance without giving the agent the dataset

The preferred agent pattern is **data-blind by default**. Give an external or
general-purpose agent documentation, schemas, synthetic fixtures, public code,
and carefully bounded diagnostics. Let it help design or debug the workflow.
RCC then runs the resulting code/workflow against the real project data inside
the governed boundary.

This separation lets users benefit from strong coding and reasoning assistance
without making disclosure of protected research data the price of using AI.
Read [AI and coding agents without exposing project data](concepts/agents-and-mcp.md).

## Choose a deeper path

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

## Learn only as much infrastructure as you need

- New to RCC? Use [Start here: your first 15 minutes](getting-started/index.md).
- Unsure which interface to use? Read the [RCC service map](concepts/rcc-services.md).
- Want the complete capability picture? Read [What RCC can do](concepts/what-rcc-can-do.md).
- Need the technical reference? Open the [day-to-day reference](reference/index.md).
- Working with human biomedical data? Complete [Class 13](course/class-13-biomedical-data-privacy.md) before transfer or analysis.
- Connecting an instrument or acquisition workstation? Start with
  [Choosing an instrument-data transfer path](data/instrument-data-options.md).
- Planning retention or archival? Use [Class 17](course/class-17-data-lifecycle.md).
- Prefer a guided local course? Use [RCC Expedition](rcc-expedition.md).
- Questions or feedback? [Meet the RCC team and find the support route](team.md).
