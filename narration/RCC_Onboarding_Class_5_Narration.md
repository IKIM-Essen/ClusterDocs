# Class 5 narration: Slurm acceptance patterns

This class uses three small patterns adapted from RCC software acceptance testing. The goal is not to test every server. The goal is to confirm that your own account can submit one bounded job, run a local Snakemake workflow, and execute an approved Apptainer image.

Every example requests one CPU, a small amount of memory, and two minutes. The gate submits jobs sequentially, compares exact output, and cleans only its own temporary directory. Do not turn these exercises into host-by-host probes, job arrays, or retry loops.

The Bash example proves the basic path from submission to output. The Snakemake example proves that a workflow can run within a scheduler allocation without downloading software. The Apptainer example proves that a pinned image can run in a clean environment. When output differs, stop and inspect the log rather than repeatedly resubmitting.

Availability is part of IT security. Small, predictable tests help everyone; uncontrolled tests can become a denial-of-service problem. A passing result is evidence for your workflow pattern, not permission to scan the cluster.
