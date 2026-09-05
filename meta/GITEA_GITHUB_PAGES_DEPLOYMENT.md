# Gitea to GitHub Pages deployment contract

The production site remains <https://ikim-essen.github.io/ClusterDocs/> for this
release. A future `docs.ikim.uk-essen.de` CNAME may be introduced through a
separate DNS and GitHub Pages review; this release does not publish a `CNAME`
file or depend on that DNS name for the Pages site.

## Source authority

The manually dispatched Gitea **production** workflow builds the exact
`refs/heads/main` commit and publishes the generated tree to the existing
`gh-pages` branch of `IKIM-Essen/ClusterDocs`.

Temporary candidate branches such as `clusterdocs-3` may run validation and
human review, but they are not accepted production sources. `clusterdocs-ng` is
also not an accepted production source. Moving an accepted candidate into
`main` is a separate repository decision requiring explicit authorization; the
production workflow never performs that merge.

GitHub Actions is manual validation only and holds no production deployment
credential.

## Required Gitea secrets

Gitea must hold two repository secrets:

- `CLUSTERDOCS_GITHUB_PAGES_DEPLOY_KEY`: a dedicated SSH deploy key with write access only to the ClusterDocs GitHub repository; and
- `CLUSTERDOCS_GITHUB_SSH_HOST_KEY`: the reviewed, pinned GitHub SSH host-key line.

The key must not be shared with other repositories or placed in GitHub Actions.
The workflow uses strict host-key checking, clones only `gh-pages`, replaces the
generated tree in an isolated temporary directory, creates a normal child commit
so the prior deployment remains in history, pushes without force, and verifies
the resulting remote commit.

## Production gates

Before publication the workflow must prove all of the following:

1. `GITHUB_REF` is exactly `refs/heads/main`;
2. checked-out `HEAD` is exactly the event SHA and the worktree is clean;
3. `tools/validate_repo.py` passes;
4. `tools/rollout_readiness.py` reports no blockers, including fresh v3 expert review, zero-SSH novice-browser acceptance, separate advanced-user acceptance, credential/media reconciliation, institutional gates, and production status;
5. `tools/build_site.py --production` succeeds;
6. generated-site link checking succeeds; and
7. `assets/release.json` records `source_branch: main` and the exact source commit.

A controlled pilot or a green `clusterdocs-3` validation does not satisfy the
main production-source requirement.

## Branch lifecycle

After a verified main-based deployment and rollback check, temporary
`clusterdocs-ng` and `clusterdocs-3` branches may be retired through repository
policy. The deployment workflow does not delete branches and branch retirement
is not implied by a successful merge.

## GitHub Pages and rollback

Before the first production dispatch, confirm GitHub Pages publishes from the
repository's `gh-pages` branch at its root and repository policy permits the
dedicated deploy key.

Rollback is a new revert/restoration commit based on the last accepted
`gh-pages` commit; do not rewrite the Pages branch.
