# Class 4: containers with Apptainer

## Learning objectives

You will run a pinned, read-only Apptainer image through Slurm and understand how images, caches, temporary directories and bind mounts interact with shared storage.

## Why RCC uses Apptainer

An immutable SIF image packages the runtime into one file. This improves reproducibility and avoids placing a very large collection of tiny environment files on network storage.

A container is not automatically trustworthy. Use approved registries, immutable digests or checksums, and reviewed definitions. A container does not validate scientific methods or make unsafe data handling acceptable.

## Safe execution pattern

```bash
apptainer exec --cleanenv /path/to/pinned-image.sif tool --version
```

Choose the command for the task:

| Command | Use |
|---|---|
| `apptainer run IMAGE.sif` | Run the image's declared default action |
| `apptainer exec IMAGE.sif COMMAND` | Run one explicit command |
| `apptainer shell IMAGE.sif` | Inspect interactively inside a bounded allocation |

Bind only what the tool needs and make input read-only where possible:

```bash
apptainer exec --cleanenv \
  --bind /projects/<project>/input:/input:ro \
  --bind "$SLURM_TMPDIR:/work" \
  image.sif tool --input /input/data.tsv --output /work/result.tsv
```

For a GPU job, Slurm allocates the GPU and Apptainer exposes the host driver using the approved RCC pattern. Do not attempt to install or replace host GPU drivers.

## Good storage pattern

- Store approved production images in the documented image location.
- Put cache and temporary activity on the approved local or managed cache path.
- Bind only the data directories required by the tool.
- Use read-only binds for input where possible.
- Record the image digest with the analysis.

> **Reference companion:** [Conda, Snakemake, and Apptainer](../reference/software-workflows.md)
> covers cache placement, GPU exposure, writable temporary layers, sandbox
> limits, and the reproducibility record for an important run.

## Completion gate

Run the approved training image in Class 5 and compare the exact output with the expected file.
