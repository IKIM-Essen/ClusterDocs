# RCC Onboarding Class 10 narration: From notebooks to services

**Estimated duration:** 7-8 minutes

This class is about choosing the right form for your work. A notebook is excellent for exploration. A Slurm job is better for repeatable computation. A Shiny or Python web app is useful when a team needs an interactive interface. A governed vhost is the production path for project web services.

The mistake to avoid is putting everything into the web request. A browser click should not start uncontrolled computation inside the web process. Instead, the app validates the request, records it, and hands heavy work to Slurm. When the workflow finishes, the app displays curated results.

This pattern protects users, developers, and the cluster. Users get a simple interface. Developers get a maintainable service. Operations can enforce authentication, project-group membership, logging, and resource limits.

Before requesting a vhost, prepare the project owner, user group, data source, version, support contact, and review date. If the service needs to run long jobs, say explicitly how those jobs will be scheduled.

The class is complete when you can write one sentence explaining the service boundary: what the web app does, what Slurm does, and what data the user is allowed to see.
