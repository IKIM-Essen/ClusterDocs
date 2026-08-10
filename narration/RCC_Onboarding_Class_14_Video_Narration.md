# Class 14: efficient I/O—copy locally, compute locally, return results — video narration

## Slide 1: Class 14: efficient I/O—copy locally, compute locally, return results

Welcome to Class 14: efficient I/O—copy locally, compute locally, return results. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this class, you should be able to: distinguish durable shared storage from temporary node-local scratch; explain streaming, random, small-file, and metadata I/O; recognize when storage rather than CPU or GPU limits a job; write an sbatch job that stages inputs and returns outputs safely; use rsync, checksums, shell traps, and atomic publication; apply the same pattern in Snakemake; and explain how poor I/O structure can turn hours of computation into weeks or months of elapsed time.

## Slide 3: Storage is part of the computation

A job does not merely execute instructions. It repeatedly moves data among: shared project storage; the network; the compute node's page cache; local disk; RAM; and CPU or GPU processes. The slowest required part of that path limits the complete job. Adding CPU cores does not help when those cores spend most of their time waiting for files. Shared storage is designed to make durable data available to many nodes. It is not designed to behave like a private local SSD for every job simultaneously. One badly structured job can also create contention for other researchers.

## Slide 4: Streaming versus random I/O

### Streaming I/O Streaming I/O reads or writes a long sequence of bytes in order: Examples include: reading a compressed FASTQ file once from beginning to end; writing one BAM, CRAM, archive, or report; piping decompressed data directly into the next program; and copying one large file. Streaming works well because storage devices, operating-system readahead, compression libraries, and network protocols can transfer large blocks efficiently. The cost of opening the file is paid once and useful throughput can approach the storage system's bandwidth. ### Random I/O Random I/O repeatedly jumps among unrelated offsets or files: Examples include: repeatedly querying tiny genomic regions across a large.

## Slide 5: Why runtime can grow from hours to months

Suppose one sample requires: 2 seconds of useful CPU work; and 20 seconds waiting for small network-storage operations. For 5,000 samples and 10 workflow stages: That estimate excludes queueing, retries, directory scans, environment startup, and contention caused by parallel jobs. If several rules repeat the same anti-pattern or failures force stages to restart, a workflow expected to finish in hours can remain active for weeks or months. Typical multipliers are: number of samples; files per sample; workflow stages; retries; parallel workers; and repeated decompression or copying. Measure one representative sample before launching thousands.

## Slide 6: The RCC staging pattern

The following job uses the scratch directory supplied by Slurm. The fallback matches the current RCC job-local layout and is used only when SLURM_TMPDIR is not set. Submit it from a login or submission host: The compute must occur inside the Slurm job, not directly on the login or submission host.

## Slide 7: Snakemake integration

The explicit staging pattern is easy to audit: Where available and tested on RCC, Snakemake shadow rules and the tmpdir resource can provide a more declarative implementation. The same invariants remain: active temporary work is local; durable inputs remain unchanged; only required outputs return to shared storage; and failed jobs do not publish apparently complete results.

## Slide 8: Cache containers, indexes, and reusable reference data

Repeatedly transferring or rebuilding the same immutable data wastes both network capacity and wall-clock time. Suitable reusable objects include: Apptainer images; read-only reference genomes; annotation databases; aligner indexes; model weights; software archives; and decompressed copies of compressed references when repeated local access justifies the space. A cache is not a substitute for provenance. Every cached object must be tied to an immutable identity such as: a cryptographic checksum; a container digest; an exact version; a versioned path; or a workflow-managed content hash. ### Node-local cache pattern Use a stable cache directory separate from job-specific scratch: The temporary file plus atomic rename prevents concurrent jobs from.

## Slide 9: Diagnose an I/O-bound job

Start with Slurm accounting: Inside an active allocation, useful tools may include: Interpretation: Use representative pilot data and change one variable at a time.

## Slide 10: Decision checklist

Use local scratch when: the tool creates many temporary files; the tool performs repeated random reads or writes; the input will be reread many times during one job; a temporary database or index is built per job; or local staging measurably reduces elapsed time and shared-storage pressure. Keep direct shared-storage streaming when: the tool performs one sequential pass; input is much larger than local capacity; staging would duplicate most of the job's total I/O; several nodes must concurrently read one durable source; or RCC policy identifies the storage tier as suitable for that pattern.
