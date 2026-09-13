# Jump host, shell host, and compute worker

RCC uses three different roles so that the Internet-facing doorway, the place
where users prepare work, and the machines that perform computation do not
have to be the same system.

## The short explanation

| Role | Think of it as | What you do there |
|---|---|---|
| Jump host | Guarded doorway | Nothing interactively; SSH forwards through it. |
| Shell host | Your RCC desk and SSH file endpoint | Edit small files, use Git, transfer authorized files, submit jobs, inspect logs, and control workflows. |
| Compute worker | Scheduled laboratory bench | Run analysis inside a Slurm allocation. |

Your SSH configuration normally joins the first two steps. You can run:

```bash
ssh -J login.ikim.uk-essen.de shellhost
```

or configure `ProxyJump login.ikim.uk-essen.de` for `shellhost` and use simply:

```bash
ssh shellhost
```

In both cases your terminal opens on the shell host. You do not open a terminal
on the jump host and then SSH again.

```text
workstation
  -> login.ikim.uk-essen.de: verify and forward
  -> shellhost: shell and authorized filesystem access
  -> Slurm: allocate a worker
  -> worker: calculate
```

## Why the jump host refuses a shell

The jump host is deliberately forwarding-only for ordinary users. It reduces
the exposed surface and prevents the public entry point from becoming a place
where data, tools, or long-lived processes accumulate. A refused interactive
shell on the gateway is therefore expected behavior, not an account failure.

The same rule applies to file transfer: the jump host is **not** the SFTP, SCP,
or rsync endpoint and should not expose `/homes`, `/groups`, or `/projects`.
Those filesystems are reached on the downstream shell host.

For example, copying a file from group storage uses:

```bash
scp -J login.ikim.uk-essen.de shellhost:/groups/blubb/demo.test1 .
```

The source is `shellhost:/groups/...`; `login.ikim.uk-essen.de` only supplies
the SSH transport path.

Test the configured destination, not the gateway:

```bash
ssh -J login.ikim.uk-essen.de shellhost
```

Do not use physical backend names such as `login1` or `login2`. Operations can
replace backends while the approved service alias `login.ikim.uk-essen.de`
remains stable.

## What belongs on the shell host

Appropriate shell-host work is light control-plane activity:

- editing a script or workflow definition;
- using Git and inspecting small text logs;
- transferring authorized files with `scp`, `sftp`, or `rsync`;
- running a Snakemake dry run;
- starting the managed Snakemake or `rcc-nextflow` controller;
- using `sbatch`, `squeue`, `sacct`, and `scancel`; and
- keeping a workflow controller alive in `tmux` when documented.

The shell host is not a free compute node. Do not run sustained analysis,
large-memory work, GPU work, or high-I/O processing in its terminal.

## What belongs on a compute worker

Slurm workers perform the scientific tasks. A job requests bounded CPU,
memory, time, and optional GPU resources. Slurm chooses the worker and starts
the task there. Temporary high-I/O files may use the job's `$TMPDIR` or
approved `/local` path; declared results must return to project storage before
the allocation ends.

Snakemake and Nextflow preserve the same separation:

| Component | Runs where |
|---|---|
| Workflow definition and durable state | Project storage |
| Snakemake or Nextflow controller | Shell host or documented interactive allocation |
| Each scientific rule or process | Slurm worker |
| Temporary task files | Worker-local scratch |
| Validated outputs and provenance | Project storage |

## A common misconception

“I connected through the login service, so my command is running on a compute
node” is incorrect. SSH provides access; Slurm provides compute. Likewise,
“the login service is in my SCP command, so my files live there” is incorrect:
with `-J`, the login service is only the jump path and the `shellhost:` operand is
the actual remote endpoint.

Unless a documented interactive allocation moved your shell to an assigned
worker, submit the program with the supported Slurm or workflow command.

Continue with [Class 1](../course/class-01-safe-access.md) for setup or
[Class 5](../course/class-05-slurm.md) for job submission.
