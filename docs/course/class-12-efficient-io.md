# Class 12: efficient I/O—copy locally, compute locally, return results

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 6 min video</p>
  <h2>Watch the class first</h2>
  <p>Why local scratch matters, safe staging, workflow integration, caching, diagnosis, and storage decisions. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/class12.png" src="{{ media_base_url }}/RCC_Onboarding_Class_12_Video_Enhanced.mp4?v=0ea17760">
    <track kind="captions" srclang="en" label="English captions" src="../../assets/captions/RCC_Onboarding_Class_12_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
</section>

> **The pattern:** Keep durable inputs and final results on approved shared
> storage. For I/O-intensive computation, copy only the required inputs to the
> compute node's local scratch space, run the computation there, validate the
> output, and copy the final result back.

This class teaches a practical RCC workflow pattern:

1. submit the work through Slurm;
2. create a job-specific directory on node-local storage;
3. stage the required input files into that directory;
4. perform temporary and random I/O locally;
5. validate the result;
6. copy only durable outputs back to shared storage; and
7. remove the temporary directory automatically.

The class is intended for biomedical researchers. The exercises use synthetic
data and must not be replaced with data containing patient names or other
primary identifying fields.

Companion material:

- [create a synthetic FASTQ file](../classes/examples/make-synthetic-fastq.sh);
- [run the direct shared-storage comparison](../classes/examples/direct-io-demo.sh);
- [run the local-staging job](../classes/examples/local-io-demo.sh); and
- continue with [Class 13: RCC storage architecture](class-13-storage-architecture.md).

## Learning objectives

After this class, you should be able to:

- distinguish durable shared storage from temporary node-local scratch;
- explain streaming, random, small-file, and metadata I/O;
- recognize when storage rather than CPU or GPU limits a job;
- write an `sbatch` job that stages inputs and returns outputs safely;
- use `rsync`, checksums, shell traps, and atomic publication;
- apply the same pattern in Snakemake; and
- explain how poor I/O structure can turn hours of computation into weeks or
  months of elapsed time.

## 1. Storage is part of the computation

A job does not merely execute instructions. It repeatedly moves data among:

- shared project storage;
- the network;
- the compute node's page cache;
- local disk;
- RAM; and
- CPU or GPU processes.

The slowest required part of that path limits the complete job. Adding CPU cores
does not help when those cores spend most of their time waiting for files.

Shared storage is designed to make durable data available to many nodes. It is
not designed to behave like a private local SSD for every job simultaneously.
One badly structured job can also create contention for other researchers.

## 2. Streaming versus random I/O

### Streaming I/O

Streaming I/O reads or writes a long sequence of bytes in order:

```text
start ------------------------------------------------------------> end
```

Examples include:

- reading a compressed FASTQ file once from beginning to end;
- writing one BAM, CRAM, archive, or report;
- piping decompressed data directly into the next program; and
- copying one large file.

Streaming works well because storage devices, operating-system readahead,
compression libraries, and network protocols can transfer large blocks
efficiently. The cost of opening the file is paid once and useful throughput can
approach the storage system's bandwidth.

### Random I/O

Random I/O repeatedly jumps among unrelated offsets or files:

```text
read here -> jump -> read there -> open another file -> seek -> close
```

Examples include:

- repeatedly querying tiny genomic regions across a large alignment;
- a temporary database that performs many small updates;
- opening thousands of small files during every workflow step;
- repeatedly scanning a directory to discover whether outputs exist; and
- software environments containing tens of thousands of small files.

Each operation may wait for network latency, metadata lookup, permission checks,
file opening, seeking, and closing. A single operation may appear cheap, but
millions of operations make latency dominate elapsed time.

> **Random access is not always wrong:** Indexed BAM, CRAM, VCF, database, and
> image formats legitimately support random access. The problem is placing a
> large, repeated random-I/O workload on shared network storage when the active
> working set could be staged to node-local storage.

## 3. RCC network topology and what it means for I/O

RCC storage and service servers are connected to the backend at up to
**100 Gb/s**, while typical compute clients are connected at **10 Gb/s**.

That topology is intentionally asymmetric:

- storage servers aggregate traffic from many clients;
- each compute node has a much smaller individual uplink;
- many nodes may read from or write to the same backend simultaneously; and
- the effective throughput of one job is limited by its own 10 Gb/s client link,
  protocol overhead, filesystem behavior, and contention.

A 100 Gb/s storage server does **not** mean that every client receives 100 Gb/s.
Ten clients each attempting to sustain 10 Gb/s can already consume the nominal
server-side link. In practice, metadata traffic, TCP overhead, other users,
multiple storage targets, and non-sequential access reduce useful throughput.

