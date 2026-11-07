# RCC Connect troubleshooting (pilot draft)

**Installer or doctor failure:** Use saved copies under `~/.rcc/backups`; do not erase an existing SSH configuration. Doctor checks effective local OpenSSH settings, not the remote host's authenticity or operational status.

**Unknown or changed host key:** Stop and consult the approved host-key registry. Never disable StrictHostKeyChecking or delete known_hosts to bypass a warning.

**Positron fails immediately:** Verify native OpenSSH transport, authenticated noninteractive SSH, approved worker host key and remote server OS/version compatibility.

**VS Code server fails:** Verify download prerequisites, supported remote OS and extension network policy. Never use shellhost computation as a fallback.

**SSH lost after submission:** A job may have been created. Do not blindly retry start. Run `rcc-open list`; attach to an existing job with `rcc-open attach positron PROJECT JOBID` or `rcc-open attach vscode PROJECT JOBID`. The client must verify exact Slurm WorkDir against the selected project; failure must not submit a new job.

**Job pending, expired or unavailable:** Review `rcc-dev-session list` and `squeue` on the shellhost. Save durable data, release idle allocations, and contact RCC support with sanitized logs. Never share private keys or unredacted research data.
