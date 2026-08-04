# Nextflow on RCC

> **Service status — not yet released:** this class documents the planned RCC
> Nextflow-to-Slurm service so projects can prepare. The pinned `rcc-nextflow`
> launcher and institutional configuration are not active for users yet. Do not
> run these commands until RCC announces the service; use the ready managed
> Snakemake path in the meantime.

> **The planned supported pattern:** start Nextflow in `tmux` on **shellhost**.
> Nextflow submits each process to Slurm. Keep the Nextflow work directory on
> shared project storage, use Apptainer for software, and opt into node-local
> scratch only for processes that benefit from it.

Do not run Nextflow on `login.ikim.uk-essen.de`, `login1`, or `login2`. Those
machines are SSH gateways. Do not run the Nextflow controller inside an
ordinary compute job unless RCC administrators have approved a dedicated
service design.

## Learning objectives

After this class, you can:

- explain what will run on shellhost and what runs on compute nodes;
- start a persistent Nextflow controller in `tmux` after release;
- use the RCC launcher and a shared project root;
- request CPU, memory, time, short-queue, scratch, array, and GPU resources;
- use Apptainer without placing Conda environments on shared storage;
- resume an interrupted pipeline safely; and
- inspect Slurm and Nextflow evidence when something fails.

## 1. How the pieces fit together

```text
Your laptop
  -> login.ikim.uk-essen.de
       -> shellhost
            -> Nextflow JVM
                 -> sbatch
                      -> RCC compute node
                           -> Bash task wrapper
                           -> Apptainer application
                           -> optional /local scratch
```

The Nextflow program remains on shellhost. It reads the pipeline graph, decides
which tasks are ready, and submits them to Slurm. Slurm allocates CPUs, memory,
time, partitions, and GPUs. Scientific computation occurs only in Slurm jobs.
Compute workers execute generated task wrappers and do not need their own Java
or Nextflow installation.

## 2. Prepare a shared project root

After the service is released, choose the project directory that owns the
workflow and results:

```bash
export RCC_PROJECT_ROOT=/projects/MY_PROJECT
mkdir -p "$RCC_PROJECT_ROOT"
```

Replace `MY_PROJECT` with a directory you are authorized to use. The launcher
creates these private per-user directories:

```text
/projects/MY_PROJECT/.nextflow/USERNAME/work
/projects/MY_PROJECT/.nextflow/USERNAME/apptainer-cache
```

The work directory is part of Nextflow's cache and resume mechanism. Never set
it below `/local`. Local scratch is disposable and belongs to one compute job;
a later task may run on another node.

## 3. Start the controller in tmux

After release, connect to the approved submission host and create a persistent
terminal session:

```bash
tmux new -s nextflow
```

Inside the `tmux` session:

```bash
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" run PIPELINE [OPTIONS]
```

Detach without stopping Nextflow:

```text
Ctrl-b, then d
```

Return later:

```bash
tmux attach -t nextflow
```

A dropped laptop or jump-host connection then does not terminate the workflow
controller.

## 4. First bounded RCC workflow

The copyable example is in
[`examples/nextflow-rcc`](examples/nextflow-rcc/README.md). After release, copy
that directory into your project, enter it, and run:

```bash
rcc-nextflow \
  --project-root "$RCC_PROJECT_ROOT" \
  run main.nf \
  -c nextflow.config \
  -with-trace trace.tsv \
  -with-report report.html \
  -with-timeline timeline.html
```

The example submits two small `cpu_short` jobs. One uses the shared task work
directory; one uses node-local scratch and returns only its declared output.
Every example has strict CPU, memory, and time limits.

Run it again with:

```bash
rcc-nextflow \
  --project-root "$RCC_PROJECT_ROOT" \
  run main.nf \
  -c nextflow.config \
  -resume
```

The second run should reuse completed task results. Keep the same project root,
pipeline revision, inputs, and work directory for resume to succeed.

## 5. Resource requests

Nextflow process directives map to Slurm requests:

```groovy
process ALIGN {
    cpus 8
    memory 32.GB
    time 4.h

    script:
    """
    aligner --threads ${task.cpus} input.fastq.gz > output.bam
    """
}
```

Request what the program can actually use. More CPUs or memory can increase
queue time without reducing runtime.

### Short jobs

Apply the RCC label only when every task instance is guaranteed to finish
within two hours:

```groovy
label 'rcc_short'
```

This selects `cpu_short` and a maximum task time of two hours.

### Local scratch

Use local scratch for repeated random I/O, temporary databases, sorting,
assembly, decompressed intermediates, or very large numbers of temporary files:

```groovy
label 'rcc_scratch'
```

