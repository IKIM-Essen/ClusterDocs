# What changed from the old cluster?

This page is for experienced IKIM cluster users whose habits came from the
original ClusterDocs. The comparison uses the legacy documentation at commit
`8f5b2bd` from 21 July 2026, the source preserved in the repository migration
audit. ClusterDocs NG replaced that public site with release v1.0 on
10 August 2026.

The short version: your account and project work still matter, but access is
more deliberately separated, computation is Slurm-first, projects are the
collaboration boundary, and repeatable workloads should use managed workflows
and immutable runtimes.

## Old habit and current RCC practice

| Topic | Original ClusterDocs | Current RCC practice | What to do now |
|---|---|---|---|
| SSH destination | Users were shown `ssh ikim`, even though the same page said not to work there. | The gateway is forwarding-only; the configured shell-host alias is the user destination. | Use `ssh {{ ssh_target_alias }}` and let `ProxyJump` cross `{{ ssh_gateway_alias }}` automatically. |
| SSH trust | Examples enabled `ForwardAgent yes` and named a fixed public host. | Agent forwarding is off and endpoint values come from the approved current configuration. | Keep `ForwardAgent no`; never copy an old host block blindly. |
| Login systems | Static names and compute-node patterns appeared as things a user could select. | Stable service aliases hide replaceable backends; allocated-node patterns are only for an active Slurm allocation. | Do not configure `login1` or `login2`, and do not choose a worker outside Slurm. |
| Workstation setup | One long mixed Mac, Linux, and Windows page assumed more prior knowledge. | Separate 15-minute macOS and Windows 11 checklists lead to the same safe configuration. RCC Expedition can run without installation. | Start with the checklist for your computer; add VS Code only after terminal SSH works. |
| VS Code | The old guide showed installation, Remote Explorer, and opening a remote folder. | VS Code is the recommended interface, with explicit remote-trust, narrow-workspace, search, file-watching, and Slurm boundaries. | Open one code directory, exclude data and caches, and submit computation through Slurm. |
| Where commands run | Submission nodes were mentioned, while direct-node and transitional practices remained visible. | The jump host forwards, the shell host controls, and Slurm workers compute. | Keep only light editing, Git, submission, monitoring, and workflow control on the shell host. |
| Slurm | The old site documented Slurm alongside direct and transitional cluster use. | Slurm is the normal execution path for batch, interactive, notebook, CPU, memory, and GPU work. | Give every sustained task bounded CPU, memory, time, partition, and GPU requests. |
| Hardware selection | Static worker counts, node ranges, memory sizes, and GPU families were published. | Users request resource capabilities and inspect live scheduler state; operators may replace hardware behind the service. | Use `sinfo` and documented typed GPU selection instead of copying a node name from an old page. |
| Home, group, and project | The three areas were listed, but group and project purposes were easy to blur. | Home is personal, the one primary group is organizational, and a project is the governed research collaboration. | Add people to a project; do not change primary groups or share accounts to exchange project data. |
| Large-team storage | The old site offered folders but little team-scale organization. | A project records owner, purpose, membership, lifecycle, and services, with a documented internal layout. | Keep durable team work under `/projects/<project>/` and document `raw`, `workflows`, `analyses`, `results`, metadata, and archive staging. |
| Temporary storage | `/local/work` was presented as a general manual performance area. | `/local` or `$TMPDIR` is job-local scratch, created and used inside the Slurm task; it is not durable shared storage. | Stage only measured high-I/O work locally and copy declared results back before the job ends. |
| Conda | Users could install and activate environments in home and sometimes inherit an interactive activation into Slurm. | Environment declarations remain useful, but active large environments and caches belong on approved node-local paths; immutable Apptainer images are preferred for repeated deployment. | Keep `environment.yml` or a lock file in Git; do not make a shared-storage environment the production runtime. |
| Snakemake | Users installed versions themselves and older profiles or automatic I/O claims could become stale. | RCC supplies a managed Snakemake command and Slurm profile; rules declare files, software, and realistic resources. | Dry-run first and submit rules through the supported profile; do not place `sbatch` inside rules. |
| Nextflow | It was absent from the original documentation. | Managed Nextflow-to-Slurm is ready now through pinned `rcc-nextflow` on a shell host or documented interactive allocation. | Keep controller and resume state persistent, let Slurm run processes, and use Apptainer for task software. |
| File access and transfer | Detailed SSHFS auto-mount recipes could look like the normal data path. | SSHFS is only for light interactive access. Project Samba is ready for approved projects and registered devices; supported transfer paths handle large data. | Do not browse or synchronize large trees through Finder, Explorer, or VS Code; choose the transfer service for the data size and source. |
| Jupyter and applications | Earlier examples focused on starting tools and opening tunnels. | Interactive tools run inside bounded Slurm allocations and listen only on loopback; production services use a governed route. | Do not expose a notebook, Shiny app, debugger, or ad-hoc web server directly to the network. |
| Biomedical data | The original technical pages had little explicit data-admission guidance. | Current guidance separates direct identifiers and re-identification keys from governed RCC research data and adds project-level review. | Complete the biomedical-data admission check before transfer or analysis. |
| Documentation facts | Screenshots and pages contained fixed endpoints, paths, hardware, and versions. | ClusterDocs labels service state, uses stable aliases, and directs users to live discovery for mutable facts. | Treat an old screenshot as orientation, not configuration. |

## What did not change

Several principles in the original documentation remain correct:

- every researcher uses an individual account and keeps the private SSH key
  private;
- a strong key passphrase is still expected;
- the shell host is not intended for substantial computation;
- durable research work belongs in shared project storage rather than a
  personal home directory;
- Slurm provides scheduled resources;
- Conda is useful for describing scientific software;
- Apptainer supports reproducible container execution; and
- SSHFS is not a bulk-transfer solution.

The new documentation makes these boundaries more consistent and removes
recipes that conflict with them.

## Migration checklist for an existing user

1. Obtain the current RCC SSH configuration through the approved
   institutional channel.
2. Compare it with your saved `~/.ssh/config`; keep unrelated SSH entries
   untouched.
3. Test `ssh -G {{ ssh_target_alias }}`, verify the published host identity,
   and make one bounded connection attempt.
4. Stop using the forwarding gateway or a chosen worker as an interactive work
   destination.
5. Confirm the project that owns each shared dataset and analysis. Move
   collaboration out of personal homes; do not solve access with primary-group
   changes or broad permissions.
6. Review VS Code workspaces. Open only the relevant code directory and exclude
   data, results, Conda environments, and workflow caches from broad search and
   watching.
7. Convert recurring command collections into a strict batch script,
   Snakemake workflow, or managed Nextflow pipeline.
8. Record Conda declarations, then use a pinned Apptainer runtime for repeated
   production tasks where appropriate.
9. Replace static node selection with bounded Slurm resource requests and live
   discovery.
10. Replace large SSHFS copies or automatic mounts with the approved transfer
    route.

Do not delete the entire `known_hosts` file, disable SSH verification, make
recursive permission changes, or move data in bulk merely to make an old setup
look like the new examples. Diagnose and migrate one boundary at a time.

## Where to continue

- [First 15 minutes](index.md)
- [Jump host, shell host, and compute worker](../concepts/jump-shell-compute.md)
- [Use VS Code with RCC](vscode.md)
- [Users, groups, projects, and large-team storage](../reference/users-groups-projects.md)
- [Convert scripts into a repeatable workflow](../paths/from-shell-scripts.md)
- [Storage and transfer reference](../reference/storage-transfer.md)
