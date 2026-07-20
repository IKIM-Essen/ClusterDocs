# Importable RCC account starter setups

The account starter kit provides optional, reviewable examples for a more useful
interactive shell, a lightweight prompt, node-local Conda storage, and a bounded
Shiny development job. Import only the pieces that fit your work.

## Choose a component

| Component | What it adds | Best fit |
|---|---|---|
| Shell | `umask 027` and compact Slurm inspection functions | Everyone who regularly submits jobs |
| Prompt | RCC context and the current Slurm job ID without expensive repository scans | Interactive SSH and VS Code terminals |
| Conda | Opt-in node-local environment and package-cache paths, plus a data-science environment | Python, notebooks, machine learning, and AI |
| Shiny | A minimal app, reproducible R environment, and bounded Slurm job | R application development |

[Download the complete starter kit as a ZIP](../../downloads/rcc-account-setup.zip),
or [read its included guide](../../downloads/examples/account-setup/README.md)
before importing it.

## Preview before installing

Download and transfer `rcc-account-setup.zip` to your RCC account. Unpack it,
enter the directory, and preview the proposed setup:

```bash
unzip rcc-account-setup.zip
cd account-setup
bash install.sh
```

Dry-run is the default. It prints every proposed source and destination without
changing the account. Then install only the desired pieces:

```bash
bash install.sh --install --component shell --component prompt
bash install.sh --install --component conda
bash install.sh --install --component shiny
```

The files are placed under `${XDG_CONFIG_HOME:-$HOME/.config}/rcc`. Existing
files are protected unless `--force` is explicitly supplied.

## Activation remains a user decision

The installer never changes `.bashrc`, `.bash_profile`, or another startup file.
It prints optional activation lines. Read the installed files, test them in one
shell, and add only the source lines you want.

The prompt deliberately avoids Git checks, recursive searches, Conda activation,
and network calls each time it is displayed. The Conda helper is also opt-in:
call `rcc-conda-init` only when you need that environment.

## Shiny safety boundary

The Shiny starter runs through Slurm with explicit CPU, memory, and time limits.
It selects a free port and listens only on `127.0.0.1`; use an SSH tunnel based
on the current [access guide](access-ssh-vscode.md). A development tunnel is not
a published service. Follow the governed publication route before sharing an
application with other users.

Treat these files as starting points, not centrally enforced configuration.
Re-check current storage, partition, and software guidance before adopting them.
