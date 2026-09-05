# What changed from the old cluster? — short video narration

**Target length:** 3–4 minutes  
**Audience:** returning RCC/IKIM cluster users  
**Release:** Stage 2 media; the written page is authoritative for Stage 1

## 1. The old mental model

If you used the old cluster, you probably remember the basic pattern: connect by SSH, open a shared filesystem, prepare commands on a login or submission host, and send larger work to compute nodes. Those concepts still exist, but they are no longer the front door to RCC.

The new RCC is organized around a research project. The same project connects people, data, storage, compute, workflows, services, results, and lifecycle. Many researchers can now start in the browser with Files and, when released, RCC Analysis, without first learning SSH or Slurm.

## 2. The most important technical lesson: I/O patterns

The largest architectural lesson from operating the old environment was not simply that we needed more CPU or more storage bandwidth. It was that **I/O pattern dominates many real workloads**.

A few large sequential files are usually efficient. Hundreds of thousands of tiny files, repeated directory scans, package environments, workflow work directories, editor indexing, and random temporary writes can spend far more time on metadata and network latency than on useful computation.

That is why RCC now teaches a simple pattern: durable inputs and results stay with the project; a Slurm job stages the active working set to node-local scratch when useful; temporary and random I/O happens locally; validated outputs return to project storage.

Changing the backend to another popular filesystem or putting everything on Kubernetes would not make millions of tiny operations free. We therefore design the workflow around the I/O pattern first.

## 3. Compute and services are deliberately separated

Scientific computation is still governed by Slurm. CPU, memory, GPU, accounting, cancellation, and fair scheduling have one authority.

Long-lived web applications, databases, brokers, and control services have a different lifecycle and belong to the RCC service plane. The user may see one web interface, but a button does not create a second scientific scheduler.

## 4. VS Code is still useful—but keep its I/O footprint small

Advanced users can keep using VS Code Remote SSH. The important change is to treat the editor as an active filesystem client.

Open the smallest useful source directory. Disable following symlinks for search, respect ignore files, and exclude data, results, environments, package trees, Snakemake and Nextflow work directories from file watching and full-text search. ClusterDocs provides a copyable RCC-safe settings block.

Do not open an entire project or shared storage root simply because VS Code can display it.

## 5. More of the research lifecycle is now connected

RCC can connect instrument ingestion, project POSIX or S3 storage, DataLad where appropriate, notebooks, governed workflows, GPUs, delegated project governance, AI assistance that is data-blind by default, and eventually preservation through Coscine. Domain applications such as SeqLab can build on the same platform and support downstream archive submission under their own governance.

So the biggest change is not a new login command. It is that researchers should need to understand less infrastructure to begin, while advanced users get a more coherent platform underneath.

For the details, open **What changed from the old cluster?**, **Efficient I/O**, and the **RCC-safe VS Code defaults** in ClusterDocs.