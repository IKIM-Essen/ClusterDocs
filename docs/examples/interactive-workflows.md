# Interactive Python, R, Jupyter and Shiny examples

Use these copy-ready examples to run bounded Python, R, Jupyter, and Shiny
workflows through Slurm. Each example includes its environment and uses
synthetic data so it can be explored safely before adapting it to a project.

## Included examples

| Directory | Purpose |
|---|---|
| `examples/interactive-workflows/python` | Python batch analysis with a pinned Conda environment. |
| `examples/interactive-workflows/r` | R batch analysis with a pinned Conda environment. |
| `examples/interactive-workflows/jupyter` | JupyterLab inside a Slurm allocation, bound to loopback. |
| `examples/interactive-workflows/shiny` | Shiny development session inside a Slurm allocation, bound to loopback. |
| `examples/interactive-workflows/notebooks` | Small synthetic Python and R notebooks for classroom use. |

## Security boundaries

- Interactive servers bind only to `127.0.0.1`.
- Users connect through a local SSH tunnel.
- Tokens remain enabled.
- Examples use synthetic data only.
- No example scans hosts, enumerates infrastructure, or exposes internal addresses.
- Production web hosting uses the governed vhost process, not a tunnelled Slurm job.

## Good cluster patterns

- Use notebooks for inspection and figures.
- Use Slurm scripts for full-scale computation.
- Keep Conda environments and caches on node-local storage when computing.
- Copy final outputs back to the project area.
- Stop interactive jobs when finished.
