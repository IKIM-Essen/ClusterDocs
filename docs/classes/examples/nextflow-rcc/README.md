# RCC Nextflow class example

> **Service status — not yet released:** keep this example for preparation and
> review. Do not run it until RCC announces the managed `rcc-nextflow` service.

After release, on the approved submission host:

```bash
export RCC_PROJECT_ROOT=/projects/MY_PROJECT
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" run main.nf -c nextflow.config
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" run main.nf -c nextflow.config -resume
```

The example is intentionally small and uses synthetic text only.
