# Positron: R analysis on RCC (pilot draft)

> Positron Remote SSH is not yet accepted against deployed RCC worker OS builds.

Install the Positron desktop app using approved channels. In local User Settings, set `remoteSSH.transport` to `native` for OpenSSH ProxyJump support. Authenticate and verify host keys through a trusted institutional procedure first: native transport cannot prompt for SSH passwords, passphrases, or host-key acceptance.

Run `rcc-open positron PROJECT`, then choose Remote SSH and the generated `rcc-dev-JOBID` alias. Work under a small source subtree of `/projects/PROJECT`. The R console, Python kernels, terminals and Positron server run on the Slurm-allocated Linux worker, not on the laptop.

Positron installs a version-matched remote extension-host binary. Verify RCC network egress and worker OS compatibility before any pilot. Never switch to shellhost computation as a workaround.

Reference: https://positron.posit.co/remote-ssh
