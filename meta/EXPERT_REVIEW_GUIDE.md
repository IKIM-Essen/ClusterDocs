# Expert review guide

## Purpose

Confirm that ClusterDocs NG is technically correct, operationally supportable,
and safe enough for a novice pilot. Record issues with a page URL, heading,
severity, proposed correction, and responsible owner.

## Review in this order

1. Complete Class 1 using a clean test account and current supported client.
2. Check Classes 2–5 for project layout, Slurm, I/O, Conda, Snakemake, and
   rootless Apptainer accuracy.
3. Check Classes 6–10 for supported website, notebook, R, Shiny, and service
   patterns.
4. Ask the institutional owners to review Classes 11 and 13–15 for privacy,
   storage, lab-network, instrument-ingestion, sharing, retention, and Coscine
   boundaries.
5. Review every reference page reached from those tasks, not just the class
   prose.
6. Follow `VIDEO_REVIEW_GUIDE.md` for each class video.

## Acceptance questions

- Do all hostnames, aliases, URLs, versions, partitions, paths, and support
  routes describe services that users can access now?
- Does every command state where it runs and avoid administrator privileges?
- Do Slurm examples request realistic resources and keep sustained work off the
  submission host?
- Does Apptainer remain rootless, immutable where appropriate, and GPU-aware
  without implying Docker-style privilege?
- Do data examples keep identifiable or re-identifiable biomedical data out of
  unapproved paths and tools?
- Are project groups, setgid directories, sharing, transfer, retention, and
  archiving instructions consistent with actual policy?
- Can support reproduce the prescribed diagnostics without asking for secrets
  or unrestricted logs?

## Severity

- **Blocker:** unsafe, legally incorrect, data-loss risk, inaccessible service,
  wrong command, or missing required institutional decision.
- **Major:** likely to prevent a user completing the task or create substantial
  support load.
- **Minor:** local ambiguity, terminology, accessibility, or presentation issue
  with a usable workaround.

The expert reviewer approves content; they do not change media manifest review
status until the matching video has also passed the video review.
