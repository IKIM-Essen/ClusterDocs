# Storage and transfer

Choose storage by lifecycle and access pattern, not only by free capacity.

> **Service status:** RCC workers and SSH transfer (`scp`, `sftp`, `rsync`) to
> the shell host are **ready now**. Existing instrument Samba shares are
> **in service**; RCC sets up each new share for an approved project and
> registered device on request. The RCC Files browser portal is **not yet released**.
> RCC-to-Coscine archive transfer is **not yet released**; references to it are
> lifecycle planning, not an operational transfer command.

> **Related learning:** [Class 1](../course/class-01-safe-access.md) introduces
> safe access and transfer, [Class 3](../course/class-03-performance.md) explains local
> staging, and [Class 13](../course/class-13-biomedical-data-privacy.md) covers
> the biomedical-data admission decision.

> **Need to give someone access?** Use [How to share data safely](data-sharing.md)
> to choose project-group access, a bounded handoff, or an approved external
> sharing route before selecting a transfer command.

For the distinction between primary-group storage and cross-group project
storage, see [Users, groups, and projects](users-groups-projects.md).

## Storage decision table

| Purpose | Location or service | Rule |
|---|---|---|
| Personal configuration and small source files | home storage | Not a shared project-data area |
| Durable project input and final results | approved project storage | Shared among approved project members, including members from different primary groups |
| Material shared only within a user's primary group | approved group storage | Not a substitute for a cross-group project |
| High-I/O intermediates during a job | job-local scratch | Not backed up; copy required results back |
| Reusable software environment | approved local Conda path or immutable container | Do not run metadata-heavy environments from shared storage |
| Browser upload and download | RCC Files (**not yet released**) | Until it is released, use `scp`, `sftp`, or `rsync` to the shell host |

## Research data belongs to a project, not a home directory

Never use a user's home directory as the authoritative destination for
instrument output, shared research inputs, or durable results. The approved
project area connects data to project ownership, membership, governance,
retention, and archival decisions. A personal account cannot substitute for
that project context, particularly when a user changes role or leaves.

Home storage is also the wrong performance boundary for large or recurring
ingestion. Large datasets and many-small-file trees exhaust shared home
capacity and create filesystem metadata load. Put durable data in the project, stage
active high-I/O computation to job-local storage, and copy validated results
back to the project.

For the complete path from instrument acquisition to a retained Coscine
archive, follow [Class 17](../course/class-17-data-lifecycle.md).

Project and group directories may be mounted on demand and may not be globally
listable. Use the full path supplied for your project rather than probing for
other names.

## Stage work inside a Slurm job

The supported pattern is durable input, local computation, durable result:

```bash
#!/usr/bin/env bash
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00

set -euo pipefail
scratch="${SLURM_TMPDIR:-/local/work/$USER/slurm-job-$SLURM_JOB_ID}"
mkdir -p "$scratch/input" "$scratch/output"
cp --reflink=auto --archive "$SLURM_SUBMIT_DIR/data/input.tsv" "$scratch/input/"
srun my-analysis "$scratch/input/input.tsv" "$scratch/output/result.tsv"
cp --archive "$scratch/output/result.tsv" "$SLURM_SUBMIT_DIR/results/"
```

Use the job-local path provided by RCC when available. Never assume local files
survive job completion, reboot, maintenance, or cleanup.

## Pick a transfer method

- Use `scp`, `sftp`, or `rsync` to `{{ ssh_target_alias }}` over the approved
  SSH route. The jump host only forwards the connection; it is never the
  transfer endpoint and stores no files.
- The browser-based **RCC Files** portal is **not yet released**. Do not use
  old Files bookmarks until RCC announces the service.
- For a large tree of small files, create one archive before transfer to reduce
  metadata operations, then verify it with a checksum.
- Use an approved institutional bulk-transfer service when the SSH route is
  unsuitable.

Example with `rsync`:

```bash
rsync --archive --partial --info=progress2 \
  ./dataset/ {{ ssh_target_alias }}:/projects/<project>/incoming/dataset/
```

Example with an archive and checksum:

```bash
tar -czf dataset.tar.gz dataset/
sha256sum dataset.tar.gz > dataset.tar.gz.sha256
scp dataset.tar.gz dataset.tar.gz.sha256 \
  {{ ssh_target_alias }}:/projects/<project>/incoming/
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