The distinction is especially important for random and small-file I/O. A job
that opens thousands of files or performs millions of small reads rarely comes
close to saturating a 10 Gb/s link with useful data. It instead spends time on:

- network round trips;
- metadata lookup;
- permission checks;
- file open and close operations;
- filesystem locking; and
- queueing behind other clients.

The correct conclusion is therefore not “the network is fast enough.” The
correct conclusion is:

> The backend has high aggregate bandwidth, but each client has limited bandwidth
> and shared latency. Use the network for durable transfer and streaming; use
> node-local storage for active random and temporary I/O.

## 4. Why runtime can grow from hours to months

Suppose one sample requires:

- 2 seconds of useful CPU work; and
- 20 seconds waiting for small network-storage operations.

For 5,000 samples and 10 workflow stages:

```text
22 seconds × 5,000 × 10 = 1,100,000 seconds ≈ 12.7 days
```

That estimate excludes queueing, retries, directory scans, environment startup,
and contention caused by parallel jobs. If several rules repeat the same
anti-pattern or failures force stages to restart, a workflow expected to finish
in hours can remain active for weeks or months.

Typical multipliers are:

- number of samples;
- files per sample;
- workflow stages;
- retries;
- parallel workers; and
- repeated decompression or copying.

Measure one representative sample before launching thousands.

## 5. The RCC staging pattern

The following job uses the scratch directory supplied by Slurm. The fallback
matches the current RCC job-local layout and is used only when `SLURM_TMPDIR` is
not set.

```bash
#!/usr/bin/env bash
#SBATCH --job-name=local-io-demo
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x-%j.out

set -Eeuo pipefail
umask 007

readonly INPUT="/projects/example/input/sample.fastq.gz"
readonly OUTPUT_DIR="/projects/example/results"
readonly WORKDIR="${SLURM_TMPDIR:-/local/work/${USER}/slurm-job-${SLURM_JOB_ID}}"

cleanup() {
    local status=$?
    rm -rf -- "${WORKDIR}"
    exit "${status}"
}
trap cleanup EXIT INT TERM

mkdir -p -- "${WORKDIR}" "${OUTPUT_DIR}"

# Stage only the files needed by this job.
rsync -a --checksum -- "${INPUT}" "${WORKDIR}/sample.fastq.gz"

# Compute locally. Temporary files and random I/O stay on the node.
gzip -cd -- "${WORKDIR}/sample.fastq.gz" \
    | awk 'NR % 4 == 2 { bases += length($0); reads += 1 }
           END { print "reads\t" reads; print "bases\t" bases }' \
    > "${WORKDIR}/summary.tsv"

# Validate before publishing.
test -s "${WORKDIR}/summary.tsv"
grep -q $'^reads\t' "${WORKDIR}/summary.tsv"
grep -q $'^bases\t' "${WORKDIR}/summary.tsv"

# Publish atomically: copy to a temporary name, then rename.
tmp_output="${OUTPUT_DIR}/.summary.${SLURM_JOB_ID}.tmp"
final_output="${OUTPUT_DIR}/summary.tsv"
rsync -a -- "${WORKDIR}/summary.tsv" "${tmp_output}"
mv -f -- "${tmp_output}" "${final_output}"

sha256sum -- "${final_output}"
```

Submit it from a login or submission host:

```bash
mkdir -p logs
sbatch local-io-demo.sh
```

The compute must occur inside the Slurm job, not directly on the login or
submission host.

## 6. Why each safety step matters

| Step | Purpose |
|---|---|
| `set -Eeuo pipefail` | Stops on failed commands, unset variables, and failed pipeline stages. |
| job-specific work directory | Prevents jobs from overwriting one another. |
| `trap cleanup EXIT` | Removes scratch on success, failure, cancellation, or interruption. |
| stage only required inputs | Avoids copying entire projects for every job. |
| validate output locally | Prevents incomplete results from being published. |
| temporary destination plus `mv` | Makes publication atomic on the destination filesystem. |
| checksum | Provides evidence that the final file is readable and stable. |

Do not copy a whole multi-terabyte project tree to every node. Staging is useful
only when the copied working set is smaller than the repeated network I/O it
replaces.

## 7. Compare the patterns

### Poor pattern

```bash
my_tool \
  --input /projects/study/all_samples \
  --tmp-dir /projects/study/tmp/job-${SLURM_JOB_ID} \
  --output /projects/study/results/sample-01
```

This may direct temporary shards, database updates, logs, and random reads to
shared storage throughout the computation.

### Better pattern

