# Class 7: Nextflow on RCC

> **Service status — ready now:** RCC provides the pinned `rcc-nextflow`
> launcher and institutional Slurm configuration on its shellhosts and
> allocation-backed interactive nodes. Ordinary workers execute the submitted
> tasks and do not host workflow controllers.

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 7 min video</p>
  <h2>Watch the class first</h2>
  <p>The managed controller on an RCC shellhost or allocation-backed interactive node, Slurm tasks, shared resume state, local scratch, GPU labels, Apptainer, nf-core, and failure recovery.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class7.png" src="{{ media_base_url }}/RCC_Onboarding_Class_7_Video_Enhanced.mp4?v=818f6aa4">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Class_7_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

> **Five rules for the supported service:**
>
> 1. Run **one Nextflow controller per analysis** on an RCC shellhost,
>    normally in `tmux`, or in an allocation-backed interactive session.
> 2. Let `rcc-nextflow` provide Slurm and Apptainer policy; do not build a
>    second site configuration.
> 3. Keep Nextflow work state on persistent shared project storage; use
>    `/local` only as task scratch.
> 4. Start with a representative pilot, measure CPU, memory, and I/O, then tune
>    only the processes that need it.
> 5. When a run stops, diagnose it and use `-resume`; do not launch duplicate
>    controllers as a retry mechanism.

Do not run Nextflow on `login.ikim.uk-essen.de`, `login1`, or `login2`. Those
machines are SSH gateways. Do not run the Nextflow controller inside an
ordinary compute job. Scientific processes are the Slurm jobs; the controller
only plans, submits, monitors, and records them.

## Learning objectives

After this class, you can:

- explain what runs on the shellhost or interactive allocation and what runs on compute nodes;
- start a persistent Nextflow controller in `tmux`;
- use the RCC launcher and a shared project root;
- pilot, measure, and tune task CPU, memory, time, and I/O;
- request short-queue, scratch, array, and GPU resources;
- use Apptainer without placing Conda environments on shared storage;
- resume an interrupted pipeline safely; and
- inspect Slurm and Nextflow evidence when something fails.

## 1. The mental model

```text
Your laptop
  -> login.ikim.uk-essen.de
       -> RCC shellhost or allocation-backed interactive node
            -> Nextflow JVM
                 -> sbatch
                      -> RCC compute node
                           -> Bash task wrapper
                           -> Apptainer application
                           -> optional /local task scratch

persistent project storage
  <- Nextflow work and cache state
  <- declared task outputs
  <- final published results
```

The Nextflow program remains on the shellhost or interactive allocation. It reads the pipeline graph, decides
which tasks are ready, and submits them to Slurm. Slurm allocates CPUs, memory,
time, partitions, and GPUs. Scientific computation occurs only in Slurm jobs.
Compute workers execute generated task wrappers and do not need their own Java
or Nextflow installation. Nextflow describes dependencies, Slurm allocates
machines, and RCC provides execution policy.

## 2. Keep RCC site policy and user resources separate

Choose the project directory that owns the
workflow and results, and give each analysis its own directory:

```bash
export RCC_PROJECT_ROOT=/projects/MY_PROJECT
mkdir -p "$RCC_PROJECT_ROOT/analyses/wes-2026-08"
cd "$RCC_PROJECT_ROOT/analyses/wes-2026-08"
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

The launcher supplies the institutional Nextflow configuration: the Slurm
executor, approved partitions, bounded scheduler interaction, Apptainer, and
shared work/cache placement. Do not copy a complete `slurm.config` or redefine
site controls such as:

```groovy
process.executor
process.queue
process.clusterOptions
executor.queueSize
executor.submitRateLimit
apptainer.enabled
apptainer.cacheDir
workDir
```

Those settings affect scheduling, node placement, the container runtime, or
resume-critical state and belong to RCC. Tune scientific task resources only
after measuring a pilot; the example `resources.config.example` shows that
narrow boundary.

## 3. One analysis, one active controller

Connect to an RCC shellhost and create a persistent terminal session, or start
the controller inside an allocation-backed interactive session. Do not start
this controller on the preceding SSH gateway or inside an ordinary batch-worker
allocation:

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

Before starting another command because a workflow looks quiet, check:

```bash
tmux ls
pgrep -af '[n]extflow.*run' || true
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" log 2>/dev/null || true
squeue -u "$USER"
```

If the controller is still running, do not start another copy of the same
analysis. Nextflow protects session/cache state with locks, and duplicate
controllers can duplicate expensive Slurm work.

The class example includes `run-rcc-nextflow.sh`. It uses a lock scoped to the
analysis directory and preserves a timestamped controller log below `logs/`.
After copying it into the analysis directory:

```bash
chmod +x run-rcc-nextflow.sh
./run-rcc-nextflow.sh run main.nf
```

## 4. First bounded RCC workflow

The copyable example is in
[`examples/nextflow-rcc`](../classes/examples/nextflow-rcc/README.md). Copy
that directory into your project, enter it, and run:

```bash
./run-rcc-nextflow.sh \
  run main.nf \
  -with-trace trace.tsv \
  -with-report report.html \
  -with-timeline timeline.html
