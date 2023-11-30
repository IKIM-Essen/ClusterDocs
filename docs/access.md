# Requesting access

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
