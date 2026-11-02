# Browser-first ClusterDocs rollout checklist

**Branch:** `rollout/browser-first-onboarding-20261023`. **Not a deployment branch and not yet published.**

## Borrowed design patterns and why

| Example | RCC usage | Source |
|---|---|---|
| Galaxy Training Network: real file → analysis → history → workflow | Hands-on first-success tutorial; sample data and reproducibility | https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/tutorial.html |
| Open OnDemand: Files, Jobs, Interactive Apps, reconnect | Sidebar and task-oriented HPC flows | https://docs.rcc.uchicago.edu/connection/open_on_demand/open_ondemand/ |
| Terra: workspace holds data, tools, documentation and provenance | Persistent selected-project context | https://support.terra.bio/hc/en-us/articles/360046095192-Intro-to-workspaces |
| JupyterHub: managed spawn/poll/stop, retained state | Explicit Notebook starting/running/reconnecting/stopping states | https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html |
| GitHub: invitation acceptance, expiration and retry | Invitation-first account claim and recovery states | https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization |

Borrow behavior and architecture principles, not trademarked design assets or copied screenshots.

## Cutover criteria

- [ ] RCC QA gates G0–G7 passed on exact deployed versions: `rcc/docs/qa/browser-first-user-journey-release-gates-2026-10-23.md`
- [ ] Invite/claim/passkey/recovery walkthrough approved by Identity team
- [ ] Actual Files/Analysis/Notebook navigation and project selector verified with the final UI
- [ ] Screenshot set recaptured and checked on desktop, tablet and mobile (no private data)
- [ ] All links resolve to accepted live routes; unavailable features marked honestly
- [ ] Existing SSH/VS Code content retained as advanced/current access; no forced migration
- [ ] Friday Computing Club disposable example and exercise rehearsed twice
- [ ] mkdocs build, internal-link check, accessibility check and visual QA pass
- [ ] Source and docs release SHAs recorded, rollback commit retained, operator approves publication
- [ ] After publication, externally verify site and cross-links from the live RCC UI

## Staging policy

No push to the deployed site, no `main` merge, no GitHub Pages publication and no unapproved invitation emails. Edit documentation here until rollout admission. Existing ClusterDocs `main` remains source of truth for what is **currently available**.


## Full researcher-experience scope (not only onboarding)

This rollout depends on the **complete RCC user experience**, recorded in
`IKIM-Essen/rcc/docs/plans/rcc-complete-researcher-experience-2026-10-23.md`
(draft PR #4061). Do not cut over merely because invitation/Files pages were
written. The same project-centered vocabulary, left sidebar and recovery help
must span Admin/My RCC, Files, Analysis (Workflow and Notebook), Jobs/results,
the contextual GB10 Assistant and advanced access.

Preserve the existing rich content: Expedition Light, optional offline RCC
Expedition, 18-class course, data-analysis path, Nextflow/Snakemake lessons,
RCC service map, biomedical-data privacy and old-cluster migration guide.
**Rewrite navigation and task entry points, not the substantive scientific
courses.**

The new **Bring your workflow** guide must be grounded in an accepted importer,
authorization-scoped dedup/index, human-readable source diff, measured paired
benchmarks and output equivalence checks. Any 95%-similarity indicator remains
review-only; it is not a statement of scientific equality. Show Original,
Optimized profile and Compare results. Never present example performance
numbers as production measurements.

The Assistant's ClusterDocs answers must cite a concrete version, tell users
when a service is still unavailable, and must not reveal documents or workflow
records beyond their current authorization. The Assistant never becomes a
second authorization or scheduling system.

### Required site content inventory before cutover

| User question | Reuse first | Remaining release-specific enhancement |
|---|---|---|
| How do I accept my invitation? | account enrollment and authentication reference | Existing-account claim, passkey, recovery and no-SSH onboarding |
| Where do I start? | Expedition Light and service map | Browser-first entry and first-success exercise |
| Where are my files? | Files concepts and storage transfer reference | Accepted UI screenshots, permissions, upload failures |
| Notebook or Workflow? | RCC Analysis + data-analysis path | Task-based examples and actual UI destinations |
| Can you improve my pipeline? | Snakemake/Nextflow classes, resource/I/O lessons | Bring-workflow comparison guide and scientific validation |
| What is taking so long? | Slurm, I/O and performance lessons | Jobs/results UI help with runtime observation |
| Can RCC Assistant help? | Guardian/Assistant and ClusterDocs content | Contextual entry points, evidence links, limitations |
| How do I work in a shell? | Existing SSH/VS Code and Expedition | Keep advanced path discoverable without making it mandatory |

Before release, run the exact end-to-end QA contract from RCC draft PR #4059
and verify the novice-user pilot can independently repeat the Computing Club
example. Site publication remains separately approved.
