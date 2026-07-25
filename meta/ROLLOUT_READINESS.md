# ClusterDocs NG rollout-readiness review

Review date: 25 July 2026  
Reviewed branch baseline: `clusterdocs-ng` at `9d6724b`

## Executive assessment

The documentation is structurally mature and suitable for a controlled pilot,
but it is **not ready for public production rollout**. The content, examples,
navigation, safety boundaries, and internal link validation are largely
complete. The remaining blockers are mostly institutional decisions,
production delivery, and human acceptance—not missing course chapters.

In practical terms, the project is one formal administrator/novice acceptance
cycle plus media publication and deployment setup away from rollout. If the
production endpoints and owners are already decided, a pilot can follow soon
after those checks. If those decisions are still open, they—not documentation
writing—control the schedule.

## Launch blockers

1. **Production configuration is unresolved.** `config/public.yml` still marks
   the site as staging and contains placeholders for the site URLs, rollout
   date, support contact, host-CA fingerprint, transfer service, and media URL.
   The production builder correctly refuses to publish it.
2. **The videos are not published.** The 15 rendered MP4s are deliberately
   excluded from Git; the configured media URL is a placeholder. A production
   HTTPS media origin must host the exact manifest versions and support browser
   byte-range playback.
3. **Video approval is automated only.** Audio, codec, captions, hashes, and
   frames have automated QA, but the manifest records no final human approval.
   Every video still needs an accuracy, pronunciation, pacing, visual, and
   sensitive-content review—especially the generated Classes 5–15.
4. **Operational instructions are not signed off.** The administrator checklist
   is incomplete for SSH, VS Code, transfer, storage, Slurm, software,
   node-local scratch, GPU, Apptainer, lab workflows, and supported versions.
5. **Privacy and domain review are outstanding.** Biomedical-data guidance,
   sharing rules, genomic/imaging scenarios, statistics, and example disclaimers
   need the named institutional and domain-owner approvals listed in the
   checklist.
6. **There is no production deployment workflow.** CI validates and uploads a
   preview artifact, but does not deploy to a reviewed production target with
   TLS, ownership, monitoring, or rollback.
7. **Rollout messaging needs one decision.** The rollout page is unlisted but
   still linked contextually, and several pages mention RCC Connect. Confirm
   that this is the user journey being launched; otherwise revise or archive
   that wording before publication.
8. **Rendered Part 1–4 artifacts need a final synchronization pass.** The
   canonical Part 4 source now includes the rootless execution model, but its
   PDF, DOCX, and PPTX derivatives must be regenerated and compared before
   release. Treat the same source-to-artifact check as required for Parts 1–3.

## Important issues fixed by this review

- Added browser-native WebVTT caption tracks to every class video; downloadable
  SRT captions remain available.
- Made `site_status: staging` a production-build blocker rather than a cosmetic
  banner value.
- Added `tools/rollout_readiness.py`, which fails closed while known launch
  blockers remain.
- Expanded the administrator checklist with media hosting, human review,
  browser caption testing, deployment, and rollout-message decisions.
- Corrected stale README statements about which classes have media sources.

## Non-blocking follow-up

- Run an online external-link check immediately before launch; CI currently
  validates internal links only. During this review, the UME privacy, Coscine,
  remote-console, and secure-tunnel links returned HTTP 200. EUR-Lex, EDPB, and the German
  federal-law pages timed out from the review environment and still require a
  clean-client check; they were not shown to be broken.
- Test current Chrome, Firefox, Safari, Edge, mobile layout, keyboard navigation,
  and a screen reader.
- Complete a novice biomedical-researcher walkthrough and edit any remaining
  operational language that assumes cluster expertise.
- Decide whether the externally hosted UME logo should be copied into the site
  to avoid a runtime dependency on another web origin.
- Replace the hard-coded historical output path in
  `build/build_new_slides.js` if that legacy regeneration helper is retained.
- Publish an update date, documentation owner, supported-version matrix, and
  review cadence.

## Release gate

Run:

```bash
python tools/validate_repo.py
python tools/build_site.py --production --output site-production
python tools/rollout_readiness.py
```

Roll out only when all three commands pass, the production media URLs have been
tested from a clean client, and the responsible owners have signed the
administrator checklist.
