# Getting Started for Researchers

## Remote directories

### Homes

Your home directory is shared among all hosts.
This directory is only for personal data such as configuration files.
Anything related to work or that should be visible by other people should not reside here.

### Projects

Subdirectories of `/projects` reside on a remote file server and are shared among all hosts.
This location should be used for data related to individual projects.

Please ask your administrator to create a directory and an associated unix group ID, providing a list of people who should have access (even just yourself).

Note that the projects list is not accessible simply via `ls /projects`.
A list of available paths is provided here:

```text
/projects/covidseq
/projects/data
/projects/deident
/projects/hitachi
/projects/seqlab
/projects/haystack
/projects/cytomine
```

### Groups

Subdirectories of `/groups` reside on a remote file server and are shared among all hosts.
This location is pre-populated with a directory and an associated unix group ID for each research group.

This is the appropriate place for any data that should be shared within a research group.
It's also convenient for storing data before it becomes part of a project at `/projects`.

Note that the group list is not accessible simply via `ls /groups`.
A list of available paths is provided here:

```text
/groups/ds
/groups/dso
/groups/pni
/groups/rb
/groups/ship
/groups/tio
```

If your group is not in the list, please ask your administrator to add a directory.

## Local-only files

The path `/local/work` is available for creating files and directories that reside on the storage drive of the current host.
This location should only be used for quick testing, preliminary experimentation and intermediate output.
As soon as you need your files saved, move them to `/projects` or `/groups`.
Local-only files are not backed up and **can be deleted without notice**.

## NFS caching

Read operations on remote files are cached transparently on the local storage drive.
Generally speaking, your first access to a dataset will be limited by network bandwidth, but any subsequent access will be made from local storage.

## Best practices

Here are tips on writing programs, scripts, containers, etc. that make good use of network resources:

- Read inputs from and write the final results to `/projects` or `/groups`.
- Write intermediate output to `/local/work`.
