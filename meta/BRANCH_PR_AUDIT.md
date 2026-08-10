# ClusterDocs branch and pull-request audit

Audit date: 9 August 2026

This audit covers the single GitHub repository `IKIM-Essen/ClusterDocs`, its
`main` and `clusterdocs-ng` development lines, all 60 pull requests numbered
1–61 (number 9 is an issue, not a pull request), all six branches currently
advertised by GitHub, and all branches advertised by the authoritative Gitea
remote after a prune/fetch.

## Pull-request dispositions

| Pull requests | State and disposition for NG |
| --- | --- |
| #1 | Merged to `main`; its automatic GitHub Actions deployment is superseded. NG uses manual Gitea validation/deployment and keeps GitHub Actions manual-only. |
| #2–8, #10–30 | Merged historical `main` material. Maintained concepts were migrated through the legacy-content audit and rewritten against current RCC boundaries; old commands and layout are not cherry-picked. |
| #31 | Closed without merge. Do not port: it proposed hand-entered host keys, deleting `known_hosts` entries, and `StrictHostKeyChecking no`. Expedition and the current safe-access guide provide the supported Windows route. |
| #32–41 | Merged historical `main` material. Maintained storage, Slurm, transfer, Snakemake, VS Code, and access guidance is represented in the NG course/reference structure. |
| #42 | Open against `main`. Do not merge into NG: it proposes an unbounded `rm -rf /local/work/$USER` over manually selected physical nodes. NG uses allocation-scoped `$SLURM_TMPDIR`/job directories and trapped per-job cleanup. |
| #43 | Merged to `main`; its VS Code Remote SSH intent is incorporated in `docs/reference/access-ssh-vscode.md`. |
| #44 | Open against `main`. Semantically incorporated: NG already gives the stronger small-workspace, `search.exclude`, and `files.watcherExclude` guidance. The legacy one-line link adds no missing NG behavior. |
| #45–47 | Merged into `clusterdocs-ng`; present in the candidate. |
| #48 | Merged to `main`; its dated/speculative transition announcement is deliberately archived until a fresh operational review supplies current dates and user routing. Its Slurm-first execution principles remain in the course. |
| #49–56 | Merged into `clusterdocs-ng`; present in the candidate. |
| #57 | Merged to `main`; the “no Environment Modules/Lmod; use managed Miniforge/Conda” guidance is present in `docs/reference/software-workflows.md`. |
| #58–59 | Merged to `main`; they repair Markdown formatting only in the legacy page set. NG's current Markdown/MkDocs strict build passes, so no legacy-file cherry-pick is needed. |
| #60–61 | Merged into `clusterdocs-ng`; they form the audited candidate baseline. |

There are no other GitHub PR numbers through #61. PRs #42 and #44 have no
review comments that introduce additional requirements. They should be closed
as superseded/rejected after the maintainers accept this disposition; this
audit does not mutate external PR state.

## GitHub branch dispositions

Snapshot tips used for the audit:

| Branch | Audited tip | Disposition |
| --- | --- | --- |
| `clusterdocs-ng` | `91f1ddc` | Candidate base. Merge the current release branch here after review. |
| `main` | `2114bc4` | Legacy source line. Four post-fork commits were audited: #48 is deliberately archived, #57 is incorporated, and #58–59 are legacy-only lint fixes. |
| `gh-pages` | `0d595ca` | Current generated production branch. The Gitea deployment workflow will replace its tree with a normal non-forced child commit, preserving rollback history. |
| `doc/apptainer` | `1a0c4ed` | Old partial Apptainer work, superseded by Class 4 and the software-workflows reference. Cleanup candidate. |
| `johanneskoester-patch-1` | `cdf31a7` | Head of open PR #42; rejected for NG on cleanup safety grounds. |
| `vscode/patterns` | `4fc993f` | Head of open PR #44; intent already incorporated in NG. |

## Gitea branch dispositions

Gitea advertises no pull-request refs for this repository. Its authoritative NG
branch is `gitea/clusterdocs-ng` at the same audited `91f1ddc` baseline.
`gitea/main`, `gitea/HEAD`, and `agent/whole-node-slurm-default` point to the
older `68615ac` line and contain no missing NG release work.

The remaining Gitea agent branches are retained historical heads whose work is
already represented by the named merged PR or the disposition above:

| Gitea branch | Disposition |
| --- | --- |
| `agent/announce-rcc-slurm-transition` | PR #48; archive-only until renewed operational review. |
| `agent/data-sharing-guide` | PR #53 merged. |
| `agent/document-user-group-project-model` | PR #56 merged. |
| `agent/efficient-local-io-class-v3` | PR #50 merged. |
| `agent/gitea-primary-ci` | CI routing is already in the NG baseline. |
| `agent/media-completion` | PR #52 merged and later expanded to 17 classes. |
| `agent/preserve-local-clusterdocs-edits` | Superseded integration branch; retained concepts entered PR #60 or were archived with #48. |
| `agent/production-review-candidate` | PR #55 merged. |
| `agent/publish-clusterdocs-ng` | PR #60 merged. |
| `agent/rcc-user-docs-refresh` | PR #45 merged. |
| `agent/rollout-readiness-audit` | PR #54 merged. |
| `agent/slurm-execution-model` | PR #46 merged. |
| `agent/slurm-resource-sharing-policy` | PR #47 merged. |
| `agent/ssh-host-identity-ng` | PR #49 merged and later safety wording retained. |
| `agent/wet-lab-instrument-course-v2` | PR #51 merged and later renumbered. |

These historical branches are cleanup candidates after the release branch is
merged and its rollback tag exists. Branch deletion is not a switchover blocker
and must not happen before maintainers confirm that no external automation
still names them.

## Remaining blockers after repository integration

The branch/PR audit found no unmerged content change required for the initial
NG switch. Remaining blockers are release evidence or external configuration:

1. complete and record human approval for all 17 videos;
2. resolve the remaining administrator checklist with the responsible RCC,
   privacy, accessibility, and service owners;
3. provision the dedicated GitHub Pages deploy key and pinned GitHub SSH host
   key in Gitea, and confirm Pages publishes `gh-pages` from `/`;
4. decide and verify the separate media endpoint before enabling players;
5. set `site_status: production` only when those gates pass; and
6. run novice acceptance against the live replacement before declaring rollout
   complete.

The optional `docs.ikim.uk-essen.de` CNAME is explicitly deferred. Its future
review must also resolve the existing planned media use of that hostname.
