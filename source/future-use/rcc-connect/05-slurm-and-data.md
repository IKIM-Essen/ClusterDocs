# Slurm and data safety (pilot draft)

RCC Connect uses `rcc-dev-session` on the shellhost. The current source helper defaults to 4 CPUs, 16 GiB and 8 hours for CPU development; these are not live capacity guarantees or autoSRE recommendations. Slurm selects the eligible worker and enforces resource limits.

Use `/projects/PROJECT` for durable authorized project data, `/homes/USER` for small personal settings, `/groups/GROUP` for approved collaboration, and allocation-local `$TMPDIR` for temporary high-I/O work. Scratch can disappear after the allocation ends.

Use an interactive Slurm allocation for R/Python kernels and debugging; use normal batch partitions for substantial unattended computation. Do not search or watch the entire `/projects`, `/groups` or `/homes` trees. Limit `rg` and file indexers to small code directories; IDE settings alone are not a filesystem security boundary.

Cancel attended development allocations with `rcc-open stop JOBID` when finished.
