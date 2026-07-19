# Repository strategy

## Decision

Use `clusterdocs-ng` as an independent staging repository until rollout. At rollout, merge the approved content into ClusterDocs proper and archive NG.

## Why not the RCC repository?

The RCC repository contains privileged operational material and changes according to infrastructure deployment needs. Public training has a different disclosure boundary, editorial workflow, media lifecycle and release cadence. Co-locating the site would increase the risk that infrastructure details are published accidentally.

## How examples remain accurate

- RCC remains the authoritative source for infrastructure behavior and acceptance tests.
- ClusterDocs stores learner-safe, bounded copies rather than importing administrator tools at runtime.
- Each copied example records the RCC release it was reviewed against.
- A documentation review is required when the relevant RCC contract changes.

## Promotion path

1. Test NG at a staging URL.
2. Review with novice biomedical researchers and IT-affine users.
3. Resolve production URLs, fingerprints and support contacts.
4. Publish media as institutional assets and record checksums.
5. Merge the content and validation workflow into ClusterDocs.
6. Redirect the staging URL to the production pages.
7. Archive NG read-only after the observation period.