```bash
work="${SLURM_TMPDIR:-/local/work/${USER}/slurm-job-${SLURM_JOB_ID}}"
mkdir -p "${work}"
rsync -a /projects/study/input/sample-01/ "${work}/input/"

my_tool \
  --input "${work}/input" \
  --tmp-dir "${work}/tmp" \
  --output "${work}/output"

test -s "${work}/output/result.tsv"
rsync -a "${work}/output/result.tsv" /projects/study/results/sample-01/
```

## 8. Snakemake integration

The explicit staging pattern is easy to audit:

```python
rule analyse_sample:
    input:
        reads="/projects/study/reads/{sample}.fastq.gz"
    output:
        report="/projects/study/results/{sample}.tsv"
    threads: 4
    resources:
        mem_mb=8000,
        runtime=30
    shell:
        r"""
        set -Eeuo pipefail

        scratch_root="${{SLURM_TMPDIR:-/local/work/$USER/slurm-job-${{SLURM_JOB_ID}}}}"
        work="$scratch_root/{wildcards.sample}"
        trap 'rm -rf -- "$work"' EXIT INT TERM
        mkdir -p -- "$work"

        rsync -a --checksum -- "{input.reads}" "$work/reads.fastq.gz"

        gzip -cd -- "$work/reads.fastq.gz" \
          | awk 'NR % 4 == 2 {{ bases += length($0); reads += 1 }}
                 END {{ print "reads\t" reads; print "bases\t" bases }}' \
          > "$work/report.tsv"

        test -s "$work/report.tsv"
        install -D -m 0660 "$work/report.tsv" "{output.report}.tmp"
        mv -f -- "{output.report}.tmp" "{output.report}"
        """
```

Where available and tested on RCC, Snakemake `shadow` rules and the `tmpdir`
resource can provide a more declarative implementation. The same invariants
remain:

- active temporary work is local;
- durable inputs remain unchanged;
- only required outputs return to shared storage; and
- failed jobs do not publish apparently complete results.

## 9. Streaming and compression

Leave files compressed when downstream tools support compressed input:

```bash
gzip -cd reads.fastq.gz | consumer --stdin
```

This avoids writing a large uncompressed intermediate. Streaming through a pipe
can reduce both storage consumption and I/O, but it also couples the processes:
if the consumer fails, `pipefail` must make the complete command fail.

Do not repeatedly decompress the same large source into shared storage. Either:

- let the tool read the compressed format;
- stream decompression into the consumer; or
- decompress once into local scratch when repeated local access justifies it.


## 10. Cache containers, indexes, and reusable reference data

Repeatedly transferring or rebuilding the same immutable data wastes both
network capacity and wall-clock time. Suitable reusable objects include:

- Apptainer images;
- read-only reference genomes;
- annotation databases;
- aligner indexes;
- model weights;
- software archives; and
- decompressed copies of compressed references when repeated local access
  justifies the space.

A cache is not a substitute for provenance. Every cached object must be tied to
an immutable identity such as:

- a cryptographic checksum;
- a container digest;
- an exact version;
- a versioned path; or
- a workflow-managed content hash.

### Node-local cache pattern

Use a stable cache directory separate from job-specific scratch:

```bash
readonly CACHE_ROOT="/local/apptainercache/${USER}"
readonly JOB_WORK="${SLURM_TMPDIR:-/local/work/${USER}/slurm-job-${SLURM_JOB_ID}}"
readonly IMAGE_SRC="/projects/containers/tool-2.4.1.sif"
readonly IMAGE_SHA256="EXPECTED_SHA256"
readonly IMAGE_CACHE="${CACHE_ROOT}/containers/${IMAGE_SHA256}.sif"

mkdir -p -- "$(dirname -- "${IMAGE_CACHE}")" "${JOB_WORK}"

if [[ ! -s "${IMAGE_CACHE}" ]]; then
    tmp="${IMAGE_CACHE}.${SLURM_JOB_ID}.tmp"
    rsync -a -- "${IMAGE_SRC}" "${tmp}"
    echo "${IMAGE_SHA256}  ${tmp}" | sha256sum -c -
    mv -f -- "${tmp}" "${IMAGE_CACHE}"
fi

apptainer exec "${IMAGE_CACHE}" tool ...
```

The temporary file plus atomic rename prevents concurrent jobs from seeing a
partially populated cache entry. For heavily shared nodes, administrators may
provide a managed read-only cache instead of per-user caches.

### What should not be cached blindly

Do not treat these as immutable cache objects without additional controls:

- patient-derived working data;
- outputs still being modified;
- files selected only by a mutable name such as `latest.sif`;
- credentials, tokens, or secrets;
- databases whose files are updated in place; and
- data whose license or governance rules prohibit local persistence.

Cached patient-related data remains subject to the same security and deletion
requirements as the source. Primary identifying fields are not allowed on RCC.

### Container cache behavior

