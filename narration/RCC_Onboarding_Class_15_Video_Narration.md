# Class 15: RCC storage architecture — video narration

## Slide 1: Class 15: RCC storage architecture

Welcome to Class 15: RCC storage architecture. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this class, you should be able to: describe the roles of Redis, MinIO, and the JuiceFS client; distinguish metadata traffic from file-content traffic; explain why small-file workloads differ from large streaming workloads; understand the RCC 100 Gb/s server and 10 Gb/s client topology; explain client and container caching; and choose appropriate I/O patterns for scientific workflows.

## Slide 3: Redis handles metadata

Redis stores information such as: paths and directory entries; ownership and permissions; file sizes and timestamps; inode-like identifiers; object mappings; locks and coordination state; and filesystem bookkeeping. Operations such as stat, ls, open, rename, mkdir, and unlink may transfer almost no file content while still generating metadata requests. This makes workloads with hundreds of thousands of files fundamentally different from workloads containing a few large files. Increasing S3 bandwidth does not remove a metadata bottleneck.

## Slide 4: MinIO stores file contents

MinIO provides the S3-compatible object-storage layer used for durable file contents. Object storage is effective for: large objects; sequential reads and writes; durable replicated or erasure-coded storage; checksummed content; and aggregate access from many clients. The JuiceFS client translates filesystem reads and writes into object operations. Large streaming transfers amortize request overhead. Tiny, scattered reads and writes can generate many requests for relatively little useful data.

## Slide 5: RCC network topology

Storage and backend servers have connectivity of up to 100 Gb/s. Typical compute clients have 10 Gb/s links. The 100 Gb/s server side is aggregate capacity. It does not provide 100 Gb/s to one compute node. Ten clients each attempting to sustain 10 Gb/s can already approach the nominal capacity of one 100 Gb/s backend link. Actual useful throughput is lower because of: protocol overhead; request latency; metadata operations; contention; checksums and encryption; filesystem translation; and application processing. Random and small-file workloads often do not fill a 10 Gb/s link with useful data. They spend their time waiting for network round trips and metadata.

## Slide 6: Large files versus many small files

Large compressed FASTQ, BAM, CRAM, archives, and model files generally support efficient streaming and readahead. Many small files require repeated: path lookups; permission checks; opens and closes; metadata updates; object requests; directory updates; and cache bookkeeping. Twenty gigabytes stored in 500,000 files can therefore perform much worse than one 20 GB archive. Conda environments are a common example: startup may require opening thousands of small files. This is one reason RCC prefers Apptainer images over Conda environments stored on shared network filesystems.

## Slide 7: JuiceFS client caching

The JuiceFS client may cache active data in memory and on node-local disk. A cache hit avoids another object download: A cache miss uses the complete path: Caching helps when stable data is reused, for example: Apptainer images; reference genomes; aligner indexes; annotation databases; model weights; and read-only database snapshots. Cache entries should be identified by immutable version, digest, or checksum. Mutable names such as latest.sif are unsafe cache identities.

## Slide 8: Slurm placement and cache locality

A parent job that stages data or warms a cache on one node should not submit child jobs that may run elsewhere: Nested submission destroys locality and can create repeated: S3 downloads; Redis metadata traffic; 10 Gb/s client-link use; container transfers; reference-index transfers; and synchronized backend load. Use job arrays, explicit Slurm dependencies, or Snakemake's Slurm executor from an approved submission host. Each compute job should receive a complete unit of work.

## Slide 9: Diagnosing the slow layer

When reporting a problem, provide the Slurm job ID, node, path, approximate file count, total size, read/write pattern, and whether local staging changes the result. Do not include patient identifiers.

## Slide 10: Completion gate

Given one streaming workload and one small-file or random-I/O workload, trace the likely metadata, object-storage, network, and cache paths. State which data should remain durable, which work should use job-local scratch, and what you would measure before changing resources.
