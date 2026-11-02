# VS Code for Python and shell on RCC (Essen pilot draft)

> **Not released.** This describes the intended allocation-backed workflow,
> not a currently supported one-click download or a promise of live capacity.
> The portable concepts are intended for future `clusterdocs` core; Essen
> connection endpoints, trust and release readiness remain in the site overlay.

## Where the VS Code server runs

| Component | Location | Responsibility |
| --- | --- | --- |
| VS Code Desktop | Your Mac or Windows laptop | Graphical editor, local Git/UI and trusted SSH client |
| SSH gateway and shellhost | Approved RCC site entrypoints | SSH routing, lightweight source editing, Slurm submit and discovery — **not scientific computation** |
| **VS Code Server**, remote extensions, terminals, Python interpreter, debugger, Jupyter kernels | **The Slurm-selected interactive worker** | Scientific development inside the user's active allocation |
| Durable project files | Approved RCC project storage | Source, environments-as-code, inputs and outputs |
| High-I/O temporary data | Allocation-local `$TMPDIR` | Disposable scratch, never the sole copy of data |

VS Code's Remote-SSH extension installs or starts its matching per-user remote
server on the SSH destination. We must connect it to the **allocated worker**,
not start the server on the shellhost for substantial Python/Jupyter work. This
is directly analogous to Positron Desktop plus its remote backend.

The intended safety boundary is Slurm job ownership and fail-closed
`pam_slurm_adopt`: the VS Code Server and **all** worker-side children must be
contained in that job's cgroup. Terminating or timing out the allocation must
terminate remote terminals, extension hosts, Python processes and notebooks.
This requires an observed operator canary; editor preferences cannot enforce it.

## The intended beginner workflow

1. Install the approved VS Code desktop application and the official
   **Remote - SSH** extension on your laptop through your institution's
   software channel. Do not disable endpoint security.
2. Verify RCC identity, SSH host keys and your registered authentication
   method independently. Run `rcc-open doctor` if the pilot tool is available.
3. Choose an approved RCC project and request a bounded Slurm development
   session using the pilot command:

   ```bash
   rcc-open vscode PROJECT
   ```

4. The tool records the Slurm job ID, waits for a running allocation, verifies
   your ownership/project and worker host identity, and creates an SSH target
   named `rcc-dev-JOBID`. **This automatic flow is a proposed pilot,
   not production functionality.**
5. Connect VS Code Remote-SSH to the generated target, then open a small
   source directory such as `/projects/PROJECT/src`. Confirm the terminal
   actually reports the allocated worker, not the shellhost.
6. Use a small bounded test for interactive debugging. Submit large or
   unattended Python work through Slurm batch/Nextflow/Snakemake instead.
7. Save results to durable project storage, then deliberately end the Slurm
   allocation with `rcc-open stop JOBID`. Merely closing VS Code does not
   guarantee a Slurm job has been cancelled.

## Five-minute practice exercise

For the approved pilot, try the [five-number VS Code exercise](13-first-session-smoke-test.md).
The operator stages a tiny Python script in your project; you open it in the
remote editor, run it, see mean **6.0**, inspect a generated CSV, reconnect
to the same Slurm job and explicitly stop. No extra packages or research data.

## Recover without creating a duplicate job

If the editor disconnects, do not automatically submit again. Inspect:

```bash
rcc-open list
rcc-open attach vscode PROJECT JOBID
```

A project mismatch, missing `WorkDir`, unverified worker host key, expired
allocation, or ambiguous Slurm state **must stop attachment**. Contact the RCC
support route instead of accepting a changed SSH key or guessing a worker.

## Reduce unnecessary storage and shellhost load

- Open only the code subtree. Avoid using `/projects`, `/groups` or
  `/homes` as a VS Code workspace.
- Exclude datasets, environments, workflows' caches and build outputs from
  recursive search and file watches, while allowing authorized source files.
- An IDE search exclusion is a performance recommendation, **not** a
  filesystem authorization boundary. An unbounded `rg` or Python traversal
  can still overload shared storage; use a bounded project-scoped search.
- Keep remote VS Code extension downloads and runtime installations under
  site-reviewed policy. The worker may have no general internet access;
  staging/pinning the matching VS Code Server is an operator prerequisite.
- Avoid local-only state on the allocated worker. A job can end because of
  timeout, cancellation, maintenance or node failure.

## Compatibility and support

A compatible VS Code Server, supported OS/architecture, strictly verified
SSH worker identities, SSH/PAM adoption and dynamic target resolution must all
be tested on the accepted site. A code editor being installed on the laptop
is **not** evidence that RCC's remote workflow is released.

See [Slurm and data](05-slurm-and-data.md),
[recovery](06-troubleshooting.md), and the
[ClusterDocs core/site migration plan](09-core-site-migration-plan.md).
