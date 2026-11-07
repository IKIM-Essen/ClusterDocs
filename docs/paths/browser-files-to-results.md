# From Files to Analysis, Notebook and results

> **ROLLOUT DRAFT — NOT YET LIVE.** These steps describe the intended browser-first RCC experience. The current public documentation continues to describe SSH/VS Code as the available route until acceptance.

## One project, one place to work

The **left sidebar** keeps the selected project visible when moving between My RCC, Files, Analysis, Notebooks and Jobs & results.

### 1. Choose a project

Sign in and select an authorized project. Check the project name before uploads or launching computation.

### 2. Open Files

Browse or upload a small, non-sensitive example file. Its path should refer to the same authorized project namespace used by compute workers. Avoid unnecessary duplicate copies of large datasets.

### 3. Choose the right way to work

- **Notebook**: explore, visualize and prototype interactively; launch a managed Slurm session and reconnect later.
- **Workflow**: run an approved repeatable or long-running analysis with durable input and output.
- **Shell/VS Code**: optional advanced access for custom development, not a prerequisite for browser tasks.

### 4. Monitor progress

Use **Jobs & results** to distinguish queued, running, completed, failed and cancelled work. A queued job does not require keeping a terminal open.

### 5. Retrieve and check results

Return to Files for durable results. Validate the scientific outputs and quality-control reports; a technically completed job does not mean the analysis is scientifically valid.

## Recover without starting again

| Status | Helpful next action |
|---|---|
| Not authorized | Check membership; do not use a colleague's credentials |
| Files unavailable | Keep your data where it is and contact RCC support |
| Job queued | Wait or review the resource profile |
| Job failed | Read the error and job logs before safe retry |
| Notebook disconnected | Reconnect to the existing session instead of creating another |
| Project missing | Verify current account and request project access |

## Friday Computing Club demonstration

Use a disposable demonstration project with non-sensitive sample data: select a project → open Files → choose a prepared analysis → inspect job state → open the result → demonstrate notebook reconnection. Allow participants to repeat it themselves.

## Further reading

- [Existing-user invitation and account activation](../getting-started/existing-user-invitation.md)
- [Current SSH and VS Code instructions](../reference/access-ssh-vscode.md)
- [RCC Analysis overview](../analysis/rcc-analysis.md)

**Note for maintainers:** When the release UI is frozen, add validated screenshots and exact routes; until then do not guess the deployed page names or claim services are available.
