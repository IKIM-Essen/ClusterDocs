# IKIM Scientific Computing

This website contains documentation for the scientific computing infrastructure at the Institute for AI in Medicine (IKIM) in Essen. The documentation is geared towards researchers and students that aim to run scientific experiments on the cluster. See [Getting Started](getting-started.md) for general instructions.

## About

The sources of this documentation can be found on [GitHub](https://github.com/IKIM-Essen/ClusterDocs) and we encourage contribution.

## Intro
We believe it is important to know a thing or two about the underlying computer and network infrastructure to be effective. We note this will also limit your frustration level. We do not provide extensive documentation, but rather jumping off points and short best practice info on your setup and your procedures.

  By configuring your environment correctly you can make your job easier, check out [./conda.md](Mamba/Conda) for info on getting the right execution environment set up for your code, it might be desirable to run them inside a [apptainer.md](container) similar to the Docker system. Some users will benefit from using interactive [jupyter.md](Jupyter Notebooks).

  Since most computes will involve [storage.md](storing, accessing and moving data), as well as [transfer.md](transferring data) into the cluster.

  If you pay attention to a few details in organizing your compute things will go a lot smoother. We recommend using reprocudible approaches with [snakemake.md](SnakeMake) to structure your compute and a use a professional resource manager ([slurm.md](Slurm)) to structure your access to computing devices.
