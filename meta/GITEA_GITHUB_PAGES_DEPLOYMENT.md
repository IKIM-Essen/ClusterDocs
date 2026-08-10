# Gitea to GitHub Pages deployment contract

The production site remains <https://ikim-essen.github.io/ClusterDocs/> for
this rollout. A future `docs.ikim.uk-essen.de` CNAME may be introduced through
a separate DNS and GitHub Pages review; this release does not publish a
`CNAME` file or depend on that DNS name.

The manually dispatched Gitea workflow builds the exact `clusterdocs-ng`
commit and publishes the generated tree to the existing `gh-pages` branch of
`IKIM-Essen/ClusterDocs`. GitHub Actions is manual validation only.

Gitea must hold two repository secrets:

- `CLUSTERDOCS_GITHUB_PAGES_DEPLOY_KEY`: a dedicated SSH deploy key with write
  access only to the ClusterDocs GitHub repository; and
- `CLUSTERDOCS_GITHUB_SSH_HOST_KEY`: the reviewed, pinned GitHub SSH host-key
  line.

The key must not be shared with other repositories or placed in GitHub Actions.
The workflow uses strict host-key checking, clones only `gh-pages`, replaces
the generated tree in an isolated temporary directory, creates a normal child
commit so the prior deployment remains in history, pushes without force, and
verifies the resulting remote commit. A concurrent or stale update therefore
fails instead of overwriting another deployment.

Before the first production dispatch, confirm that GitHub Pages is configured
to publish from the repository's `gh-pages` branch at its root and that branch
protection permits the dedicated deploy key. Rollback is a new revert or
restoration commit based on the last accepted `gh-pages` commit; do not rewrite
the branch.
