# Creating containers with Apptainer

[Apptainer][apptainer] is the container system installed on the Slurm cluster. In contrast to Docker, it does not grant the user elevated privileges and is well-suited to multi-user environments. Nonetheless, it can run containers from Docker images as long as they do not depend on intrinsic root privileges such as binding to host ports below 1024.

## Basic commands

Apptainer provides the following commands for launching containers:

- `apptainer run`: executes the default startup command.
- `apptainer exec`: executes a custom command.
- `apptainer shell`: executes an interactive shell.
- `apptainer instance start`: executes a background service.

The above commands support mostly the same set of options.

## Executing a Docker image

When using the prefix `docker://`, Apptainer pulls the image from Docker Hub.

```sh
apptainer run docker://alpine
```

The default execution model of Apptainer is different from Docker's. The container filesystem in Apptainer is read-only, although a number of paths such as `/tmp`, the user's home and the current directory are mounted read-write from the host into the container. Additionally, the default container user is the host user rather than root. The following examples demonstrate the effects of this behavior.

```sh
# When creating a file in the container, it is owned by the current user both in the container and on the host.
alice@c1:~$ apptainer exec \
    docker://alpine \
    sh -c 'touch hello && ls -l hello'
-rw-rw-r--    1 alice   alice           0 Apr 13 10:07 hello
alice@c1:~$ ls -l hello
-rw-rw-r-- 1 alice alice 0 Apr 13 10:07 hello
```

```sh
# Non-mounted paths are read-only.
alice@c1:~$ apptainer exec \
    docker://alpine \
    apk add busybox-extras
ERROR: Unable to lock database: Read-only file system
ERROR: Failed to open apk database: Read-only file system
```

The immutability of non-mounted paths, in combination with executing as the host user, makes it convenient to run multiple containers in parallel on the cluster with easy access to NFS storage. If this is not desired, other modes of operation are listed below.

### Bind-mounting

If a Docker image expects to be able to write in specific locations, they can simply be mounted in the container while preserving the read-only mode for the rest of the filesystem. For example:

```sh
alice@c1:~$ mkdir ~/pgrun ~/pgdata
alice@c1:~$ apptainer run \
    --bind ~/pgdata:/var/lib/postgresql/data \
    --bind ~/pgrun:/var/run/postgresql \
    --env POSTGRES_PASSWORD=secret \
    docker://postgres
```

### Writable tmpfs

The option `--writable-tmpfs` creates a writable area that allows making changes to the container filesystem. The default size is 16 MiB, therefore it is only suitable for small writes such as PID or state-tracking files. Any changes are lost when the container exits.

```sh
alice@c1:~$ mkdir ~/pgdata
alice@c1:~$ apptainer run \
    --bind ~/pgdata:/var/lib/postgresql/data \
    --writable-tmpfs \
    --env POSTGRES_PASSWORD=secret \
    docker://postgres
```

### Sandbox

To switch to a full read-write model, Apptainer allows executing the container filesystem from a directory on the host. Such a directory is called _sandbox_ in Apptainer terminology. After creating a sandbox, it can be passed to `apptainer` commands as any other image and made writable with `--writable --fakeroot`.

```sh
# Create a sandbox.
alice@c1:~$ apptainer build --sandbox mysandbox docker://alpine
alice@c1:~$ ls mysandbox
bin  dev  environment  etc  home  lib  media  mnt  opt  proc  root  run  sbin  singularity  srv  sys  tmp  usr  var

# Install a package in the sandbox.
alice@c1:~$ apptainer exec \
    --writable \
    --fakeroot \
    mysandbox \
    apk add busybox-extras
```

The `--fakeroot` option makes the user appears as root in the container and mounts its home directory at `/root`.

## Using GPUs

The `--nv` option instructs Apptainer to add GPU support to the container.

```sh
apptainer exec --nv docker://nvcr.io/nvidia/cuda:12.1.0-base-ubuntu22.04 /usr/bin/nvidia-smi
```

Apptainer doesn't have an equivalent of the `--gpus` option from the NVIDIA Docker runtime. The environment variable `CUDA_VISIBLE_DEVICES` should be used to control GPU visibility inside the container. See [Targeting GPU nodes with Slurm](./slurm.md).

[apptainer]: https://apptainer.org
