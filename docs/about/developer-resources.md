# Build portable RCC projects with Codex, Claude, or Cowork

_Project development_

Use the cluster contract plus the versioned Application & Agent Contract so generated code, client products, and device requests stay inside logical RCC capabilities instead of binding to private infrastructure.

S

### Start with the cluster

Design for shellhosts, bounded interactive allocations, Slurm workers, shared data, and job-local scratch.

[Open the cluster guide](https://rcc.ikim.uk-essen.de/developers/cluster-integration.md)

A

### Agent contract

Choose a component class, request logical capabilities, and declare missing capabilities instead of inventing infrastructure paths.

[Read the contract](https://rcc.ikim.uk-essen.de/developers/application-agent-contract.md) · [Manifest schema](https://rcc.ikim.uk-essen.de/developers/rcc-application-agent-manifest.schema.json)

C

### Capability catalogs

Use the cluster-wide catalog plus the versioned application capability and component-class catalogs.

[Cluster capabilities](https://rcc.ikim.uk-essen.de/developers/cluster-capabilities.yml) · [Application capabilities](https://rcc.ikim.uk-essen.de/developers/contracts/rcc/v1/capabilities.yml)

H

### Project handoff

Declare non-secret project, resource, data, software, interactive, and service requirements.

[Download the handoff](https://rcc.ikim.uk-essen.de/developers/project-cluster-handoff.yml) · [Schema](https://rcc.ikim.uk-essen.de/developers/project-cluster-handoff.schema.json)

P

### Client products and devices

The coding-agent entrypoint defines product-repository boundaries and proposal-only proxy requests for any client-managed device.

[Download project instructions](https://rcc.ikim.uk-essen.de/developers/AGENTS.md)

W

### Managed web services

Use the additional profile for a static site, protected application, or application-local database.

[Open the service guide](https://rcc.ikim.uk-essen.de/developers/project-vhost-dbhost-integration.md)

T

### Contract checker

Validate `rcc-app.yml`, explain capabilities, and catch a small set of high-confidence lane escapes before review.

[Download rcc-contract.py](https://rcc.ikim.uk-essen.de/developers/rcc-contract.py) · [Example manifest](https://rcc.ikim.uk-essen.de/developers/contracts/rcc/v1/examples/slurm-batch.yml)

I

### Coding-agent files

Add project-safe instructions without exposing RCC operational configuration or authority.

[Download AGENTS.md](https://rcc.ikim.uk-essen.de/developers/AGENTS.md) · [Download CLAUDE.md](https://rcc.ikim.uk-essen.de/developers/CLAUDE.md)

_Safe boundary_

## Portable preparation is not infrastructure authority

- Anything absent from the application capability catalog is unavailable; declare it under unmet_requirements.

- Never place credentials, connection material, private data, or unpublished results in Git.

- Do not depend on one physical worker, a node-local environment, or the only copy of data on local disk.

- Client-device proxy proposals use exact destinations and never activate their own access.

- Leave scheduling policy, storage, host, network, certificate, proxy, and service assignments to RCC review.

- Require separate RCC evidence before claiming a cluster run or live service.
