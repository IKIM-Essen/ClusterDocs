# RCC Migration Assistant

This is for experienced users who already know how they worked on the old IKIM
cluster and do **not** want to reread a beginner course just to discover what
changed.

The assistant uses the same visual/process language as RCC Journey: identify the
old habit, show why RCC changed it, and point to the smallest current action.
The authoritative detailed comparison remains
[What changed from the old cluster?](what-changed.md).

<section class="expedition-callout" aria-labelledby="migration-title">
  <p class="expedition-kicker">Old habit → current RCC practice</p>
  <h2 id="migration-title">Tell us what you still do</h2>
  <p>You do not need to migrate everything at once. Pick the habits that still describe your setup and change one boundary at a time.</p>
  <div class="expedition-actions">
    <a class="expedition-primary" href="#access">I still start with SSH →</a>
    <a href="#storage">I still mount/browse storage →</a>
    <a href="#workflows">I still run scripts by hand →</a>
    <a href="#resources">I still request nodes/resources the old way →</a>
  </div>
  <p class="expedition-privacy">Do not delete known_hosts, disable SSH verification, recursively chmod data, or bulk-move files just to make an old setup resemble a new example.</p>
</section>

## Migration state

```text
OLD RCC HABITS
      │
      ▼
● keep the scientific work that still matters
○ identify one old assumption at a time
○ translate it to the current RCC service model
○ test the new path with bounded work
○ keep evidence that the new path behaves correctly
      │
      ▼
● NEW RCC HABITS WITHOUT A FLAG DAY
```

`●` means established; `○` is the next available step; `×` means blocked or no
longer supported; `!` marks something that deserves explicit attention.

<section class="path-grid" aria-label="Migration assistant topics">
  <article class="path-card analysis-path" id="access">
    <span class="path-number">01</span>
    <p class="path-label">Access</p>
    <h3>I still think “using the cluster” means SSHing to a login host</h3>
    <p><code>×</code> The forwarding gateway is not a work destination and users do not choose workers directly.</p>
    <p><code>○</code> Start from the research task. Browser Files/Analysis are first-class paths; advanced users can use the supported shell-host alias through the jump host.</p>
    <a class="path-action" href="../concepts/jump-shell-compute.md">See jump, shell, and compute roles →</a>
  </article>
  <article class="path-card development-path" id="storage">
    <span class="path-number">02</span>
    <p class="path-label">Storage & I/O</p>
    <h3>I still browse large shared trees through SSHFS, Finder, Explorer, or VS Code</h3>
    <p><code>!</code> Large directory scans, small-file activity, indexing, and random temporary I/O can become the bottleneck even when raw bandwidth looks large.</p>
    <p><code>○</code> Keep durable data with the project; use supported transfer paths and stage active temporary/random work to node-local scratch when useful.</p>
    <a class="path-action" href="../course/class-14-efficient-io.md">Open efficient-I/O guidance →</a>
  </article>
  <article class="path-card analysis-path" id="workflows">
    <span class="path-number">03</span>
    <p class="path-label">Scripts & workflows</p>
    <h3>I still have a folder of scripts and commands that I run in the right order by memory</h3>
    <p><code>●</code> Keep the scripts. Existing scientific work is useful input.</p>
    <p><code>○</code> RCC's assistant direction is to infer dependencies, create a locked environment/container, and generate Snakemake or Nextflow where a workflow helps—without requiring you to write workflow code first.</p>
    <a class="path-action" href="../paths/from-shell-scripts.md">Convert existing scripts into a repeatable workflow →</a>
  </article>
  <article class="path-card development-path" id="resources">
    <span class="path-number">04</span>
    <p class="path-label">Compute sizing</p>
    <h3>I still copy an old memory/time/node request because it used to work</h3>
    <p><code>×</code> Static node selection and inherited resource guesses are not the service contract.</p>
    <p><code>○</code> Request bounded capabilities, let Slurm place the job, and use measured CPU/RAM/GPU/I/O evidence to right-shape later runs.</p>
    <a class="path-action" href="../reference/slurm.md">Open current Slurm guidance →</a>
  </article>
  <article class="path-card analysis-path" id="projects">
    <span class="path-number">05</span>
    <p class="path-label">Groups & projects</p>
    <h3>I still solve collaboration by changing groups, broad permissions, or sharing paths informally</h3>
    <p><code>×</code> Primary groups are organizational identity, not the collaboration boundary.</p>
    <p><code>○</code> The project is the governed workroom: approved people, data, compute, services, results, and lifecycle stay connected there.</p>
    <a class="path-action" href="../reference/users-groups-projects.md">See users, groups, and projects →</a>
  </article>
  <article class="path-card development-path" id="agents">
    <span class="path-number">06</span>
    <p class="path-label">AI & coding agents</p>
    <h3>I want an agent to help, but the old model never had a safe agent path</h3>
    <p><code>!</code> If an external/general-purpose service can read protected files or retrieved context, treat that material as disclosed to the service.</p>
    <p><code>○</code> Prefer a data-blind path: documentation, schemas, synthetic fixtures, bounded diagnostics, explicit contracts, returned code, and real-data execution inside RCC.</p>
    <a class="path-action" href="../concepts/agents-and-mcp.md">See the data-blind agent pattern →</a>
  </article>
</section>

## One migration example: old scripts to reproducible RCC execution

```text
old folder
  analysis.py
  helper.R
  commands.txt
      │
      ▼
● keep the scientific logic
○ discover dependencies
○ generate Conda environment + lock
○ package reproducible container
○ generate Snakemake / Nextflow if useful
○ test on bounded examples
○ run against real project data in RCC
      │
      ▼
● reproducible execution package
```

The point is not to reward users for adopting a particular workflow engine. The
point is that the scientist should be able to preserve and rerun the method
without reconstructing the execution environment from memory.

## One migration example: old node thinking to service thinking

![Illustrated RCC Slurm execution path](../assets/slurm-execution-flow.svg)

The new mental model is deliberately capability-based: describe CPU, memory,
time, and GPU requirements; Slurm chooses an eligible place to run. Hardware can
change behind that contract.

## What should not be automated blindly

A migration assistant can inspect or explain an old configuration, but it should
not silently make broad destructive changes.

- `×` do not erase the entire SSH trust database;
- `×` do not disable host-key verification;
- `×` do not recursively change permissions across project data;
- `×` do not copy/move large datasets simply to match a documentation example;
- `×` do not convert every script into a workflow merely because automation is
  available; and
- `!` do not treat an AI-generated migration as authoritative until the explicit
  configuration/artifacts are reviewed and bounded tests pass.

## Need the complete old-to-new table?

Use [What changed from the old cluster?](what-changed.md) for the full detailed
comparison of access, VS Code, Slurm, storage, Conda, Snakemake, Nextflow,
projects, data transfer, notebooks, AI assistance, and biomedical-data handling.
