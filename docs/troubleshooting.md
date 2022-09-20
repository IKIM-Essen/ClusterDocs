# Troubleshooting

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

## GPU memory is held by zombie or orphan processes

If a process allocates GPU memory and later terminates abnormally, it might die without releasing the GPU memory.
Since the process cannot be killed again, it can't be targeted directly in order to reclaim the memory.
In such a case, `fuser` can be used to identify and kill the parent or children of the dead process.

For example, if `nvidia-smi` reports memory allocated in GPU 0, `fuser -v /dev/nvidia0` can display which processes are accessing it.
```
                     USER        PID ACCESS COMMAND
/dev/nvidia0:        root       1383 F.... nvidia-persiste
                     <user1>  2934164 F...m python3
                     <user2>   3279314 F... python3
                     <user2>   3279314 F...m python3
```

To learn more about the output format and how to kill processes using `fuser`, see `man fuser`.

Note:

- Processes belonging to a different user can only be killed by an administrator.
- Avoid killing `nvidia-persistenced` if possible.
  If necessary, use `systemctl` to interact with the `nvidia-persistenced` service.
