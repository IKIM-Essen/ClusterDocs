# Getting Started

Welcome the IKIM cluster documentation. The goal of this document is to give you enough background to work on the IKIM cluster. It is not meant as a general introduction to remote computing services. We will refer to external sources where necessary.

If you have any questions, please reach out to your project coordinator for help.

## Getting cluster access

_Note: we assume that you are using a Linux or MacOS operating system. If you are using Windows, please see below for recommendations._

To get access to the IKIM computing infrastructure you need an SSH key. Use the command below to create your SSH key. When prompted, make sure to choose a **strong passphrase** and save the passphrase in your password manager.

```sh
ssh-keygen -t ed25519 -f ~/.ssh/id_ikim
```

Please send the public key along with following contact details to your project coordinator:

- First name
- Last name
- Email address (domain _uk-essen.de_ or _uni-due.de_ if available)
- Public SSH key (`~/.ssh/id_ikim.pub`)

Afterwards, an account will be created for you in the central user management. When this is done, you should be able to SSH into the cluster.

<details>
<summary>Example: output of SSH-keypair generation. </summary>
When executing the command above, you should should see output similar to this:

```text
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/<user>/.ssh/id_ikim
Your public key has been saved in /Users/<user>/.ssh/id_ikim.pub
The key fingerprint is:
SHA256:PQyNrogYs001Y0IlsG75teDBFVlDmd7xSJPNI1lrQr4 user@<host>
The key's randomart image is:
+--[ED25519 256]--+
|..o...++o.*.     |
| o . ..o+X +.    |
|. . =.. =oBo.    |
|. o+.o o *+.     |
|o+.+ .  SE+      |
|.Bo.+...   .     |
|o oo...          |
|                 |
|                 |
+----[SHA256]-----+
```

Note that two files were created in your home directory in the `.ssh` subdirectory:

```sh
$ ls ~/.ssh
config  id_ikim  id_ikim.pub  known_hosts
```

- `~/.ssh/id_ikim` - This is your private SSH key. Treat this file like a password. Do not share it with anyone.
- `~/.ssh/id_ikim.pub` - This is your public SSH key. This should be shared with your project coordinator. You can open it with any text editor.

The contents of `~/.ssh/id_ikim.pub` look similar to this:

```sh
$ cat ~/.ssh/id_ikim.pub
ssh-ed25519 [long random string] <user>@<host>
```

</details>

### Setting up your SSH configuration

To provide the appropriate parameters for the connection, create a file at `~/.ssh/config` and copy the snippet below, replacing `$USERNAME` appropriately.

```ssh
Host *
  AddKeysToAgent yes
  CanonicalizeHostname yes

Host ikim
  HostName login.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ForwardAgent yes

Host g1-? c? c?? slurmq
  Hostname %h.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ProxyJump ikim
  ForwardAgent yes
```

With `~/.ssh/config` in place, you can use the following command to log into any host, replacing `$HOSTNAME` appropriately.

```sh
ssh $HOSTNAME
```

The connection will transparently jump through the host labeled `ikim` and proceed to the target `$HOSTNAME`. The `ikim` host itself must _not_ be used for computational work.

### Test your SSH login

Try the example below to test that your SSH client is properly configured:

```sh
# Log into the slurm submission node
ssh slurmq
```

If the above is not working, please run the commands below and send the debug messages to your project coordinator for help.

```sh
ssh -v slurmq
```

```sh
ssh -v ikim
```

### SSH clients on Windows

We recommend two options for installing and using an SSH client on Windows:

