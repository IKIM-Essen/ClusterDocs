# Class 4: containers with Apptainer

<section class="course-video-hero" id="watch-first">
  <p class="course-video-kicker">Recommended starting point · 10 min video</p>
  <h2>Watch the class first</h2>
  <p>Reproducible containers, trusted images, binds, and scratch. Watch the complete lesson, then use the written page below for copyable commands, exercises, and reference details.</p>
  <video controls preload="metadata" playsinline poster="../../assets/video-posters/part4.png" src="{{ media_base_url }}/RCC_Onboarding_Part_4_Video_Enhanced.mp4?v=0cb25d31">
    <track kind="captions" srclang="en" label="English captions" src="../../downloads/captions/RCC_Onboarding_Part_4_Captions.vtt" default>
    Your browser does not support embedded video.
  </video>
  <div class="course-video-links" aria-label="Video alternatives and downloads">
    <a href="../../downloads/captions/RCC_Onboarding_Part_4_Captions.srt">Captions</a>
    <a href="../../downloads/narration/RCC_Onboarding_Part_4_Narration.md">Read transcript</a>
  </div>
</section>

## Learning objectives

You will run a pinned, read-only Apptainer image through Slurm and understand how images, caches, temporary directories and bind mounts interact with shared storage.

## Why RCC uses Apptainer

An immutable SIF image packages the runtime into one file. This improves reproducibility and avoids placing a very large collection of tiny environment files on network storage.

A container is not automatically trustworthy. Use approved registries, immutable digests or checksums, and reviewed definitions. A container does not validate scientific methods or make unsafe data handling acceptable.

## What rootless Apptainer means—and why RCC uses it

For normal execution, Apptainer is **rootless**: the program in the container
runs with your RCC user and group identity, not as the host's `root` user, and
there is no privileged Docker-style daemon starting jobs on your behalf. Even
if software inside the image displays a user called `root`, that identity does
not become unrestricted root on the RCC host.

This model matters on a shared research cluster because it:

- keeps the host kernel, devices, drivers, scheduler and system configuration
  under RCC administration;
- applies the same project-file permissions and Slurm allocation boundaries
  inside and outside the container;
- limits the damage from a mistaken command or compromised application to the
  access already held by the submitting user; and
- avoids giving every container workflow access to a long-running privileged
  container daemon.

Rootless does **not** mean harmless or isolated from your data. A process in the
container can read, change or delete any host file that your user can access
and that is visible or bound into the container. Bind only required paths,
make inputs read-only where possible, keep credentials outside the image, and
continue to use trusted images. Building an image can have different privilege
requirements; use an RCC-approved builder, reviewed definition, or supported
rootless/fakeroot workflow rather than assuming production jobs may build with
host privileges.

## Safe execution pattern

```bash
apptainer exec --cleanenv /path/to/pinned-image.sif tool --version
```

Choose the command for the task:

| Command | Use |
|---|---|
| `apptainer run IMAGE.sif` | Run the image's declared default action |
| `apptainer exec IMAGE.sif COMMAND` | Run one explicit command |
| `apptainer shell IMAGE.sif` | Inspect interactively inside a bounded allocation |

Bind only what the tool needs and make input read-only where possible:

```bash
apptainer exec --cleanenv \
  --bind /projects/<project>/input:/input:ro \
  --bind "$SLURM_TMPDIR:/work" \
  image.sif tool --input /input/data.tsv --output /work/result.tsv
```

For a GPU job, Slurm allocates the GPU and Apptainer exposes the host driver using the approved RCC pattern. Do not attempt to install or replace host GPU drivers.

## Good storage pattern

- Store approved production images in the documented image location.
- Put cache and temporary activity on the approved local or managed cache path.
- Bind only the data directories required by the tool.
- Use read-only binds for input where possible.
- Record the image digest with the analysis.

> **Reference companion:** [Conda, Snakemake, and Apptainer](../reference/software-workflows.md)
> covers cache placement, GPU exposure, writable temporary layers, sandbox
> limits, and the reproducibility record for an important run.

## Completion gate

Run the approved training image in Class 5 and compare the exact output with the expected file.
