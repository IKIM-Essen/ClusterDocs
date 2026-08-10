# Maintaining RCC Expedition releases

Current release:

```text
RCC-Expedition-USB-v1.0.0.zip
SHA-256 680cc16b4d226de59e4dd7c6e0468ac3e9137b3bb7d438b94ad0c93152aa18c7
```

## Publication policy

RCC Expedition may be published after static validation and content review.

A native Windows 11 smoke test is **recommended during rollout but is not a
publication blocker**. Do not wire that test into the MkDocs build or site
deployment gate.

If a native Windows test identifies a defect, publish a corrected versioned
course asset and update `docs/rcc-expedition.md`.

## Ownership boundary

RCC Expedition owns workstation-security onboarding and the local
challenge-first learning experience.

ClusterDocs owns mutable RCC technical facts. Prefer links from the course to
ClusterDocs over copying changing RCC configuration into the download.

All embedded ClusterDocs links must use the current production origin
`https://ikim-essen.github.io/ClusterDocs/` and, where a matching NG lesson
exists, link to that future page rather than a retired legacy route or only the
home page. A possible later `docs.ikim.uk-essen.de` CNAME is not active release
input. Rebuild and validate the release with:

```bash
python tools/rebuild_expedition_release.py
python tools/validate_expedition_release.py
```

Commit the resulting ZIP, outer checksum, and the checksum printed on the
public Expedition page together. The repository validator checks the outer
digest, every inner digest, archive path safety, and embedded documentation
origins.