- [Windows Subsystem for Linux (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/about) provides Linux distributions running in a lightweight virtual machine on Windows. With WSL, the instructions above can be followed without changes and the default shell environment is identical to the one found on IKIM hosts.
- [OpenSSH](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview) is the same software suite that comes preinstalled on other operating systems. To install it, go to the _Apps & Features_ settings page and select _Optional Features_, then add the _OpenSSH Client_ feature. The instructions above should work simply by adapting paths to Windows-style. Older clients might produce an error message that starts with ["Bad stdio forwarding specification"](https://github.com/PowerShell/Win32-OpenSSH/issues/1172), which can be fixed by replacing the `ProxyJump` directive with:

  ```text
  ProxyCommand ssh.exe -W %h:%p ikim
  ```

## What hardware is available on the IKIM cluster?

The cluster has two sets of servers: 120 nodes for CPU-bound tasks and 10 nodes for GPU-bound tasks. At this moment, not all of these nodes are available for general computation tasks. However, more will be added in future. The following hardware is installed in the servers:

- CPU nodes (`c1` - `c120`): Each with 192GB RAM, 2 CPU Intel, 1 SSD for system and 1 SSD for data (2TB).
- GPU nodes (`g1-1` - `g1-10`): Each with 6 NVIDIA RTX 6000 GPUs, 1024GB RAM, 2 CPU AMD, 1 SSD for system (1TB) and 2 NVMe for data (12TB configured as RAID-0).
- GPU node (`g2-1`): One node with 8 NVIDIA A100 80G GPUs, 2TB RAM, 2 AMD EPYC CPUs (256 logical processors), 1 SSD for system (1TB) and 2 NVMe for data (30TB configured as RAID-0).

A subset of these nodes are deployed as a Slurm cluster. Unless instructed otherwise, you should interact with worker nodes using Slurm.

## What software is available on the IKIM cluster?

We aim to keep the computing environments on the cluster as clean as possible. Therefore, only commonly used software packages are pre-installed and configured. At this moment this includes:

- Slurm
- Python 3
- Mamba/Conda
- Apptainer

Comprehensive guides on these tools are outside the scope of this document. To learn more, see the following resources:

- [Slurm](./slurm.md)
- [Conda Getting Started](./conda.md)
- [Apptainer User Guide](https://apptainer.org/docs/user/main/index.html)

## Where to store your data?

There are several locations where you can store data on the cluster:

- **Your home directory** (`/homes/<username>/`): This directory is only for personal data such as configuration files. Anything related to work or that should be visible to other people should not reside here.
- **Project directory** (`/projects/<project_name>/`): This location should be used for data related to your project. If you are starting a project, ask your project coordinator to create a directory and provide a list of participating users. Note that you cannot simply list all project directories via `ls /projects`; instead, you need to specify the full path, such as: `ls /projects/dso_mp_ws2021/`
- **Public dataset directory** (`/projects/datashare`): A world-readable location for datasets for which no special access rights are required. To lower the risk of data loss, each user can write only in a subdirectory corresponding to their research group. For example, a user which belongs to group `tio` must add new datasets in `/projects/datashare/tio` but can browse and read throughout `/projects/datashare`.
- **Group directory** (`/groups/<group_name>`): This is the appropriate place for any data that should be shared _within an IKIM research group_. In student projects you will most likely not need group directories.

All of the above directories (homes, projects, groups) are shared with other hosts on the cluster through the network file system (NFS). This is convenient: sharing data between hosts becomes effortless and your data is stored redundantly on the file server.

Also see the [storage](./storage.md) for details and also info on performance.

## GitHub Authentication through SSH

To clone GitHub repositories on the cluster over the `git+ssh` protocol, you need to (1) configure your local ssh client as per the [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), and (2) enable agent forwarding (if you use the ssh config above, this should already be done). You can verify your setup with following command:

```sh
USER@g1-9:~$ ssh -T git@github.com
Hi USER! You've successfully authenticated, but GitHub does not provide shell access.
```

## Tips on Working with remote computing services

- [Unix Crash Course](https://tildesites.bowdoin.edu/~sbarker/unix/)
- [Another Unix Course](https://www.csoft.net/docs/course.html)
- [Tactical tmux: The 10 Most Important Commands](https://danielmiessler.com/study/tmux/)
- [How To Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)
- [Git Book](https://git-scm.com/book/en/v2)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda)
