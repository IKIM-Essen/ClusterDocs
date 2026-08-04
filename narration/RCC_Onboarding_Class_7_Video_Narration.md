# Class 7: Nextflow on RCC — video narration

## Slide 1: Class 7: Nextflow on RCC

Welcome to Class 7: Nextflow on RCC. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this class, you can: explain what will run on shellhost and what runs on compute nodes; start a persistent Nextflow controller in tmux after release; use the RCC launcher and a shared project root; request CPU, memory, time, short-queue, scratch, array, and GPU resources; use Apptainer without placing Conda environments on shared storage; resume an interrupted pipeline safely; and inspect Slurm and Nextflow evidence when something fails.

## Slide 3: How the pieces fit together

The Nextflow program remains on shellhost. It reads the pipeline graph, decides which tasks are ready, and submits them to Slurm. Slurm allocates CPUs, memory, time, partitions, and GPUs. Scientific computation occurs only in Slurm jobs. Compute workers execute generated task wrappers and do not need their own Java or Nextflow installation.

## Slide 4: Prepare a shared project root

After the service is released, choose the project directory that owns the workflow and results: Replace MY_PROJECT with a directory you are authorized to use. The launcher creates these private per-user directories: The work directory is part of Nextflow's cache and resume mechanism. Never set it below /local. Local scratch is disposable and belongs to one compute job; a later task may run on another node.

## Slide 5: Start the controller in tmux

After release, connect to the approved submission host and create a persistent terminal session: Inside the tmux session: Detach without stopping Nextflow: Return later: A dropped laptop or jump-host connection then does not terminate the workflow controller.

## Slide 6: First bounded RCC workflow

The copyable example is in examples/nextflow-rcc. After release, copy that directory into your project, enter it, and run: The example submits two small cpu_short jobs. One uses the shared task work directory; one uses node-local scratch and returns only its declared output. Every example has strict CPU, memory, and time limits. Run it again with: The second run should reuse completed task results. Keep the same project root, pipeline revision, inputs, and work directory for resume to succeed.

## Slide 7: Resource requests

Nextflow process directives map to Slurm requests: Request what the program can actually use. More CPUs or memory can increase queue time without reducing runtime. ### Short jobs Apply the RCC label only when every task instance is guaranteed to finish within two hours: This selects cpu_short and a maximum task time of two hours. ### Local scratch Use local scratch for repeated random I/O, temporary databases, sorting, assembly, decompressed intermediates, or very large numbers of temporary files: Nextflow creates a unique task directory below the Slurm job's $TMPDIR, stages inputs, executes locally, copies declared outputs back with rsync, and removes the task scratch directory.

## Slide 8: GPU labels

Request any standard GPU: Request the current exact RTX A6000 type: Request an architecture family: Request the special ARM64/GB10 platform only when the workflow supports that architecture and platform policy: RCC adds Apptainer --nv for these labels. GPU VRAM is not the same resource as host memory requested with memory.

## Slide 9: Containers

RCC uses Apptainer for Nextflow tasks. A process can declare an immutable image: Prefer a reviewed SIF file or a digest-pinned OCI reference. Do not use mutable latest tags. The per-user Apptainer cache is on shared project storage so a job scheduled on another node can reuse the image. Avoid Nextflow-managed Conda as the default RCC profile. Conda environments contain many small files and create poor metadata-I/O patterns on shared storage. Use Apptainer unless a reviewed pipeline has a specific exception.

## Slide 10: Running nf-core pipelines

The separate bounded nf-core example pins nf-core/demo release 1.2.0, uses public synthetic test data, caps scheduler concurrency, and supplies teaching resources through rcc-test.config. Its run-demo.sh wrapper fails closed unless rcc-nextflow, apptainer, and sbatch are present. After release, copy both files into an approved project directory and run: The first run may retrieve pipeline source, public test data, and reviewed container images through the approved proxy path. Do not add tokens or copy credentials into the project. For a real pipeline, use an explicit release and its Apptainer profile: Replace RELEASE_TAG with a reviewed release. Do not implicitly follow a pipeline's changing default branch. Pilot a.

## Slide 11: Failures and resume

After correcting the input, configuration, resource request, or software issue: Do not delete the work directory as a first troubleshooting step. Do not start several copies of the same workflow because one appears slow. Record: the Nextflow command and exact pipeline revision; the Nextflow run name; relevant .nextflow.log lines; Slurm job IDs and states; the failed task work directory; requested and observed resources; and whether the process used shared or local scratch. Never include passwords, tokens, private keys, or patient-identifying data in a support request.

## Slide 12: Completion gate

Before release, you have completed the preparation gate when you can explain: why the controller belongs on shellhost rather than an SSH gateway or ordinary worker allocation; why every scientific task must pass through Slurm; why NXF_WORK must remain on persistent shared project storage; when explicit /local task scratch helps and how declared outputs return; why workers use Apptainer but do not require Java or Nextflow; and which pipeline revision, parameters, trace, report, image digests, checksums, and Slurm identifiers belong in retained provenance. After RCC releases rcc-nextflow, complete the live gate with the bounded synthetic example and confirm that its second run reuses completed work.
