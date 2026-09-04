# Set up RCC on a Mac

This checklist uses Terminal and the OpenSSH client included with current
macOS. Allow about 15 minutes after your RCC account and approved connection
settings are available.

## 1. Check the built-in SSH client

Open **Terminal** from Applications → Utilities, then run:

```bash
ssh -V
```

A line beginning with `OpenSSH` means the client is ready. Keep macOS patched;
do not replace the system client merely because another tutorial uses a
different package manager.

## 2. Create one RCC key

If you do not already have a dedicated RCC key, run:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_rcc
```

Use a strong passphrase. `~/.ssh/id_rcc` is private and stays on this Mac.
`~/.ssh/id_rcc.pub` is public and is the only key file you register with RCC.

Display the public key when the account form asks for it:

```bash
cat ~/.ssh/id_rcc.pub
```

## 3. Add the approved RCC configuration

Open the SSH configuration in the simple terminal editor:

```bash
nano ~/.ssh/config
```

Paste the current configuration supplied through the approved institutional
channel. Its shape is:

```sshconfig
Host {{ ssh_gateway_alias }}
    HostName VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION
    User YOUR_RCC_USERNAME
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ForwardAgent no

Host {{ ssh_target_alias }} c? c?? c??? d?? g?-? g?-??
    HostName %h.ikim.uk-essen.de
    User YOUR_RCC_USERNAME
    IdentityFile ~/.ssh/id_rcc
    IdentitiesOnly yes
    ProxyJump {{ ssh_gateway_alias }}
    ForwardAgent no
```

Replace only the values identified by the approved RCC instructions. Save in
`nano` with Control-O, Return, then exit with Control-X. Protect the file:

```bash
chmod 600 ~/.ssh/config ~/.ssh/id_rcc
```

The first block describes the jump host. The second describes the shell host
you actually use. You do not log into the jump host; `ProxyJump` forwards the
connection automatically.

## 4. Check, then connect once

Inspect the effective settings without connecting:

```bash
ssh -G {{ ssh_target_alias }}
```

Verify the approved server identity through the institutional instructions,
then make one connection attempt:

```bash
ssh {{ ssh_target_alias }}
```

Stop if SSH reports an unexpected host-key change. Do not delete all
`known_hosts` entries or disable host-key checking.

## 5. Add VS Code only after Terminal works

For most users, VS Code with Microsoft's Remote - SSH extension is the easiest
day-to-day editor. Follow the dedicated
[VS Code with RCC](vscode.md) section and select `{{ ssh_target_alias }}` as the
destination. VS Code uses the same configuration and cannot repair an SSH
connection that fails in Terminal.

Use the shell host to edit code, use Git, submit jobs, and inspect logs. Submit
computation through Slurm.

## If you want the guided course

Download and extract [RCC Expedition](../rcc-expedition.md), then open
`START HERE.html`. Choose **Open the course now**; installing a Desktop
shortcut is optional.

Continue with [your first 15 minutes](index.md) or the
[full access reference](../reference/access-ssh-vscode.md).
