# ClusterDocs NG GitHub Pages publication runbook

This replaces the content of the existing GitHub Pages site while keeping media
deployment, online verification, link activation, and site publication as
separate guarded steps. A failure leaves the generated site without dead video
links.

## Fixed targets and content set

- Site URL: <https://ikim-essen.github.io/ClusterDocs/>
- Media URL: <https://docs.ikim.uk-essen.de/media/rcc-onboarding/>
- Media web root: `/srv/www/docs/media/rcc-onboarding`
- Reviewed local MP4 source: `new-videos/`
- Manifest: `config/media-manifest.yml`
- Media set: 17 MP4 files, 122,808,554 bytes total
- Media-set checksum receipt: `9bcbc20ff36123e77dc103f7619444b17b08c4d09aaa43fff1a1316bcef1ab11`

The site publishes no local MP4 copies, GitHub media URLs, general downloads
tree, source captions, narration downloads, or office-document downloads. The
only versioned download is the validated RCC Expedition archive and its outer
checksum. WebVTT captions and posters are built into the site as player assets.

## 1. Verify the exact handoff before copying it

From the ClusterDocs worktree that will be deployed, run:

```bash
python tools/validate_repo.py
python tools/media_gate.py --local-dir new-videos
python tools/rollout_readiness.py --manual-review
```

The media gate must report `PASS (17 videos)`. It checks the manifest filename
set, exact size, SHA-256, H.264 1280×720 video, stereo AAC audio, and duration.
Do not deploy an extra file or substitute a same-named file with another hash.

## 2. Deploy the separate media vhost and fixed media directory

Deploy the reviewed RCC `docs.ikim.uk-essen.de` static-vhost configuration with
document root `/srv/www/docs`. Copy exactly the 17 files from `new-videos/` into
`/srv/www/docs/media/rcc-onboarding`; directories must be readable/executable
by the web service and MP4 files must be read-only to it. Do not publish the
temporary upload directory or point the vhost into a user or project tree.

Before DNS cut-over, test the intended hostname through the deployment network.
The final listener must provide a trusted certificate for
`docs.ikim.uk-essen.de`, serve MP4s as `video/mp4`, support byte ranges with
HTTP 206 and `Content-Range`, and serve the exact manifest bytes. Directory
listing is not required and should remain disabled.

## 3. Verify the released URL before enabling players

After DNS and TLS are live, run the full online gate:

```bash
python tools/media_gate.py \
  --base-url https://docs.ikim.uk-essen.de/media/rcc-onboarding
```

This range-tests and fully downloads all 17 videos. It must report
`media publication gate: PASS (17 videos)`. Also test one class in Firefox with
captions enabled. A successful home page or one successful MP4 is insufficient.

## 4. Activate video links with one reviewed configuration change

Only after the online gate passes, change these two values in
`config/media-manifest.yml`:

```yaml
status: verified_live
preview_links: enabled
```

Record the verification time and result in the deployment change. Both values
are required: changing only one keeps the build fail-closed and emits the
“Video not yet released” notice instead of an MP4 URL.

Rebuild and prove that all 17 unique RCC URLs—and no local or GitHub media
URLs—are present:

```bash
python tools/build_site.py --output site-preview
python tools/check_site_links.py site-preview
```

Review the course overview, Classes 1, 6, 7, 16, and 17, one caption track, seeking
within a video, mobile layout, and Firefox playback before production cut-over.

## 5. Publish the site

Complete `ADMIN_CHECKLIST.md`, record the required human content reviews, set
`site_status: production`, and run:

```bash
python tools/validate_repo.py
python tools/rollout_readiness.py
python tools/build_site.py --production --output site-production
python tools/check_site_links.py site-production
```

Site deployment is owned by the manually dispatched Gitea workflow in
`.gitea/workflows/deploy-production.yml`. GitHub Actions remains a manual
validation fallback and must never hold production deployment credentials or
deploy the site. The workflow replaces the generated content of the existing
`IKIM-Essen/ClusterDocs` `gh-pages` branch; it does not create another Pages
project.

Before the first dispatch, provision these repository secrets in Gitea only:

- `CLUSTERDOCS_GITHUB_PAGES_DEPLOY_KEY`: a dedicated write-enabled deploy key
  for only the ClusterDocs GitHub repository; and
- `CLUSTERDOCS_GITHUB_SSH_HOST_KEY`: the reviewed, pinned GitHub SSH host-key
  line.

Follow `meta/GITEA_GITHUB_PAGES_DEPLOYMENT.md`. The workflow accepts only the
`clusterdocs-ng` branch, checks out the exact event SHA through the RCC runner
helper, runs every production gate, creates a normal child commit of the
current `gh-pages` head, pushes without force, and verifies the published
commit. It deliberately emits `.nojekyll` and refuses a `CNAME` file.

After GitHub Pages serves the new commit, re-run the online media gate and
Firefox playback acceptance, then perform the novice acceptance tasks
immediately against the live site. Novice acceptance does not block the initial
switch, but it blocks declaring rollout complete; a blocking safety or
task-completion finding requires rollback or a corrected release.

A future `docs.ikim.uk-essen.de` CNAME remains a separate decision. Do not add
DNS or a Pages `CNAME` file during this content rollout. That review must also
resolve where `/media/rcc-onboarding/` will live, because the current media
plan uses the same hostname on the RCC web service.

## Rollback

Keep the previous `gh-pages` commit and media directory until post-release
acceptance completes. If the media path fails, immediately set
`preview_links: disabled_until_verified_live` and rebuild; this removes all
player URLs without introducing a local or third-party fallback. Roll back the
site with a new commit restoring the previously accepted generated tree; do not
force-rewrite `gh-pages`. Never replace an MP4 in place without updating the
manifest hash, cache key, staged-set receipt, and verification evidence.
