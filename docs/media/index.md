# Training videos, slides, and narration

All fifteen numbered classes include slide-based videos with natural
British-English narration. Speech is paced for technical learning, mastered to
a consistent loudness target, and accompanied by downloadable captions and a
plain-text transcript. The same videos are prominent at the start of every
class so learners can watch them in context.

## Class 1: safe access to RCC

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_1_Video_Enhanced.mp4"><track kind="captions" srclang="en" label="English captions" src="../downloads/captions/RCC_Onboarding_Part_1_Captions.vtt" default></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_1_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_1.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_1_Narration.md)

## Class 2: reproducible scientific workflows

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_2_Video_Enhanced.mp4"><track kind="captions" srclang="en" label="English captions" src="../downloads/captions/RCC_Onboarding_Part_2_Captions.vtt" default></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_2_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_2.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_2_Narration.md)

## Class 3: performance and efficient I/O

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_3_Video_Enhanced.mp4"><track kind="captions" srclang="en" label="English captions" src="../downloads/captions/RCC_Onboarding_Part_3_Captions.vtt" default></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_3_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_3.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_3_Narration.md)

## Class 4: containers with Apptainer

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_4_Video_Enhanced.mp4"><track kind="captions" srclang="en" label="English captions" src="../downloads/captions/RCC_Onboarding_Part_4_Captions.vtt" default></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_4_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_4.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_4_Narration.md)

## Classes 5–15

The remaining concise video lessons are embedded on their class pages, with
captions and transcripts immediately below each player:

- [Class 5 · Slurm acceptance patterns](../course/class-05-slurm.md#watch-first)
- [Class 6 · Protected project websites](../course/class-06-vhosts.md#watch-first)
- [Class 7 · Python notebooks for large datasets](../course/class-07-python-notebooks.md#watch-first)
- [Class 8 · R notebooks and large-data analysis](../course/class-08-r-analysis.md#watch-first)
- [Class 9 · Shiny applications](../course/class-09-shiny.md#watch-first)
- [Class 10 · Notebooks to governed services](../course/class-10-notebook-to-service.md#watch-first)
- [Class 11 · Biomedical data protection](../course/class-11-biomedical-data-privacy.md#watch-first)
- [Class 12 · Efficient local I/O](../course/class-12-efficient-io.md#watch-first)
- [Class 13 · RCC storage architecture](../course/class-13-storage-architecture.md#watch-first)
- [Class 14 · Wet-lab instrument workflows](../course/class-14-wet-lab-data-workflows.md#watch-first)
- [Class 15 · Research data lifecycle](../course/class-15-data-lifecycle.md#watch-first)

The original [Class 7 large-data slide deck](../downloads/slides/RCC_Class_7_Interactive_Large_Data.pptx)
and [Class 9 Shiny slide deck](../downloads/slides/RCC_Class_9_Shiny_Jupyter_Project_Apps.pptx)
remain available as instructor resources.

## Rebuilding the videos

The committed 1280 × 720 frames are the reviewed visual source. On macOS, run
`python3 build/build_videos.py` for Classes 1–4 and
`python3 build/build_course_videos.py` for Classes 5–15. Both builds use the
installed Daniel British-English voice by default and create captions, hashes,
durations, and audio-quality records in `meta/`.
