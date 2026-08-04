# ClusterDocs NG production-candidate status

Review date: 4 August 2026

## Current decision

ClusterDocs NG is **ready to begin structured expert and novice review**. It is
not yet approved for public production. The automated candidate gate now keeps
those two decisions separate: human review can start without weakening the
fail-closed production gate.

## Completed in this round

- Verified the expanded 17-video RCC handoff locally: the exact filename set,
  122,653,131 total bytes, SHA-256 values, H.264 1280×720 video, stereo AAC,
  and durations match `config/media-manifest.yml`.
- Prepared the RCC documentation-vhost target and a fail-closed activation
  gate. Until DNS, TLS, MIME type, byte ranges, and full downloads pass, the
  generated site displays a release notice and emits no MP4 URL.
- Replaced the obsolete GitHub Pages handoff with an RCC-vhost deployment,
  acceptance, activation, and rollback runbook. `site_status` remains
  `staging` until the operational, human, and institutional gates close.
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

## Production blockers that remain

1. Deploy `docs.ikim.uk-essen.de`, publish the exact staged MP4 set, and pass
   the full online media gate for trusted HTTPS, `video/mp4`, byte ranges,
   exact sizes, and SHA-256 values.
2. Activate the players, complete Firefox playback and clean-client visual
   checks, then record human video approval for all 17 classes.
3. Complete the institutional administrator checklist: operational endpoints,
   supported versions, storage and Slurm behavior, privacy/domain approval,
   accessibility, ownership, monitoring, and rollback.
4. Add and review a production deployment workflow. Current CI validates and
   uploads a preview artifact but does not deploy.
5. Change `site_status` to `production` only after the preceding gates pass.

## Start manual review

Use `meta/EXPERT_REVIEW_GUIDE.md`, `meta/NOVICE_REVIEW_GUIDE.md`, and
`meta/VIDEO_REVIEW_GUIDE.md`. Build the exact candidate and verify the gate:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The final command must report `READY_FOR_EXPERT_AND_NOVICE_REVIEW`.

## Production release gate

After review findings and institutional values are resolved, run:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

All three commands must pass. A production build is expected to fail while the
candidate remains explicitly configured as staging.
