# Class 15: RCC storage architecture

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 5 min video</p>
  <h2>Watch the class first</h2>
  <p>How RCC metadata, object storage, networking, caching, and Slurm placement fit together. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class15.png" src="{{ media_base_url }}/RCC_Onboarding_Class_15_Video_Enhanced.mp4?v=21133685">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Class_15_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

> **Architecture rule:** the user-facing lesson is the storage **contract and I/O
> pattern**, not one permanent product name. RCC may change the S3-compatible
> object backend during an accepted migration without changing how researchers
> should structure their workflows.

This optional class explains the RCC data path:

```text
Compute application
       |
       v
JuiceFS client
   |         |
   |         +---- metadata ----> Redis-compatible metadata service
   |
   +-------------- file data ---> S3-compatible object storage
       |
       +---- memory and node-local cache
```

JuiceFS presents a POSIX filesystem to applications. Metadata is maintained by
the RCC metadata service, while file contents live in an S3-compatible object
layer. A single filesystem operation can therefore generate metadata,
object-storage, network, and cache operations.

RCC has operated MinIO-backed object storage and is migrating/targeting
SeaweedFS-backed S3 for the newer storage plane. **Do not build a scientific
workflow around either product name.** The stable contract is S3/object semantics
plus the JuiceFS POSIX view where provided. The migration does not change the
central performance lesson: access pattern matters more than the backend label.

## Learning objectives

After this class, you should be able to:

- describe the roles of the metadata service, S3-compatible object storage, and
  the JuiceFS client;
- distinguish metadata traffic from file-content traffic;
- explain why small-file workloads differ from large streaming workloads;
- understand the RCC aggregate-backend versus per-client network topology;
- explain client and container caching; and
- choose appropriate I/O patterns for scientific workflows.

## 1. Metadata is a separate workload

The metadata layer stores information such as:

- paths and directory entries;
- ownership and permissions;
- file sizes and timestamps;
- inode-like identifiers;
- object mappings;
- locks and coordination state; and
- filesystem bookkeeping.

Operations such as `stat`, `ls`, `open`, `rename`, `mkdir`, and `unlink` may
transfer almost no file content while still generating metadata requests.

This makes workloads with hundreds of thousands of files fundamentally
different from workloads containing a few large files. Increasing S3 bandwidth
or replacing one object-store implementation with another does not remove a
metadata bottleneck.

## 2. The S3-compatible object layer stores file contents

The object layer is effective for:

- large objects;
- sequential reads and writes;
- durable replicated or erasure-coded storage;
- checksummed content; and
- aggregate access from many clients.

The JuiceFS client translates filesystem reads and writes into object
operations. Large streaming transfers amortize request overhead. Tiny,
scattered reads and writes can generate many requests for relatively little
useful data.

This is why “move the data to Ceph,” “move it to SeaweedFS,” or “use another S3
backend” is not, by itself, a fix for an inefficient workload. The storage
technology changes operational tradeoffs; the application still controls its
access pattern.

## 3. RCC network topology

Storage/backend servers have high aggregate connectivity, while individual
compute clients have smaller per-node links.

```text
compute process
    |
JuiceFS client
    |
per-client link
    |
RCC network
    |
high aggregate backend bandwidth
    |
metadata + S3-compatible object layer
```

High backend bandwidth is **aggregate capacity**. It does not mean every client
receives the full backend rate. Many clients can consume the shared capacity at
once.

Actual useful throughput is lower because of:

- protocol overhead;
- request latency;
- metadata operations;
- contention;
- checksums and encryption;
- filesystem translation; and
- application processing.

Random and small-file workloads often do not fill even a modest client link with
useful data. They spend their time waiting for network round trips and metadata.

## 4. Large files versus many small files

Large compressed FASTQ, BAM, CRAM, archives, image blocks, and model files
generally support efficient streaming and readahead.

Many small files require repeated:

- path lookups;
- permission checks;
- opens and closes;
- metadata updates;
- object requests;
- directory updates; and
- cache bookkeeping.

Twenty gigabytes stored in 500,000 files can therefore perform much worse than
one 20 GB archive.

