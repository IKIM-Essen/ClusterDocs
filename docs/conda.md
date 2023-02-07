# Mamba/Conda

[Mambaforge][mambaforge] provides `mamba` and `conda` on the cluster.
Users who prefer to manage their own installation can install a Conda distribution in their home directory.

## Using Conda with Slurm

Submitting a slurm job which includes `conda activate` will result in the following error:

```sh
$ srun -N1 conda activate myenv

CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>
```

This happens because `conda activate` is made available as a shell function which is not preserved when slurm executes a job.

The suggestion of executing `conda init` **does not apply to Slurm**.
Instead, an environment can be activated with one of the following methods:

- Execute `conda activate` while logged into the submission node, then submit the job:

  ```sh
  $ conda activate myenv
  (myenv) $ srun -N1 env | grep CONDA_PREFIX
  CONDA_PREFIX=/homes/user/.conda/envs/myenv
  ```

- Execute `eval "$(conda shell.bash hook)"` as part of the slurm job in order to make `conda activate` available:

  ```sh
  $ cat run.sh
  #!/usr/bin/env bash
  #SBATCH -N1
  eval "$(conda shell.bash hook)"
  conda activate myenv
  srun -N1 env | grep CONDA_PREFIX

  $ sbatch run.sh

  $ cat slurm-120651.out
  CONDA_PREFIX=/homes/user/.conda/envs/myenv
  ```

[mambaforge]: https://github.com/conda-forge/miniforge#mambaforge
