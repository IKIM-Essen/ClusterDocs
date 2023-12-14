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
### Are GPU drivers installed everywhere?

Yes, but you might need to install CUDA in your environment:

Enrico writes that 

```text
the cuda version output from nvidia-smi doesn't mean necessarily that cuda is installed. It simply tells you which cuda release matches the installed drivers```

on slurm nodes, cuda is not preinstalled because I encourage people to install it in their own conda environments so that they can keep it stable

On non-slurm nodes, i.e. g1-7 and g1-9 currently, cuda is still preinstalled
```

## GPU memory is held by orphan processes

If processes are holding GPU memory while their parent terminates abnormally, they could be left with claimed memory and no work to do.
In such a case, `nvidia-smi` will display occupied memory with no associated processes.
The `fuser` command can help perform cleanup and reclaim GPU memory.

For example, if `nvidia-smi` reports memory allocated in GPU 0, `fuser -v /dev/nvidia0` can display which processes are accessing it.

```text
                USER    PID ACCESS COMMAND
/dev/nvidia0:   bob  869108 F...m python
                bob  1236874 F...m python
                bob  1236922 F...m python
```

Users can only see processes owned by themselves.
Administrators can run `fuser` as root to see all processes.

`fuser -k` sends a termination signal to the listed processes.
It can be convenient as a last resort if certain processes are difficult to terminate cleanly.

A typical troubleshooting sessions against leftover GPU memory might be as follows:

1. Examine the output of `nvidia-smi` and look for GPUs with allocated memory but no processes attached.
1. Execute `fuser -v /dev/nvidiaN` to list processes owned by you accessing the device (replace `N` with a GPU index).
1. Save all important work, then try closing open programs cleanly.
1. Execute `fuser -v /dev/nvidiaN` again.
  If any processes show up and you don't have a way to terminate them cleanly, you can use `fuser -k /dev/nvidiaN` to kill them bluntly.
1. Examine the output of `nvidia-smi` again.
   If GPU memory is still occupied, ask an administrator to look into processes owned by other users.
