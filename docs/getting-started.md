# Getting Started

Welcome the IKIM cluster documentation. The goal of this document is to give you enough background to work on the IKIM cluster. It is not meant as a general introduction to remote computing services. We will refer to external sources where necessary.

If you have any questions, please reach out to your project coordinator for help.

## Getting cluster access

### Generating the SSH key on Linux and MacOS

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

### Generating the SSH key on Windows

Windows requires the OpenSSH client, which has been permanently integrated into the system since the October 2018 Windows 10 update. If this is not available (so you can't use the command `ssh-keygen`), simply follow the instructions at the following link: [OpenSSH](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui#install-openssh-using-windows-settings)

Open Powershell and Use the command below to create your SSH key. When prompted, make sure to choose a strong passphrase and save the passphrase in your password manager.

```sh
ssh-keygen -t ed25519
```

You can accept the default settings for the path, but name the key `id_ikim` when prompted. The key pair (public and private) will appear by default at `C:\Users\<username>\.ssh\` (note that the name of this directory begins with a dot and is therefore invisible by default) inside your user directory. When done, send the contents of the public key with the file name id_ikim.pub with contact details (name and email adress) to your project coordinator.

### Setting up your SSH configuration

To provide the appropriate parameters for the connection, create a file at `~/.ssh/config` (on Windows: `C:\Users\<username>\.ssh\config`) and copy the snippet below, replacing `$USERNAME` appropriately.

```ssh
Host *
  AddKeysToAgent yes
  CanonicalizeHostname yes

Host ikim
  HostName login.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ForwardAgent yes

Host g?-? c? c?? c??? shellhost
  Hostname %h.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ProxyJump ikim
  ForwardAgent yes
```

### Test your SSH login

Try the example below to test that your SSH client is properly configured:

```sh
ssh ikim
```

If it succeeds, type `exit` to log out. The `ikim` host must be used only for ssh authentication and _not_ for computational work; in fact, users should not log into it directly. Using the provided configuration file, ssh will automatically "jump through" the `ikim` host to reach the compute nodes.

For instructions on using the compute nodes, see the section [What software is available on the IKIM cluster?](#what-software-is-available-on-the-ikim-cluster)

If the login test fails, please run the command below and send the output to your project coordinator for help.

```sh
ssh -v ikim
```

## What hardware is available on the IKIM cluster?

The cluster has two sets of servers: 120 nodes for CPU-bound tasks and 10+ nodes for GPU-bound tasks. At this moment, not all of these nodes are available for general computation tasks. However, more will be added in future. The following hardware is installed in the servers:

- CPU nodes (`c1` - `c120`): Each with 192GB RAM, 2 CPU Intel, 1 SSD for system and 1 SSD for data (2TB).
- GPU nodes (`g1-1` - `g1-10`): Each with 6 NVIDIA RTX 6000 GPUs, 1024GB RAM, 2 CPU AMD, 1 SSD for system (1TB) and 2 NVMe for data (12TB configured as RAID-0).
- GPU node (`g2-1`): One node with 8 NVIDIA A100 80G GPUs, 2TB RAM, 2 AMD EPYC CPUs (256 logical processors), 1 SSD for system (1TB) and 2 NVMe for data (30TB configured as RAID-0).

A subset of these nodes are deployed as a Slurm cluster. Unless instructed otherwise, you should interact with worker nodes using Slurm.

## What software is available on the IKIM cluster?

Short answer: Everything under the sun. Familiarize yourself with our [job scheduler](slurm.md), then install software using either a [package manager](conda.md) or build a [container](apptainer.md). Compared to package managers like Conda, containers provide greater isolation from the host operating system and are recommended for producing repeatable workflows.

Example: To install [scikit-learn](https://scikit-learn.org/stable/install.html) all you need to do is

```sh
conda create -n sklearn-env -c conda-forge scikit-learn
conda activate sklearn-env
```

Conda and its siblings (anaconda and mamba) provide access to [thousands of software packages](https://conda-forge.org/feedstock-outputs/), you can
set up your required software by yourself and even have multiple environments. The [conda intro](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) provides a good starting point.

## Where to store your data?

There are several locations where you can store data on the cluster:

- **Your home directory** (`/homes/<username>/`): This directory is only for personal data such as configuration files. Anything related to work or that should be visible to other people should not reside here.
- **Project directory** (`/projects/<project_name>/`): This location should be used for data related to your project. If you are starting a project, ask your project coordinator to create a directory and provide a list of participating users. Note that you cannot simply list all project directories via `ls /projects`; instead, you need to specify the full path, such as: `ls /projects/dso_mp_ws2021/`
- **Public dataset directory** (`/projects/datashare`): A world-readable location for datasets for which no special access rights are required. To lower the risk of data loss, each user can write only in a subdirectory corresponding to their research group. For example, a user which belongs to group `tio` should add new datasets in `/projects/datashare/tio` but can browse and read throughout `/projects/datashare`.
- **Group directory** (`/groups/<group_name>`): This is the appropriate place for any data that should be shared _within an IKIM research group_. In student projects you will most likely not need group directories.

All of the above directories (homes, projects, groups) are shared with other hosts on the cluster through the network file system (NFS). This is convenient: sharing data between hosts becomes effortless and your data is stored redundantly on the file server.

Also see the [storage](storage.md) for details and also info on performance. If you need to transfer data, reading [transfer](transfer.md)

## Tips on Working with remote computing services

- [Unix Crash Course](https://tildesites.bowdoin.edu/~sbarker/unix/)
- [Another Unix Course](https://www.csoft.net/docs/course.html)
- [Tactical tmux: The 10 Most Important Commands](https://danielmiessler.com/study/tmux/)
- [How To Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)
- [Git Book](https://git-scm.com/book/en/v2)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-conda)
