# RCC should make good computing paths easy (future-use guide)

> **Design proposal, not a released RCC feature.** This is a generic lesson
> candidate for the future site-neutral ClusterDocs core. The current Essen
> site must not publish it as an available service before operator acceptance.

## You do not have to become a cluster administrator to do research

Many researchers already have a comfortable method for their own scientific
work. Sometimes that familiar method becomes frustrating on a shared cluster:
a Python script that worked on a laptop needs more memory, a search takes
forever, or an editor loses its connection. Knowledge of Bash, R, Python or
notebooks does not automatically include knowledge of Slurm, shared storage
or secure remote sessions.

**RCC's job is to make a better path easy to discover and easy to use.**
We should guide people without guessing how experienced they are, testing
their expertise or requiring them to learn every layer first.

## Choose the interface you prefer

**Start in your browser** when you want the fewest installation steps: choose
an approved project, explore or run a managed analysis.

Prefer an editor? Use **Positron** for R or **VS Code** for Python and
shell development. The graphical application stays on your laptop;
the remote backend and scientific computation run in a Slurm allocation.

Prefer a terminal? Continue with **SSH and Slurm commands**. You do not need
to prove you are an "expert". The same project permissions, resource limits,
and security requirements apply to everyone.

You can switch interfaces when your work changes. A simple/detailed control
view is just a presentation preference; it is not a change of privilege.

## Helpful alternatives instead of dead ends

| You encounter... | RCC should help you do this... |
| --- | --- |
| "My Python/R script overwhelms the shellhost" | Offer a bounded Slurm development or batch allocation, with a preview and an easy way to open the same project |
| "I want to search everything with `rg`" | Offer a search of the current small code directory, not all shared storage, and explain how to choose another narrow subtree |
| "I have 500 independent samples" | Suggest a Slurm job array or reproducible workflow instead of one enormous interactive process |
| "I need more than one machine" | Offer a reviewed multi-node Slurm batch request, explaining that the program must already support its task layout |
| "My VS Code/Positron connection dropped" | Find an existing allocation by its job ID; reconnect safely instead of starting another job |
| "There is no compute capacity available now" | Show the real queue/denial reason and permitted alternatives, without claiming that the work has started |
| "I do not know how much memory to ask for" | Suggest a conservative profile, explain it, and improve later from Slurm job measurements when available |

These are **proposed experience goals**, not claims that the software already
performs all of them. The current CLI, batch support, browser interface,
installer and site acceptance each have their own implementation gates.

## What a good message sounds like

> Your analysis needs more resources than a shared shellhost should use.
> You can run it as a Slurm job without changing your project files.
> Review the proposed memory, CPUs and duration, or choose another allowed
> configuration.

Or, for a potentially expensive search:

> That folder contains more than source code and may generate heavy shared
> storage activity. Would you like to search only the current code folder?
> You can inspect the exact search location before continuing.

Good guidance explains the consequence and offers an immediate usable action.
It does not say the user is wrong, shame them for using shell commands, hide
alternatives or silently alter their scientific method.

## What remains important even with a better interface

- **Slurm** still selects resources and starts permitted compute tasks.
- **RCC project permissions** still govern the data you may access.
- The **shellhost** remains a lightweight entry and submission point.
- A desktop setting cannot enforce a security boundary or prevent every
  filesystem-wide search; server-side controls still matter.
- **Saving work** means retaining valuable files in durable project storage,
  not only on an allocated worker's temporary disk.
- A disconnected session may still be running. Before restarting, inspect
  the existing job; repeated submission can waste resources.
- Neither a web page nor an AI recommendation grants extra privileges or
  guarantees resource availability.

## A short guided first experience

1. Choose **your project**.
2. Choose **what you want to accomplish** (explore, develop, process many
   samples, run a larger job).
3. Review **one suggested path**; optionally switch to browser, VS Code,
   Positron or terminal and open **Details**.
4. Check **where work runs** and **where results go**.
5. Start only after the site has admitted that service and your project has
   access. Follow a clear queued/running/completed status.
6. If something fails, see the next safe action and preserve your existing
   job/results rather than starting from scratch.

No formal course or self-declared expertise category is required to choose a
tool. Short concept explanations should be available exactly when useful.
Advanced documentation should remain accessible at any point.

Continue with [choose your environment](01-choose-your-environment.md),
[Slurm and data](05-slurm-and-data.md),
[recover a session](06-troubleshooting.md), or
[multi-node batch workloads](10-multinode-batch.md).

For the planned RCC implementation contract, see the companion source-only
`docs/ux/researcher-paths-and-gentle-guidance.md` in the RCC repository.
