# Class 11: Shiny applications on RCC — video narration

## Slide 1: Class 11: Shiny applications on RCC

Welcome to Class 11: Shiny applications on RCC. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning goals

After this class, you can: run a small Shiny app inside a Slurm allocation; explain why tunnelled development is different from production hosting; avoid direct exposure of project files; design a Shiny app that uses curated data rather than browsing the filesystem; prepare the information needed for a governed vhost request.

## Slide 3: Development mode

Copy the example: Read the job output and use the SSH tunnel shown there. The Shiny process binds to 127.0.0.1 on the worker. This is a development pattern only. It is not a public service and it is not a replacement for the vhost process.

## Slide 4: Safe data pattern

A Shiny app should not receive a raw mount of an entire project directory. Use one of these safer patterns: a read-only SQLite, DuckDB, or PostgreSQL view; a curated result directory with approved files; opaque file IDs rather than user-supplied paths; a separate upload staging area for write workflows.

## Slide 5: Common mistakes

Running Shiny on a login host. Binding Shiny to every network interface. Sharing the URL to a worker port without a tunnel. Letting users type arbitrary filesystem paths. Using a personal account as the application identity. Skipping the vhost request because the demo worked for one person.

## Slide 6: Completion gate

Run the local example validation: Then run the Shiny development job once, open it through the tunnel, and stop it with scancel. The class is complete when you can explain whether your app is a one-person development session or a governed project service.
