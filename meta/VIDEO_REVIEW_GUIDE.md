# Stage-2 ClusterDocs video review guide

Video publication is a **Stage-2** ClusterDocs activity. Stage 1 publishes the
reviewed written site with player links fail-closed; incomplete or stale video
review must not block the Stage-1 written release while those links remain
disabled.

After the written/narration source has settled, regenerate the required media on
the approved workstation and review every video that will be enabled. Review in
a current supported browser with headphones or speakers. Captions should be
enabled for at least one full pass. Record reviewer, date, browser, device,
source commit, media hash, and result.

## Course videos

| Class | Topic | Previous approx. length | Audio | Captions | Visuals | Accuracy | Result |
|---:|---|---:|---|---|---|---|---|
| 1 | Safe access — **must be regenerated for current SSH-key policy** | 8:06 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Reproducible workflows | 8:37 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Performance and I/O | 10:35 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Apptainer containers | 9:42 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Slurm and GPU selection | 3:04 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Snakemake on RCC | 5:34 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Nextflow on RCC — **ready now** | 6:45 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Protected project websites | 3:15 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Python notebooks | 3:40 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | R analysis | 2:26 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Shiny apps | 1:53 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Notebook to service | 1:32 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Biomedical data privacy | 7:21 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 14 | Efficient local I/O | 5:32 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 15 | Storage architecture | 5:07 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 16 | Wet-lab workflows | 4:49 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 17 | Research data lifecycle | 6:03 | ☐ | ☐ | ☐ | ☐ | ☐ |

Any class whose final narration/source changed materially after its previous
render should be regenerated before approval even if the old MP4 still plays.

## Returning-user orientation video

Stage 2 may also include one short non-course video:

| Video | Target length | Audio | Captions | Visuals | Accuracy | Result |
|---|---:|---|---|---|---|---|
| What changed from the old cluster? | 3–4 min | ☐ | ☐ | ☐ | ☐ | ☐ |

Use
`narration/RCC_What_Changed_From_Old_Cluster_Narration.md` as the starting
narration. The video should remain short and focus on:

1. browser/project-first use rather than shell-first onboarding;
2. **I/O pattern as the main architecture/performance lesson**;
3. local scratch and deliberate workflow staging;
4. RCC-safe VS Code search/watcher defaults;
5. Slurm for scientific compute versus the long-lived service plane; and
6. the broader project lifecycle and capabilities now available.

Do not turn this into another complete RCC course. Its purpose is to let a
returning user understand the changed mental model quickly and then follow links
to the authoritative written pages.

## Acceptance criteria

Accept a video only when:

- speech is intelligible and natural;
- technical terms are pronounced correctly;
- loudness is comfortable and consistent;
- captions match the regenerated audio and convey technical notation correctly;
- visuals remain legible at normal playback;
- narration agrees with the accepted written source and current service status;
- no stale credential, hostname, release-state, or architecture claim remains;
- no sensitive research data or operational secret appears; and
- the exact file hash/size/duration is recorded before player activation.

For the I/O classes and the returning-user video, explicitly verify that the
message is not merely “storage is slow.” The intended lesson is that **access
pattern and metadata/random/temp I/O shape can dominate performance regardless
of headline backend bandwidth**.

After course-video approval, update that class's `review_status` in
`config/media-manifest.yml` to `human_review_approved` with reviewer/date/source
receipt in the review commit or pull request. Add any new returning-user video
to the manifest only when its filename, hash, size, duration, caption source and
review state are known. Do not mark media approved merely to silence a gate.
