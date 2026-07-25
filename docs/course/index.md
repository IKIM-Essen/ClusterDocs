# Fifteen-class RCC learning path

The classes are sequential for new users, but experienced users can take the readiness gates and skip material they already know.

## Prefer to learn by video?

Start with one of the complete video lessons below. Each class page opens with
the player; the written material remains underneath for commands, exercises,
and detailed reference.

<div class="video-course-grid">
  <a class="video-course-card" href="class-01-safe-access.md#watch-first"><img src="../assets/video-posters/part1.png" alt="Class 1 video title: Your first day on the RCC cluster"><span><strong>Class 1 · Safe access</strong><small>8 min video</small></span></a>
  <a class="video-course-card" href="class-02-workflows.md#watch-first"><img src="../assets/video-posters/part2.png" alt="Class 2 video title: Reproducible scientific workflows"><span><strong>Class 2 · Workflows</strong><small>9 min video</small></span></a>
  <a class="video-course-card" href="class-03-performance.md#watch-first"><img src="../assets/video-posters/part3.png" alt="Class 3 video title: Performance and efficient I/O"><span><strong>Class 3 · Performance</strong><small>11 min video</small></span></a>
  <a class="video-course-card" href="class-04-containers.md#watch-first"><img src="../assets/video-posters/part4.png" alt="Class 4 video title: Containers with Apptainer"><span><strong>Class 4 · Containers</strong><small>9 min video</small></span></a>
</div>

| Class | Main outcome | Typical time | Gate |
|---|---|---:|---|
| 1 | Connect safely using SSH and VS Code | 45-60 min | Local tools and one bounded SSH test |
| 2 | Build a reproducible Snakemake project | 60-90 min | Dry run and reproducible output |
| 3 | Choose CPU, RAM, GPU and I/O patterns | 45-60 min | Diagnose a synthetic bottleneck |
| 4 | Run a pinned Apptainer image | 45-60 min | Immutable image and clean environment |
| 5 | Submit three small Slurm acceptance jobs | 45-60 min | Byte-for-byte expected output |
| 6 | Select, build and request an appropriately scoped protected project website | 75-100 min | Local tests, scope decision and vhost checklist |
| 7 | Use Python notebooks for large-data inspection, data science, and responsible AI exploration | 75-100 min | Loopback-only Jupyter job and example validation |
| 8 | Use R notebooks and batch scripts for statistical and larger tabular analysis | 75-100 min | R example job and reproducibility explanation |
| 9 | Develop Shiny apps safely before governed deployment | 60-90 min | Tunnelled development session and vhost readiness decision |
| 10 | Convert notebooks into governed services or Slurm workflows | 60-90 min | Architecture statement and review checklist |
| 11 | Use biomedical data lawfully and safely in the RCC research enclave | 60-75 min | Scenario-based knowledge check and project-governance confirmation |
| 12 | Stage I/O-intensive work to job-local scratch and publish results safely | 60-90 min | Direct-versus-local synthetic comparison and justified storage choice |
| 13 | Trace RCC metadata, object-storage, network, and cache behavior | 45-60 min | Storage-path diagnosis and measurement plan |
| 14 | Move wet-lab instrument data into an approved RCC workflow | 60-90 min | Verified synthetic handoff plan with ownership and retention |
| 15 | Move instrument data through governed project storage and analysis to Coscine | 60-75 min | Synthetic instrument-to-Coscine lifecycle plan with verified acceptance criteria |

## Course rules

1. Never paste passwords, private keys, passkey exports, tokens, patient identifiers, or restricted sample sheets into exercises.
2. Run computation through Slurm rather than on the login host.
3. Use one small test at a time. Do not create job arrays, retry loops, connection loops, or host scans.
4. Store durable project data under the approved project area and use node-local temporary storage for high-I/O intermediate work.
5. Treat generated output as reproducible, not as a reason to bypass version control and provenance.
6. Ask for project membership rather than sharing another person's account.
7. Keep notebooks and web apps small enough that another person can review what they do.
8. Use `cpu_short` for jobs up to two hours, keep interactive work attended,
   and move long runners into bounded, restartable Slurm batch jobs on regular
   compute.
9. Keep direct identifiers and re-identification keys outside RCC; process genomic, imaging, and other biomedical research data only under the project governance that covers RCC.

## Progress bookkeeping

Progress is stored locally on the learner's computer; no central tracking is required:

```bash
python3 tools/coursectl.py status
python3 tools/coursectl.py mark 1 ssh-ready
```

The progress file contains only class and gate names. It never records credentials, host keys, filenames, project names, or research data.
