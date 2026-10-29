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
9. [Plan the portable ClusterDocs core and Essen site split](09-core-site-migration-plan.md) — internal.

## User-facing principle: recommend, never gate

The planned entry screen recommends **work in your browser** for a low-friction
start but presents **VS Code**, **Positron** and **SSH / terminal** as
equally legitimate choices. Users decide by task and preference, not by an
assigned "beginner" or "expert" level. Someone comfortable with Bash may still
need Slurm/storage guidance; someone experienced with HPC may still prefer
the browser. A simple/detailed presentation option must never change
permissions or execution limits. See
[Choose how to work](01-choose-your-environment.md).

This principle belongs in site-neutral `clusterdocs`; the eventual Essen
overlay supplies accepted availability and local login instructions only.

**Multi-node batch jobs:** [Run one analysis across multiple Slurm nodes](10-multinode-batch.md) — portable future-use guide. Interactive IDEs stay single-node; multi-node CPU/MPI/distributed GPU work requires reviewed batch resources. Not published or enabled.\n\n**Editorial conventions:** Explain user outcomes before technical terms. Distinguish
"planned", "staged", and "available" explicitly. Use project names, not
canonical physical nodes, in screenshots and examples. Provide equivalent
macOS and Windows commands. Link to authoritative RCC documentation for host
fingerprints and account/2FA/device enrollment; never paste live secrets.

**Required screenshots for publication:** installer first run, host-key
verification decision, `rcc-open doctor`, Positron Remote SSH selection, VS Code
Remote-SSH selection, Slurm job status, and recovering an existing allocation.
Screenshots must use synthetic users and projects only.
## Repository boundary (future work)

The current `IKIM-Essen/ClusterDocs` is the **Essen-specific publication
source** and is not being renamed or republished by this draft PR. Portable
RCC explanations and source-neutral VS Code/Positron-on-Slurm guidance should
be extracted into a new `clusterdocs` repository with sanitized history;
site URLs, hostnames, institutional rules, host-key identities and operational
readiness should remain in a future `clusterdocs-site-essen` overlay.

See the [migration and publication plan](09-core-site-migration-plan.md).
The companion RCC draft PR #4263 records the portable core contract. New
pages remain intentionally excluded from the public navigation and site build
until the migration and user pilot have both passed acceptance.
