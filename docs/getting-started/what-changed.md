# What changed from the old cluster?

This page is for experienced IKIM cluster users whose habits came from the
original ClusterDocs. The comparison uses the legacy documentation at commit
`8f5b2bd` from 21 July 2026, preserved in the repository migration audit. The
previous ClusterDocs generation replaced that public site with release v1.0 on
10 August 2026.

The short version: RCC is no longer presented primarily as a login host plus
shared filesystem. It is a project-centric research platform with browser
surfaces, governed workflows, Slurm-backed compute, instrument ingestion,
object-storage options, lifecycle services, and AI assistance.

But the most important technical lesson behind the redesign is simpler:
**I/O pattern matters more than raw storage bandwidth.** The new platform and
workflow guidance are designed to keep pathological metadata/random/temp I/O
off shared storage whenever possible.

> **Stage-2 video plan:** after the written release is stable, publish one short
> **3–4 minute “What changed from the old cluster?” video** for returning users.
> It should summarize the browser/project/workflow changes, spend the largest
> technical segment on I/O behavior and local scratch, show the RCC-safe VS Code
> settings, and point to this page for detail. The written page remains the
> authoritative source; the video is not a Stage-1 release dependency.

## The biggest architectural change: design around I/O behavior

The old mental model made it easy to think primarily in terms of CPU count,
storage capacity, or advertised network/storage bandwidth. RCC experience showed
that many real scientific slowdowns and shared-service incidents are driven by
**access pattern**, especially:

- hundreds of thousands or millions of small files;
- repeated `stat`/directory scans and file opens;
- Conda/package trees on shared filesystems;
- workflow work directories and temporary databases on shared storage;
- many jobs simultaneously fetching the same references or containers;
- editor/search/indexer activity across large data trees; and
- random temporary I/O that could have happened on node-local scratch.

This was a major reason not to assume that moving everything onto a different
popular storage/orchestration platform—whether Ceph, Kubernetes, or another
single substrate—would solve the research workload. A different backend cannot
make a hostile I/O pattern free.

The preferred RCC model is therefore:

```text
durable project data
       -> scheduled Slurm job
       -> stage active working set locally when useful
       -> temporary/random/high-I/O work on node-local scratch
       -> validate outputs
       -> return only durable results to project storage
```

Read [Class 14: efficient I/O](../course/class-14-efficient-io.md),
[Class 15: storage architecture](../course/class-15-storage-architecture.md), and
[Why RCC does not run everything on Kubernetes](../concepts/why-not-kubernetes-everywhere.md).

## Old habit and current RCC practice

