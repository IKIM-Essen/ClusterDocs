# RCC account starter setups

These optional examples provide small, reviewable defaults for an RCC account.
They do not replace the course or current operational guidance.

## Preview first

```bash
bash install.sh
```

Dry-run is the default and changes nothing. To install selected components:

```bash
bash install.sh --install --component shell --component prompt
bash install.sh --install --component conda
bash install.sh --install --component shiny
```

Files go to `${XDG_CONFIG_HOME:-$HOME/.config}/rcc`. Existing files are not
replaced unless `--force` is explicitly supplied. The installer never edits
`.bashrc`, `.bash_profile`, or another startup file; it prints optional source
lines for the user to review and add manually.

## Components

- **Shell:** private-by-default file permissions and compact Slurm inspection
  functions.
- **Prompt:** an inexpensive RCC marker and the current Slurm job ID, without a
  Git or filesystem scan on every prompt.
- **Conda:** an opt-in helper for node-local environment and package-cache paths,
  plus a modest data-science environment definition.
- **Shiny:** a small app, environment, and bounded Slurm submission script that
  listens only on `127.0.0.1`.

Review every file before activation. Adapt resource requests to measurements
and current RCC policy; do not add credentials, patient identifiers, or project
data to these templates.
