# Snakemake

The Snakemake workflow management system is a tool to create transparent reproducible and scalable data analyses.

* Workflows are described via a human readable, Python based language. 
* They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. 
* Snakemake workflows can entail a description of required software (via Mamba/Conda or container images), which will be automatically deployed to any execution environment.
* Snakemake can automatically create portable, server-less interactive HTML reports that contain all requested results and connect them to data provenance information like code and parameters.

## Installation

Snakemake can be easily installed using the mamba package manager that is preinstalled on the cluster:

```sh
mamba create -c conda-forge -c bioconda --name snakemake snakemake
```

It is recommended to execute your analyses via Slurm, for maintenance and performance reasons (while Snakemake would also work without it).
To do this by default set the default Snakemake profile (i.e. Snakemake's default options) to be the slurm profile in your `.bashrc`:

```sh
echo "export SNAKEMAKE_PROFILE=slurm" >> .bashrc
```

## Usage

Given that you are inside of a working directory that contains a Snakemake workflow, after above installation steps, you can use Snakemake on the slurm cluster by running

```sh
nice snakemake --jobs N
```

with `N` being the number of jobs you want to run in parallel at most, and it will automatically submit the jobs to the slurm cluster.
In order to perform a dry-run (i.e. just see the plan, which is highly recommended before actually executing, run

```sh
snakemake -n
```

For a full tutorial on Snakemake, please check out [the official Snakemake tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html).

## Further hints

* Make sure to follow the [best-practices](https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html).
* If you and your colleagues have common tasks that often reoccur in workflows, you can save a lot of time by activating Snakemake's [between workflow caching](https://snakemake.readthedocs.io/en/stable/executing/caching.html).
