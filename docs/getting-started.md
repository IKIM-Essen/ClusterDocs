# Getting Started

Welcome the IKIM cluster documentation. The goal of this document is to give you enough background to work on the IKIM cluster. It is not meant as a general introduction to remote computing services. We will refer to external sources where necessary.

If you have any questions, please reach out to your project coordinator for help.

## Getting cluster access

_Note: we assume that you are using a Linux or MacOS operating system. If you are using Windows, please see below for recommendations._

To get access to the IKIM computing infrastructure you need an SSH key. Use the command below to create your SSH key. When prompted, make sure to choose a **strong passphrase** and save the passphrase in your password manager.

```sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_ikim
```

Please send the public key along with following contact details to your project coordinator:

- Desired username (e.g., `firstname.lastname`)
- First name
- Last name
- UK/UDE email
- Public SSH key (`~/.ssh/id_ikim.pub`)

Afterwards, an account will be created for you in the central user management. When this is done, you should be able to SSH into the cluster.

<details>
<summary>Example: output of SSH-keypair generation. </summary>
When executing the command above, you should should see output similar to this:

```text
$ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/<user>/.ssh/id_ikim):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/<user>/.ssh/id_ikim.
Your public key has been saved in /Users/<user>/.ssh/id_ikim.pub.
The key fingerprint is:
SHA256:Fq6OklSiCUQ3G1UsnDu8dFb+VwBfMakRGROe+A2D78Y user@<host>
The key's randomart image is:
+---[RSA 4096]----+
|.. +o.+.   ..==+o|
| .. ++ . .  =++..|
|.  .. o +  o *+  |
|. . .= + o  o.+. |
|.o o. = S .  o.. |
|o .  . o   .o.   |
| . .  .     .E   |
|  o  o      .    |
|   .. .          |
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
ssh-rsa [very long random string]== <user>@<host>
```

</details>

### Setting up your SSH configuration

There is only a single gateway into the IKIM cluster which is called the jumphost. This host should only be used to connect to other servers on the cluster and should _not_ be used for computational work. Use the command below to login to any host, replacing `$USERNAME` and `$HOSTNAME` appropriately.

```sh
ssh -J $USERNAME@login.ikim.uk-essen.de $USERNAME@$HOSTNAME

# Example
ssh -J john.doe@login.ikim.uk-essen.de john.doe@c52
```

For convenience, you can configure your SSH client to automatically use the jumphost. Place the snippet below into your `~/.ssh/config` file, replacing `$USERNAME` appropriately.

```ssh
Host *
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_ikim
  CanonicalizeHostname yes

Host ikim
  HostName login.ikim.uk-essen.de
  User $USERNAME
  ForwardAgent yes

Host g1-? c? c??
  Hostname %h.ikim.uk-essen.de
  ForwardAgent yes

Host g1-*.ikim.uk-essen.de c*.ikim.uk-essen.de
  User $USERNAME
  ProxyJump ikim
  ForwardAgent yes
```

### Test your SSH login

Try some of the examples below to test that your SSH client is properly configured:

```sh
# Login to CPU-node c52
ssh c52.ikim.uk-essen.de

# Shorthand for above command
ssh c52

# Login to GPU-node
ssh g1-7
```

If any of the above is not working, please run the command below and send the debug message to your project coordinator for help.

```sh
ssh -v $USERNAME@login.ikim.uk-essen.de
```

### SSH clients on Windows

We strongly recommend that you use a Linux or MacOS operating systems with the built-in terminals. If you are running a Windows system and a Linux VM is not an option, you can try the [Windows Subsystem for Linux (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/about) which will give you a Ubuntu bash terminal. Finally the [Putty](https://www.putty.org) SSH client may be an alternative but we cannot give any support.

## What hardware is available on the IKIM cluster?

The cluster has two sets of servers: 120 nodes for CPU-bound tasks and 10 nodes for GPU-bound tasks. At this moment, not all of these nodes are available for general computation tasks. However, more will be added in future. The following hardware is installed in the servers:

- CPU nodes (`c_nodes`): Each with 192GB RAM, 2 CPU Intel, 1 SSD for system and 1 SSD for data (2TB).
- GPU nodes (`g_nodes`): Each with 6 NVIDIA RTX 6000 GPUs, 1024GB RAM, 2 CPU AMD, 1 SSD for system (1TB) and 2 NWMe for data (12TB configured as RAID-0).

Your project coordinator can give you recommendations on where to run your jobs.

## What software is available on the IKIM cluster?

We aim to keep the computing environments on the cluster as clean as possible. Therefore, only commonly used software packages are pre-installed and configured. At this moment this includes:

- Python 3
- Conda
- Docker (for applications with dependencies not available in the default set of software).

We assume basic familiarity with the tools above. If you want to learn more, you can take a look at following resources:

- [Docker Curriculum](https://docker-curriculum.com)
- [Conda Getting Started](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda)

## Where to store your data?

There are several locations where you can store data on the cluster:

- **Your home directory** (`/homes/<username>/`): This directory is only for personal data such as configuration files. Anything related to work or that should be visible to other people should not reside here.
- **Project pirectory** (`/projects/<project_name>/`): This location should be used for data related to your project. If you are starting a project, ask your project coordinator to create a directory and provide a list of participating users. Note that you cannot simply list all project directories via `ls /projects`; instead, you need to specify the full path, such as: `ls /projects/dso_mp_ws2021/`
- **Public dataset directory** (`/projects/datashare`): A world-readable location for datasets for which no special access rights are required. To lower the risk of data loss, each user can write only in a subdirectory corresponding to their research group. For example, a user which belongs to group `tio` must add new datasets in `/projects/datashare/tio` but can browse and read throughout `/projects/datashare`.
- **Group directory** (`/groups/<group_name>`): This is the appropriate place for any data that should be shared _within an IKIM research group_. In student projects you will most likely not need group directories.

All of the above directories (homes, projects, groups) are shared with other hosts on the cluster through the network file system (NFS). This is convenient: sharing data between hosts becomes effortless and your data is stored redundantly on the file server.

### Local-only files

For some operations the NFS comes with unnecessary overhead. Therefore, the path `/local/work` is available for creating files and directories that reside on the storage drive of the current host. This location should only be used for quick testing, preliminary experimentation and intermediate output. As soon as you need your files saved, move them to `/projects` or `/groups`. Local-only files are not backed up and **can be deleted without notice**.

Here are tips on writing programs, scripts, containers, etc. that make good use of network resources:

- Read inputs from and write the final results to `/projects` or `/groups`.
- Write intermediate output to `/local/work`.

### NFS caching

Read operations on remote files (homes, projects, groups) are cached transparently on the local storage drive. Generally speaking, your first access to a dataset will be limited by network bandwidth, but any subsequent access will be made from local storage to should be substantially faster.

## Tips on Working with remote computing services

- [Unix Crash Course](https://tildesites.bowdoin.edu/~sbarker/unix/)
- [Another Unix Course](https://www.csoft.net/docs/course.html)
- [Tactical tmux: The 10 Most Important Commands](https://danielmiessler.com/study/tmux/)
- [How To Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)
- [Git Book](https://git-scm.com/book/en/v2)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda)