| Topic | Original ClusterDocs | Current RCC practice | What to do now |
|---|---|---|---|
| SSH destination | Users were shown `ssh ikim`, even though the same page said not to work there. | The gateway is forwarding-only; the configured shell-host alias is the user destination. | Use `ssh {{ ssh_target_alias }}` and let `ProxyJump` cross `{{ ssh_gateway_alias }}` automatically. |
| SSH trust | Examples enabled `ForwardAgent yes` and named a fixed public host. | Agent forwarding is off and endpoint values come from the approved current configuration. | Keep `ForwardAgent no`; never copy an old host block blindly. |
| SSH key passphrases | Generic cluster guidance often treated a memorized key passphrase as mandatory. | RCC does **not** recommend a passphrase on the normal software-backed RCC SSH key; endpoint protection and private-key handling remain mandatory, with hardware-backed FIDO keys preferred where appropriate. | Follow the current RCC `ssh-keygen` command rather than adding a passphrase from a generic tutorial. |
| Web credentials | Passwords, passkeys, and recovery material were not clearly separated from SSH keys. | Web/account credentials use the supported Windows/macOS/browser credential-manager and passkey facilities or another approved manager. | Store web passwords/passkeys/recovery material in the supported credential manager; do not turn that into an SSH-key passphrase requirement. |
| Normal first-use path | Shell access was the implicit starting point. | Browser-first Files/account/project surfaces are legitimate first-class entry points; RCC Analysis adds Notebook/Workflow when released. | Start with the research task. Add SSH only when the work actually requires the advanced path. |
| Login systems | Static names and compute-node patterns appeared as things a user could select. | Stable service aliases hide replaceable backends; allocated-node patterns are only for an active Slurm allocation. | Do not configure `login1` or `login2`, and do not choose a worker outside Slurm. |
| Workstation setup | One long mixed Mac, Linux, and Windows page assumed more prior knowledge. | Separate macOS and Windows 11 checklists lead to the same safe advanced configuration. RCC Expedition can run without installation. | Start with the browser path unless you need the advanced SSH/developer route. |
| VS Code | The old guide showed installation, Remote Explorer, and opening a remote folder. | VS Code remains available for advanced development, but its search/watch/index behavior is treated as a real shared-I/O workload. | Open one small code directory and apply the [RCC-safe low-I/O settings](vscode.md#rcc-safe-vs-code-defaults) before working in large projects. |
| Where commands run | Submission nodes were mentioned, while direct-node and transitional practices remained visible. | The jump host forwards, the shell host controls, and Slurm workers compute. | Keep only light editing, Git, submission, monitoring, and workflow control on the shell host. |
| Slurm | The old site documented Slurm alongside direct and transitional cluster use. | Slurm is the normal execution authority for batch, interactive, notebook, CPU, memory, and GPU work. | Give every sustained task bounded CPU, memory, time, partition, and GPU requests. |
| Temporary/high-I/O work | Shared storage was too easily treated like local disk. | `/local` or `$TMPDIR` is job-local scratch for active temporary/random I/O; durable inputs/results stay in the project. | Stage measured high-I/O working sets locally and return declared outputs. |
| Hardware selection | Static worker counts, node ranges, memory sizes, and GPU families were published. | Users request resource capabilities and inspect live scheduler state; operators may replace hardware behind the service. | Use live discovery and typed resource requests instead of copying a node name from an old page. |
| Home, group, and project | The three areas were listed, but group and project purposes were easy to blur. | Home is personal, the one primary group is organizational, and a project is the governed research collaboration. | Add people to a project; do not change primary groups or share accounts to exchange project data. |
| Large-team storage | The old site offered folders but little team-scale organization. | A project records owner, purpose, membership, lifecycle, storage/services, and an internal data layout. | Keep durable team work under `/projects/<project>/`; separate raw, workflows, analyses/results, metadata, and archive staging. |
| Storage semantics | Shared POSIX was the dominant visible model. | Projects can use POSIX, S3/object storage where separately enabled, DataLad-backed state, and local scratch according to workload semantics. | Choose storage by access pattern and lifecycle rather than treating one backend as universal. |
| Conda | Users could install and activate environments in home and sometimes inherit an interactive activation into Slurm. | Environment declarations remain useful, but active large environments/caches should not become massive shared-small-file workloads; immutable Apptainer images are preferred for repeated deployment. | Keep environment definitions in Git and avoid turning shared storage into a package filesystem. |
| Snakemake | Users installed versions themselves and older profiles or automatic I/O claims could become stale. | RCC supplies a managed Snakemake route; rules declare files, software, resources, and staging behavior. | Dry-run first and submit rules through the supported profile; do not place `sbatch` inside rules. |
| Nextflow | It was absent from the original documentation. | Managed Nextflow-to-Slurm is ready now through pinned `rcc-nextflow` on a shell host or documented interactive allocation. | Keep controller and resume state persistent, let Slurm run processes, and use Apptainer for task software. |
| File access and transfer | Detailed SSHFS auto-mount recipes could look like the normal data path. | SSHFS is only for light interactive access. Project Samba is ready for approved projects and registered devices; supported transfer paths handle larger/recurring data. | Do not browse or synchronize large trees through Finder, Explorer, VS Code, or SSHFS. |
| Jupyter and applications | Earlier examples focused on starting tools and opening tunnels. | Interactive tools run inside bounded Slurm allocations; long-lived project/control services belong to the service plane. | Do not expose a notebook, Shiny app, debugger, or ad-hoc web server directly to the network. |
| AI assistance | External AI tools were not part of the cluster model. | Agents can help from documentation, public code, schemas, synthetic fixtures, and bounded diagnostics; real protected data stays governed in RCC by default. | Use the data-blind agent path unless a separately approved local data-near capability exists. |
| Biomedical data | The original technical pages had little explicit data-admission guidance. | Current guidance separates direct identifiers and re-identification keys from governed RCC research data and adds project-level review. | Complete the biomedical-data admission check before transfer or analysis. |
| Documentation facts | Screenshots and pages contained fixed endpoints, paths, hardware, and versions. | ClusterDocs labels service state, uses stable aliases, and directs users to live discovery for mutable facts. | Treat an old screenshot as orientation, not configuration. |

## What did not change

Several principles remain correct:

- every researcher uses an individual account and keeps any SSH private key private and local;
- the shell host is not intended for substantial computation;
- durable research work belongs in shared project storage rather than a personal home directory;
- Slurm provides scheduled scientific resources;
- reproducible software declarations matter;
- Apptainer supports reproducible scientific container execution; and
- SSHFS is not a bulk-transfer or high-I/O analysis solution.

## Migration checklist for an existing user

1. Start from the [current task-first entry page](index.md) rather than assuming SSH is required.
2. If you still use SSH, obtain the current configuration through the approved institutional channel and compare it with your saved `~/.ssh/config`.
3. If your old RCC software key has a passphrase, do not treat that as the new policy. Follow current replacement guidance when you rotate it.
4. Stop using the forwarding gateway or a chosen worker as an interactive work destination.
5. Confirm the project that owns each shared dataset and analysis; do not solve collaboration with primary-group changes or broad permissions.
6. Review VS Code workspaces. Open only the relevant source/workflow directory and apply the [RCC-safe VS Code defaults](vscode.md#rcc-safe-vs-code-defaults).
7. Identify workflows that repeatedly scan or write shared storage; move temporary/random/high-I/O work to job-local scratch when appropriate.
8. Convert recurring command collections into a strict batch script, Snakemake workflow, or managed Nextflow pipeline.
9. Record software/environment identity and prefer pinned reusable runtimes where appropriate.
10. Replace static node selection with bounded Slurm resource requests and live discovery.
11. Replace large SSHFS copies, editor-driven data traversal, or automatic mounts with an approved transfer/ingestion route.

Do not delete the entire `known_hosts` file, disable SSH verification, make
recursive permission changes, or move data in bulk merely to make an old setup
look like the new examples. Diagnose and migrate one boundary at a time.

## Where to continue

- [First 15 minutes](index.md)
- [RCC-safe VS Code settings](vscode.md#rcc-safe-vs-code-defaults)
- [Efficient I/O](../course/class-14-efficient-io.md)
- [Storage architecture](../course/class-15-storage-architecture.md)
- [Why not Kubernetes everywhere?](../concepts/why-not-kubernetes-everywhere.md)
- [Users, groups, projects, and large-team storage](../reference/users-groups-projects.md)
- [Convert scripts into a repeatable workflow](../paths/from-shell-scripts.md)
- [Storage and transfer reference](../reference/storage-transfer.md)