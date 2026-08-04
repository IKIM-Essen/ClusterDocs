# Class 12: From notebooks to governed project services — video narration

## Slide 1: Class 12: From notebooks to governed project services

Welcome to Class 12: From notebooks to governed project services. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning goals

After this class, you can: choose between notebook, batch job, Shiny app, Python web app, and vhost; separate interactive presentation from expensive computation; package a small service for review; write a minimal release note for project users; avoid patterns that leak data or overload shared infrastructure.

## Slide 3: Service boundary

A governed web app should be a presentation and coordination layer. It may read approved data, collect small forms, start reviewed workflows, or display curated results. It should not perform long-running analysis inside the web request. A good pattern is: The web app validates input. The app writes a small request record. A Slurm workflow performs the heavy computation. The app displays completed results. Logs and receipts keep the action attributable to a named user.

## Slide 4: Completion gate

Use the vhost request checklist from Class 8 and add one architectural sentence: Heavy computation for this service will run through Slurm, while the web app only handles authentication, parameter collection, status display, and curated result access. If that sentence is false, redesign the application before requesting a vhost.