```

The example submits two small `cpu_short` jobs. One uses the shared task work
directory; one uses node-local scratch and returns only its declared output.
Every example has strict CPU, memory, and time limits.

Run it again with:

```bash
./run-rcc-nextflow.sh \
  run main.nf \
  -with-trace trace-resume.tsv \
  -resume
```

The second run should reuse completed task results. Keep the same project root,
pipeline revision, inputs, and work directory for resume to succeed.

## 5. Pilot, measure, tune, then scale

Do not tune a large workflow by intuition alone:

```text
representative samples -> pilot -> trace/report plus sacct -> tune -> repeat -> scale
```

Record task evidence on every serious pilot:

```bash
-with-trace trace.tsv \
-with-report report.html \
-with-timeline timeline.html
```

Then compare it with Slurm accounting:

```bash
sacct -S today -u "$USER" \
  --format=JobID,JobName%35,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

Resource requests are reservations. Asking for 32 CPUs or 100 GB when a task
repeatedly uses a fraction of them reduces cluster throughput and can increase
queue time without making the task faster. Use several representative task
instances rather than one anomalous measurement.

## 6. Resource requests

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

## 7. GPU labels

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

## 8. Containers

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

If Apptainer reports missing user-account information, `Operation not
permitted`, or a missing RCC scratch path, treat that as a possible worker or
runtime problem and report the Slurm job ID and node. Do not work around it with
privileged container modes.

## 9. Running nf-core pipelines

The separate bounded nf-core example pins `nf-core/demo` release `1.2.0`, uses
public synthetic test data, caps scheduler concurrency, and supplies teaching
resources through
[`rcc-test.config`](../classes/examples/nf-core/rcc-test.config). Its
[`run-demo.sh`](../classes/examples/nf-core/run-demo.sh) wrapper fails closed
unless `rcc-nextflow`, `apptainer`, and `sbatch` are present.

Copy both files into an approved project directory and run:

```bash
bash run-demo.sh /projects/PROJECT \
  /projects/PROJECT/training/nf-core-demo/run-01
```

The first run may retrieve pipeline source, public test data, and reviewed
container images through the approved proxy path. Do not add tokens or copy
credentials into the project.

For a real pipeline, use an explicit release and its Apptainer profile:

```bash
./run-rcc-nextflow.sh \
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

Start with the pipeline defaults and a small pilot. If one process repeatedly
needs adjustment, override only that process in a small file such as
`resources.config.example`, then add `-c resources.config` to the command. Do
not copy every nf-core resource label into a local `slurm.config` before you
have measured the pipeline.

An exit code `137` or Slurm `OUT_OF_MEMORY` makes memory a reasonable first
hypothesis. If Nextflow instead reports that a process was "terminated by the
external system" without a task exit status, collect Slurm and node evidence
before automatically increasing memory.

## 10. Monitor the run

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

## 11. Diagnose before resuming

A failed task has useful evidence in its work directory:

```text
.command.sh      command Nextflow executed
.command.run     generated task wrapper
.command.out     standard output
.command.err     standard error
.command.log     combined task log where available
.exitcode        task exit status when the wrapper completed normally
```

Common first interpretations are:

| Evidence | First interpretation |
|---|---|
| exit `137`, `OUT_OF_MEMORY` | investigate task memory |
| `TIMEOUT` | task walltime too short |
| `NODE_FAIL` or failed node | cluster/node incident |
| Apptainer says `unknown userid` | worker identity/NSS/SSSD incident |
| missing `/local/...` scratch path | worker/prolog/runtime incident |
| `terminated by the external system` with no task exit code | inspect Slurm and node state first |
| Nextflow session lock error | another controller for this analysis is active |

After correcting the input, configuration, resource request, or software issue:

```bash
./run-rcc-nextflow.sh \
  run PIPELINE [THE SAME OPTIONS] \
  -resume
```

Do not delete the work directory as a first troubleshooting step. Do not start
several copies of the same workflow because one appears slow. Record:

- the Nextflow command and exact pipeline revision;
- the Nextflow run name;
- the timestamped controller log below `logs/`;
- relevant `.command.err` and `.command.log` excerpts;
- Slurm job IDs, states, and nodes;
- the failed task work directory;
- requested and observed resources; and
- whether the process used shared or local scratch.

Never include passwords, tokens, private keys, or patient-identifying data in a
support request.

## 12. Decision checklist

After the service is released and before a large run, confirm:

- one active Nextflow controller is running on an interactive node (`shellhost`)
  inside `tmux`;
- `rcc-nextflow` supplies Slurm and Apptainer policy;
- no copied site-level `slurm.config` overrides RCC infrastructure;
- the project root and `NXF_WORK` are shared and persistent;
- the pipeline is pinned to an exact revision;
- Apptainer images are reviewed or digest-pinned;
- each task has realistic CPU, memory, and time requests;
- scratch is used only where its staging cost is justified;
- high-fan-out uniform processes use arrays where appropriate;
- a small pilot completed and resumed successfully;
- trace/report and Slurm accounting evidence was reviewed; and
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

> One controller on a shellhost or allocation-backed interactive node; Slurm for every compute task;
> shared state for resume; local scratch for measured I/O bottlenecks;
> Apptainer for software. Pilot, measure, tune, then scale.
