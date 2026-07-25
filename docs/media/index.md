# Training videos, slides, and narration

The first four numbered classes include slide-based videos with natural
British-English narration. Speech is paced for technical learning, mastered to
a consistent loudness target, and accompanied by downloadable captions and a
plain-text transcript. The same videos are embedded at the start of Classes
1–4 so learners can watch them in context.

## Class 1: safe access to RCC

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_1_Video_Enhanced.mp4"></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_1_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_1.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_1_Narration.md)

## Class 2: reproducible scientific workflows

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_2_Video_Enhanced.mp4"></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_2_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_2.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_2_Narration.md)

## Class 3: performance and efficient I/O

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_3_Video_Enhanced.mp4"></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_3_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_3.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_3_Narration.md)

## Class 4: containers with Apptainer

<video controls preload="metadata" width="100%" src="{{ media_base_url }}/RCC_Onboarding_Part_4_Video_Enhanced.mp4"></video>

[Captions](../downloads/captions/RCC_Onboarding_Part_4_Captions.srt) ·
[slides](../downloads/slides/RCC_Onboarding_Part_4.pptx) ·
[narration transcript](../downloads/narration/RCC_Onboarding_Part_4_Narration.md)

## Newer classes

Recording-ready narration is available while additional class videos are being
produced:

- [Class 5 narration](../downloads/narration/RCC_Onboarding_Class_5_Narration.md)
- [Class 6 narration](../downloads/narration/RCC_Onboarding_Class_6_Narration.md)
- [Class 7 narration](../downloads/narration/RCC_Onboarding_Class_7_Narration.md)
- [Class 8 narration](../downloads/narration/RCC_Onboarding_Class_8_Narration.md)
- [Class 9 narration](../downloads/narration/RCC_Onboarding_Class_9_Narration.md)
- [Class 10 narration](../downloads/narration/RCC_Onboarding_Class_10_Narration.md)
- [Class 7 large-data slide deck](../downloads/slides/RCC_Class_7_Interactive_Large_Data.pptx)
- [Class 9 Shiny and project-app slide deck](../downloads/slides/RCC_Class_9_Shiny_Jupyter_Project_Apps.pptx)

## Rebuilding the videos

The committed 1280 × 720 frames are the reviewed visual source for Classes
1–4. On macOS, run `python3 build/build_videos.py`. The build uses the installed
Daniel British-English voice by default, creates fresh captions, and records
durations, hashes, voice settings, and audio targets in
`meta/video-build-report.json`.
