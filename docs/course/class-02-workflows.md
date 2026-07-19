# Class 2: reproducible scientific workflows

## Learning objectives

You will create a project that separates raw data, workflow definitions, software declarations, logs, benchmarks and generated results.

## Recommended layout

```text
project/
├── config/
├── workflow/
├── scripts/
├── envs/
├── data/raw/        # treated as read-only
├── results/         # generated
├── logs/
└── benchmarks/
```

Git should contain workflow logic, text configuration and documentation. It should not contain credentials, private keys, patient identifiers, raw research data or large generated outputs.

## Good cluster pattern

Use Snakemake to describe dependencies and submit work through Slurm. Do not keep a large workflow running as ordinary processes on the login host. Use a dry run before submission:

```bash
snakemake --dry-run --printshellcmds
```

Then use the RCC-supported execution profile described on the production site.

## Security moment

A reproducible workflow is also a security control: changes can be reviewed, inputs and outputs are explicit, and unexpected code is easier to identify. Pin software versions, review contributed scripts, and never run downloaded code merely because it is in a shared project directory.

## Self-learning exercise

Build a three-rule workflow that creates a small synthetic input, transforms it, and writes a checksum. Run it twice and verify that the second run performs no unnecessary work.

## Knowledge check

<details><summary>Why keep raw data read-only?</summary>

It protects the original evidence and makes the transformation from input to result reproducible.
</details>

<details><summary>What belongs in Git?</summary>

Workflow logic, scripts, environment declarations, small configuration files and documentation—not credentials or controlled data.
</details>

## Completion gate

- The workflow dry run succeeds.
- The first run creates the expected checksum.
- The second run reports that no work is required.
- `git status` contains no credentials, private data, raw datasets or generated result directories.
