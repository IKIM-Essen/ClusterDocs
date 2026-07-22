# Upcoming RCC changes

The rollout improves login routing, SSH server-identity verification, browser-based project data transfer, central service reliability and protected project websites.

## What most users need to do

1. Read the final rollout date on this page.
2. Complete the Class 1 readiness check.
3. Close VS Code and download RCC Connect only when this page says the new connection kit is active.
4. Run `RCC-Test` and use the repair action if it finds stale or overwritten settings.
5. Verify the RCC host-CA fingerprint through an independent trusted institutional channel.
6. Reopen VS Code only after the test reports that the RCC connection is ready.
7. Use the web transfer service with your own RCC account.

Your RCC account, files, user SSH key and password do not change as part of the host-identity migration. RCC Connect keeps RCC trust in its own file and leaves ordinary `known_hosts` entries for GitHub, other clusters and unrelated services untouched.

> **Do not approve an unexpected SSH identity warning.** Do not delete host records merely to make a connection work. Run RCC Connect or contact RCC support.

Access from inside the hospital remains intentionally simple. Informational sites can open without login. Data transfer and active project applications identify the user with a password or passkey. External access uses additional authentication.

## For technical users

The site provides bounded terminal checks, VS Code guidance, Slurm acceptance examples, Apptainer guidance and a protected web-application pattern. The [SSH host-identity policy](../policies/ssh-host-identity.md) documents the host-CA architecture, dedicated trust file, endpoint policy and phased migration without publishing private infrastructure credentials.

## Current staging values

- Rollout date: **{{ rollout_date }}**
- Documentation URL: **{{ production_url }}**
- Support contact: **{{ support_contact }}**
- RCC host-CA fingerprint: **{{ ssh_host_ca_fingerprint }}**
