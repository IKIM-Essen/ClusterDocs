# ClusterDocs NG production-candidate status

Review date: 25 July 2026

## Current decision

ClusterDocs NG is **ready to begin structured expert and novice review**. It is
not yet approved for public production. The automated candidate gate now keeps
those two decisions separate: human review can start without weakening the
fail-closed production gate.

## Completed in this round

- Archived the speculative rollout page and removed “RCC Connect” and rollout
  language from public instructions. Users are directed to the current
  institutional RCC configuration and support route.
- Added expert, novice, and all-15-video review guides with task-based checks,
  severity definitions, and media approval criteria.
- Added a `--manual-review` readiness gate. It verifies that review guides are
  present, speculative rollout wording is absent, rootless Apptainer is in the
  canonical source, and unsynchronized office exports are not public.
- Normalized speech-oriented caption spellings into readable technical text in
  built SRT and WebVTT files, including `SSH`, `SIF`, `--nv`, `/data`, and `I/O`.
- Withheld stale Part 1–4 DOCX, PDF, and PowerPoint derivatives from generated
  downloads. Their source files are preserved, but reviewers will assess the
  current class pages, videos, captions, and transcripts.
- Removed unused rollout-only production placeholders, reducing the unresolved
  configuration to values the published site actually needs.

## Production blockers that remain

1. Set the production site URL, support contact, transfer-service URL, and
   media origin, then change `site_status` only after the other gates pass.
2. Publish the 15 exact video assets at the configured HTTPS origin and test
   playback, byte-range requests, captions, and a clean client.
3. Complete and record human video approval for all 15 classes.
4. Complete the institutional administrator checklist: operational endpoints,
   supported versions, storage and Slurm behavior, privacy/domain approval,
   accessibility, ownership, monitoring, and rollback.
5. Add and review a production deployment workflow. Current CI validates and
   uploads a preview artifact but does not deploy.

## Start manual review

Use `meta/EXPERT_REVIEW_GUIDE.md`, `meta/NOVICE_REVIEW_GUIDE.md`, and
`meta/VIDEO_REVIEW_GUIDE.md`. Build the exact candidate and verify the gate:

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review --include-media
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
