# ClusterDocs split: portable RCC core and Essen site documentation

> **Proposal — not published or deployed.** The current
> `IKIM-Essen/ClusterDocs` repository remains authoritative for its existing
> publication until a separate reviewed migration. No repository rename or
> website change is approved by this page.

## Destination

| Planned repository | Owns |
| --- | --- |
| `clusterdocs` (new generic source) | Site-neutral RCC concepts, Slurm use, safe storage and I/O, reproducible workflows, desktop VS Code and Positron workflow, development-session lifecycle, generic screenshots/tutorials and documentation build contract |
| `clusterdocs-site-essen` (eventual rename of current `ClusterDocs`) | Current Essen-facing website, local SSH/DNS and host-key instructions, institutional account/device processes and policies, accepted service availability, site support information, real site media, publication/redirects and local overlays |

Portable technical behavior is governed by `IKIM-Essen/rcc`. Site operational
configuration stays in `rcc-site-essen`, not copied into public documentation
or committed secrets. The eventual site docs must use a reviewed **public**
projection of site facts.

## Current repository migration inventory

Initial classifications, subject to page-by-page review:

| Current content | Proposed classification |
| --- | --- |
| `docs/getting-started/macos.md`, `docs/getting-started/windows.md`, `docs/getting-started/vscode.md` | Mixed — extract portable editor/SSH guidance; site-specific addresses/enrollment stay in Essen |
| `docs/connecting/stable-endpoints.md` | Essen site — real hostnames, routing and maintenance |
| `docs/reference/slurm.md`, `docs/course/class-05-slurm.md` | Mixed — generic Slurm concepts plus approved local partition names/limits |
| `docs/concepts/jump-shell-compute.md` | Mixed — generic topology and local endpoints |
| `meta/PUBLICATION_RUNBOOK.md`, `meta/GITEA_GITHUB_PAGES_DEPLOYMENT.md` | Essen site — site URL, publication/media endpoint and deployment |
| `docs/security/*`, `docs/data/*` and course text | Mixed until independently reviewed for institution-specific data protection, policy and service availability |
| Images, subtitles, narration, decks, PDFs and video/media manifests | Review separately for site names, user identities, hostnames, hidden metadata and licensing |

**Do not fork the full current Git history as the new generic repository.**
Removed site information would remain recoverable from history. Curate and
review portable content into a fresh generic history instead.

## Migration waves

1. **Freeze and classify.** Inventory current URLs, navigation, custom
   `tools/build_site.py` renderer, `mkdocs.yml`, assets and media; record
   current accepted site deployment state, link paths and screenshots.
2. **Extract portable source.** Create the new `clusterdocs` repository only
   when separately authorized. Move reusable pages with placeholders and an
   explicit documented extension contract. Keep local details in the current
   repo's Essen overlay. Generic source must contain no Essen-specific
   addresses, contacts, fingerprints, identity data, policies or host lists.
3. **Build the site with a pinned core.** The Essen site selects an exact
   generic core commit/digest and supplies its own reviewed public manifest.
   Unknown placeholders and unrecognized overrides fail the build. Neither
   docs repository reads private RCC secrets.
4. **Adversarial and publication tests.** Leakage check for text and assets,
   link audit, navigation and search-index parity, required redirects,
   accessibility/localization, synthetic screenshots, data privacy review,
   installation and Slurm canary.
5. **Preserve existing web access.** Verify the current
   `https://ikim-essen.github.io/ClusterDocs/` URL, asset paths, media, DNS
   and deep links before any repository rename or website cutover. Rehearse
   old-to-new redirects where feasible. No abrupt removal of current pages.
6. **Publish only after site acceptance.** Rename `ClusterDocs` to
   `clusterdocs-site-essen` only with explicit operator authorization and
   verified GitHub Pages/redirect behavior; keep the generic source distinct.
   The site-specific public build remains the single publication authority.

## RCC Connect content boundary

**Generic:** Laptop IDE → trusted SSH gateway → client-only shellhost → user-
and project-bound Slurm development allocation → VS Code Server or Positron
backend on the worker. Document resource accounting, cgroup adoption,
reconnect, cancellation, batch handoff, bounded `rg` and workspace indexing.

**Essen:** Download and signing route, approved jump/shellhost addresses,
trusted SSH worker-key distribution, currently accepted service status,
device registration/2FA, partitions/limits and institutional support.

The current RCC Connect lessons in this branch are an **Essen pilot draft**
with reusable text. They are not yet the generic source and should not be
published or copied as a whole into generic history.

## Acceptance and rollback

All old pages remain intact until the mixed-content migration is independently
reviewed. Site preview must reproduce the current user journey, media and
links. Failure in generic validation, missing approved site manifest, release
provenance, public redirects, or live SSH/Slurm acceptance means **hold** and
keep serving the original site.

Companion architecture proposal:
`IKIM-Essen/rcc` → `docs/architecture/clusterdocs-core-site-boundary.md`.
