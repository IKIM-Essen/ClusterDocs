# Your first RCC session: 5 numbers, 1 result (pilot walkthrough)

> **Pilot exercise, not yet a generally available RCC service.**
> Use only after your site operator has accepted RCC Connect, the relevant
> IDE backend, Slurm worker and trusted SSH configuration for your device.
> The commands below do not install or authorize those prerequisites.

This exercise is designed for scientists who just want to check that the
computer is ready. **No research data, extra packages or cluster expertise
are needed.** Both editors use the same five made-up measurements:
2, 4, 6, 8, 10. The expected mean is **6.0**.

## Before you begin

Ask your pilot operator to stage two tiny example source files from the
reviewed RCC core revision under a synthetic or approved exercise project:

    /projects/PROJECT/rcc-ide-smoke/vscode-python.py
    /projects/PROJECT/rcc-ide-smoke/positron-r.R

The files are maintained in the RCC source at
examples/ide-smoke/ (same project source across institutions). Do not
download source scripts from an untrusted site or use private research files.
You need the approved laptop editor, registered RCC account/SSH device,
independently verified SSH host keys and permission to use PROJECT.

Pick whichever editor you want; **you do not have to do both**.

## Option A: VS Code — write and inspect a CSV

1. On your laptop use the **approved pilot** RCC Connect command:

       rcc-open vscode PROJECT

   If the command is not installed or the site does not accept this service,
   stop and ask the operator for the site-approved connection method.
   Do not create your own SSH host entry or accept an unknown host key.

2. Write down the **JOBID** shown by RCC. In VS Code Desktop select
   Remote-SSH: Connect to Host and choose rcc-dev-JOBID.
3. Open the small folder /projects/PROJECT/rcc-ide-smoke. In VS Code,
   open a **remote** terminal and run:

       python3 vscode-python.py

4. Look for these three facts in the terminal:

       Slurm job: <your job ID>
       Synthetic mean: 6.0
       Saved CSV: .../rcc-ide-smoke-output/python-summary.csv

   Open the CSV in VS Code. It contains five synthetic measurements plus
   one row showing the mean.

5. Close the VS Code window, then reconnect to the **same** job:

       rcc-open attach vscode PROJECT JOBID

   Open the CSV again. Do not request a second allocation to reconnect.

## Option B: Positron — make a small R plot

1. On your laptop use the approved pilot command:

       rcc-open positron PROJECT

2. Record its **JOBID**. In Positron Desktop use Remote SSH: Show Remote
   Menu → Connect to Host and select rcc-dev-JOBID. Use an approved remote
   R interpreter (not R on your laptop).
3. Open /projects/PROJECT/rcc-ide-smoke. In the **remote R console** run:

       source("positron-r.R")

4. Check the console for the Slurm job ID and Synthetic mean: 6.0.
   Look for an R plot and the saved PNG:

       rcc-ide-smoke-output/positron-plot.png

   A CSV is also saved as positron-summary.csv. You can open and view both.

5. Close Positron, reconnect with:

       rcc-open attach positron PROJECT JOBID

   Reopen the saved plot. This should **not** create another Slurm job.

## Finish and check that your work is kept

For either editor, explicitly end the session:

    rcc-open stop JOBID

Your synthetic result files should remain under the project exercise folder.
The Slurm allocation should no longer be running. If you are disconnected or
a command gives an uncertain result, check rcc-open list and ask the pilot
operator to reconcile it; do not automatically resubmit.

## Quick result checklist

| You should be able to... | Expected result |
| --- | --- |
| Connect through the selected IDE | A remote window on the allocation's worker |
| Run the example | Mean 6.0, and your **own** Slurm job ID |
| See a result | Python CSV or R PNG/CSV |
| Disconnect and reconnect | Same JOBID, same authorized project, no duplicate job |
| End the allocation | Job stopped; synthetic project output remains |
| Work without expert knowledge | No manual node selection, special package setup or private data |

**If something fails:** write down the last command, job ID and error text
(no passwords, private keys, tokens or real research data). The failure is
useful pilot feedback. Do not switch to running R/Python on the shellhost.

**Operator-only release criteria:** This walk-through establishes a usable
first experience, not full backend security. Before publication the operator
must separately verify Slurm cgroups for the editor backend and all children,
cleanup after cancellation, approved Positron version, client OS compatibility,
and an authenticated worker host-key registry.

The exercise source is in RCC:
https://github.com/IKIM-Essen/rcc/tree/feature/rcc-connect-desktop-pilot-20261029/examples/ide-smoke

See also [VS Code details](03-vscode-python.md),
[Positron details](04-positron-r.md),
[session recovery](06-troubleshooting.md) and
[operator acceptance](07-operator-acceptance.md).
