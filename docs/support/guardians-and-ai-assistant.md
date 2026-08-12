# RCC Guardians and AI-assisted support

RCC uses automation to reduce repetitive support and operations work while
keeping consequential actions bounded.

## Coding agent

The RCC coding agent can explain RCC concepts, find documentation, interpret
common Slurm states/errors, diagnose supported environment/container problems,
explain transfer/storage guidance, prepare project requests, and escalate with
useful evidence.

## Guardians

Guardians observe scheduler, service, hardware, storage, and policy state.
Observation and action remain separate.

## Constrained actors

A Guardian does not receive unrestricted root simply because it can diagnose a
problem. Supported remediation uses named operations such as:

```text
drain node with reason
restart approved service
prepare archive plan
```

rather than arbitrary shell access.

## Escalation is valid

Success includes safe resolution, a useful explanation, preparation of a
guarded request, or correct recognition that a human operator is required.

For project actions, Guardians use the same authority model as users and
delegated proxies.

Never paste protected research data, credentials, private keys, or MFA secrets
into a support conversation unless an explicitly approved process requires it.
