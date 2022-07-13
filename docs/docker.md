# Docker on cluster hosts

Features of the cluster hosts such as centralized identity management, NFS shares and automounting may cause issues with Docker containers. This guide describes how to work around the most common problems.

## Accessing NFS shares

For security and performance reasons, [NFS shares](getting-started.md#where-to-store-your-data) on IKIM hosts are configured in a way that makes them incompatible with Docker's defaults. They aren't available to the root user, although containers are usually launched as root. Additionally, NFS locations are only mounted on access, but by default Docker doesn't see mount paths that spawn on the host.

### Executing containers as a regular user

The root user problem is solved by launching the container as the current user and primary group:

```sh
docker run --rm --user="$(id -u):$(id -g)" <image> <command>
```

For example:

```sh
$ docker run --rm --user="$(id -u):$(id -g)" alpine id
uid=477800001 gid=477800001
```

With Docker Compose, this can be achieved with the `user:` directive and environment variables in the `docker-compose.yml` file:

```yml
services:
  app:
    # Instruct the container to run as the specified user and group.
    # This only affects executing an image, not the build process.
    user: ${DOCKER_UID}:${DOCKER_GID}
```

The variables can be defined in the launch command _(a)_ or by creating a `.env` file alongside `docker-compose.yml` _(b)_.

_a_:

```sh
DOCKER_UID=$(id -u) DOCKER_GID=$(id -g) docker compose up
```

_b_:

```sh
echo "DOCKER_UID=$(id -u)" >> .env
echo "DOCKER_GID=$(id -g)" >> .env
```

### Mounting project or group directories

Automounted NFS locations have a parent which is permanently mounted and several subdirectories which are automounted. For example, `/projects/datashare` consists of a permanently mounted path `/projects` and an automounted subdirectory `datashare`. In order to access any level below the automounted directory, Docker needs to mount the top level so that it spawns on the host:

```sh
docker run --rm --user="$(id -u):$(id -g)" -v /projects/datashare:/datashare alpine ls /datashare
```

The example above is not enough to access NFS shares which require the user to be a member of a specific group. For example, `/projects/myproject` would be acessible by members of the group `myproject`, therefore the Docker container needs to be launched with a user who belongs to the appropriate group. First, obtain the correct group ID by inspecting the target directory:

```sh
$ ls -nd /projects/myproject
drwxrws--- 3 0 54321 3 Dec  2 12:21 /projects/myproject
```

The output of `ls -nd` in the example shows that the gid is `54321`. The container can now be launched by passing the gid to the `--group-add` option:

```sh
docker run --rm -it --user="$(id -u):$(id -g)" --group-add=54321 -v /projects/myproject:/myproject alpine
```

## Adding account information to containers

Launching a container with `--user="$(id -u):$(id -g)"` simply sets the uid and gid but does not create an account in the container. This option is insufficient for containerized applications which require unix accounts to exist in the image.

A possible solution involves modifying the image by adding a local account to it, for example by adding `RUN groupadd mygroup && useradd --no-log-init -g mygroup myuser` to `Dockerfile`.

An alternative approach is to list all required groups and accounts in local files using the `/etc/group` and `/etc/passwd` formats, then mount these files in the container. The following example generates local `group` and `passwd` files containing the current account:

```sh
mkdir "/local/work/$USER-docker"
echo "$(id -un):x:$(id -u):$(id -g)::/home/$USER:/bin/sh" > "/local/work/$USER-docker/fakepasswd"
echo "$(id -gn):x:$(id -g):" > "/local/work/$USER-docker/fakegroup"
```

The container is then launched by mounting the files (optionally in read-only mode):

```sh
docker run --rm --user="$(id -u):$(id -g)" -v "/local/work/$USER-docker/fakegroup:/etc/group:ro" -v "/local/work/$USER-docker/fakepasswd:/etc/passwd:ro" <image> <command>
```

It's also possible to save these files in the home directory, but docker won't be able to bind-mount them directly on hosts with NFS homes.
As a workaround, the path on local storage can be a symbolic link:

```sh
echo "$(id -un):x:$(id -u):$(id -g)::/home/$USER:/bin/sh" > "$HOME/fakepasswd"
echo "$(id -gn):x:$(id -g):" > "$HOME/fakegroup"
mkdir "/local/work/$USER-docker"
ln -s "$HOME/fakepasswd" "$HOME/fakegroup" "/local/work/$USER-docker/"
```

With Docker Compose, it's recommended to generate a `.env` file to provide the necessary values for `docker-compose.yml`:

```yml
services:
  app:
    # Instruct the container to run as the specified user and group.
    # This only affects executing an image, not the build process.
    user: ${DOCKER_UID}:${DOCKER_GID}
    volumes:
      # Bind-mount the fake passwd and group files.
      - ${FAKE_PASSWDFILE}:/etc/passwd:ro
      - ${FAKE_GROUPFILE}:/etc/group:ro
```

```sh
cat > .env <<EOF
DOCKER_UID=$(id -u)
DOCKER_GID=$(id -g)
FAKE_PASSWDFILE=/local/work/$USER-docker/fakepasswd
FAKE_GROUPFILE=/local/work/$USER-docker/fakegroup
EOF
```
