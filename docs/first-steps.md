# Welcome to the cluster

You now have connected successfully the cluster.  You can now use [Mamba](conda.md) to configure your environment or [Apptainer](apptainer.md) to execute a binary object.

You should be connected to one of the computers we have designated 

## How to find a computing device

You will be connected to one of a number of interactive servers (SHELLHOST). Please do not perform extensive computing on these nodes. Use our [resource manager](slurm.md) to obtain access to the resources you need.

## Where to store your data?

There are several locations where you can store data on the cluster:

- **Your home directory** (`/homes/<username>/`): This directory is only for personal data such as configuration files. Anything related to work or that should be visible to other people should not reside here.
- **Project directory** (`/projects/<project_name>/`): This location should be used for data related to your project. If you are starting a project, ask your project coordinator to create a directory and provide a list of participating users. Note that you cannot simply list all project directories via `ls /projects`; instead, you need to specify the full path, such as: `ls /projects/dso_mp_ws2021/`
- **Public dataset directory** (`/projects/datashare`): A world-readable location for datasets for which no special access rights are required. To lower the risk of data loss, each user can write only in a subdirectory corresponding to their research group. For example, a user which belongs to group `tio` should add new datasets in `/projects/datashare/tio` but can browse and read throughout `/projects/datashare`.
- **Group directory** (`/groups/<group_name>`): This is the appropriate place for any data that should be shared _within an IKIM research group_. In student projects you will most likely not need group directories.

All of the above directories (homes, projects, groups) are shared with other hosts on the cluster through the network file system (NFS). This is convenient: sharing data between hosts becomes effortless and your data is stored redundantly on the file server.

Also see the [storage](storage.md) for details and also info on performance. If you need to transfer data, reading [transfer](transfer.md)



