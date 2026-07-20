# Conda, Snakemake, and Apptainer reference

This guide complements Classes 2 and 4 with the command-level material from the
earlier ClusterDocs site.

## Conda and Mamba environments

Keep an environment declaration with the project and pin important versions:

```yaml
name: analysis
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.12
  - pandas
  - snakemake
```

Create and update the environment with the RCC-supported Conda-compatible
client. Do not place credentials in `environment.yml`.

Create environments inside an allocated worker. Confirm `CONDA_ENVS_PATH` and
`CONDA_PKGS_DIRS` use the approved RCC node-local paths rather than shared home
or project storage.

An active Conda environment can contain thousands of small files. For heavy or
repeated workloads, prefer an approved managed environment, a packed
environment staged locally, or an immutable Apptainer image.

### Activate Conda inside a Slurm script

`conda activate` is a shell function and may be unavailable in a non-interactive
batch shell. Initialize the shell hook explicitly:

```bash
#!/usr/bin/env bash
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1

eval "$(conda shell.bash hook)"
conda activate analysis
srun python analysis.py
```

Do not run `conda init` inside each Slurm job. Record the environment export or
lock file with the analysis.

## Snakemake

Snakemake describes dependencies between files and can submit bounded work to
Slurm. Keep workflow definitions on shared project storage so every allocated
worker can reach them, while allowing individual rules to stage high-I/O data
to local scratch.

Start with a dry run:

```bash
snakemake --dry-run --printshellcmds
```

Then use the currently supported RCC execution profile. Limit concurrency to a
value justified by the workflow rather than launching an unbounded number of
jobs. Keep the scheduler process in a named `tmux` session only when the
approved profile requires a persistent submission process:

```bash
tmux new -s workflow
snakemake --jobs 4
```

After reconnecting to the same approved submission service:

```bash
tmux attach -t workflow
```

Do not rely on a historic Snakemake version or profile name from a copied guide.
Check the rollout page for the supported version and profile before updating a
production workflow.

## Apptainer execution model

Apptainer runs containers as the calling user and does not grant Docker-style
root privileges. Production images should be immutable SIF files identified by
a digest.

Common commands are:

- `apptainer run IMAGE.sif` for the image's default action;
- `apptainer exec IMAGE.sif COMMAND` for a specific command;
- `apptainer shell IMAGE.sif` for bounded interactive inspection.

Use a clean environment and explicit binds:

```bash
apptainer exec --cleanenv \
  --bind /APPROVED/INPUT:/input:ro \
  --bind "$PWD/results:/results" \
  /APPROVED/IMAGES/tool.sif \
  tool --input /input/sample.dat --output /results/result.dat
```

The container filesystem is normally read-only. Host directories such as the
working directory may be visible inside the container, so a container is not a
security boundary for project data. Bind only what the tool needs.

### Cache and temporary files

Image conversion and pulls can create substantial cache and temporary data.
Point those locations at the approved local or managed cache path rather than a
metadata-sensitive shared environment tree:

```bash
export APPTAINER_CACHEDIR=/APPROVED/CACHE/PATH
export APPTAINER_TMPDIR=/APPROVED/TEMP/PATH
```

### GPU jobs

Request the GPU through Slurm, then expose the assigned host driver using the
approved Apptainer option:

```bash
apptainer exec --cleanenv --nv /APPROVED/IMAGES/gpu-tool.sif nvidia-smi
```

Do not override `CUDA_VISIBLE_DEVICES`; Slurm uses it to identify the devices
allocated to the job.

### Writable sandboxes

Writable sandboxes generate many files and are unsuitable as a production
artifact on shared storage. Build and inspect them only in an approved local
development location, then produce an immutable reviewed SIF image for normal
use.

## Reproducibility record

For an important run, retain the Git commit, environment or container
declaration, container SHA-256 digest where applicable, input and final-output
checksums, Slurm job ID and resource request, application versions, parameters,
logs, and benchmark output.
