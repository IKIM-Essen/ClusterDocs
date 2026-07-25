# Legacy ClusterDocs content audit

This audit records how the public content from `origin/main` at
`8f5b2bd12e3647f79d35e5881aa3bfce3dd1c280` is represented in ClusterDocs NG.
It exists to prevent useful explanations and visual material from disappearing
during the transition while keeping obsolete or unsafe instructions out of the
current path.

## Migration rule

- Preserve the user outcome, explanation, and useful visual orientation.
- Replace machine-specific names with the configured RCC alias or live
  discovery.
- Put computation under Slurm and active high-I/O work on job-local storage.
- Keep historical setup material only where it helps users recognize and
  migrate an existing configuration.
- Label every screenshot that exposes old aliases, paths, ports, versions, or
  UI as historical.
- Do not republish an unsafe procedure merely for completeness.

## Document mapping

| Legacy document | ClusterDocs NG destination | Disposition |
|---|---|---|
| `docs/index.md` | `docs/index.md`, `docs/tldr.md`, `docs/team.md` | Welcome, scope, team context, and optimized cluster image preserved |
| `docs/access.md` | `docs/course/class-01-safe-access.md`, `docs/reference/access-ssh-vscode.md` | Key creation and account request updated; private-key and host-verification rules strengthened |
| `docs/getting-started.md` | Classes 1, 3, and 5; access and resource references | Access, storage, software, hardware-discovery, and remote-work outcomes retained in the staged course |
| `docs/ssh-setup.md` | Class 1 and access reference | Current alias and host-identity migration replace fixed hosts |
| `docs/vs-code-setup.md` | Class 1 and access reference | Text updated; all three screenshots retained with historical labels |
| `docs/first-steps.md` | Course overview; Classes 1, 3, and 5 | First-login, compute discovery, and storage choices expanded into gates |
| `docs/resources.md` | `docs/reference/resources.md` | Static inventory replaced with live scheduler and software discovery |
| `docs/computing.md` | Classes 3, 12, and 13 | Local-versus-remote filesystem guidance expanded and measured |
| `docs/patterns.md` | Classes 3 and 12; troubleshooting reference | Local I/O and VS Code search guidance retained |
| `docs/performance.md` | Classes 3, 12, and 13; resource reference | CPU, RAM, GPU, I/O, and hardware-selection concepts retained without stale node inventory |
| `docs/storage.md` | Classes 3, 12, and 13; storage reference | Local, shared, project, and object-storage roles updated |
| `docs/s3.md` | Class 13 and storage reference | Object semantics and approved-client boundary retained |
| `docs/transfer.md` | Storage reference; instrument transfer guide; Class 14 | SCP/SFTP, archive, checksum, large-data selection, and EGA caution retained; unsafe legacy recipes excluded |
| `docs/accessing-storage.md` | Legacy Windows/macOS guides and storage reference | SSHFS limitations retained; all nine instructional screenshots restored and labeled historical |
| `docs/slurm.md` | Class 5, Slurm reference, execution-model content, and sharing policy | Command coverage, allocations, dependencies, GPUs, etiquette, and cancellation retained with bounded examples |
| `docs/conda.md` | Class 2 and software-workflow reference | Job activation and environment guidance retained |
| `docs/snakemake.md` | Class 2 and software-workflow reference | Installation concepts, profiles, execution, and reproducibility retained in current patterns |
| `docs/apptainer.md` | Class 4 and software-workflow reference | Execution, binds, writable modes, caches, and GPU behavior retained with safer defaults |
| `docs/jupyter.md` | Class 7 and interactive-workflow examples | Slurm and tunnel workflow updated; both screenshots retained with historical-value warnings |
| `docs/troubleshooting.md` | `docs/reference/troubleshooting.md` | Open files, permissions, GPU, VS Code, SSH, Slurm, and interactive diagnostics retained with bounded fixes |
| `docs/upcoming-rcc-changes.md` | `source/future-use/rollout.md`, Class 5, Slurm reference and policies | Slurm-first outcomes retained; speculative announcement archived outside the public site |
| `README.md` | `README.md`, course overview, and repository metadata | Purpose and build/test orientation retained for maintainers |

## Image inventory

| Legacy image | NG use |
|---|---|
| `cluster_barnraiser.png` | Replaced by the visually equivalent optimized `cluster-barnraiser.webp` on the home page; the 10.7 MB original is not duplicated |
| `vs_code_ssh_remote_plugin.png` | Access and VS Code reference |
| `vs_code_ssh_remote_explorer.png` | Access and VS Code reference; old aliases explicitly identified as historical |
| `vs_code_ssh_remote_folder.png` | Access and VS Code reference; old remote label identified as historical |
| `jupyter-home.png` | Class 7 visual orientation; local loopback address highlighted |
| `jupyter-notebook.png` | Class 7 visual orientation; former host, path, user, and versions identified as historical |
| `WinFSP_download.png` | Legacy Windows storage guide |
| `sshfs_win_manager.png` | Legacy Windows storage guide; old port and paths identified as historical |
| `sshfs_win_manager_details1.png` | Legacy Windows storage guide |
| `sshfs_win_manager_details2.png` | Legacy Windows storage guide |
| `sshfs_win_manager_conditions.png` | Legacy Windows storage guide |
| `sshfs_win_manager_settings.png` | Legacy Windows storage guide |
| `ConnectMeNow-share-setup.png` | Legacy macOS storage guide; old alias identified as historical |
| `ConnectMeNow-advanced-setup.png` | Legacy macOS storage guide; personal mount path identified as historical |
| `ConnectMeNow-icon.png` | Legacy macOS storage guide |

## Intentionally excluded or replaced procedures

These legacy details are not copied into current instructions:

- raw Netcat listeners for data transfer, because they lack the required
  authentication and encryption boundary;
- unencrypted legacy FTP submission recipes, including old EGA examples;
- fixed worker, login, shell, project, group, port, and hardware names;
- example notebook tokens and commands that bind Jupyter to all interfaces;
- direct computation outside Slurm;
- automatic background SSH tunnels or mounts as a default recommendation;
- broad recursive permission changes without a scoped diagnosis; and
- static hardware inventories that users could mistake for current capacity.

The relevant user goal is retained through a current approved alternative and,
where useful, an explicit explanation of why the old pattern is unsupported.

## Future audit gate

Before retiring the legacy site, verify that:

1. every public legacy Markdown page appears in the mapping above;
2. every legacy instructional image is either referenced in NG or documented as
   replaced;
3. the NG publication lint and link checker pass;
4. historical screenshots render with meaningful alternative text and adjacent
   warning text; and
5. current endpoint, Slurm, project-storage, biomedical-data, and Lab-network
   rules take precedence over legacy values.
