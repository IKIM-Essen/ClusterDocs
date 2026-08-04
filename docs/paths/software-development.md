# Software development path

Use this path when your main goal is to build reproducible research software,
workflow automation, containers, protected applications, Shiny interfaces, or
model-backed services.

> **Service status:** RCC Admin, RCC workers, and Slurm workflows are **ready
> now**. Project vhost hosting is **not yet released**; website and service
> classes currently prepare future requests and applications.

Use VS Code with Remote - SSH as the default editor and project interface unless
your team has a reviewed alternative. Open the smallest useful repository,
exclude data and generated trees from search and file watching, and submit
sustained work from the integrated terminal through Slurm.

## 1. Build the shared foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 1](../course/class-01-safe-access.md) | Safe SSH and VS Code Remote SSH | Develop through an individual, verified account |
| [Class 2](../course/class-02-workflows.md) | Project structure, Git, environments, and Snakemake | Make changes reviewable and repeatable |
| [Class 5](../course/class-05-slurm.md) | Slurm execution patterns | Keep sustained work off login hosts |
| [Class 4](../course/class-04-containers.md) | Immutable Apptainer images | Package reviewed runtimes reproducibly |

## 2. Choose the software shape

The optional [account setup patterns](../reference/account-starter-setups.md)
describe reviewable shell, prompt, Conda, and bounded Shiny practices.

| Goal | Continue with |
|---|---|
| Batch analysis or dependency graph | [Class 2: workflows](../course/class-02-workflows.md) |
| Python analysis package or notebook workflow | [Class 7: Python](../course/class-07-python-notebooks.md) |
| R analysis package or report | [Class 8: R](../course/class-08-r-analysis.md) |
| Shiny application | [Class 9: Shiny](../course/class-09-shiny.md) |
| Future protected project website or API | [Class 6: project websites — not yet released](../course/class-06-vhosts.md) |
| Notebook or model prepared for a future service | [Class 10: notebook to service](../course/class-10-notebook-to-service.md) |
| I/O-intensive workflow or temporary database | [Class 12: efficient local I/O](../course/class-12-efficient-io.md) |
| Storage-path or cache diagnosis | [Class 13: storage architecture](../course/class-13-storage-architecture.md) |

## 3. Design for review and operation

Keep configuration separate from code. Validate inputs, bound CPU, memory,
storage, request size, concurrency, and execution time. Run expensive work
through Slurm and return later for results instead of keeping a web request
open. Use read-only inputs and narrowly scoped write locations.

Record dependencies, image digests, migrations, tests, logs, health checks,
backup expectations, and an owner. Never embed credentials, patient identifiers,
internal topology, or project data in Git or container images.

## 4. Publish through the governed route

A local demonstration is not a production deployment. Project vhosts are not
yet released. Use Class 6 to prepare the application contract and future
request, but do not present it as deployed. After release, authentication,
reverse proxying, TLS, logging, lifecycle management, data protection, and
incident handling will remain part of the reviewed RCC service boundary.
