# Storage on the IKIM cluster

The cluster has a number of options for retrieving and storing data. They have vastly different performance characteristics and greatly influence the time required to complete your computational analyses.

## Classes of storage

Not all storage locations are alike and it is worth your while to understand their specific properties.

### Local storage on the system partition

The local storage on each node typically consists of a system partition and a data partition. The system partition is used for the operating system, the configuration, [swap files](https://www.unix.com/man-page/linux/1m/swap/), pre-installed software. Most directories on the node are read-only to users.

| location | purpose | user read-write status | comment |
| ---  | --- |  -- | ---|
| /etc/    | configuration | read-only |  |
| /var/    | temporary files | read-only |  |
| /var/tmp | user-generated temporary files | read-write | local disk |
| /tmp/    | user-generated temporary files, deleted on reboot | read-write | local disk |

### Local storage on the data partition

For some operations the NFS comes with unnecessary overhead. Therefore, the path `/local/work` is available for creating files and directories that reside on the data partition of the current host. This location should only be used for quick testing, preliminary experimentation and intermediate output. As soon as you need your files saved, move them to `/projects` or `/groups`. Local-only files are not backed up and **can be deleted without notice**.

Here are tips on writing programs, scripts, containers, etc. that make good use of network resources:

- Read inputs from and write the final results to `/projects` or `/groups`.
- Write intermediate output to `/local/work`.

### NFS storage

Read operations on network storage (`/projects`, `/groups`) are cached transparently on local storage in the data partition. Generally speaking, your first access to a dataset will be slightly slower than usual due, but any subsequent access will be made from local storage.

The file server has a 10Gib (10Gbs, 10 gigabit per second connection to the entire cluster. As a consequence each node can access a fraction of 10Gib, in the worst case a tiny fraction. However we note that a 250MB (megabyte) file will need a fraction of a second to transfer from the server to the client. This rather brilliant performance stats drastically change if and when random IO (as in not streaming large files, write-locking files, etc.) enter the equation. Those complex operations are best left to local disk.

As a consequence, using local files or cached files is a good idea to ensure good runtime performance.

Three different storage locations exist on the file server:

| location | purpose | user read-write status | comment |
| ---  | --- |  -- | ---|
| /projects/    | project data | read-write |  not listable |
| /groups/    | group files | read-write  |  not listable |
| /homes  | user home directory | read-write | not cached |

Each user has a private home-directory. The contents of which are private to the userm typically no data relevant to any other user, project or your PI should be stored here.

The projects directory provides a means to generate project specific storage, typically associated with a linux group shared by all members of the project. Thus `/projects/abc` is shared only by members of the project `abc`. We note that by using the `id` command users can identify all the groups they belong to. The contents of /projects are cached on the local disk, read access against data in /projects will typically no place too much of burden on the file server. The contents of the `/projects` folder will not be completely listed when e.g. executing `ls /projects/` as contents are mounted on demand by [automounter](https://help.ubuntu.com/community/Autofs). You can request a `/project` directory by talking to us on Mattermost or have your PI request one.

The `/groups` directory is identical to `/projects` in technology. However every group on the organization has their own subdirectory.
