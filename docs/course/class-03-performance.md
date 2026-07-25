# Class 3: performance and efficient I/O

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 11 min video</p>
  <h2>Watch the class first</h2>
  <p>CPU, GPU, memory, storage, and efficient I/O. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/part3.png" src="{{ media_base_url }}/RCC_Onboarding_Part_3_Video_Enhanced.mp4?v=0c74af89">
    <track kind="captions" srclang="en" label="English captions" src="../../downloads/captions/RCC_Onboarding_Part_3_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
  <div class="course-video-links" aria-label="Video alternatives and downloads">
    <a href="../../downloads/captions/RCC_Onboarding_Part_3_Captions.srt">Captions</a>
    <a href="../../downloads/slides/RCC_Onboarding_Part_3.pptx">Download slides</a>
    <a href="../../downloads/narration/RCC_Onboarding_Part_3_Narration.md">Read transcript</a>
  </div>
</section>

## Learning objectives

You will distinguish CPU, GPU, memory, storage capacity, throughput, latency, IOPS and metadata operations, then select a resource request based on measurement rather than guesswork.

## The most important pattern

Keep durable input and final output on approved shared storage. Stage high-I/O temporary data to node-local storage inside the job, process it there, and copy only the required results back.

Poor I/O structure can turn work expected to take hours into work that takes weeks or months. Typical causes are:

- millions of tiny files;
- random reads against network storage;
- active Conda environments with many metadata operations;
- uncompressed intermediate text files;
- too many threads competing for the same storage path;
- requests for far more memory or CPU than the program can use.

## Storage at a glance

| Data | Place during computation | Place after computation |
|---|---|---|
| Project input | Copy or stream the required subset to job-local scratch | Approved project storage |
| High-I/O intermediate files | Job-local scratch | Delete or retain only when scientifically required |
| Final results | Produce locally | Copy to approved project storage before the job exits |
| Source, notebooks, small configuration | Project or home storage | Version control where appropriate |
| Conda and Apptainer caches | Approved node-local cache | Recreate from declarations or immutable images |

A simple measurement loop is:

```bash
sacct -j <jobid> --format=JobID,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

Compare the request with actual memory, elapsed time, application benchmarks,
and I/O behavior before asking for more resources.

## Good habits

- Keep sequence files compressed when tools can stream them.
- Avoid thousands of files in one directory; use a planned hierarchy or archive format.
- Measure with Slurm accounting and application benchmarks.
- Increase resources only when evidence shows the current resource is limiting performance.
- Never run synthetic load generators or broad benchmarks on shared services without approval.

> **Reference companions:** [Storage and transfer](../reference/storage-transfer.md)
> maps durable, shared, object, and local storage to their intended uses.
> [Troubleshooting](../reference/troubleshooting.md) covers failed jobs,
> permissions, file limits, and expensive VS Code searches.

## Security moment

Availability is part of security. Accidental denial of service can come from excessive job arrays, tight retry loops, recursive metadata scans, or filling shared storage. The training exercises therefore use bounded data and one job at a time.

## Completion gate

Explain which of CPU, RAM, GPU or I/O is the likely bottleneck for one representative workflow, and name the measurement that supports your conclusion.
