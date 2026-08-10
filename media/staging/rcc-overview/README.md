# RCC overview image staging set

These images are candidate visual material for ClusterDocs NG. They are stored
outside `docs/` deliberately: several currently contain RCC-internal hostnames,
network ranges, service placement, or operations/security topology and therefore
must not be published automatically by the MkDocs build.

## Status

- Versioned in ClusterDocs NG for editorial review and future course/material use.
- Not linked from `mkdocs.yml` or any page by this change.
- Not copied into `docs/` by this change.
- Publication requires a separate disclosure review and, where necessary, a
  learner-safe/redacted derivative.

## Images

- `rcc-login-user-journey.png` — user-oriented login and resource journey.
- `rcc-login-security-trust-boundaries.png` — corrected security and trust-boundary view.
- `rcc-login-infrastructure-view.png` — corrected service/infrastructure view.
- `rcc-login-onboarding-poster.png` — simplified learner/onboarding poster.
- `rcc-login-security-trust-boundaries-alt.png` — alternate detailed security composition retained for comparison.

## Intended later use

After editorial and publication-security review, selected images may be linked
from the onboarding, SSH/access, Slurm, storage, and security material. The
public derivative should contain only information allowed by the ClusterDocs
publication boundary.

Do not move these files into `docs/` merely to make them visible in a preview.
Create a reviewed public derivative first.
