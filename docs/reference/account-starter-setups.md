# RCC account setup patterns

These optional patterns can make an interactive shell, prompt, Conda setup, or
Shiny development job easier to use. Apply only the pieces that fit your work;
RCC no longer publishes a downloadable account-setup bundle.

## Choose a component

| Component | What it adds | Best fit |
|---|---|---|
| Shell | `umask 027` and compact Slurm inspection functions | Everyone who regularly submits jobs |
| Prompt | RCC context and the current Slurm job ID without expensive repository scans | Interactive SSH and VS Code terminals |
| Conda | Opt-in node-local environment and package-cache paths, plus a data-science environment | Python, notebooks, machine learning, and AI |
| Shiny | A minimal app, reproducible R environment, and bounded Slurm job | R application development |

## Apply patterns deliberately

Keep optional configuration under `${XDG_CONFIG_HOME:-$HOME/.config}/rcc` and
review it before sourcing it from a shell startup file. Test one change in one
interactive shell first, and preserve any existing configuration. If your team
needs a shared setup, maintain it in the project's reviewed source repository
rather than copying an unversioned bundle between accounts.

## Activation remains a user decision

Do not let an account-setup script change `.bashrc`, `.bash_profile`, or another
startup file without an explicit review. Read the proposed files, test them in
one shell, and add only the source lines you want.

The prompt deliberately avoids Git checks, recursive searches, Conda activation,
and network calls each time it is displayed. The Conda helper is also opt-in:
call `rcc-conda-init` only when you need that environment.

## Shiny safety boundary

The Shiny starter runs through Slurm with explicit CPU, memory, and time limits.
It selects a free port and listens only on `127.0.0.1`; use an SSH tunnel based
on the current [access guide](access-ssh-vscode.md). A development tunnel is not
a published service. Follow the governed publication route before sharing an
application with other users.

Treat these patterns as starting points, not centrally enforced configuration.
Re-check current storage, partition, and software guidance before adopting them.
