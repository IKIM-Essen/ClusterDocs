# ClusterDocs publication runbook

This runbook separates candidate review, explicit promotion into `main`, Stage-1
written-site publication, later Stage-2 media activation, and rollback. A failed
gate leaves the current production site in place.

## Fixed targets and branch roles

- Temporary candidate branch: `clusterdocs-3`
- Long-term production source: `main`
- Legacy temporary branch to retire after successful promotion: `clusterdocs-ng`
- Site URL: <https://ikim-essen.github.io/ClusterDocs/>
- Media URL: <https://docs.ikim.uk-essen.de/media/rcc-onboarding/>
- Media web root: `/srv/www/docs/media/rcc-onboarding`
- Local MP4 regeneration source: `new-videos/`
- Manifest: `config/media-manifest.yml`

Production must never be dispatched directly from `clusterdocs-3` or
`clusterdocs-ng`. The production workflow accepts `main` only.

## Release strategy

ClusterDocs 3 intentionally rolls out in two stages.

### Stage 1 — written site

Publish the final reviewed text, navigation, workflow guidance, screenshots and
other non-video assets. Keep `config/media-manifest.yml` player links disabled.
The site renderer must replace video elements with the fail-closed **Video not
yet released** state.

Stage 1 is allowed to become the production site **without regenerated/human-
approved videos**, provided every non-media production gate has passed.

### Stage 2 — videos

After the repository text/narration is stable, regenerate media on the approved
workstation, review it, publish it to the RCC media endpoint, update the manifest
hashes/metadata, and only then enable player links.

Stage 2 includes the corrected Part-1 video and the proposed short 3–4 minute
**What changed from the old cluster?** orientation video. Its narration source is
`narration/RCC_What_Changed_From_Old_Cluster_Narration.md`.

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

## 2. Run Stage-1 human acceptance before promotion

Before broad Stage-1 exposure complete:

1. the fresh ClusterDocs 3 adversarial review;
2. the zero-SSH naive-user browser session using synthetic/non-sensitive data;
3. separate advanced-user acceptance including SSH/VS Code/Slurm/containers/GPU/workflows and the current no-passphrase SSH-key policy;
4. architecture review of the I/O-first Slurm/service-plane/Kubernetes/Ceph rationale;
5. verification of the RCC-safe VS Code search/watcher settings on a realistic project tree; and
6. institutional/privacy/accessibility/operational review.

Do not reuse the August expert receipt as v3 evidence.

Media review is **not** a Stage-1 gate while player links remain disabled. The
written site must nevertheless contain current narration/source text and must
not expose stale video links.

## 3. Prove Stage 1 is genuinely text-only

Before promotion, verify:

```bash
python3 tools/build_site.py --output site-stage1
python3 tools/check_site_links.py site-stage1
```

Inspect representative course pages and prove that unpublished media is rendered
as the fail-closed notice rather than a playable/dead MP4 URL. Do not use a
third-party video fallback.

## 4. Explicit promotion checkpoint

After every Stage-1 candidate gate closes, stop. Merging `clusterdocs-3` into
`main` requires **explicit authorization at that time**. This runbook and a green
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

For Stage 1, `tools/rollout_readiness.py` must explicitly report that player
links are fail-closed and that video human approval is deferred to Stage 2.

## 6. Publish Stage 1 with the manual Gitea workflow

`.gitea/workflows/deploy-production.yml` must:

- accept only `refs/heads/main`;
- validate the exact event SHA and clean worktree;
- rerun the full active-stage production gates;
- emit `assets/release.json` with `source_branch: main` and the exact commit;
- clone only the existing GitHub `gh-pages` branch;
- create a normal child commit, never a forced update; and
- verify the remote Pages head after push.

GitHub Actions remains manual validation fallback only and must not hold the
Pages deployment credential.

## 7. Stage-1 post-publication verification

After the Pages commit becomes visible:

- verify `assets/release.json` matches the intended main commit;
- rerun external link and representative browser/mobile/accessibility checks;
- verify course pages show the expected video-unavailable state with no broken
  media requests; and
- confirm rollback to the previous accepted Pages commit remains possible.

These are verification checks, not substitutes for pre-promotion human
acceptance.

## 8. Prepare Stage 2 only after text is stable

Regenerate the videos on the approved workstation from the accepted source tree.
At minimum:

- regenerate Part 1 from the corrected no-passphrase SSH-key source/narration;
- regenerate any course video whose narration/content changed materially;
- optionally build the short returning-user **What changed** video from the
  staged narration script; and
- re-time captions to the regenerated audio.

Update `config/media-manifest.yml` with the exact files, sizes, durations and
SHA-256 values. Do not replace a same-named file in place without updating the
receipt.

Run the local media gate, publish the exact approved set to the RCC media
endpoint, then run the online media gate. Complete human review for narration,
visual accuracy, pronunciation, pacing, captions and absence of sensitive data.

Only after those checks set the governed media publication state to
`verified_live` and enable preview/player links. Once links are enabled, the
rollout readiness gate treats media approval as a hard production requirement.

## 9. Publish Stage 2 from main

Stage 2 is a normal reviewed change to `main`, not a resurrection of
`clusterdocs-3`. Validate the exact main commit and dispatch the same main-only
production workflow. Verify representative video playback, seeking, byte ranges,
captions, mobile behavior and the complete media gate after publication.

## 10. Retire temporary branches only after Stage-1 success

The temporary branches do not need to remain alive until Stage 2. Once the
accepted ClusterDocs 3 text has been merged to `main`, Stage-1 main publication
and rollback evidence are verified, `clusterdocs-ng` and `clusterdocs-3` may be
retired according to repository policy.

Stage-2 media work should then branch normally from `main` and return to `main`.

## Rollback

Keep the previous accepted `gh-pages` commit available. Roll back the site with a
new commit restoring the last accepted generated tree; never force-rewrite
`gh-pages`.

If Stage-2 media fails independently, disable preview links through governed
media configuration and republish from an accepted `main`; the Stage-1 written
site remains a valid fallback. Do not introduce local or third-party media
fallbacks.