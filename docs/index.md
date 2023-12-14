# IKIM Scientific Computing

This website contains documentation for the scientific computing infrastructure at the Institute for AI in Medicine (IKIM) in Essen. The documentation is geared towards researchers and students that aim to run scientific experiments on the cluster. See [Getting Started](getting-started.md) for general instructions.

The image below shows members of IKIM assembling the cluster
![Cluster](./assets/cluster_barnraiser.png)

## About

The sources of this documentation can be found on [GitHub](https://github.com/IKIM-Essen/ClusterDocs) and we encourage contribution.

## Intro

We believe it is important to know a thing or two about the underlying computer and network infrastructure to be effective. We note this will also limit your frustration level. We do not provide extensive documentation, but rather jumping off points and short best practice info on your setup and your procedures.

By configuring your environment correctly you can make your job easier. Start off by learning the basics of the [Slurm](slurm.md) cluster. For info on getting the right execution environment set up for your code, check out [Mamba/Conda](conda.md) or install your software in a [container](apptainer.md) as you would with Docker. Some users will benefit from using interactive [Jupyter Notebooks](jupyter.md).

Most computes involve [storing, accessing and moving data](storage.md), as well as [transferring data](transfer.md) into the cluster.

If you pay attention to a few details in organizing your compute things will go a lot smoother. We recommend using reproducible approaches with [SnakeMake](snakemake.md) to structure your compute.

We note that typically compute resources are available but the lack of good computing practices leads to contention for IO resources, which in turn slow everyone down.

We are adding things to the documentation to aid our users, please familiarize yourself with it. Also check out the [lessons learned](antipatterns.md).
