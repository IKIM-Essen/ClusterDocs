# RCC Nextflow class example

> **Service status — not yet released:** keep this example for preparation and
> review. Do not run it until RCC announces the managed `rcc-nextflow` service.

After release, on an RCC interactive node (a `shellhost`), not on an SSH
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
