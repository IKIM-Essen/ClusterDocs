# RCC Onboarding Class 9 narration: Shiny applications

**Estimated duration:** 7-8 minutes

Shiny is a good way to give colleagues an interactive view of results. But a Shiny app has to be treated differently depending on the audience.

For one developer or a small demonstration, Shiny can run in a Slurm allocation and listen only on loopback. You connect through an SSH tunnel, just like with Jupyter. This is development mode. It is not a production service.

For other users, a Shiny app must go through the governed vhost process. The gateway handles authentication. The app must know which project group is allowed. The data source must be reviewed. The application must not simply expose a project directory through the browser.

A safe Shiny app usually reads a curated table, a database view, or a small result collection. If it accepts uploads, those uploads go into a staging area and are validated before they become part of a project collection. Expensive computation belongs in Slurm, not in a browser request.

The class is complete when you can run the Shiny development example and then decide whether your own app is a tunnelled demo or a governed project service.
