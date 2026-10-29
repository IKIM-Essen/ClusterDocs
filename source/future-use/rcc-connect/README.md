# ClusterDocs draft — RCC Connect and Slurm-first development

> **Draft for user pilot, 29 October 2026. Not published or accepted as a live service.**
> Link to these pages from future **myRCC → Connect your laptop** only after
> the operational acceptance checklist has been satisfied.

## Suggested ClusterDocs navigation

1. [Choose how to work on RCC](01-choose-your-environment.md) — **start here**.
2. [Connect a macOS or Windows laptop](02-install-rcc-connect.md).
3. [Develop with VS Code (Python and shell)](03-vscode-python.md).
4. [Develop with Positron (R)](04-positron-r.md).
5. [Slurm sessions and good resource use](05-slurm-and-data.md).
6. [Troubleshooting and recovering sessions](06-troubleshooting.md).
7. [Deutsche Kurzanleitung](08-kurzanleitung-de.md).
8. [Operator readiness, rollout and editorial checklist](07-operator-acceptance.md) — internal.

**Editorial conventions:** Explain user outcomes before technical terms. Distinguish
"planned", "staged", and "available" explicitly. Use project names, not
canonical physical nodes, in screenshots and examples. Provide equivalent
macOS and Windows commands. Link to authoritative RCC documentation for host
fingerprints and account/2FA/device enrollment; never paste live secrets.

**Required screenshots for publication:** installer first run, host-key
verification decision, `rcc-open doctor`, Positron Remote SSH selection, VS Code
Remote-SSH selection, Slurm job status, and recovering an existing allocation.
Screenshots must use synthetic users and projects only.