Nextflow creates a unique task directory below the Slurm job's `$TMPDIR`, stages
inputs, executes locally, copies declared outputs back with `rsync`, and removes
the task scratch directory after successful stage-out.

Do not label every process as scratch. Copying a multi-terabyte input for one
sequential pass may cost more than reading it once from shared storage.

### Job arrays

For a process with many tasks and identical resource requirements:

```groovy
label 'rcc_array'
```

RCC initially groups up to 50 tasks per Slurm array submission. CPUs, memory,
time, queue, and cluster options must be uniform for all array members. Failed
members can be retried separately.

## 6. GPU labels

Request any standard GPU:

```groovy
label 'rcc_gpu'
```

Request the current exact RTX A6000 type:

```groovy
label 'rcc_gpu_a6000'
```

Request an architecture family:

```groovy
label 'rcc_gpu_ampere'
// or, when a standard Blackwell node is available in gpu_nodes:
label 'rcc_gpu_blackwell'
```

Request the special ARM64/GB10 platform only when the workflow supports that
architecture and platform policy:

```groovy
label 'rcc_ai_top_atom'
```

RCC adds Apptainer `--nv` for these labels. GPU VRAM is not the same resource
as host memory requested with `memory`.

## 7. Containers

RCC uses Apptainer for Nextflow tasks. A process can declare an immutable image:

```groovy
process TOOL {
    container 'docker://REGISTRY/PROJECT/IMAGE@sha256:DIGEST'
    cpus 4
    memory 8.GB
    time 1.h

    script:
    """
    tool --threads ${task.cpus}
    """
}
```

Prefer a reviewed SIF file or a digest-pinned OCI reference. Do not use mutable
`latest` tags. The per-user Apptainer cache is on shared project storage so a
job scheduled on another node can reuse the image.

Avoid Nextflow-managed Conda as the default RCC profile. Conda environments
contain many small files and create poor metadata-I/O patterns on shared
storage. Use Apptainer unless a reviewed pipeline has a specific exception.

## 8. Running nf-core pipelines

After release, use an explicit pipeline release and the pipeline's Apptainer
profile:

```bash
rcc-nextflow \
  --project-root "$RCC_PROJECT_ROOT" \
  run nf-core/rnaseq \
  -r RELEASE_TAG \
  -profile apptainer \
  -resume \
  --input samplesheet.csv \
  --outdir results
```

Replace `RELEASE_TAG` with a reviewed release. Do not implicitly follow a
pipeline's changing default branch. Pilot a small synthetic or non-sensitive
input before launching a complete study.

The RCC institutional config is appended by the launcher. The pipeline may
keep its own profiles and process-specific resources, while RCC retains the
Slurm executor, approved partitions, bounded scheduler interaction, and
Apptainer runtime.

## 9. Monitor the run

Nextflow view:

```bash
cat .nextflow.log
column -t -s $'\t' trace.tsv | less -S
```

Slurm view:

```bash
squeue -u "$USER" -o '%.18i %.16j %.10T %.10M %.6D %R'
sacct -S today -u "$USER" \
  --format=JobID,JobName%30,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

A pending reason such as `Resources`, `Priority`, or `QOS...` is scheduler
information, not a signal to submit duplicate workflows.

## 10. Failures and resume

After correcting the input, configuration, resource request, or software issue:

```bash
rcc-nextflow \
  --project-root "$RCC_PROJECT_ROOT" \
  run PIPELINE [THE SAME OPTIONS] \
  -resume
```

Do not delete the work directory as a first troubleshooting step. Do not start
several copies of the same workflow because one appears slow. Record:

- the Nextflow command and exact pipeline revision;
- the Nextflow run name;
- relevant `.nextflow.log` lines;
- Slurm job IDs and states;
- the failed task work directory;
- requested and observed resources; and
- whether the process used shared or local scratch.

Never include passwords, tokens, private keys, or patient-identifying data in a
support request.

## 11. Decision checklist

After the service is released and before a large run, confirm:

- Nextflow is running on shellhost inside `tmux`;
- the project root and `NXF_WORK` are shared and persistent;
- the pipeline is pinned to an exact revision;
- Apptainer images are reviewed or digest-pinned;
- each task has realistic CPU, memory, and time requests;
- scratch is used only where its staging cost is justified;
- high-fan-out uniform processes use arrays where appropriate;
- a small pilot completed and resumed successfully; and
- primary identifying patient data is absent.

## Take-home rule

> Once released, Nextflow orchestrates on shellhost. Slurm computes on workers.
> Shared storage preserves workflow state. `/local` accelerates selected tasks.
> Apptainer carries the software. Keep the revision and work directory so
> `-resume` works.
