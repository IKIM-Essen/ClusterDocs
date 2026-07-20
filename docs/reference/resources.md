# Resources and live discovery

Static node counts, model names, partition names, and memory totals become stale
quickly. Discover the schedulable service at the time you submit work.

> **Related learning:** [Class 3](../course/class-03-performance.md) explains
> how to choose resources from measurements rather than static inventory claims.

## Scheduler summaries

```bash
sinfo
sinfo -o '%P %a %l %D %c %m %G'
scontrol show partition
```

These commands answer:

- which partitions are available;
- their time limits and current state;
- the CPU and memory shape visible to Slurm;
- whether GPU resources are advertised.

Use `scontrol show node <allocated-node>` only when detailed information about
a node assigned to your job is necessary. Do not probe or publish the full
physical inventory.

## Measure a completed job

```bash
sacct -j <jobid> --format=JobID,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

Compare requested resources with actual elapsed time and maximum resident
memory. Application-specific profilers remain necessary for CPU scaling, I/O,
GPU utilization, and algorithmic bottlenecks.

## Choose CPU or GPU

Use a GPU only when the application has a supported GPU implementation and the
environment contains compatible user-space libraries. `nvidia-smi` proves that
a GPU and driver are visible; it does not prove that Python, R, CUDA toolkits,
or a particular model can use them.

For CPU work, match `--cpus-per-task` to the application's actual threads. More
cores do not accelerate serial code and can lengthen queue time.

## Available software

RCC provides a managed baseline including Slurm clients, Miniforge/Conda,
Snakemake support, and Apptainer. Verify the executable you will use:

```bash
command -v conda mamba snakemake apptainer
conda --version
snakemake --version
apptainer --version
```

Project software belongs in a versioned Conda environment or reviewed container,
not in system directories. If a required runtime or architecture is absent,
document the requirement and ask RCC support rather than targeting a physical
host by name.

## Storage is also a resource

Capacity, throughput, latency, IOPS, metadata operations, and durability are
different properties. Shared storage is appropriate for durable input and final
results; job-local scratch is appropriate for high-I/O intermediates. Measure
the workflow before requesting more CPU, RAM, or GPU resources to compensate
for an I/O bottleneck.
