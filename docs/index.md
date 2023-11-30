# IKIM Scientific Computing

This website contains documentation for the scientific computing infrastructure at the Institute for AI in Medicine (IKIM) in Essen. The documentation is geared towards researchers and students that aim to run scientific experiments on the cluster. See [Getting Started](getting-started.md) for general instructions.

The image below shows members of IKIM assembling the cluster
![Cluster](./assets/cluster_barnraiser.png)

## About

The sources of this documentation can be found on [GitHub](https://github.com/IKIM-Essen/ClusterDocs) and we encourage contribution.

## Intro

We believe it is important to know a thing or two about the underlying computer and network infrastructure to be effective. We note this will also limit your frustration level. We do not provide extensive documentation, but rather jumping off points and short best practice info on your setup and your procedures.

  By configuring your environment correctly you can make your job easier, check out [Mamba/Conda](conda) for info on getting the right execution environment set up for your code, it might be desirable to run them inside a [container](apptainer) similar to the Docker system. Some users will benefit from using interactive [Jupyter Notebooks](jupyter).

  Since most computes will involve [storing, accessing and moving data](storage), as well as [transferring data](transfer) into the cluster.

  If you pay attention to a few details in organizing your compute things will go a lot smoother. We
  recommend using reprocudible approaches with [SnakeMake](snakemake) to structure your compute and a
  use a resource manager ([slurm](slurm)) to structure your access to computing devices.

  We note that typically compute resources are available but the lack of good computing practices leads
  contention for IO resources, that in turn slow everyone down.

We are adding things to the documentation to aid our users, please familiarize yourself with it. Also check out the [lessons learned](antipatterns).
