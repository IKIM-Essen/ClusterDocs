# Video review guide for Classes 1–17

Review every video on its class page in a current browser with headphones or
speakers. Captions should be enabled for at least one full pass. Record the
reviewer, date, browser, device, and result for each class.

| Class | Topic | Approx. length | Audio | Captions | Visuals | Accuracy | Result |
|---:|---|---:|---|---|---|---|---|
| 1 | Safe access | 8:06 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Reproducible workflows | 8:37 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Performance and I/O | 10:35 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Apptainer containers | 9:42 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Slurm and GPU selection | 3:04 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Snakemake on RCC | 5:34 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Nextflow on RCC (not yet released) | 6:45 | ☐ | ☐ | ☐ | ☐ | ☐ |
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

Accept only when speech is intelligible and natural, technical terms are
pronounced correctly, loudness is comfortable and consistent, captions convey
the intended technical notation, visuals remain legible at normal playback,
and narration agrees with the current page. Pause on every command or diagram
long enough to verify it. Classes 5–17 require particular attention because
their scripts and frames were generated from longer Markdown lessons.

After approval, set that class's `review_status` in
`config/media-manifest.yml` to `human_review_approved`, including the reviewer
and date in the review commit or pull request. Do not mark a class approved to
silence the readiness gate.

## Re-render a video after its narration changes

A class whose narration changed after rendering carries
`review_status: rerender_required_narration_changed` in
`config/media-manifest.yml`, and `tools/rollout_readiness.py` reports it as a
blocker. Class 15 is currently in this state (backend-S3 versus
direct-project-S3 boundary, #88).

The course videos use the macOS Daniel voice, so re-render on a Mac with
`say`, `ffmpeg`, `ffprobe`, and `rsvg-convert` installed:

```bash
python3 build/build_course_videos.py 15
```

This rewrites the MP4 under `videos-enhanced/`, the class captions under
`captions/`, and the class entry in `meta/course-video-build-report.json`.
Then:

1. copy the new MP4 into the reviewed `new-videos/` set;
2. update that class's `size_bytes`, `duration_seconds` and `sha256` in
   `config/media-manifest.yml`, plus the staged-set totals and
   `sha256s_file_sha256`;
3. update the `?v=` cache key in the class page's `<video>` source to the first
   eight hex digits of the new SHA-256, and remove the page's "Video note";
4. run `python tools/media_gate.py --local-dir new-videos`; it must report
   `PASS (17 videos)`;
5. set `review_status` back to `rendered_and_automated_qa_complete`, remove
   `rerender_reason`, and complete the human review above before approval.
