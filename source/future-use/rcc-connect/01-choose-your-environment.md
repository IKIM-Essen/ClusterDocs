# Choose how you want to work on RCC (pilot draft)

> **Planned experience, not released.** Available capabilities depend on
> site acceptance. Choose the interface that helps with your task; no
> self-declared beginner/expert status or shell proficiency test is required.

## Start where it feels natural

**Recommended starting point: browser-based RCC Analysis/Workbench.**
It requires no local editor setup and provides project-based notebooks,
workflow submission, status and results when the service is accepted.

**Want a desktop editor?** Choose VS Code for Python, scripting, Git or
debugging, or Positron for R, statistics, plots and exploratory work. Both
use RCC Connect to reach a **Slurm-allocated worker**, rather than running
substantial code on a login/shellhost.

**Prefer a terminal?** SSH and command-line tools remain supported,
visible and documented, including direct `sbatch`, `srun`, Snakemake and
Nextflow use. The shell is not restricted to a named "expert" group.
Interactive CPU/GPU work still requires an authorized Slurm allocation;
substantial unattended work belongs in batch jobs.

| I want to… | Suggested starting interface | Compute placement |
| --- | --- | --- |
| Explore data, run a notebook or workflow without local setup | Browser-based RCC Analysis | Slurm after service acceptance |
| Develop and debug Python or shell scripts | VS Code Remote-SSH | Slurm development allocation |
| Analyze and plot with R | Positron Remote-SSH | Slurm development allocation |
| Write or submit commands and scripts myself | SSH terminal | Shellhost for lightweight work; Slurm for compute |
| Run large or unattended/reproducible analysis | Whichever interface I prefer to submit from | Slurm batch partitions |

These are **recommendations, not permissions**. Users can switch whenever
their work changes. An expert bioinformatician may choose a browser,
and somebody comfortable with Bash may prefer VS Code or need help with
Slurm. Facility with one part of the shell is not evidence of familiarity
with scheduler allocation, shared-storage I/O, secure access or reproducibility.

## All choices share the same protections

- One project and its approved permissions are authoritative, regardless
  of interface. A desktop workspace or SSH hostname is not access permission.
- RCC/Slurm chooses the worker and enforces CPU, RAM, GPU, time and concurrency
  limits; no desktop application may create unscheduled compute.
- Shellhosts remain lightweight editing, transfer and submission endpoints.
  Avoid whole-filesystem `rg`, indexing, or heavy R/Python processes there.
- Only use accepted SSH identities. Never disable SSH host-key checking or
  invent a new worker destination after a disconnected session.
- A session can be resumed through its verified job identity where supported,
  or a workflow can be submitted from another interface; never resubmit after
  ambiguous transport failure without checking the previous job.

## What the future chooser should do

Present **Work in browser** prominently as the low-friction recommendation,
next to **Use VS Code**, **Use Positron**, and **Use SSH / terminal** as equally
accessible choices. Do not put the shell behind an "I am an expert" prompt,
require a certification, or call someone a beginner based on their editor.

Remember an explicit user preference per device/account, where authorized,
but never infer proficiency from it. Offer a reversible **simplified / detailed
view of controls** within any interface instead of a beginner/expert account
tier. Advanced Slurm controls are disclosed on demand with safe defaults,
clear queue/resource feedback, and explicit user confirmation when needed.

When a workflow cannot proceed (no project access, no available interactive
capacity, expired SSH trust), explain the real reason, give supported
alternatives and preserve the user's choice. Do not silently change interface
or fall back to running computation on the shellhost.

## Learn only the concepts you need

First-time readers should learn **project**, **shellhost**, **Slurm allocation**,
**durable storage**, and **job scratch** using one short example. People who
already script can skip the introduction and jump directly to the CLI or
resource-reference documentation. Explain scheduler and I/O concepts without
assuming that shell command familiarity transfers to cluster operation.

Continue with [laptop setup](02-install-rcc-connect.md),
[VS Code](03-vscode-python.md), [Positron](04-positron-r.md),
[Slurm/data](05-slurm-and-data.md), or [recovery](06-troubleshooting.md).
The final site-specific publication must identify which surfaces are
actually available and link to verified local access and support instructions.
