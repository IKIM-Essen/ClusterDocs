# Choose your RCC development interface (pilot draft)

> Not released. No claim of currently available desktop allocations.

| Task | Interface | Execution |
| --- | --- | --- |
| R, plots, statistics | Positron desktop | Slurm development allocation |
| Python, shell, debugging | VS Code Remote SSH | Slurm development allocation |
| Browser-first notebooks/workflows | Future RCC Analysis | Slurm allocation after acceptance |
| Long unattended analysis | Batch / Nextflow / Snakemake | Slurm batch partitions |

Shellhosts are for login, Git, editing and submission, not sustained computing or broad filesystem scanning. Open only small source subtrees in IDEs. Slurm selects the worker; you do not select a physical node.

Next: [Laptop setup](02-install-rcc-connect.md), [VS Code](03-vscode-python.md), or [Positron](04-positron-r.md).
