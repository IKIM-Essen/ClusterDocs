# ClusterDocs publication runbook

This runbook separates candidate review, explicit promotion into `main`, media
verification, and production publication. A failed gate leaves the current
production site in place.

## Fixed targets and branch roles

- Temporary candidate branch: `clusterdocs-3`
- Long-term production source: `main`
- Legacy temporary branch to retire after successful promotion: `clusterdocs-ng`
- Site URL: <https://ikim-essen.github.io/ClusterDocs/>
- Media URL: <https://docs.ikim.uk-essen.de/media/rcc-onboarding/>
- Media web root: `/srv/www/docs/media/rcc-onboarding`
- Reviewed local MP4 source: `new-videos/`
- Manifest: `config/media-manifest.yml`

Production must never be dispatched directly from `clusterdocs-3` or
`clusterdocs-ng`. The production workflow accepts `main` only.

## 1. Build the exact staged candidate

```bash
git switch clusterdocs-3
git status --short
git rev-parse HEAD
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The worktree must be clean. Candidate validation proves only that human review
can proceed; it does **not** authorize a merge or production publication.

## 2. Run human acceptance before promotion

Before broad exposure complete:

1. the fresh ClusterDocs 3 adversarial review;
2. the zero-SSH naive-user browser session using synthetic/non-sensitive data;
3. separate advanced-user acceptance including SSH/VS Code/Slurm/containers/GPU/workflows and the current no-passphrase SSH-key policy;
4. architecture review of the Slurm/service-plane/Kubernetes rationale;
5. institutional/privacy/accessibility/operational review; and
6. media review, including regeneration of Part 1 after reconciling the canonical source with current credential policy.

Do not reuse the August expert receipt or the old Part 1 audio as v3 evidence.

## 3. Verify media before promotion

Run the local and online media gates as documented by `tools/media_gate.py` and
`config/media-manifest.yml`. The currently staged Part 1 media must remain
fail-closed until regenerated from corrected source/narration and re-reviewed.
Do not substitute a same-named file with another hash without updating the
manifest and evidence.

## 4. Explicit promotion checkpoint

After every candidate gate closes, stop. Merging `clusterdocs-3` into `main`
requires **explicit authorization at that time**. This runbook and a green
candidate do not authorize the merge.

When authorization is given, use the normal repository merge path. Do not force
move `main` and do not publish from the candidate branch as a shortcut.

## 5. Revalidate the exact main commit

After the authorized merge:

```bash
git switch main
git pull --ff-only
git status --short
git rev-parse HEAD
python3 tools/validate_repo.py
python3 tools/rollout_readiness.py
python3 tools/build_site.py --production --output site-production
python3 tools/check_site_links.py site-production
```

Confirm the exact main tree corresponds to the accepted candidate plus only the
explicitly reviewed merge/promotion changes. Any new content change requires
re-review appropriate to its scope.

## 6. Publish with the manual Gitea workflow

`.gitea/workflows/deploy-production.yml` must:

- accept only `refs/heads/main`;
- validate the exact event SHA and clean worktree;
- rerun the full production gates;
- emit `assets/release.json` with `source_branch: main` and the exact commit;
- clone only the existing GitHub `gh-pages` branch;
- create a normal child commit, never a forced update; and
- verify the remote Pages head after push.

GitHub Actions remains manual validation fallback only and must not hold the
Pages deployment credential.

## 7. Post-publication verification

After the Pages commit becomes visible:

- verify `assets/release.json` matches the intended main commit;
- rerun external link and representative browser/mobile/accessibility checks;
- rerun the online media gate and representative video/caption playback; and
- confirm rollback to the previous accepted Pages commit remains possible.

These are verification checks, not substitutes for pre-promotion human
acceptance.

## 8. Retire temporary branches only after success

Only after the main-based publication and rollback evidence are verified should
`clusterdocs-ng` and `clusterdocs-3` be retired according to repository policy.
Do not delete them during candidate review, immediately on merge, or as part of
the production workflow itself.

After retirement, ordinary ClusterDocs development should branch from `main` and
return to `main`; future production publication should continue to originate
from `main`.

## Rollback

Keep the previous accepted `gh-pages` commit and media set available until the
new release is verified. Roll back the site with a new commit restoring the last
accepted generated tree; never force-rewrite `gh-pages`.

If media fails independently, disable preview links through governed media
configuration and republish from an accepted `main`; do not introduce a local or
third-party fallback.
