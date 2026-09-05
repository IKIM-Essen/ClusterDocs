# Class 15: RCC storage architecture — video narration

## Slide 1: Class 15: RCC storage architecture

Welcome to Class 15: RCC storage architecture. This lesson explains the storage contract and the I/O patterns that matter to scientific workflows. RCC may change individual storage products during reviewed migrations, so the important lesson is how metadata, object storage, networking, caching, local scratch, and Slurm placement fit together.

## Slide 2: Learning objectives

After this class, you should be able to describe the roles of the metadata service, the S3-compatible object layer, and the JuiceFS client; distinguish metadata traffic from file-content traffic; explain why small-file workloads differ from large streaming workloads; understand aggregate backend bandwidth versus per-client bandwidth; explain client and container caching; and choose appropriate I/O patterns for scientific workflows.

## Slide 3: Metadata is a separate workload

The metadata service stores information such as paths, directory entries, ownership, permissions, sizes, timestamps, object mappings, locks, and filesystem bookkeeping. Operations such as stat, ls, open, rename, mkdir, and unlink may transfer almost no file content while still generating metadata requests. This makes workloads with hundreds of thousands of files fundamentally different from workloads containing a few large files. Increasing S3 bandwidth or replacing one object backend with another does not remove a metadata bottleneck.

## Slide 4: The S3-compatible object layer stores file contents

RCC uses an S3-compatible object layer for durable file content. RCC has operated MinIO-backed storage and is moving toward SeaweedFS-backed S3 in the newer storage plane, but scientific workflows should not depend on either product name. Object storage is effective for large objects, sequential reads and writes, checksummed durable content, and aggregate access from many clients. Large streaming transfers amortize request overhead. Tiny scattered operations can generate many requests for little useful data.

## Slide 5: I/O pattern matters more than headline bandwidth

A high-bandwidth backend is aggregate capacity. It does not mean every compute node receives the full backend rate. More importantly, many small-file and random-access workloads never come close to filling the link with useful data. They wait for metadata lookups, permission checks, file opens and closes, request latency, cache misses, and contention. This is the central RCC storage lesson: changing to Ceph, SeaweedFS, MinIO, or another backend cannot make an inefficient access pattern free.

## Slide 6: Large files versus many small files

Large compressed FASTQ, BAM, CRAM, archives, image blocks, and model files generally support efficient streaming and readahead. Many small files require repeated path lookups, permission checks, opens and closes, metadata updates, object requests, directory updates, and cache bookkeeping. Twenty gigabytes stored in five hundred thousand files can therefore perform much worse than one twenty-gigabyte archive. Conda environments are a common example, which is one reason RCC prefers reusable Apptainer images for repeated production execution.

## Slide 7: Local scratch and caching

The JuiceFS client can cache active data in memory and on node-local disk. Stable reference data, container images, indexes, databases, and model weights can benefit from immutable cache identities. Temporary and random I/O often benefits even more from explicit node-local scratch. Keep durable inputs and final outputs with the project, but move the active working set close to the process when the workload would otherwise generate large amounts of random or temporary shared-storage traffic.

## Slide 8: Slurm placement and locality

A job that warms a cache or stages data on one worker should not blindly launch child work onto unrelated workers and download everything again. Repeated placement changes can cause duplicate S3 downloads, metadata traffic, client-link use, container transfers, and synchronized backend load. Use reviewed workflow-to-Slurm patterns so each task receives a complete unit of work and its locality assumptions are explicit.

## Slide 9: Diagnosing the slow layer

When reporting a storage-performance problem, provide the Slurm job ID, node, path, approximate file count, total size, read/write pattern, and whether local staging changes the result. Those facts are usually more useful than saying only that the filesystem is slow. Do not include patient identifiers.

## Slide 10: Completion gate

Given one streaming workload and one small-file or random-I/O workload, trace the likely metadata, object-storage, network, cache, and local-scratch paths. State which data should remain durable, which work should use job-local scratch, and what you would measure before changing resources or proposing a different storage backend.
