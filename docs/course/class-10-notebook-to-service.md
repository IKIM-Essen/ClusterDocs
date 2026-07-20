# Class 10: From notebooks to governed project services

This includes model-backed research services. A trained model, embedding index,
or AI inference endpoint inherits the governance of its source data and requires
the same reviewable service boundary as any other protected project application.

This class helps you decide when a notebook should remain a notebook, when a Shiny or Python web app is appropriate, and when computation should move into a Slurm workflow.

## Learning goals

After this class, you can:

- choose between notebook, batch job, Shiny app, Python web app, and vhost;
- separate interactive presentation from expensive computation;
- package a small service for review;
- write a minimal release note for project users;
- avoid patterns that leak data or overload shared infrastructure.

## Decision guide

| Need | Best pattern |
|---|---|
| Explore data and make notes | Notebook in a Slurm allocation |
| Repeat an analysis reliably | Slurm batch job or Snakemake workflow |
| Let a small team adjust parameters interactively | Shiny or Python app behind the gateway |
| Publish static instructions or reports | Static information vhost |
| Provide a dashboard against approved data | Active read-only vhost |
| Process large uploads | Upload vhost plus backend Slurm workflow |

## Service boundary

A governed web app should be a presentation and coordination layer. It may read approved data, collect small forms, start reviewed workflows, or display curated results. It should not perform long-running analysis inside the web request.

A good pattern is:

1. The web app validates input.
2. The app writes a small request record.
3. A Slurm workflow performs the heavy computation.
4. The app displays completed results.
5. Logs and receipts keep the action attributable to a named user.

## Preparing for review

Before asking for a vhost, prepare:

- project name and project lead;
- who may access the application;
- whether it is static, read-only, standard, or upload-capable;
- the deployment source and version;
- data sources and whether they contain sensitive content;
- resource expectations;
- support contact and review date.

## Completion gate

Use the vhost request checklist from Class 6 and add one architectural sentence:

> Heavy computation for this service will run through Slurm, while the web app only handles authentication, parameter collection, status display, and curated result access.

If that sentence is false, redesign the application before requesting a vhost.

## Self-check questions

1. What is the risk of doing large computation inside a web request?
2. Why should project access be granted through group membership instead of account sharing?
3. How does a vhost differ from a tunnelled notebook or Shiny session?
4. What evidence should be available after a user uploads or downloads data?
