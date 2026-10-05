# From shell commands to a repeatable workflow

A useful analysis often begins as commands copied into a terminal. That is a
good experiment and a poor long-term record. This guide turns a working command
collection into a workflow another team member can review, rerun, and resume.

## Choose the smallest useful improvement

| Current situation | Next step |
|---|---|
| One short command used once | Record it in the project README with software version and inputs. |
| Several commands that must run in order | Put them in a strict shell script and submit it with `sbatch`. |
| Steps have named input and output files | Use Snakemake. |
| The team adopts an existing Nextflow or nf-core pipeline | Use managed `rcc-nextflow`. |
| Many independent samples use the same steps | Use Snakemake or Nextflow so Slurm can schedule each task. |

For a team-authored, file-oriented analysis, Snakemake is usually the simplest
first choice. Use Nextflow when the project already owns or adopts a reviewed
Nextflow pipeline, particularly an nf-core workflow. Do not translate between
workflow languages merely for fashion.

## 1. Write down the contract before rewriting code

For every command or script, record:

- input files and how they are validated;
- output files that prove the step completed;
- parameters and reference-data versions;
- software and version;
- CPU, memory, time, GPU, and temporary-storage needs;
- whether the step may be repeated safely; and
- what must remain available to resume after interruption.

Use synthetic or non-sensitive test data while restructuring the workflow.
Never put credentials, protected data, patient-related filenames, or private
keys in Git, support chat, container definitions, or examples.

## 2. Stabilise the shell script

Before introducing a workflow engine, make the current behavior explicit:

```bash
#!/usr/bin/env bash
set -euo pipefail

input=$1
output=$2
threads=${3:-1}

test -r "$input"
mkdir -p "$(dirname "$output")"

tool --threads "$threads" --input "$input" --output "$output"
test -s "$output"
```

Do not hide paths, sample names, or resource values inside a long script. Pass
them as arguments or read them from reviewed configuration. Send diagnostic
text to a log and make failure return a non-zero exit status.

## 3. Describe software with Conda, deploy it with Apptainer

Keep a small `environment.yml` beside the code while developing:

```yaml
name: analysis
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.12
  - samtools=1.21
```

Resolve and test it, then produce a lock file. For repeated or production RCC
work, build that locked environment into an immutable container and record its
digest. RCC executes the result with rootless Apptainer. Docker daemons do not
run on Slurm compute nodes.

The intended progression is:

```text
environment.yml
  -> resolved lock
  -> reviewed container build
  -> immutable SIF or digest-pinned OCI image
  -> Snakemake rule or Nextflow process
  -> Slurm worker running Apptainer
```

Conda remains useful for defining and resolving packages. The deployed
container prevents hundreds of jobs from repeatedly traversing an unpacked
Conda environment containing thousands of small files on shared storage.
Build images through the approved RCC or CI builder, not through a Docker
daemon on a compute worker.

## 4. Express files and dependencies

In Snakemake, one command becomes a rule:

```python
rule align:
    input:
        reads="inputs/{sample}.fastq.gz"
    output:
        bam="results/{sample}.bam"
    log:
        "logs/align/{sample}.log"
    threads: 8
    resources:
        mem_mb=32000,
        runtime=240,
        slurm_partition="cpu_nodes"
    container:
        "containers/alignment.sif"
    shell:
        "align.sh {input.reads} {output.bam} {threads} 2> {log}"
```

In Nextflow, the same boundary becomes a process:

```groovy
process ALIGN {
    tag sample_id
    cpus 8
    memory 32.GB
    time 4.h
    container 'docker://REGISTRY/PROJECT/ALIGNER@sha256:DIGEST'

    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path("${sample_id}.bam")

    script:
    """
    align.sh ${reads} ${sample_id}.bam ${task.cpus}
    """
}
```

The examples declare the task's files, software, and resources. The managed
RCC profile or launcher submits the task through Slurm. Do not call `sbatch`
inside a Snakemake rule or Nextflow process.

## 5. Use a project layout the team can understand

```text
/projects/<project>/analyses/<analysis>/
├── README.md
├── config/
├── workflow/
├── scripts/
├── envs/
├── containers/
├── inputs/
├── results/
├── logs/
└── tests/
```

Keep code, environment declarations, test configuration, and documentation in
Git. Keep research data, generated results, credentials, caches, installed
Conda environments, and workflow work directories out of Git.

## 6. Prove the small run before scaling

Use this order:

1. Run a shell-level test with tiny synthetic input.
2. Validate the workflow syntax and configuration.
3. Dry-run the complete dependency graph.
4. Run one or two representative samples through the RCC Slurm integration.
5. Inspect application logs and `sacct` CPU, memory, time, and exit status.
6. Correct the resource requests and failure behavior.
7. Rerun or resume and confirm completed work is reused.
8. Review scientific validity separately from technical success.

For Snakemake, use the managed RCC profile described in
[Class 6](../course/class-06-snakemake.md). For Nextflow, run the pinned
`rcc-nextflow` controller on a shell host or documented interactive allocation
and keep resume-critical work state in project storage as described in
[Class 7](../course/class-07-nextflow.md).

## 7. Ask for conversion help with a safe handoff

The RCC coding agent or workflow support can prepare a first conversion from:

- the scripts or commands, with secrets removed;
- a synthetic example input and expected output;
- the current `environment.yml`, lock file, or version list;
- an estimate of sample count and file sizes;
- one successful log and one representative failure, both sanitized; and
- known CPU, memory, time, GPU, and I/O behavior.

Ask for a dry-run-capable workflow, synthetic tests, explicit Slurm resources,
a pinned Apptainer runtime, restart behavior, and a short README. The project
team still reviews the scientific method, parameters, reference data, and
interpretation.

## Completion gate

The conversion is ready for team use when:

- a new user can identify every input, output, parameter, and software image;
- the small synthetic test passes twice without repeating completed work;
- each scientific task runs through Slurm with bounded resources;
- a failed task stops dependent work and leaves a useful log;
- project storage contains durable state while scratch contains only temporary
  task files; and
- the retained run records code revision, configuration, image digest, input
  identity, Slurm evidence, outputs, and scientific validation.
