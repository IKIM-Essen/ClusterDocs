# ClusterDocs 3 publication runbook

This runbook publishes the future ClusterDocs 3 site while keeping media
publication, human acceptance, online verification, and site promotion as
separate fail-closed steps. A failed gate leaves the current production site in
place.

## Fixed targets and source

- Production source branch: `clusterdocs-3`
- Site URL: <https://ikim-essen.github.io/ClusterDocs/>
- Media URL: <https://docs.ikim.uk-essen.de/media/rcc-onboarding/>
- Media web root: `/srv/www/docs/media/rcc-onboarding`
- Reviewed local MP4 source: `new-videos/`
- Manifest: `config/media-manifest.yml`
- Media set: 17 MP4 files, 122,808,554 bytes total
- Media-set checksum receipt: `9bcbc20ff36123e77dc103f7619444b17b08c4d09aaa43fff1a1316bcef1ab11`

The site publishes no local MP4 copies, GitHub media URLs, general downloads
tree, source-caption downloads, narration downloads, or office-document
downloads. The only versioned general download is the validated RCC Expedition
archive and its checksum. WebVTT captions and posters are generated as player
assets.

## 1. Build the exact staged candidate

Work only from the exact `clusterdocs-3` candidate to be reviewed. Record its
commit before testing:

```bash
git switch clusterdocs-3
git status --short
git rev-parse HEAD
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The worktree must be clean. `--manual-review` means the candidate is coherent
enough to begin human acceptance; it does **not** mean it is production-ready.

## 2. Run human acceptance before broad exposure

A very small controlled pilot may be exposed first to prove the deployed browser
journey works in principle. Before broad exposure, complete all of:

1. the fresh ClusterDocs 3 adversarial review in
   `meta/EXPERT_REVIEW_GUIDE.md`;
2. the zero-SSH naive-user browser session in
   `meta/NOVICE_REVIEW_GUIDE.md` using synthetic/non-sensitive data;
3. a separate advanced-user acceptance covering SSH, VS Code, Slurm,
   containers, workflow development, GPUs, and lower-level diagnostics; and
4. institutional/privacy/accessibility/operational review in
   `ADMIN_CHECKLIST.md`.

Do **not** substitute a successful SSH exercise for browser-first acceptance and
do not reuse the August expert receipt for ClusterDocs 3.

Record completed evidence in `config/review-status.yml` only after blocker/major
findings are resolved or explicitly accepted by the responsible owner.

## 3. Verify the exact media handoff before copying it

From the same candidate, run:

```bash
python3 tools/media_gate.py --local-dir new-videos
```

The gate must report `PASS (17 videos)`. It checks the manifest filename set,
exact size, SHA-256, H.264 1280×720 video, stereo AAC audio, and duration. Do not
deploy an extra file or substitute a same-named file with another hash.

## 4. Deploy and verify the separate media endpoint

Deploy the reviewed RCC `docs.ikim.uk-essen.de` static-vhost configuration with
document root `/srv/www/docs`. Copy exactly the approved files into
`/srv/www/docs/media/rcc-onboarding`; the web service receives read access, not a
writable project/user tree.

Before enabling players, the final endpoint must provide trusted TLS, correct
`video/mp4`, byte ranges with HTTP 206/`Content-Range`, and the exact manifest
bytes. Directory listing should remain disabled.

Run the online gate:

```bash
python3 tools/media_gate.py \
  --base-url https://docs.ikim.uk-essen.de/media/rcc-onboarding
```

It must report `media publication gate: PASS (17 videos)`. Also perform the
required human video/caption review and clean-client browser playback tests.

## 5. Activate video links only after online verification

Only after the online/media reviews pass, change the governed publication values
in `config/media-manifest.yml` to their verified-live state. Both the live status
and link-enablement condition are required; partial activation must remain
fail-closed and show the “Video not yet released” notice.

Rebuild and verify:

```bash
python3 tools/build_site.py --output site-review
python3 tools/check_site_links.py site-review
```

Review the course overview plus representative early, workflow, instrument, and
lifecycle classes; verify captions, seeking, mobile layout, and the supported
browser set.

## 6. Final production gate

Only after every required review is recorded and `ADMIN_CHECKLIST.md` is closed,
set `site_status: production` and run on the exact source commit:

```bash
python3 tools/validate_repo.py
python3 tools/rollout_readiness.py
python3 tools/build_site.py --production --output site-production
python3 tools/check_site_links.py site-production
```

All commands must pass. The readiness gate intentionally rejects a candidate
that still lacks fresh expert, zero-SSH novice, advanced-user, media,
accessibility, or administrator evidence.

## 7. Publish with the manual Gitea workflow

Production deployment is owned by
`.gitea/workflows/deploy-production.yml`. The workflow:

- accepts only `refs/heads/clusterdocs-3`;
- checks out and validates the exact event SHA;
- refuses a dirty/stale source;
- reruns the full fail-closed production gates;
- emits `assets/release.json` with source branch and commit;
- clones only the existing GitHub `gh-pages` branch;
- creates a normal child commit, never a forced update; and
- verifies the remote `gh-pages` head after push.

GitHub Actions remains manual validation fallback only and must not hold the
Pages deployment credential.

Before the first dispatch, provision the Gitea-only secrets documented in
`meta/GITEA_GITHUB_PAGES_DEPLOYMENT.md` and confirm Pages publishes the root of
`gh-pages`.

## 8. Post-publication verification

After the Pages commit becomes visible:

- verify `assets/release.json` matches the intended `clusterdocs-3` commit;
- re-run external links and representative browser/mobile/accessibility checks;
- re-run the online media gate and representative video/caption playback; and
- watch support/telemetry that has been institutionally approved for obvious
  breakage.

These are verification checks, not a deferred substitute for pre-broad-rollout
naive-user acceptance.

## Rollback

Keep the previous accepted `gh-pages` commit and media set available until the
new release is verified. Roll back the site with a new commit restoring the last
accepted generated tree; never force-rewrite `gh-pages`.

If media fails independently, disable preview links through the governed media
configuration and republish the site; do not introduce a local or third-party
fallback. Never replace an MP4 in place without updating its manifest hash and
verification evidence.

A future `docs.ikim.uk-essen.de` Pages CNAME remains a separate decision. Do not
add a Pages `CNAME` file as part of this release unless that DNS/hosting review is
completed separately.
