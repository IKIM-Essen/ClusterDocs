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
