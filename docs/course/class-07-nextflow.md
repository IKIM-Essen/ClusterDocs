# Class 7: Nextflow on RCC

> **Service status — not yet released:** this numbered class documents the planned RCC
> Nextflow-to-Slurm service so projects can prepare. The pinned `rcc-nextflow`
> launcher and institutional configuration are not active for users yet. Do not
> run these commands until RCC announces the service; use the ready managed
> Snakemake path in the meantime.

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 7 min video</p>
  <h2>Watch the class first</h2>
  <p>The planned controller on an RCC interactive node (a shellhost), Slurm tasks, shared resume state, local scratch, GPU labels, Apptainer, nf-core, and failure recovery. Watch the lesson as preparation; the managed service is not yet released.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class7.png" src="{{ media_base_url }}/RCC_Onboarding_Class_7_Video_Enhanced.mp4?v=818f6aa4">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Class_7_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

> **The planned supported pattern:** start Nextflow in `tmux` on an RCC
> **interactive node (`shellhost`)**.
> Nextflow submits each process to Slurm. Keep the Nextflow work directory on
> shared project storage, use Apptainer for software, and opt into node-local
> scratch only for processes that benefit from it.

Do not run Nextflow on `login.ikim.uk-essen.de`, `login1`, or `login2`. Those
machines are SSH gateways. Do not run the Nextflow controller inside an
ordinary compute job unless RCC administrators have approved a dedicated
service design.

## Learning objectives

After this class, you can:

- explain what runs on the interactive node (`shellhost`) and what runs on compute nodes;
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
       -> RCC interactive node (shellhost)
            -> Nextflow JVM
                 -> sbatch
                      -> RCC compute node
                           -> Bash task wrapper
                           -> Apptainer application
                           -> optional /local scratch
```

The Nextflow program remains on the interactive node (`shellhost`). It reads the pipeline graph, decides
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

After release, connect to an RCC interactive node (a `shellhost`) and create a
persistent terminal session. Do not start this controller on the preceding SSH
gateway or inside a compute-worker allocation:

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
[`examples/nextflow-rcc`](../classes/examples/nextflow-rcc/README.md). After release, copy
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

The separate bounded nf-core example pins `nf-core/demo` release `1.2.0`, uses
public synthetic test data, caps scheduler concurrency, and supplies teaching
resources through
[`rcc-test.config`](../classes/examples/nf-core/rcc-test.config). Its
[`run-demo.sh`](../classes/examples/nf-core/run-demo.sh) wrapper fails closed
unless `rcc-nextflow`, `apptainer`, and `sbatch` are present.

After release, copy both files into an approved project directory and run:

```bash
bash run-demo.sh /projects/PROJECT \
  /projects/PROJECT/training/nf-core-demo/run-01
```

The first run may retrieve pipeline source, public test data, and reviewed
container images through the approved proxy path. Do not add tokens or copy
credentials into the project.

For a real pipeline, use an explicit release and its Apptainer profile:

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

The production-shaped
[`params-rnaseq.example.json`](../classes/examples/nf-core/params-rnaseq.example.json)
is a template, not a command to paste unchanged. Replace every placeholder
with approved project paths, validate the samplesheet and references, and
review the pipeline-specific resource requirements before submission.

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

- Nextflow is running on an interactive node (`shellhost`) inside `tmux`;
- the project root and `NXF_WORK` are shared and persistent;
- the pipeline is pinned to an exact revision;
- Apptainer images are reviewed or digest-pinned;
- each task has realistic CPU, memory, and time requests;
- scratch is used only where its staging cost is justified;
- high-fan-out uniform processes use arrays where appropriate;
- a small pilot completed and resumed successfully; and
- primary identifying patient data is absent.

## Completion gate

Before release, you have completed the preparation gate when you can explain:

1. why the controller runs on an interactive node (`shellhost`), never an SSH
   gateway or worker allocation;
2. why every scientific task goes through Slurm;
3. why `NXF_WORK` stays on persistent shared project storage;
4. when `/local` task scratch helps and how outputs return;
5. why workers need Apptainer, but not Java or Nextflow; and
6. which revisions, parameters, reports, image digests, checksums, and Slurm
   IDs form retained provenance.

After RCC releases `rcc-nextflow`, run the bounded synthetic example and verify
that `-resume` reuses completed work.

## Take-home rule

> Once released, Nextflow orchestrates on an interactive node (`shellhost`). Slurm computes on workers.
> Shared storage preserves workflow state. `/local` accelerates selected tasks.
> Apptainer carries the software. Keep the revision and work directory so
> `-resume` works.
