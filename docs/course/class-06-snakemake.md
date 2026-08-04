# Class 6: Snakemake on RCC

Snakemake support is **ready now** on RCC. This class turns the workflow ideas
from Class 2 and the Slurm resource model from Class 5 into a complete,
copyable execution pattern.

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 6 min video</p>
  <h2>Watch the class first</h2>
  <p>Managed Snakemake, dependency graphs, the IKIM profile, bounded resources, scratch, recovery, and provenance. Watch the complete lesson, then use the written page below for copyable commands and exercises.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class6.png" src="{{ media_base_url }}/RCC_Onboarding_Class_6_Video_Enhanced.mp4?v=18bfd7e6">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Class_6_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

## Learning objectives

After this class, you can:

- explain what Snakemake controls and what Slurm controls;
- structure a workflow around inputs, outputs, rules, configuration, and logs;
- dry-run and inspect a workflow before it submits jobs;
- use the managed RCC `IKIM` profile instead of copying scheduler settings;
- request CPU, memory, time, partitions, GPUs, and local scratch per rule;
- keep software and data in the correct storage locations;
- resume safely after correcting a failed rule; and
- retain enough provenance to reproduce a scientific result.

## 1. Snakemake and Slurm have different jobs

Snakemake builds a directed graph from declared input and output files. It
decides which rules need to run and which completed outputs can be reused.
Slurm decides where and when each submitted rule job runs and enforces its CPU,
memory, time, partition, and GPU allocation.

```text
Snakefile + configuration + existing files
                  -> Snakemake dependency graph
                       -> managed IKIM profile
                            -> Slurm job per ready rule
                                 -> RCC worker
```

Do not run scientific rule bodies as unmanaged processes on an SSH gateway.
Do not add `sbatch` calls inside a rule: the managed profile is the scheduler
boundary.

## 2. Prepare the project layout

Keep durable workflow state in an approved shared project directory:

```text
/projects/PROJECT/analysis/
├── Snakefile
├── config.yaml
├── workflow/
├── scripts/
├── envs/
├── inputs/       # authoritative or verified inputs; treat as read-only
├── results/      # declared generated outputs
├── logs/
└── benchmarks/
```

Git should contain workflow logic, configuration templates, environment or
container declarations, and documentation. It must not contain credentials,
patient identifiers, raw research data, large generated results, workflow
caches, or Conda environments.

## 3. Use the managed installation

The managed command is `/usr/local/bin/snakemake`, normally available as
`snakemake`. Confirm the version for a retained analysis:

```bash
command -v snakemake
snakemake --version
snakemake --profile IKIM --help >/dev/null
```

The control environment belongs to RCC administrators. Analysis tools belong
in reviewed per-rule Apptainer images or approved per-rule environments; do not
install pipeline packages into the managed Snakemake environment.

## 4. First bounded workflow

Copy the synthetic example from
[`examples/snakemake-rcc`](../classes/examples/snakemake-rcc/README.md) into an
approved project directory:

```bash
mkdir -p /projects/PROJECT/training/snakemake-rcc
cp -R docs/classes/examples/snakemake-rcc/. \
  /projects/PROJECT/training/snakemake-rcc/
cd /projects/PROJECT/training/snakemake-rcc
```

Replace `PROJECT` with a project you may use. Inspect `Snakefile` and
`config.yaml`, then ask Snakemake what it would do without running anything:

```bash
snakemake --dry-run --printshellcmds --reason
```

Render the dependency graph when Graphviz is available:

```bash
snakemake --dag | dot -Tsvg > workflow-dag.svg
```

Run the bounded workflow through Slurm:

```bash
snakemake --profile IKIM --jobs 4 --printshellcmds
```

The example creates three tiny synthetic sample files and one summary. It uses
one CPU, 256 MiB, five minutes, and `cpu_short` per rule job. `--jobs 4` is a
concurrency ceiling, not a request for four CPUs in every job.

## 5. Declare resources per rule

Give each rule realistic resources based on a small measured pilot:

