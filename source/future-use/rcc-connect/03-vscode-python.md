# VS Code: Python and shell on RCC (pilot draft)

> Do not treat this prototype as an approved workstation download.

Install VS Code and the official Remote - SSH extension using an approved software route. Complete SSH host-key verification before opening the IDE. Run `rcc-open doctor` locally, then `rcc-open vscode PROJECT` to request a Slurm allocation. Connect to the generated `rcc-dev-JOBID` alias and open only a narrow code subdirectory under `/projects/PROJECT`.

Terminals, tests, notebooks and extensions on a worker consume allocated resources. Use batch jobs for long unattended work. Do not run sustained computation on the shellhost, and exclude large datasets and environments from workspace file watching and search.

To reconnect, run `rcc-open list` then `rcc-open attach vscode PROJECT JOBID`. Failed project verification is a stop condition; do not submit again to recover a lost receipt. When finished save durable results and run `rcc-open stop JOBID`.