Apptainer may cache downloaded images and layers. Workflows should avoid
independent jobs repeatedly pulling the same container from the internet or
shared storage. Prefer:

1. a centrally managed, versioned `.sif` image;
2. a digest-pinned image;
3. a node-local or administrator-managed cache; and
4. pre-staging before the compute-intensive phase.

A cached container improves startup time and reduces repeated small-file or
network operations, but it does not make the application's own data access
pattern efficient. Application inputs and temporary files may still require
local staging.

## 11. Do not submit Slurm jobs from inside Slurm jobs

A batch job should normally perform the computation assigned to it. It should
not act as an uncontrolled scheduler that creates additional `sbatch` jobs.

Nested job submission is harmful because it separates resource allocation from
the process that understands the data:

- the parent allocation may sit idle while child jobs wait in the queue;
- child jobs may run on unrelated nodes where no staged data or warm cache
  exists;
- the same input or container may be copied repeatedly to many nodes;
- temporary data produced by the parent may be inaccessible to children;
- cancellation of the parent does not necessarily cancel all descendants;
- accounting, failure handling, and dependency tracking become harder;
- job storms can overload the scheduler; and
- large bursts of child jobs can create synchronized metadata and network
  traffic against shared storage.

This directly disrupts good I/O patterns. A parent job may stage 100 GB to local
disk, then submit child jobs that are scheduled elsewhere and must read the same
100 GB again from the network. The staged copy becomes useless, caches are cold,
and the workflow produces avoidable traffic.

### Bad pattern

```bash
#!/usr/bin/env bash
#SBATCH --cpus-per-task=1

for sample in samples/*; do
    sbatch run-one-sample.sh "${sample}"
done
```

This uses a compute allocation merely to submit work and gives Slurm no
structured view of the complete workflow's data dependencies.

### Better patterns

Submit arrays from a login or submission host:

```bash
sbatch --array=0-999 run-one-sample.sh
```

Use explicit Slurm dependencies:

```bash
first=$(sbatch --parsable stage-data.sh)
second=$(sbatch --parsable --dependency=afterok:"${first}" analyse.sh)
sbatch --dependency=afterok:"${second}" publish.sh
```

Or let Snakemake submit the workflow from an approved submission service using
the configured Slurm executor. Snakemake should express files, resources,
retries, and dependencies; individual compute jobs should not recursively
create more jobs.

There are advanced cases in which a scheduler-aware workflow engine submits
jobs while itself running under a controlled service allocation, but this must
be an RCC-approved design. It is not the default user pattern.


## 12. Diagnose an I/O-bound job

Start with Slurm accounting:

```bash
sacct -j JOB_ID \
  --format=JobID,State,Elapsed,AllocCPUS,TotalCPU,ReqMem,MaxRSS
```

Inside an active allocation, useful tools may include:

```bash
time command ...
pidstat -dru 2
vmstat 2
iostat -xz 2
```

Interpretation:

| Observation | Likely issue |
|---|---|
| elapsed time is high but total CPU time is low | waiting, serial work, or I/O |
| high I/O wait and low CPU utilization | storage bottleneck |
| many file opens and long startup | small-file or metadata pressure |
| CPU use increases after staging locally | network I/O was limiting |
| local staging costs more than it saves | working set too large or workload already streams efficiently |

Use representative pilot data and change one variable at a time.

## 13. Class exercise

1. Create a synthetic compressed FASTQ file on approved shared storage.
2. Run the supplied direct shared-storage example.
3. Run the local-staging example with the same input and resources.
4. Compare elapsed time, CPU time, output checksum, and file-operation pattern.
5. Increase the number of small temporary files and observe how runtime changes.
6. Explain which version is safer for scaling to thousands of samples.

The exercise is about the access pattern, not about producing an artificially
large benchmark that disrupts the cluster.

## 14. Decision checklist

Use local scratch when:

- the tool creates many temporary files;
- the tool performs repeated random reads or writes;
- the input will be reread many times during one job;
- a temporary database or index is built per job; or
- local staging measurably reduces elapsed time and shared-storage pressure.

Keep direct shared-storage streaming when:

- the tool performs one sequential pass;
- input is much larger than local capacity;
- staging would duplicate most of the job's total I/O;
- several nodes must concurrently read one durable source; or
- RCC policy identifies the storage tier as suitable for that pattern.

## Take-home rule

> Shared storage is for durable data. Node-local scratch is for active
> temporary computation. Stream when possible; stage locally when random or
> small-file I/O would otherwise dominate.

## Completion gate

Using only synthetic data, run the direct and local-staging examples with the
same Slurm resources. Record elapsed time, CPU time, output checksums, and the
access pattern. Explain which version you would choose for a larger workload
and why.
