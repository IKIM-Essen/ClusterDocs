# RCC onboarding curriculum for biomedical researchers

This staging package contains an eleven-class English-language onboarding curriculum for researchers who are new to Linux clusters, distributed workflows, Slurm, VS Code, performance engineering, Apptainer, and governed project web applications.

## Curriculum

### Part 1 - Your first day on the RCC cluster

Mental model of a shared cluster, local versus remote work, SSH and key handling, Windows and macOS preparation, VS Code Remote SSH, managed data transfer, checksums, the Slurm job lifecycle, and appropriate use of tmux.

### Part 2 - Reproducible scientific workflows

Project structure, Miniforge, Mamba, Bioconda, software environments, Snakemake dependency graphs, Slurm execution, a minimal statistical workflow, a synthetic DNA sequence workflow, logging, benchmarking, and Git.

### Part 3 - Performance and efficient I/O

CPU, threads, GPU, RAM, storage capacity, throughput, latency, IOPS, metadata operations, streaming versus random access, large versus small files, crowded directories, compression, node-local scratch, Snakemake staging patterns, and bottleneck diagnosis. It explicitly warns that poor workflow structure can turn an analysis expected to take hours into one that takes weeks or months.

### Part 4 - Containers with Apptainer

Why containerized software is useful on a shared cluster; why active Conda environments on network storage can create a small-file and metadata workload; immutable SIF images; cache, temporary space, bind mounts, read-only inputs, GPU use, Snakemake container directives, image trust, and production image lifecycle.

## Deliverable types

The original four classes include:

- a long-form PDF;
- an editable DOCX source;
- an editable PowerPoint slide deck with speaker notes;
- a 5-10 minute MP4 training video with processed synthetic narration;
- an SRT caption file; and
- a Markdown narration script.

The canonical source for the original four classes is the Markdown document in `source/`. Classes 5-11 are maintained directly in the course, exercise and narration trees until their additional media assets are recorded. The DOCX, PDF, PPTX, and MP4 files are rendered review artifacts.

## Video format

The videos are 1280 x 720 H.264/AAC slide-based training videos. Narration uses a synthetic British-English voice with slower pacing, acronym pronunciation handling, equalization, dynamic-range compression, normalization, and captions. They do not connect to production RCC services and contain no credentials or biomedical data.

## Production status

This is a publication candidate, not a claim that every local command has already been validated against the production RCC configuration. Before publication, administrators must complete the local values and run the tests in `ADMIN_CHECKLIST.md`.

The statistical and DNA examples are educational. They are not validated clinical pipelines and do not replace study-design, statistical, bioinformatics, data-protection, or clinical review.

## Local website preview

The custom RCC-styled site produced by `tools/build_site.py` is the canonical
ClusterDocs NG website. The `mkdocs.yml` file remains useful for content and
navigation checks, but `mkdocs serve` does not reproduce the published design.

Build and browse the same site used by the validation and deployment workflow:

```bash
python tools/build_site.py --output site-preview
python -m http.server 8765 --bind 127.0.0.1 --directory site-preview
```

Then open <http://127.0.0.1:8765/>.

## Repository integration

`meta/PULL_REQUEST_PLAN.md` recommends an umbrella issue and four reviewable documentation pull requests. Markdown should remain the authoritative repository content. Large MP4 files should normally be hosted as approved institutional media or release assets rather than added to ordinary Git history.


## v0.1.2 additions

This staging version adds Classes 7-10 for Python notebooks, R analysis, Shiny development, and notebook-to-service workflows. It also includes copyable examples under `examples/interactive-workflows` and two new slide decks for instructors.

## v0.1.3 additions

This version adds Class 11 on European and German data protection for biomedical research. It explains that direct identifiers and re-identification keys remain outside RCC, while approved genomic and X-ray/CT/MRI research data may be processed in the controlled enclave. It includes proportionate guidance on pseudonymisation, data minimisation, defacing, official legal resources, and the Universitätsklinikum Essen data-protection contact. Completion is based on training scenarios and project governance, not automated inspection of research files.
