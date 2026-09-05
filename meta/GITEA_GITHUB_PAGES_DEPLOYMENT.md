# ClusterDocs 3 Gitea to GitHub Pages deployment contract

The production site remains <https://ikim-essen.github.io/ClusterDocs/> for this
release. A future `docs.ikim.uk-essen.de` CNAME may be introduced through a
separate DNS and GitHub Pages review; ClusterDocs 3 does not publish a `CNAME`
file or depend on that DNS name for the Pages site.

The manually dispatched Gitea workflow builds the **exact
`refs/heads/clusterdocs-3` commit** and publishes the generated tree to the
existing `gh-pages` branch of `IKIM-Essen/ClusterDocs`. The retired
`clusterdocs-ng` branch is not an accepted production source. GitHub Actions is
manual validation only and holds no production deployment credential.

## Required Gitea secrets

Gitea must hold two repository secrets:

- `CLUSTERDOCS_GITHUB_PAGES_DEPLOY_KEY`: a dedicated SSH deploy key with write
  access only to the ClusterDocs GitHub repository; and
- `CLUSTERDOCS_GITHUB_SSH_HOST_KEY`: the reviewed, pinned GitHub SSH host-key
  line.

The key must not be shared with other repositories or placed in GitHub Actions.
The workflow uses strict host-key checking, clones only `gh-pages`, replaces the
generated tree in an isolated temporary directory, creates a normal child
commit so the prior deployment remains in history, pushes without force, and
verifies the resulting remote commit. A concurrent or stale update therefore
fails instead of overwriting another deployment.

## Source and review gates

Before publication, the workflow must prove all of the following:

1. `GITHUB_REF` is exactly `refs/heads/clusterdocs-3`;
2. the checked-out `HEAD` is exactly the event SHA and the worktree is clean;
3. `tools/validate_repo.py` passes on that exact source;
4. `tools/rollout_readiness.py` reports no blockers, including fresh
   ClusterDocs 3 expert review, zero-SSH novice-browser acceptance, separate
   advanced-user acceptance, media/institutional gates, and production status;
5. `tools/build_site.py --production` succeeds;
6. the generated-site link check succeeds; and
7. `assets/release.json` records `source_branch: clusterdocs-3` and the exact
   source commit.

A controlled pilot may be used to collect acceptance evidence, but the
production workflow does not treat pilot exposure as completed broad-release
acceptance.

## GitHub Pages and rollback

Before the first production dispatch, confirm GitHub Pages is configured to
publish from the repository's `gh-pages` branch at its root and that repository
policy permits the dedicated deploy key.

Rollback is a new revert/restoration commit based on the last accepted
`gh-pages` commit; do not rewrite the Pages branch. The release receipt makes it
possible to identify exactly which `clusterdocs-3` commit produced any published
site tree.
