# Class 9: Shiny applications on RCC

Shiny is useful when a project needs an interactive browser view for plots, parameters, and curated results. On RCC there are two separate modes:

1. **Development or demonstration:** Shiny runs in a Slurm allocation and you connect through an SSH tunnel.
2. **Service for other users:** the application must go through the governed vhost process described in Class 6.

## Learning goals

After this class, you can:

- run a small Shiny app inside a Slurm allocation;
- explain why tunnelled development is different from production hosting;
- avoid direct exposure of project files;
- design a Shiny app that uses curated data rather than browsing the filesystem;
- prepare the information needed for a governed vhost request.

## Development mode

Copy the example:

```bash
cp -a examples/interactive-workflows/shiny my-shiny-app
cd my-shiny-app
sbatch shiny.sbatch
```

Read the job output and use the SSH tunnel shown there. The Shiny process binds to `127.0.0.1` on the worker. This is a development pattern only. It is not a public service and it is not a replacement for the vhost process.

## What makes Shiny production-ready?

A production Shiny service needs:

- an identified project owner and technical contact;
- authentication through the RCC gateway;
- project-group authorization;
- resource limits;
- application logs;
- a defined deployment version;
- reviewed data access;
- a retirement date or review date.

## Safe data pattern

A Shiny app should not receive a raw mount of an entire project directory. Use one of these safer patterns:

- a read-only SQLite, DuckDB, or PostgreSQL view;
- a curated result directory with approved files;
- opaque file IDs rather than user-supplied paths;
- a separate upload staging area for write workflows.

## Common mistakes

- Running Shiny on a login host.
- Binding Shiny to every network interface.
- Sharing the URL to a worker port without a tunnel.
- Letting users type arbitrary filesystem paths.
- Using a personal account as the application identity.
- Skipping the vhost request because the demo worked for one person.

## Completion gate

Run the local example validation:

```bash
python3 exercises/interactive/validate-interactive-examples.py
```

Then run the Shiny development job once, open it through the tunnel, and stop it with `scancel`. The class is complete when you can explain whether your app is a one-person development session or a governed project service.

## Self-check questions

1. Why is a tunnelled Shiny job not a production web service?
2. Why should a Shiny app not browse `/projects` directly?
3. Which information must a project lead provide for a governed vhost request?
4. What should happen when a Shiny app needs heavy computation?
