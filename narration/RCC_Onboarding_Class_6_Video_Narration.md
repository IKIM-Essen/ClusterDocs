# Class 6: Snakemake on RCC — video narration

## Slide 1: Class 6: Snakemake on RCC

Welcome to Class 6: Snakemake on RCC. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this class, you can: explain what Snakemake controls and what Slurm controls; structure a workflow around inputs, outputs, rules, configuration, and logs; dry-run and inspect a workflow before it submits jobs; use the managed RCC IKIM profile instead of copying scheduler settings; request CPU, memory, time, partitions, GPUs, and local scratch per rule; keep software and data in the correct storage locations; resume safely after correcting a failed rule; and retain enough provenance to reproduce a scientific result.

## Slide 3: Snakemake and Slurm have different jobs

Snakemake builds a directed graph from declared input and output files. It decides which rules need to run and which completed outputs can be reused. Slurm decides where and when each submitted rule job runs and enforces its CPU, memory, time, partition, and GPU allocation. Do not run scientific rule bodies as unmanaged processes on an SSH gateway. Do not add sbatch calls inside a rule: the managed profile is the scheduler boundary.

## Slide 4: Prepare the project layout

Keep durable workflow state in an approved shared project directory: Git should contain workflow logic, configuration templates, environment or container declarations, and documentation. It must not contain credentials, patient identifiers, raw research data, large generated results, workflow caches, or Conda environments.

## Slide 5: Use the managed installation

The managed command is /usr/local/bin/snakemake, normally available as snakemake. Confirm the version for a retained analysis: The control environment belongs to RCC administrators. Analysis tools belong in reviewed per-rule Apptainer images or approved per-rule environments; do not install pipeline packages into the managed Snakemake environment.

## Slide 6: First bounded workflow

Copy the synthetic example from examples/snakemake-rcc into an approved project directory: Replace PROJECT with a project you may use. Inspect Snakefile and config.yaml, then ask Snakemake what it would do without running anything: Render the dependency graph when Graphviz is available: Run the bounded workflow through Slurm: The example creates three tiny synthetic sample files and one summary. It uses one CPU, 256 MiB, five minutes, and cpu_short per rule job. --jobs 4 is a concurrency ceiling, not a request for four CPUs in every job.

## Slide 7: Declare resources per rule

Give each rule realistic resources based on a small measured pilot: threads becomes the rule's usable CPU count. mem_mb is host memory, not GPU VRAM. runtime is minutes. The managed profile translates the supported resource names into Slurm requests; keep cluster-specific defaults in the profile or project configuration rather than scattering raw scheduler flags through every rule.

## Slide 8: Local scratch for I/O-heavy rules

Use node-local storage only inside a Slurm rule job and only for temporary work. The approved pattern stages required inputs to $TMPDIR, computes there, and copies declared outputs back to shared project storage before success. Never place the Snakefile, durable results, logs, or resume-critical state under /local. A rule should use local scratch only when measurement justifies the staging cost—for example repeated random I/O, sorting, assembly, decompression, or many temporary files. Class 14 contains the detailed local-I/O lesson.

## Slide 9: Failures, reruns, and safe recovery

Inspect the failed rule's log and its Slurm accounting record. Correct the input, command, environment, or resource request, then dry-run again: Snakemake reuses outputs whose declared dependencies are still satisfied. Do not delete the whole results tree as a first troubleshooting step, submit several copies of the same workflow, or create an automatic retry storm. Use explicit rerun triggers or --forcerun RULE only after understanding why the existing output must be replaced. Treat protected inputs as read-only.

## Slide 10: Provenance for retained analyses

Retain: the Git commit or archived workflow version; Snakefile, included rule files, and resolved configuration; input inventory and checksums where appropriate; exact container digests or environment lock files; the Snakemake and profile versions; the resolved command and concurrency limit; rule logs, benchmarks, and relevant Slurm job identifiers; and output checksums and the scientific validation record. A technically successful workflow can still use the wrong samples, reference, parameters, or model. Scheduler success is not scientific validation.

## Slide 11: Completion gate

You have completed Class 6 when: the synthetic workflow dry-run lists the expected four rule jobs; the managed IKIM profile completes the bounded run; a second dry-run reports that nothing needs to be done; you can explain the difference between --jobs, threads, mem_mb, and runtime; you can identify which files belong in Git, shared project storage, and node-local scratch; and you can name the provenance required before retaining a scientific result.
