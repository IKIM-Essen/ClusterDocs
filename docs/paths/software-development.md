# Software development path

Use this path when your main goal is to build reproducible research software,
workflow automation, containers, protected applications, Shiny interfaces, or
model-backed services.

> **Service status:** RCC Admin, RCC workers, and Slurm workflows are **ready
> now**. The newer general RCC-authenticated Gitea access plane, Workbench, and
> project-vhost hosting are rollout-gated/not yet released as general user
> surfaces; the linked pages document their stable product boundary without
> claiming activation.

Use VS Code with Remote - SSH as the default editor and project interface unless
your team has a reviewed alternative. Open the smallest useful repository,
exclude data and generated trees from search and file watching, and submit
sustained work from the integrated terminal through Slurm.

## 1. Build the shared foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 1](../course/class-01-safe-access.md) | Safe SSH and VS Code Remote SSH | Develop through an individual, verified account |
| [Class 2](../course/class-02-workflows.md) | Project structure, Git, and environments | Make changes reviewable and repeatable |
| [Class 5](../course/class-05-slurm.md) | Slurm execution patterns | Keep sustained work off login hosts |
| [Class 6](../course/class-06-snakemake.md) | Managed Snakemake | Turn dependency graphs into bounded Slurm jobs |
| [Class 7](../course/class-07-nextflow.md) | Ready-now managed Nextflow and nf-core | Run reviewed pipelines through Slurm and Apptainer |
| [Class 4](../course/class-04-containers.md) | Immutable Apptainer images | Package reviewed runtimes reproducibly |

## 2. Use source control deliberately

Read [RCC Gitea: source control inside RCC](../concepts/rcc-gitea.md) for the
stable source-control model.

The key boundaries are:

- RCC browser identity and repository ACLs are separate;
- project filesystem membership does not automatically grant repository write
  access;
- Git/OCI browser sessions do not become general machine credentials;
- credentials and research datasets do not belong in Git history; and
- users should depend on the stable RCC service identity rather than a
  transitional physical host.

Until the general RCC-authenticated Gitea access plane is explicitly announced,
continue using the currently approved repository route for your team.

## 3. Choose the software shape

The optional [account setup patterns](../reference/account-starter-setups.md)
describe reviewable shell, prompt, Conda, and bounded Shiny practices.

For existing scripts or command collections, start with the
[script-to-workflow conversion guide](from-shell-scripts.md).

| Goal | Continue with |
|---|---|
| Batch analysis or dependency graph | [Class 6: Snakemake](../course/class-06-snakemake.md) |
| Reviewed Nextflow or nf-core pipeline | [Class 7: Nextflow](../course/class-07-nextflow.md) |
| Python analysis package or notebook workflow | [Class 9: Python](../course/class-09-python-notebooks.md) |
| R analysis package or report | [Class 10: R](../course/class-10-r-analysis.md) |
| Shiny application | [Class 11: Shiny](../course/class-11-shiny.md) |
| Future protected project website or API | [Class 8: project websites — not yet released](../course/class-08-vhosts.md) |
| Notebook or model prepared for a future service | [Class 12: notebook to service](../course/class-12-notebook-to-service.md) |
| I/O-intensive workflow or temporary database | [Class 14: efficient local I/O](../course/class-14-efficient-io.md) |
| Storage-path or cache diagnosis | [Class 15: storage architecture](../course/class-15-storage-architecture.md) |
| Versioned large-dataset state | [Managed DataLad](../data/datalad-managed-service.md) when enabled for the project |

## 4. Design for review and operation

Keep configuration separate from code. Validate inputs, bound CPU, memory,
storage, request size, concurrency, and execution time. Run expensive work
through Slurm and return later for results instead of keeping a web request
open. Use read-only inputs and narrowly scoped write locations.

Record dependencies, image digests, migrations, tests, logs, health checks,
backup expectations, and an owner. Never embed credentials, patient identifiers,
internal topology, or project data in Git or container images.

## 5. Publish through the governed route

A local demonstration is not a production deployment. Project vhosts are not
yet released. Use Class 8 to prepare the application contract and future
request, but do not present it as deployed. After release, authentication,
reverse proxying, TLS, logging, lifecycle management, data protection, and
incident handling will remain part of the reviewed RCC service boundary.