```python
rule align:
    input:
        reads="inputs/{sample}.fastq.gz"
    output:
        "results/{sample}.bam"
    threads: 8
    resources:
        mem_mb=32000,
        runtime=240,
        slurm_partition="cpu_nodes"
    log:
        "logs/align/{sample}.log"
    benchmark:
        "benchmarks/align/{sample}.tsv"
    shell:
        "aligner --threads {threads} {input.reads} > {output} 2> {log}"
```

`threads` becomes the rule's usable CPU count. `mem_mb` is host memory, not
GPU VRAM. `runtime` is minutes. The managed profile translates the supported
resource names into Slurm requests; keep cluster-specific defaults in the
profile or project configuration rather than scattering raw scheduler flags
through every rule.

## 6. Short jobs, regular jobs, and GPUs

Use `cpu_short` only when every rule instance is guaranteed to finish within
two hours. Use `cpu_nodes` for longer bounded CPU jobs. For a standard GPU:

```python
resources:
    slurm_partition="gpu_nodes",
    gpu=1,
    mem_mb=16000,
    runtime=30
```

Only add an exact GPU model or architecture when the measured workload or
validated software requires it. Class 5 contains the full GPU decision guide.

## 7. Local scratch for I/O-heavy rules

Use node-local storage only inside a Slurm rule job and only for temporary work.
The approved pattern stages required inputs to `$TMPDIR`, computes there, and
copies declared outputs back to shared project storage before success. Never
place the Snakefile, durable results, logs, or resume-critical state under
`/local`.

A rule should use local scratch only when measurement justifies the staging
cost—for example repeated random I/O, sorting, assembly, decompression, or many
temporary files. Class 14 contains the detailed local-I/O lesson.

## 8. Software environments and containers

Prefer a digest-pinned Apptainer image for stable production rules:

```python
rule tool:
    input:
        "inputs/data.tsv"
    output:
        "results/data.tsv"
    container:
        "docker://REGISTRY/PROJECT/IMAGE@sha256:DIGEST"
    threads: 4
    resources:
        mem_mb=8000,
        runtime=60,
        slurm_partition="cpu_nodes"
    shell:
        "tool --threads {threads} {input} > {output}"
```

Use reviewed immutable SIF files or digest-pinned OCI references. Avoid mutable
`latest` tags. Large Conda environments with thousands of small files do not
belong on metadata-sensitive shared storage; follow the RCC node-local or
packed-environment guidance when a container is not suitable.

## 9. Failures, reruns, and safe recovery

Inspect the failed rule's log and its Slurm accounting record. Correct the
input, command, environment, or resource request, then dry-run again:

```bash
snakemake --dry-run --printshellcmds --reason
snakemake --profile IKIM --jobs 4 --rerun-incomplete
```

Snakemake reuses outputs whose declared dependencies are still satisfied. Do
not delete the whole results tree as a first troubleshooting step, submit
several copies of the same workflow, or create an automatic retry storm.

Use explicit rerun triggers or `--forcerun RULE` only after understanding why
the existing output must be replaced. Treat protected inputs as read-only.

## 10. Provenance for retained analyses

Retain:

- the Git commit or archived workflow version;
- `Snakefile`, included rule files, and resolved configuration;
- input inventory and checksums where appropriate;
- exact container digests or environment lock files;
- the Snakemake and profile versions;
- the resolved command and concurrency limit;
- rule logs, benchmarks, and relevant Slurm job identifiers; and
- output checksums and the scientific validation record.

A technically successful workflow can still use the wrong samples, reference,
parameters, or model. Scheduler success is not scientific validation.

## Completion gate

You have completed Class 6 when:

1. the synthetic workflow dry-run lists the expected four rule jobs;
2. the managed `IKIM` profile completes the bounded run;
3. a second dry-run reports that nothing needs to be done;
4. you can explain the difference between `--jobs`, `threads`, `mem_mb`, and
   `runtime`;
5. you can identify which files belong in Git, shared project storage, and
   node-local scratch; and
6. you can name the provenance required before retaining a scientific result.
