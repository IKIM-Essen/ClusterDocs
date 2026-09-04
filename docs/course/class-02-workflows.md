# Class 2: reproducible scientific workflows

> **Starting from scripts or copied commands?** Use the
> [script-to-workflow conversion guide](../paths/from-shell-scripts.md)
> first. It turns the current analysis into explicit inputs, outputs,
> software, resources, and a small test before choosing Snakemake or Nextflow.

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 9 min video</p>
  <h2>Watch the class first</h2>
  <p>Projects, environments, Snakemake, Slurm, and reproducibility. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/part2.png" src="{{ media_base_url }}/RCC_Onboarding_Part_2_Video_Enhanced.mp4?v=28494fd2">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Part_2_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

## Learning objectives

You will create a project that separates raw data, workflow definitions,
software declarations, logs, benchmarks and generated results. You will also
compare a project-authored Snakemake workflow with a versioned community
pipeline run through Nextflow and nf-core.

## Recommended layout

```text
project/
├── config/
├── workflow/
├── scripts/
├── envs/
├── data/raw/        # treated as read-only
├── results/         # generated
├── logs/
└── benchmarks/
```

Git should contain workflow logic, text configuration and documentation. It should not contain credentials, private keys, patient identifiers, raw research data or large generated outputs.

VS Code with Remote - SSH is the suggested project interface for most users.
Open this repository directory rather than the project-storage root, review Git
changes before committing, and exclude `data/`, `results/`, environments, and
workflow caches from search and file watching.

## Good cluster pattern

Use a workflow engine to describe dependencies and submit scientific work
through Slurm. Do not keep a large workflow running as ordinary processes on
an SSH gateway. Class 6 teaches the ready-now managed Snakemake path; Class 7
teaches the ready-now managed Nextflow path.

The first safe question is always a non-mutating dry run. For Snakemake:

```bash
snakemake --dry-run --printshellcmds
```

Then continue with [Class 6: Snakemake on RCC](class-06-snakemake.md). If a
reviewed project uses Nextflow or nf-core, read [Class 7](class-07-nextflow.md)
for the managed controller, Slurm, shared-work, scratch, Apptainer, and
`-resume` boundary. **Managed Nextflow support is ready now.**

## Software environments inside jobs

Keep the environment declaration in Git and create it inside an allocated
worker. In a non-interactive Slurm script, load the shell hook before activation:

```bash
eval "$(conda shell.bash hook)"
conda activate analysis
srun python analysis.py
```

Do not run `conda init` in every job. Confirm environment and package caches use
the approved node-local paths rather than metadata-sensitive shared storage.

> **Reference companion:** [Conda, Snakemake, Nextflow, nf-core, and Apptainer](../reference/software-workflows.md)
> covers batch activation, Snakemake sessions, Nextflow and nf-core, explicit
> container binds, cache placement, GPU exposure, and reproducibility records.

## Security moment

A reproducible workflow is also a security control: changes can be reviewed, inputs and outputs are explicit, and unexpected code is easier to identify. Pin software versions, review contributed scripts, and never run downloaded code merely because it is in a shared project directory.

## Self-learning exercise

Build a three-rule workflow that creates a small synthetic input, transforms it, and writes a checksum. Run it twice and verify that the second run performs no unnecessary work.

## Knowledge check

<details><summary>Why keep raw data read-only?</summary>

It protects the original evidence and makes the transformation from input to result reproducible.
</details>

<details><summary>What belongs in Git?</summary>

Workflow logic, scripts, environment declarations, small configuration files and documentation—not credentials or controlled data.
</details>

## Completion gate

- The workflow dry run succeeds.
- The first run creates the expected checksum.
- The second run reports that no work is required.
- `git status` contains no credentials, private data, raw datasets or generated result directories.
