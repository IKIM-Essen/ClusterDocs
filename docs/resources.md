# Resources

## Available hardware

The cluster has two sets of servers: 120 nodes for CPU-bound tasks and 10+ nodes for GPU-bound tasks. At this moment, not all of these nodes are available for general computation tasks. However, more will be added in future. The following hardware is installed in the servers:

- CPU nodes (`c1` - `c120`): Each with 192GB RAM, 2 CPU Intel, 1 SSD for system and 1 SSD for data (2TB).
- GPU nodes (`g1-1` - `g1-10`): Each with 6 NVIDIA RTX 6000 GPUs, 1024GB RAM, 2 CPU AMD, 1 SSD for system (1TB) and 2 NVMe for data (12TB configured as RAID-0).
<!-- - GPU node (`g2-1`): One node with 8 NVIDIA A100 80G GPUs, 2TB RAM, 2 AMD EPYC CPUs (256 logical processors), 1 SSD for system (1TB) and 2 NVMe for data (30TB configured as RAID-0). -->

A subset of these nodes are deployed as a Slurm cluster. Unless instructed otherwise, you should interact with worker nodes using Slurm.

## Available software

Short answer: Everything under the sun. You can install software yourself using either a [package manager](conda.pm) or build / run a
[container](apptainer.md). Containers can even be used e.g. to run a different operating system should you need to.
To avoid resource contention we recommend using our [resource manager](slurm.md).

Example: To install [scikit-learn](https://scikit-learn.org/stable/install.html) all you need to do is

```sh
conda create -n sklearn-env -c conda-forge scikit-learn
conda activate sklearn-env
```

Conda and its siblings (anaconda and mamba) provide access to [thousands of software packages](https://conda-forge.org/feedstock-outputs/), you can
set up your required software by yourself and even have multiple environments.
The [conda intro](conda.md) provides a good starting point.
