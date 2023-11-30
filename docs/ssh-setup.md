## Configuring the ssh client on your system

On your laptop do these steps.

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

Host g?-? c? c?? c??? shellhost
  Hostname %h.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ProxyJump ikim
  ForwardAgent yes
```

# Test your SSH login

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

# SSH clients on Windows

We recommend two options for installing and using an SSH client on Windows:

- [Windows Subsystem for Linux (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/about) provides Linux distributions running in a lightweight virtual machine on Windows. With WSL, the instructions above can be followed without changes and the default shell environment is identical to the one found on IKIM hosts.
- [OpenSSH](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview) is the same software suite that comes preinstalled on other operating systems. To install it, go to the _Apps & Features_ settings page and select _Optional Features_, then add the _OpenSSH Client_ feature. The instructions above should work simply by adapting paths to Windows-style. Older clients might produce an error message that starts with ["Bad stdio forwarding specification"](https://github.com/PowerShell/Win32-OpenSSH/issues/1172), which can be fixed by replacing the `ProxyJump` directive with:

  ```text
  ProxyCommand ssh.exe -W %h:%p ikim
  ```

