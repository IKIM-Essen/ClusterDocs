# RCC documentation origin and GitHub contribution model

## User-facing decision

ClusterDocs is an RCC product surface. The target reader-facing location is:

`https://rcc.ikim.uk-essen.de/docs/`

Reading RCC documentation must not require a GitHub account or an RCC account. Account setup, recovery, access-request guidance, and incident/help material must remain reachable when a reader is not signed in.

GitHub remains the preferred public collaboration surface for documentation changes:

- source browsing;
- issues for documentation problems;
- user branches/forks where applicable;
- pull requests;
- review discussion.

This is an intentional transition: a reader stays inside RCC while reading and enters GitHub only when they choose to contribute.

## Contribution affordances

Every generated documentation page should eventually expose two contextual actions:

1. **Edit this page on GitHub** — points to the exact Markdown source path in `IKIM-Essen/ClusterDocs`;
2. **Report a documentation problem** — opens a GitHub issue path with the page identity available to the contributor.

The links must not imply that GitHub is the production documentation origin or RCC authentication authority.

## Publication migration

The current production-origin declarations still point to GitHub Pages and remain unchanged until the RCC `/docs/` route is live and accepted. Migration is a release transaction, not a textual substitution.

Before changing `site_url` and production-origin validators, prove:

- `https://rcc.ikim.uk-essen.de/docs/` serves the exact accepted ClusterDocs build;
- nested routes, assets, search/navigation, videos/captions, and relative links work below `/docs/`;
- old GitHub Pages URLs have an explicit compatibility/redirect policy;
- RCC Home and contextual help link to `/docs/` without bouncing through GitHub;
- signed-out readers can reach signup, activation, recovery, and access-request guidance;
- GitHub contribution links preserve the exact source page;
- rollback restores the previous accepted documentation tree without changing source history.

Once those gates pass, `site_url`, release validators, generated canonical metadata, Expedition overlays, and publication documentation should move together to the RCC origin.

## Relationship to RCC access

Most newcomers receive a recipient-bound invitation/setup URL by email. ClusterDocs should describe that as the normal path.

For a newcomer without an invitation, documentation should use the user concept **Get RCC access** rather than asking the reader to select an account type, LDAP group, guest class, or sponsor mechanism. RCC resolves the requested project/team/work intent into the appropriate governed identity or project-access workflow.

SSH activation is an existing-account/bootstrap mechanism and must not be taught as ordinary signup.
