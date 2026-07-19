# Class 5: Slurm acceptance patterns

This class adapts the same three patterns used by RCC software acceptance testing, but scales them down for one learner and one tiny job at a time.

## Pattern 1: Bash hello

The first job verifies scheduling, environment capture, output handling and exact comparison.

```bash
bash exercises/slurm/run-gate.sh bash
```

## Pattern 2: Snakemake inside an allocation

The second job runs a minimal local Snakemake workflow. It does not download packages or contact external services.

```bash
bash exercises/slurm/run-gate.sh snakemake
```

## Pattern 3: Apptainer inside an allocation

The third job uses an instructor-provided, immutable training image:

```bash
export RCC_TRAINING_IMAGE=/approved/path/to/training-image.sif
bash exercises/slurm/run-gate.sh apptainer
```

## Built-in availability protection

The gate:

- submits only one job at a time;
- uses one CPU, 128 MiB RAM and a two-minute limit;
- refuses job arrays;
- refuses to run when another learner gate is active for the same user;
- waits for a bounded period;
- compares output byte-for-byte;
- cleans only its own temporary directory;
- does not enumerate nodes or expose scheduler configuration.

## What the examples prove

A passing class gate shows that your account can execute the pattern. It is not a cluster-wide health test and must not be expanded into host-by-host probing.

## Knowledge check

<details><summary>Why compare output byte-for-byte?</summary>

It detects small, unexpected changes and makes the gate deterministic.
</details>

<details><summary>Why not run all examples in parallel?</summary>

Parallelism is unnecessary for a learner gate and creates avoidable load and harder-to-understand failures.
</details>
