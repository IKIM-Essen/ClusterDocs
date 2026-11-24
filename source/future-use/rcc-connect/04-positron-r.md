# Positron for R on RCC — pilot draft

> **Not released.** Remote Positron/R sessions require a reviewed Slurm
> allocation, an accepted server build and an authenticated site SSH trust
> registry. Source code and settings files alone do not establish availability.

## What runs where?

- **On your laptop:** the Positron desktop window, plots interface and
  native OpenSSH client.
- **On the Slurm worker:** the matching Positron remote extension host,
  extensions, R/Python interpreters, kernels and terminals.
- **On the shellhost:** lightweight SSH routing and Slurm submission. It
  is not where substantial R computation belongs.
- **In your RCC project:** source, durable inputs and results; temporary
  high-I/O files belong in allocation-local scratch.

This is equivalent in principle to the VS Code Remote-SSH development path,
but Positron has its own backend build and R runtime acceptance requirements.

## Proposed connection experience

1. Install the reviewed Positron Desktop build using the approved university
   software route. The local `remoteSSH.transport` must be `native` for
   RCC's OpenSSH jump configuration.
2. Complete authorized project membership, device registration and the
   independently verified RCC SSH host-key setup. Native OpenSSH cannot
   display interactive password/passphrase/host-key confirmation prompts.
3. The proposed `rcc-open positron PROJECT` first requests a project-bound
   Slurm development allocation. After recording its job ID, the client
   checks the selected worker and exact desktop/backend qualification before
   suggesting the `rcc-dev-JOBID` SSH target.
4. In Positron, connect to that alias and open a small source directory under
   `/projects/PROJECT`. Select the approved R interpreter, test a small
   synthetic dataset, plot, and inspect session status.
5. Save reusable analysis and output in the project. Close the IDE as you
   prefer, but explicitly release the Slurm allocation when finished:
   `rcc-open stop JOBID`.

**Current source pilot limitation:** on both macOS and Windows, the launcher
requires a Positron CLI returning a parseable exact version. This may need
platform-specific integration before it can be presented as a one-click
installer. The accepted worker/backend and signed site host-key registry are
not available as general RCC services.

## Five-minute practice exercise

Try the [five-number Positron R exercise](13-first-session-smoke-test.md)
when the pilot backend is approved. Use the remote R console to run one
synthetic script; you should get mean **6.0**, an R plot and a saved PNG.
Then reconnect to the same Slurm job and stop it explicitly. It uses
base R only and never needs real research data.

## What RCC checks before allowing the pilot

The worker's read-only preflight refuses a mismatched job or project,
unrecognized R runtime, unqualified OS/architecture, and unmatched
Positron desktop/backend versions. Its operator-owned qualification record
must correspond to the exact Positron backend archive and reviewed site
acceptance. No automatic external download or changed SSH key is accepted as
a workaround.

This preflight **does not prove full process containment**. Operators still
need a real Positron/R session and evidence that backend, R, extensions and
terminals remain inside the Slurm job and all end on timeout/cancellation.

If the connection fails, the job might still exist. Run `rcc-open list`
before any new submission. Contact site support for missing SSH keys or
version mismatch. Do not remove your SSH trust records or run a copy of R on
the shellhost to get around the blocker.

## Protect performance

Open only the source directory needed for your project. Avoid indexing
entire projects, datasets, `renv/library` or shared storage roots. RCC
should eventually supply the recommended Positron settings and safe worker
environment automatically; workstation settings are convenience measures,
not resource enforcement.

For the planned release see
[implementation waves](12-implementation-waves.md),
[operator acceptance](07-operator-acceptance.md) and
[session recovery](06-troubleshooting.md).

Upstream reference: https://positron.posit.co/remote-ssh
