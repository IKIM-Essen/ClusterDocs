# ClusterDocs NG production-candidate status

Review date: 9 August 2026

## Current decision

ClusterDocs NG has completed expert content review. Novice acceptance is
scheduled immediately after the new site is rolled out and therefore does not
block the initial switch; it does block declaring rollout complete. The site
is not yet approved for public production because the remaining operational,
media, institutional, and accessibility gates are still fail-closed.

## Completed in this round

- Verified the expanded 17-video RCC handoff locally: the exact filename set,
  122,808,554 total bytes, SHA-256 values, H.264 1280×720 video, stereo AAC,
  and durations match `config/media-manifest.yml`.
- Prepared the separate RCC media-vhost target and a fail-closed activation
  gate. Until DNS, TLS, MIME type, byte ranges, and full downloads pass, the
  generated site displays a release notice and emits no MP4 URL.
- Reworked publication so Gitea replaces the current GitHub Pages content with
  the NG build. `site_status` remains `staging` until the operational, human,
  and institutional gates close.
- Archived the speculative rollout page and removed “RCC Connect” and rollout
  language from public instructions. Users are directed to the current
  institutional RCC configuration and support route.
- Added expert, novice, and all-17-video review guides with task-based checks,
  severity definitions, and media approval criteria.
- Added a `--manual-review` readiness gate. It verifies that review guides are
  present, speculative rollout wording is absent, rootless Apptainer is in the
  canonical source, and unsynchronized office exports are not public.
- Normalized speech-oriented caption spellings into readable technical text in
  built SRT and WebVTT files, including `SSH`, `SIF`, `--nv`, `/data`, and `I/O`.
- Retired the standalone Media and downloads page and the generated downloads
  tree. Once the RCC documentation vhost is verified live, videos will be
  embedded there and WebVTT captions will remain available directly to each
  video player.
- Removed unused rollout-only production placeholders, reducing the unresolved
  configuration to values the published site actually needs.
- Added a manually dispatched Gitea-only production workflow. It validates the
  exact `clusterdocs-ng` commit and publishes a normal, non-forced child commit
  to the existing GitHub `gh-pages` branch. GitHub Actions remains manual
  validation only and has no deployment credentials.
- Rebuilt RCC Expedition with the current GitHub Pages production origin and
  the future NG lesson routes, then added archive, checksum, path-safety, and
  embedded public-content validation.
- Recorded expert content review as complete and the approved post-rollout
  timing for novice acceptance in `config/review-status.yml`.
- Audited all 60 GitHub PRs through #61, all six surviving GitHub branches, and
  every advertised Gitea branch. No missing content change blocks the switch;
  the two open legacy PRs are respectively unsafe to port and already
  incorporated semantically. See `meta/BRANCH_PR_AUDIT.md`.

## Production blockers that remain

1. Publish the exact staged MP4 set at its separate media endpoint and pass the
   full online media gate for trusted HTTPS, `video/mp4`, byte ranges, exact
   sizes, and SHA-256 values.
2. Activate the players, complete Firefox playback and clean-client visual
   checks, then record human video approval for all 17 classes.
3. Complete the institutional administrator checklist: operational endpoints,
   supported versions, storage and Slurm behavior, privacy/domain approval,
   accessibility, ownership, monitoring, and rollback.
4. Provision and review the dedicated GitHub Pages deploy key and pinned host
   key in Gitea as described in `meta/GITEA_GITHUB_PAGES_DEPLOYMENT.md`; verify
   the Pages branch/root setting, non-forced update, receipt, and rollback.
5. Change `site_status` to `production` only after the preceding gates pass.
6. Run novice acceptance against the live site immediately after switching;
   resolve blockers before declaring rollout complete.

## Continue manual review

Use `meta/EXPERT_REVIEW_GUIDE.md`, `meta/NOVICE_REVIEW_GUIDE.md`, and
`meta/VIDEO_REVIEW_GUIDE.md`. Build the exact candidate and verify the gate:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The final command verifies that the review materials remain coherent. Expert
completion and post-rollout novice timing are enforced separately by the full
rollout readiness gate.

## Production release gate

After review findings and institutional values are resolved, run:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

All three commands must pass. A production build is expected to fail while the
candidate remains explicitly configured as staging.
