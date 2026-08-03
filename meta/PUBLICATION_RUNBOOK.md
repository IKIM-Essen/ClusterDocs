# ClusterDocs NG GitHub Pages publication runbook

This runbook keeps the video publication, source promotion, and Pages cut-over
as separate transactions. A failed gate stops the process without changing the
currently published documentation.

## Fixed publication targets

- Source repository: `IKIM-Essen/ClusterDocs`
- Reviewed source branch: `main`
- Pages branch: `gh-pages`
- Site URL: <https://ikim-essen.github.io/ClusterDocs/>
- Media URL: <https://ikim-essen.github.io/ClusterDocs/media/rcc-onboarding/>
- Primary automatic validation: Gitea
- GitHub validation: manually dispatched fallback only

## 1. Verify the media transaction

The media commit is deliberately independent of the site cut-over. Run both
checks against the final manifest:

```bash
python tools/media_gate.py --local-dir /path/to/final-videos
python tools/media_gate.py \
  --base-url https://ikim-essen.github.io/ClusterDocs/media/rcc-onboarding
```

The second command range-tests and fully downloads all 15 videos. It must
report `media publication gate: PASS (15 videos)`. Do not replace a failed file
in place without updating the source manifest, cache-busting URL, and retained
evidence together.

## 2. Promote the source through review

Merge the `clusterdocs-ng` publication branch into `main` only after local
validation and the Gitea result pass. Preserve the old `main` history; do not
rewrite it. The source merge does not itself alter the live Pages branch.

```bash
python tools/validate_repo.py
python tools/rollout_readiness.py
python tools/build_site.py --production --output site-production
python tools/check_site_links.py site-production
```

All commands must pass. A `staging` site status, incomplete human video review,
or an unchecked institutional gate blocks the production build and cut-over.

## 3. Review the exact rendered candidate

Serve `site-production` on loopback and review the exact output on current
desktop and mobile browsers. Check the home page, course overview, at least one
deep reference page, responsive navigation, all embedded video controls, one
caption track, and one download link. Also verify that no administrative files
or internal infrastructure values are published.

Record the source commit, build command, reviewer, browsers, and result in the
cut-over pull request.

## 4. Cut over Pages as one guarded commit

Before changing `gh-pages`, record its current commit and create an immutable
rollback tag. The first retained tag is `pages-legacy-20260803`.

Create a clean `gh-pages` checkout. Replace generated site files with the exact
`site-production` output, but preserve `media/rcc-onboarding/` unchanged. Verify
the local Pages tree again, make one cut-over commit, and push only if the remote
`gh-pages` commit still equals the reviewed predecessor. Never force-push the
Pages branch.

## 5. Post-cut-over acceptance

Wait for GitHub Pages propagation, then repeat:

- the full online media gate;
- internal-link validation against the hosted site;
- desktop and mobile visual review;
- embedded playback and captions;
- essential external service links.

Keep the old site available through the rollback tag until the acceptance
record is complete.

## Rollback

If the new site fails acceptance, revert the single Pages cut-over commit and
push the resulting rollback commit. Do not reset or force-push `gh-pages`.
Because the media upload is independent and unlinked by the legacy site, it may
remain in place during rollback. Confirm the legacy home page and key links
after GitHub Pages propagates the revert.
