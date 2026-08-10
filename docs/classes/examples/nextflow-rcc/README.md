# RCC Nextflow class example

> **Service status — ready now:** run this bounded example through the managed
> `rcc-nextflow` launcher on a shellhost or allocation-backed interactive node.

On an RCC shellhost or allocation-backed interactive node, not on an SSH
gateway or a compute worker:

```bash
export RCC_PROJECT_ROOT=/projects/MY_PROJECT
mkdir -p "$RCC_PROJECT_ROOT/analyses/nextflow-class"
cd "$RCC_PROJECT_ROOT/analyses/nextflow-class"

# Copy main.nf and run-rcc-nextflow.sh here, then:
./run-rcc-nextflow.sh \
  run main.nf \
  -with-trace trace.tsv \
  -with-report report.html \
  -with-timeline timeline.html

./run-rcc-nextflow.sh run main.nf -resume
```

This directory is intentionally small and uses synthetic text only.
`run-rcc-nextflow.sh` uses `flock` to refuse a second controller in the same
analysis directory and writes each Nextflow controller log below `logs/`.

`resources.config.example` demonstrates the intended boundary for user tuning:
adjust individual task resources after measuring a pilot, but do not replace the
RCC Slurm, scheduler, work-directory, or Apptainer configuration.
