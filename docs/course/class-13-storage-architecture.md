# Class 13: RCC storage architecture

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 6 min video</p>
  <h2>Watch the class first</h2>
  <p>How RCC metadata, object storage, networking, caching, and Slurm placement fit together. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class13.png" src="{{ media_base_url }}/RCC_Onboarding_Class_13_Video_Enhanced.mp4?v=f963ffcd">
    <track kind="captions" srclang="en" label="English captions" src="../../downloads/captions/RCC_Onboarding_Class_13_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
  <div class="course-video-links" aria-label="Video alternatives and downloads">
    <a href="../../downloads/captions/RCC_Onboarding_Class_13_Captions.srt">Captions</a>
    <a href="../../downloads/narration/RCC_Onboarding_Class_13_Video_Narration.md">Read transcript</a>
  </div>
</section>

This optional class explains the RCC data path:

```text
Compute application
       |
       v
JuiceFS client
   |         |
   |         +---- metadata ----> Redis
   |
   +-------------- file data ---> S3 / MinIO
       |
       +---- memory and node-local cache
```

JuiceFS presents a POSIX filesystem to applications. Redis stores filesystem
metadata, while MinIO stores file contents through an S3-compatible object
interface. A single filesystem operation can therefore generate metadata,
object-storage, network, and cache operations.

## Learning objectives

After this class, you should be able to:

- describe the roles of Redis, MinIO, and the JuiceFS client;
- distinguish metadata traffic from file-content traffic;
- explain why small-file workloads differ from large streaming workloads;
- understand the RCC 100 Gb/s server and 10 Gb/s client topology;
- explain client and container caching; and
- choose appropriate I/O patterns for scientific workflows.

## 1. Redis handles metadata

Redis stores information such as:

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
does not remove a metadata bottleneck.

## 2. MinIO stores file contents

MinIO provides the S3-compatible object-storage layer used for durable file
contents. Object storage is effective for:

- large objects;
- sequential reads and writes;
- durable replicated or erasure-coded storage;
- checksummed content; and
- aggregate access from many clients.

The JuiceFS client translates filesystem reads and writes into object
operations. Large streaming transfers amortize request overhead. Tiny,
scattered reads and writes can generate many requests for relatively little
useful data.

## 3. RCC network topology

Storage and backend servers have connectivity of up to **100 Gb/s**. Typical
compute clients have **10 Gb/s** links.

```text
compute process
    |
JuiceFS client
    |
10 Gb/s client link
    |
RCC network
    |
100 Gb/s aggregate backend
    |
Redis and MinIO
```

The 100 Gb/s server side is aggregate capacity. It does not provide 100 Gb/s to
one compute node. Ten clients each attempting to sustain 10 Gb/s can already
approach the nominal capacity of one 100 Gb/s backend link.

Actual useful throughput is lower because of:

- protocol overhead;
- request latency;
- metadata operations;
- contention;
- checksums and encryption;
- filesystem translation; and
- application processing.

Random and small-file workloads often do not fill a 10 Gb/s link with useful
data. They spend their time waiting for network round trips and metadata.

## 4. Large files versus many small files

Large compressed FASTQ, BAM, CRAM, archives, and model files generally support
efficient streaming and readahead.

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
of small files. This is one reason RCC prefers Apptainer images over Conda
environments stored on shared network filesystems.

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
application -> JuiceFS client -> network -> MinIO -> local cache
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
performs inefficient random I/O against JuiceFS.

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
- Redis metadata traffic;
- 10 Gb/s client-link use;
- container transfers;
- reference-index transfers; and
- synchronized backend load.

Use job arrays, explicit Slurm dependencies, or Snakemake's Slurm executor from
an approved submission host. Each compute job should receive a complete unit of
work.

## 9. Recommended patterns

Use shared JuiceFS storage for:

- durable inputs;
- validated final results;
- large sequential transfers;
- shared read-only references; and
- workflow-visible state.

Use node-local storage for:

- temporary files;
- random-I/O working sets;
- per-job databases;
- decompressed intermediates;
- container and reference caches; and
- files that are created and deleted rapidly.

Do not place primary identifying patient data on RCC.

## 10. Diagnosing the slow layer

| Symptom | Likely layer |
|---|---|
| `ls`, `stat`, or file creation is slow | Redis metadata path or namespace pressure |
| large sequential reads are slow | MinIO, network, contention, or client link |
| first read is slow and second read is fast | cold versus warm client cache |
| many nodes slow simultaneously | shared backend or network contention |
| one node alone is slow | client link, local disk, cache, or mount state |
| container startup repeats downloads | cold or incorrectly keyed image cache |
| temporary-file-heavy tool is slow | metadata load and network round trips |

When reporting a problem, provide the Slurm job ID, node, path, approximate file
count, total size, read/write pattern, and whether local staging changes the
result. Do not include patient identifiers.

## Take-home model

> JuiceFS supplies the POSIX interface. Redis handles metadata. MinIO stores file
> contents as S3 objects. The network connects the layers. Good performance
> comes from streaming large data, minimizing metadata storms, reusing immutable
> caches, and moving temporary random I/O to node-local storage.

## Completion gate

Given one streaming workload and one small-file or random-I/O workload, trace
the likely metadata, object-storage, network, and cache paths. State which data
should remain durable, which work should use job-local scratch, and what you
would measure before changing resources.
