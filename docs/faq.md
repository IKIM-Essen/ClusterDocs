# Frequently Asked Questions

## VSCode fails set itself up on a remote host

Enable the VSCode setting `remote.SSH.lockfilesInTmp`.

## A program fails with the message `too many open files`

This limit can be changed for the current user session with `ulimit -Sn` followed by the desired number. For example:

```sh
ulimit -Sn 4096
```

It is advisable to execute the `ulimit` command only when a workflow requires keeping many files open at the same time. For example:

```sh
ulimit -Sn 4096 && python mywork.py
```

## Fixing permissions for shared files

If the permissions of files that are supposed to be shared are too restrictive, ask the owner to extend the permissions with:

```sh
# Allow everyone to read everything in a directory.
chmod -R a+r <path to directory>

# Allow the owner's group to modify every file in a directory.
chmod -R g+w <path to directory>

# Extend the execution and directory browsing permissions that the owner has in a directory to everyone.
find <path to directory> -executable -exec chmod a+x {} \;
```
