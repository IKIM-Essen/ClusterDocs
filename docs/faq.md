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
