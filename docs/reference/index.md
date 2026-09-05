# RCC day-to-day reference

The course teaches RCC workflows in sequence. These reference pages collect
commands, decisions, architecture explanations, and practical details that you
may need later without repeating an entire class.

Use a class when learning a workflow for the first time. Use its reference
companion when you already understand the safety boundary and need a command,
decision table, diagnostic sequence, or explanation of why RCC is structured a
particular way.

## Find the right guide

| Task | Reference |
|---|---|
| Understand individual accounts, primary groups, external collaborators, and project membership | [Users, groups, and projects](users-groups-projects.md) |
| Import optional shell, prompt, Conda, or Shiny account defaults | [Account starter setups](account-starter-setups.md) |
| Create an SSH key, configure a client, connect with VS Code, or mount a small remote folder | [Account access, SSH, and VS Code](access-ssh-vscode.md) |
| Choose durable or temporary storage and transfer project data | [Storage and transfer](storage-transfer.md) |
| Share data within a project, across RCC groups, or outside RCC | [How to share data safely](data-sharing.md) |
| Submit, inspect, connect to, and cancel jobs | [Slurm commands](slurm.md) |
| Understand shared, owner, borrowed, and interactive compute capacity | [How shared compute works](how-shared-compute-works.md) |
| Understand why scientific work uses Slurm while long-lived services use the RCC service plane instead of putting everything onto Kubernetes | [Why RCC does not run everything on Kubernetes](../concepts/why-not-kubernetes-everywhere.md) |
| See the complete RCC platform from instruments through analysis, services, agents, and preservation | [What RCC can do](../concepts/what-rcc-can-do.md) |
| Use Conda, Snakemake, or Apptainer | [Software workflows](software-workflows.md) |
| Diagnose permissions, file limits, GPU processes, searches, and failed jobs | [Troubleshooting](troubleshooting.md) |
| Discover available CPUs, memory, GPUs, partitions, and supported software | [Resources and discovery](resources.md) |
| Plan machine learning, AI, validation, inference, or distributed data processing | [AI and data science](ai-data-science.md) |

## Important boundary

Examples use public aliases and replaceable values. The site deliberately does
not publish physical host inventories, internal addresses, firewall rules, or
administrator commands. Use the current institutional RCC instructions and
support channel for operational values.

The architecture references explain responsibility boundaries rather than
publishing sensitive service placement. Ordinary researchers should not need to
know which long-lived service scheduler is behind a button; advanced users
should be able to understand why scientific-compute authority remains with
Slurm and why RCC avoids adding another scheduler without a concrete need.
