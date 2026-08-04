# Class 2: reproducible scientific workflows

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

Use Snakemake to describe dependencies and submit work through Slurm. Do not keep a large workflow running as ordinary processes on the login host. Use a dry run before submission:

```bash
snakemake --dry-run --printshellcmds
```

Then use the managed RCC execution profile: `snakemake --profile IKIM`.

## Guided nf-core and Nextflow example

> **Optional prerequisite:** RCC does not currently publish a centrally
> managed, pinned Nextflow command. Before this exercise, ask the IKIM Cluster
> Mattermost channel for the approved project environment and version. The
> supplied runner stops without changing project data when `nextflow`,
> `apptainer`, or `sbatch` is missing; do not install an unpinned launcher just
> to bypass that check.

[nf-core](https://nf-co.re/) publishes reviewed community pipelines that run
with [Nextflow](https://www.nextflow.io/). They complement Snakemake: use the
workflow system that your reviewed analysis and research community support.
Do not translate a validated pipeline merely to standardize on one engine.

The class example runs the small public `nf-core/demo` test dataset. It pins the
pipeline release, submits processes through Slurm, runs tools in Apptainer, and
limits scheduler concurrency and process resources. From a local clone of the
class materials, copy the
[`rcc-test.config`](../classes/examples/nf-core/rcc-test.config) and
[`run-demo.sh`](../classes/examples/nf-core/run-demo.sh) files into an approved
project directory:

```bash
mkdir -p /projects/PROJECT/training/nf-core-demo
cp docs/classes/examples/nf-core/rcc-test.config \
  /projects/PROJECT/training/nf-core-demo/
cp docs/classes/examples/nf-core/run-demo.sh \
  /projects/PROJECT/training/nf-core-demo/
cd /projects/PROJECT/training/nf-core-demo
```

Replace `PROJECT` with a project to which you have access. Inspect both files,
then run one bounded test:

```bash
bash run-demo.sh "$PWD/run-01"
```

The test profile downloads public test data and container images. Run it only
when the RCC outbound proxy path is available; do not add tokens or copy
credentials into the project. The Nextflow coordinator stays on the approved
submission host while individual tasks use Slurm. Durable Nextflow state,
container images, and results remain on shared project storage so every worker
can reach them. Task bodies use `scratch = true`, which stages work through the
worker's `$TMPDIR` under `/local/tmp` and copies declared outputs back.

Inspect the run without opening every task directory:

```bash
squeue --me
nextflow log
find run-01/results -maxdepth 2 -type f | sort
```

The corresponding production-shaped RNA-seq example is intentionally a
template, not a command to paste unchanged. Review
[`params-rnaseq.example.json`](../classes/examples/nf-core/params-rnaseq.example.json),
replace every placeholder with approved project paths, select a reviewed
pipeline release, and validate the pipeline-specific samplesheet and reference
requirements before submission:

```bash
nextflow run nf-core/rnaseq \
  -r PINNED_RELEASE \
  -profile apptainer \
  -c rcc-test.config \
  -params-file params-rnaseq.json \
  -work-dir /projects/PROJECT/nextflow-work/rnaseq
```

Do not use the classroom resource caps for a real analysis without reviewing
the pipeline's requirements. The official [nf-core running guide](https://nf-co.re/docs/running/run-pipelines)
and the [Nextflow Slurm executor reference](https://docs.seqera.io/nextflow/executor#slurm)
explain the command structure and scheduler mapping.

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
