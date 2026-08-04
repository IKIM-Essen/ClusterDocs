# ClusterDocs NG RCC-vhost publication runbook

This is the handoff for the RCC documentation vhost. It keeps media deployment,
online verification, link activation, and site deployment as separate guarded
steps. A failure leaves the generated site without dead video links.

## Fixed targets and content set

- Site URL: <https://docs.ikim.uk-essen.de/>
- Media URL: <https://docs.ikim.uk-essen.de/media/rcc-onboarding/>
- Media web root: `/srv/www/docs/media/rcc-onboarding`
- Reviewed local MP4 source: `new-videos/`
- Manifest: `config/media-manifest.yml`
- Media set: 17 MP4 files, 122,653,131 bytes total
- Media-set checksum receipt: `abf271e7b4c3998abf27a38efa0494e3a01c3c1eb94cd40f7b1af1204045ace0`

The site publishes no local MP4 copies, GitHub media URLs, downloads tree,
source captions, narration downloads, or office-document downloads. WebVTT
captions and posters are built into the site as player assets.

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

## 2. Deploy the vhost and the fixed media directory

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

Deploy the exact `site-production` tree to `/srv/www/docs` while preserving the
already verified `/srv/www/docs/media/rcc-onboarding` directory. Re-run the
online media gate and Firefox playback acceptance after deployment.

## Rollback

Keep the previously accepted site tree and media directory until post-release
acceptance completes. If the media path fails, immediately set
`preview_links: disabled_until_verified_live` and rebuild; this removes all
player URLs without introducing a local or third-party fallback. Roll back the
site tree independently. Never replace an MP4 in place without updating the
manifest hash, cache key, staged-set receipt, and verification evidence.
