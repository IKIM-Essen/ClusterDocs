# RCC Nextflow class example

> **Service status — ready now:** run this bounded example through the managed
> `rcc-nextflow` launcher on a shellhost or allocation-backed interactive node.

On an RCC shellhost or allocation-backed interactive node, not on an SSH
gateway or a compute worker:

```bash
export RCC_PROJECT_ROOT=/projects/MY_PROJECT
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" run main.nf -c nextflow.config
rcc-nextflow --project-root "$RCC_PROJECT_ROOT" run main.nf -c nextflow.config -resume
```

The example is intentionally small and uses synthetic text only.
