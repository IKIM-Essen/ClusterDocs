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

For a GPU job, Slurm allocates the GPU and Apptainer exposes the host driver using the approved RCC pattern. Do not attempt to install or replace host GPU drivers.

## Good storage pattern

- Store approved production images in the documented image location.
- Put cache and temporary activity on the approved local or managed cache path.
- Bind only the data directories required by the tool.
- Use read-only binds for input where possible.
- Record the image digest with the analysis.

## Completion gate

Run the approved training image in Class 5 and compare the exact output with the expected file.
