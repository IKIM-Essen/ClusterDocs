# Setting up your ssh client

## Configuring the ssh client on your system

On your laptop do these steps.

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

Host g?-? g?-?? c? c?? c??? shellhost
  Hostname %h.ikim.uk-essen.de
  User $USERNAME
  IdentityFile ~/.ssh/id_ikim
  ProxyJump ikim
  ForwardAgent yes
```

## Test your SSH login

Try the example below to test that your SSH client is properly configured:

```sh
ssh ikim
```

If it succeeds, type `exit` to log out. The `ikim` host must be used only for ssh authentication and _not_ for computational work; in fact, users should not log into it directly. Using the provided configuration file, ssh will automatically "jump through" the `ikim` host to reach the compute nodes.

If the login test fails, please run the command below and send the output to your project coordinator for help.

```sh
ssh -v ikim
```
