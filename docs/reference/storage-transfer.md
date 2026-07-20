# Storage and transfer

Choose storage by lifecycle and access pattern, not only by free capacity.

> **Related learning:** [Class 1](../course/class-01-safe-access.md) introduces
> the files portal, [Class 3](../course/class-03-performance.md) explains local
> staging, and [Class 11](../course/class-11-biomedical-data-privacy.md) covers
> the biomedical-data admission decision.

## Storage decision table

| Purpose | Location or service | Rule |
|---|---|---|
| Personal configuration and small source files | home storage | Not a shared project-data area |
| Durable project input and final results | approved project storage | Shared according to project membership |
| Group material outside a specific project | approved group storage | Use only when group governance applies |
| High-I/O intermediates during a job | job-local scratch | Not backed up; copy required results back |
| Reusable software environment | approved local Conda path or immutable container | Do not run metadata-heavy environments from shared storage |
| Browser upload and download | RCC files portal | Confirm project and destination before transfer |

Project and group directories may be mounted on demand and may not be globally
listable. Use the full path supplied for your project rather than probing for
other names.

## Stage work inside a Slurm job

The supported pattern is durable input, local computation, durable result:

```bash
#!/usr/bin/env bash
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00

set -euo pipefail
scratch="${SLURM_TMPDIR:-/local/work/slurm-jobs/$USER/slurm-job-$SLURM_JOB_ID}"
mkdir -p "$scratch/input" "$scratch/output"
cp --reflink=auto --archive "$SLURM_SUBMIT_DIR/data/input.tsv" "$scratch/input/"
srun my-analysis "$scratch/input/input.tsv" "$scratch/output/result.tsv"
cp --archive "$scratch/output/result.tsv" "$SLURM_SUBMIT_DIR/results/"
```

Use the job-local path provided by RCC when available. Never assume local files
survive job completion, reboot, maintenance, or cleanup.

## Pick a transfer method

- Use the **RCC files portal** for ordinary browser-based project transfers.
- Use `scp`, `sftp`, or `rsync` over the approved SSH route for scripted or
  resumable transfers.
- For a large tree of small files, create one archive before transfer to reduce
  metadata operations, then verify it with a checksum.
- Use an approved institutional bulk-transfer service when the files portal or
  SSH route is unsuitable.

Example with `rsync`:

```bash
rsync --archive --partial --info=progress2 \
  ./dataset/ {{ ssh_alias }}:/projects/<project>/incoming/dataset/
```

Example with an archive and checksum:

```bash
tar -czf dataset.tar.gz dataset/
sha256sum dataset.tar.gz > dataset.tar.gz.sha256
scp dataset.tar.gz dataset.tar.gz.sha256 \
  {{ ssh_alias }}:/projects/<project>/incoming/
```

On RCC, verify before extracting:

```bash
cd /projects/<project>/incoming
sha256sum -c dataset.tar.gz.sha256
tar -tzf dataset.tar.gz | sed -n '1,20p'
```

Inspect archive paths before extraction. Reject archives containing absolute
paths or unexpected `..` components.

## Unsupported transfer pattern

Do not transfer project data with a raw Netcat listener. It has no built-in
authentication or encryption, can expose an unintended port, and bypasses the
reviewed RCC entry points. The old ClusterDocs Netcat recipe is intentionally
not retained.

## Object storage

Object storage does not behave like a POSIX filesystem. Applications must use
an object client or API, and data commonly needs staging to job-local storage.
Use it only when the project has an approved endpoint, credentials, retention
policy, and documented client configuration. Never place access keys in shell
history, notebooks, Git, or shared configuration files.

## Controlled and archival data

Before transfer, confirm that the project governance covers RCC and follow the
[biomedical-data admission guide](../security/rcc-biomedical-data-admission.md).
For submission to repositories such as the European Genome-phenome Archive,
follow the repository's current official submission and encryption workflow;
do not reuse historical FTP commands from the old site without validation.