Conda environments are a common example: startup may require opening thousands
of small files. This is one reason RCC prefers immutable Apptainer images over
large Conda environments stored as production runtimes on shared network
filesystems.

## 5. Streaming and random access

Streaming:

```text
chunk 1 -> chunk 2 -> chunk 3 -> chunk 4
```

Random access:

```text
chunk 70 -> chunk 2 -> chunk 800 -> chunk 71
```

Streaming supports readahead, larger requests, and efficient network transfer.
Random access can repeatedly miss caches, request separate objects, and wait for
metadata and network latency.

Indexed scientific formats are useful. The problem is millions of tiny,
poorly-localized requests against shared storage when the active working set
could be staged locally.

## 6. JuiceFS client caching

The JuiceFS client may cache active data in memory and on node-local disk.

A cache hit avoids another object download:

```text
application -> JuiceFS client -> local cache
```

A cache miss uses the complete path:

```text
application -> JuiceFS client -> network -> S3-compatible object backend -> local cache
```

Caching helps when stable data is reused, for example:

- Apptainer images;
- reference genomes;
- aligner indexes;
- annotation databases;
- model weights; and
- read-only database snapshots.

Cache entries should be identified by immutable version, digest, or checksum.
Mutable names such as `latest.sif` are unsafe cache identities.

## 7. What caching does not solve

Caching does not remove:

- repeated metadata lookups;
- creation and deletion of thousands of temporary files;
- constantly changing writes;
- directory scans;
- cold starts on many different nodes;
- synchronized reads by hundreds of clients;
- data larger than cache capacity; or
- a poor access pattern inside a cached container.

A cached container may start quickly while the application inside it still
performs inefficient random I/O against shared project storage.

## 8. Slurm placement and cache locality

A parent job that stages data or warms a cache on one node should not submit
child jobs that may run elsewhere:

```text
parent on worker A warms cache
child on worker B downloads again
child on worker C downloads again
child on worker D downloads again
```

Nested submission destroys locality and can create repeated:

- S3 downloads;
- metadata traffic;
- client-link use;
- container transfers;
- reference-index transfers; and
- synchronized backend load.

Use job arrays, explicit Slurm dependencies, or Snakemake/Nextflow's reviewed
Slurm integration from an approved controller. Each compute job should receive a
complete unit of work.

## 9. Recommended patterns

Use shared project storage for:

- durable inputs;
- validated final results;
- large sequential transfers;
- shared read-only references; and
- workflow-visible state that genuinely must survive between jobs.

Use node-local storage for:

- temporary files;
- random-I/O working sets;
- per-job databases;
- decompressed intermediates;
- container and reference caches; and
- files that are created and deleted rapidly.

Use project S3/object access when the application genuinely benefits from object
semantics rather than forcing object data through a POSIX view unnecessarily.

## 10. Diagnosing the slow layer

| Symptom | Likely layer |
|---|---|
| `ls`, `stat`, or file creation is slow | metadata path or namespace pressure |
| large sequential reads are slow | object backend, network, contention, or client link |
| first read is slow and second read is fast | cold versus warm client cache |
| many nodes slow simultaneously | shared backend or network contention |
| one node alone is slow | client link, local disk, cache, or mount state |
| container startup repeats downloads | cold or incorrectly keyed image cache |
| temporary-file-heavy tool is slow | metadata load and network round trips |

When reporting a problem, provide the Slurm job ID, node, path, approximate file
count, total size, read/write pattern, and whether local staging changes the
result. Do not include patient identifiers.

## Take-home model

> JuiceFS supplies a POSIX interface where RCC exposes one. The metadata service
> handles namespace operations. The S3-compatible object layer stores file
> contents. The network and caches connect those layers. **Good performance comes
> primarily from good I/O patterns**: stream large data, minimize metadata
> storms, reuse immutable caches, and move temporary/random I/O to node-local
> storage.

The exact object backend can change through an accepted migration. The workflow
rule should not.

## Completion gate

Given one streaming workload and one small-file or random-I/O workload, trace
the likely metadata, object-storage, network, and cache paths. State which data
should remain durable, which work should use job-local scratch, and what you
would measure before changing resources or proposing a different storage
backend.
