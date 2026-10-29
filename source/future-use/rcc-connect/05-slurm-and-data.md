# Slurm and data safety (pilot draft)

RCC Connect uses `rcc-dev-session` on the shellhost. The current source helper defaults to 4 CPUs, 16 GiB and 8 hours for CPU development; these are not live capacity guarantees or autoSRE recommendations. Slurm selects the eligible worker and enforces resource limits.

Use `/projects/PROJECT` for durable authorized project data, `/homes/USER` for small personal settings, `/groups/GROUP` for approved collaboration, and allocation-local `$TMPDIR` for temporary high-I/O work. Scratch can disappear after the allocation ends.

Use an interactive Slurm allocation for R/Python kernels and debugging; use normal batch partitions for substantial unattended computation. Do not search or watch the entire `/projects`, `/groups` or `/homes` trees. Limit `rg` and file indexers to small code directories; IDE settings alone are not a filesystem security boundary.

Cancel attended development allocations with `rcc-open stop JOBID` when finished.

## Distributed and multi-node batch work

A multi-node job is a Slurm **batch** allocation with several compute workers,
not a VS Code or Positron remote session spread across hosts. Specify nodes,
tasks per node, CPUs per task, per-node memory and maximum runtime, and use
MPI/PMIx only when accepted by the site. See
[Multi-node batch workflows](10-multinode-batch.md). For independent files or
samples, prefer a job array or workflow when appropriate. The UI choice does
not restrict whether a person may request authorized multi-node resources.
