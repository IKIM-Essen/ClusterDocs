# Software development path

Use this path when your main goal is to build reproducible research software,
workflow automation, containers, protected applications, Shiny interfaces, or
model-backed services.

## 1. Build the shared foundation

| Step | Learn | Why it matters |
|---|---|---|
| [Class 1](../course/class-01-safe-access.md) | Safe SSH and VS Code Remote SSH | Develop through an individual, verified account |
| [Class 2](../course/class-02-workflows.md) | Project structure, Git, environments, and Snakemake | Make changes reviewable and repeatable |
| [Class 5](../course/class-05-slurm.md) | Slurm execution patterns | Keep sustained work off login hosts |
| [Class 4](../course/class-04-containers.md) | Immutable Apptainer images | Package reviewed runtimes reproducibly |

## 2. Choose the software shape

The optional [account starter setups](../reference/account-starter-setups.md)
provide importable shell and prompt helpers, a Conda baseline, and a bounded
Shiny project. Each component can be previewed and installed independently.

| Goal | Continue with |
|---|---|
| Batch analysis or dependency graph | [Class 2: workflows](../course/class-02-workflows.md) |
| Python analysis package or notebook workflow | [Class 7: Python](../course/class-07-python-notebooks.md) |
| R analysis package or report | [Class 8: R](../course/class-08-r-analysis.md) |
| Shiny application | [Class 9: Shiny](../course/class-09-shiny.md) |
| Protected project website or API | [Class 6: project websites](../course/class-06-vhosts.md) |
| Notebook or model promoted to a service | [Class 10: notebook to service](../course/class-10-notebook-to-service.md) |

## 3. Design for review and operation

Keep configuration separate from code. Validate inputs, bound CPU, memory,
storage, request size, concurrency, and execution time. Run expensive work
through Slurm and return later for results instead of keeping a web request
open. Use read-only inputs and narrowly scoped write locations.

Record dependencies, image digests, migrations, tests, logs, health checks,
backup expectations, and an owner. Never embed credentials, patient identifiers,
internal topology, or project data in Git or container images.

## 4. Publish through the governed route

A local demonstration is not a production deployment. Complete the Class 6
application contract and request workflow before publication. Authentication,
reverse proxying, TLS, logging, lifecycle management, data protection, and
incident handling remain part of the reviewed RCC service boundary.
