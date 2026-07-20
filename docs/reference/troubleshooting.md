# Troubleshooting

Start with the smallest read-only check that can distinguish likely causes.
Do not create retry loops, broad scans, or synthetic load while diagnosing a
shared service.

> **Related learning:** Start with the relevant class gate. A failed gate is a
> smaller and safer diagnostic target than a full research workflow.

## SSH does not connect

1. Run the local readiness gate without `--live`.
2. Confirm the public alias and fingerprint through a trusted channel.
3. Make one bounded verbose attempt.
4. Redact sensitive values before sharing the output with support.

Never disable host-key checking or borrow another person's key.

## A Slurm job is pending

```bash
squeue -j <jobid> -o '%.18i %.2t %.10M %.6D %R'
scontrol show job <jobid>
```

The reason may be ordinary capacity, a dependency, an unavailable resource, or
an impossible request. Reduce resources only when the program can genuinely run
with less; do not repeatedly resubmit.

## A job failed

```bash
sacct -j <jobid> --format=JobID,State,Elapsed,ReqMem,MaxRSS,ExitCode
tail -n 100 logs/<job-name>-<jobid>.out
```

- `OUT_OF_MEMORY`: measure peak memory, then request an evidence-based amount or
  process the data in chunks.
- `TIMEOUT`: checkpoint or request a realistic upper bound.
- non-zero exit code: inspect the application log before changing resources.
- missing file after staging: use `SLURM_SUBMIT_DIR` and absolute paths, and copy
  final outputs back before exit.

## Too many open files

Inspect the current soft and hard limits:

```bash
ulimit -Sn
ulimit -Hn
```

If the workflow legitimately needs more descriptors, raise only the soft limit
for that job, without exceeding the hard limit:

```bash
ulimit -Sn 4096
srun python analysis.py
```

First check whether the program is leaking handles or opening thousands of
files unnecessarily.

## Shared-file permissions

Inspect ownership and every directory component:

```bash
namei -l /projects/<project>/path/to/file
getfacl /projects/<project>/path/to/file
```

Do not recursively grant access to everyone. For a small, reviewed project
tree, the owner can apply group-based permissions:

```bash
chgrp -R <project-group> path
chmod -R g+rwX,o-rwx path
find path -type d -exec chmod g+s {} +
```

For a large tree or unclear ownership, stop and ask support; recursive metadata
changes can be expensive and can expose data.

## Conda environment creation is slow

```bash
printf '%s\n' "$CONDA_ENVS_PATH" "$CONDA_PKGS_DIRS"
```

Both should use the approved node-local RCC paths. Build environments inside a
worker allocation, not on the login host or shared storage.

## VS Code search consumes resources

Remote full-text search can traverse datasets, environments, package trees, and
generated results. Add them to `.gitignore` or `.ignore`, or configure
`search.exclude`. Open the smallest useful project directory rather than a home,
group, or project root.

## GPU memory remains occupied

Inside your allocation:

```bash
nvidia-smi
fuser -v /dev/nvidia<N>
```

Save work and terminate your own application cleanly first. If a process you
own remains, use `kill <pid>`, wait, and recheck. Use `kill -KILL` only as a last
resort on your own process. If memory remains without a process you can see,
record the job ID and GPU index and contact RCC support; do not attempt
administrator commands or reset the device.

## Browser cannot reach Jupyter or Shiny

- Confirm the Slurm job is running.
- Use the worker and port printed by that job, not a value from an older run.
- Confirm the service listens on `127.0.0.1`, not `0.0.0.0`.
- Keep the SSH tunnel terminal open.
- Stop the job with `scancel <jobid>` when finished.
