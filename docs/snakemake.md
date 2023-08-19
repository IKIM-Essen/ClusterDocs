# Snakemake

The Snakemake workflow management system is a tool to create transparent reproducible and scalable data analyses.

* Workflows are described via a human readable, Python based language.
* They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition.
* Snakemake workflows can entail a description of required software (via Mamba/Conda or container images), which will be automatically deployed to any execution environment.
* Snakemake can automatically create portable, server-less interactive HTML reports that contain all requested results and connect them to data provenance information like code and parameters.

## Installation

Snakemake can be easily installed using the mamba package manager that is preinstalled on the cluster.
First, ssh into a shellhost machine

```sh
ssh shellhost
```

Then create a snakemake environment via the preinstalled mamba package manager:

```sh
mamba create -c conda-forge -c bioconda --name snakemake snakemake
```

It is recommended to execute your analyses via Slurm, for maintenance and performance reasons (while Snakemake would also work without it).
To do this by default set the default Snakemake profile (i.e. Snakemake's default options) to be the slurm profile in your `.bashrc`:

```sh
echo "export SNAKEMAKE_PROFILE=slurm" >> .bashrc
```

## Usage

Assumptions:

* You are on one of the `shellhost` machines (`ssh shellhost`).
* You are inside of a working directory that contains a Snakemake workflow (either a file `Snakefile` or `workflow/Snakefile` in the same dir)
* You have completed above installation steps.

Since your Snakemake workflow might run for a longer time, you usually want it to be independent of the current shell session (otherwise, the Snakemake process would be killed when the session is closed or disconnected).
Therefore, we recommend to first generate a so-called tmux session via

```sh
tmux new -s SESSIONNAME
```

with `SESSIONNAME` being a reasonable name under which you can remember your intended Snakemake run.
For a full summary of all tmux functionality, see [here](https://tmuxcheatsheet.com/).
In addition, note for youself the name of the host (`hostname -a`), so that you can later come back to the same in case you log youself out or are disconnected.
In such a case, you can come back to the same host (say, `HOSTNAME`) and open the tmux session via

```sh
ssh HOSTNAME
tmux attach -t SESSIONNAME
```

Inside of the tmux session, you can use Snakemake on the slurm cluster by running

```sh
nice snakemake --jobs N
```

with `N` being the number of jobs you want to run in parallel at most, and it will automatically submit the jobs to the slurm cluster.
The `nice` command before the `snakemake` invocation ensures that your Snakemake process on the `shellhost` has less priority than any user interaction.
This is important to ensure that the `shellhost` remains responsive.
In order to perform a dry-run (i.e. just see the plan), which is highly recommended before actually executing, run

```sh
snakemake -n
```

For a full tutorial on Snakemake, please check out [the official Snakemake tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html).

## Further hints

* Make sure to follow the [best-practices](https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html).
* If you and your colleagues have common tasks that often reoccur in workflows, you can save a lot of time by activating Snakemake's [between workflow caching](https://snakemake.readthedocs.io/en/stable/executing/caching.html).
