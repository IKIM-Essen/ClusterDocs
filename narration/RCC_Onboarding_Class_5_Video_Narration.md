# Class 5: Slurm acceptance patterns — video narration

## Slide 1: Class 5: Slurm acceptance patterns

Welcome to Class 5: Slurm acceptance patterns. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Three execution modes

GPU work follows the same principle: request the current GPU partition in a batch job and keep interactive GPU exploration attended and bounded.

## Slide 3: Everyday Slurm commands

The following screenshot was captured from the RCC scheduler on 25 July 2026. It shows what sinfo looks like, but the available nodes and partitions can change. Run sinfo yourself before choosing a partition. A minimal batch script is: Slurm normally allocates the requested CPU, memory, GPU, and time on a suitable node. It does not give the job an exclusive whole node. Ordinary jobs should not add --nodes or --exclusive; request whole or multiple nodes only for a measured application designed to use them.

## Slide 4: Pattern 1: Bash hello

The first job verifies scheduling, environment capture, output handling and exact comparison.

## Slide 5: Pattern 2: Snakemake inside an allocation

The second job runs a minimal local Snakemake workflow. It does not download packages or contact external services.

## Slide 6: Pattern 3: Apptainer inside an allocation

The third job uses an instructor-provided, immutable training image:

## Slide 7: Built-in availability protection

The gate: submits only one job at a time; uses one CPU, 128 MiB RAM and a two-minute limit; refuses job arrays; refuses to run when another learner gate is active for the same user; waits for a bounded period; compares output byte-for-byte; cleans only its own temporary directory; does not enumerate nodes or expose scheduler configuration.

## Slide 8: What the examples prove

A passing class gate shows that your account can execute the pattern. It is not a cluster-wide health test and must not be expanded into host-by-host probing. Reference companion: After completing the bounded gates, use the Slurm command reference for dependencies, reusable allocations, GPU requests, accounting, cancellation, and checkpointing.
