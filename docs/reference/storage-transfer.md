# Storage and transfer

Choose storage by lifecycle and access pattern, not only by free capacity.

> **Service status:** RCC workers and project Samba shares are **ready now**.
> RCC-to-Coscine archive transfer is **not yet released**; references to it are
> lifecycle planning, not an operational transfer command.

> **Related learning:** [Class 1](../course/class-01-safe-access.md) introduces
> the files portal, [Class 3](../course/class-03-performance.md) explains local
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
| Browser upload and download | RCC files portal | Confirm project and destination before transfer |

## Research data belongs to a project, not a home directory

Never use a user's home directory as the authoritative destination for
instrument output, shared research inputs, or durable results. The approved
project area connects data to project ownership, membership, governance,
retention, and archival decisions. A personal account cannot substitute for
that project context, particularly when a user changes role or leaves.

Home storage is also the wrong performance boundary for large or recurring
ingestion. Large datasets and many-small-file trees can consume personal quota
and create filesystem metadata load. Put durable data in the project, stage
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

- Use the **RCC files portal** for ordinary browser-based project transfers.
- Use `scp`, `sftp`, or `rsync` to a **shell host**, routed through
  `login.ikim.uk-essen.de` with SSH `ProxyJump`, for scripted or resumable
  transfers.
- For a large tree of small files, create one archive before transfer to reduce
  metadata operations, then verify it with a checksum.
- Use an approved institutional bulk-transfer service when the files portal or
  SSH route is unsuitable.

The important endpoint distinction is:

```text
workstation -> login.ikim.uk-essen.de -> shellhost -> /homes, /groups, /projects
              forwarding only          transfer endpoint
```

Do **not** use `login.ikim.uk-essen.de` as the source or destination of a data
copy. The login tier is the guarded transport boundary; research filesystems are
available on the shell-host tier.

The explicit `scp` form is:

```bash
scp -J login.ikim.uk-essen.de shellhost:/groups/blubb/demo.test1 .
```

For SFTP:

```bash
sftp -J login.ikim.uk-essen.de shellhost
```

For `rsync`:

```bash
rsync --archive --partial --info=progress2 \
  -e 'ssh -J login.ikim.uk-essen.de' \
  ./dataset/ shellhost:/projects/<project>/incoming/dataset/
```

If your approved SSH configuration already gives `shellhost` the setting
`ProxyJump login.ikim.uk-essen.de`, the shorter forms such as
`scp file shellhost:/projects/<project>/` are equivalent. The explicit form is
shown here first so that it remains clear which machine is the jump host and
which machine actually accesses the data.

Example with an archive and checksum:

```bash
tar -czf dataset.tar.gz dataset/
sha256sum dataset.tar.gz > dataset.tar.gz.sha256
scp -J login.ikim.uk-essen.de dataset.tar.gz dataset.tar.gz.sha256 \
  shellhost:/projects/<project>/incoming/
```

On RCC, verify before extracting:

```bash
ssh -J login.ikim.uk-essen.de shellhost
cd /projects/<project>/incoming
sha256sum -c dataset.tar.gz.sha256
tar -tzf dataset.tar.gz | sed -n '1,20p'
```

Inspect archive paths before extraction. Reject archives containing absolute
paths or unexpected `..` components.

## Unsupported transfer patterns

Do not transfer data directly to `login.ikim.uk-essen.de`, `login1`, or
`login2`. Ordinary user sessions on those hosts are forwarding-only; they are
not RCC storage endpoints and should not expose `/homes`, `/groups`, or
`/projects`.

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
