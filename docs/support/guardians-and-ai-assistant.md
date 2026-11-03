# RCC Guardians and AI-assisted support

RCC uses automation to reduce repetitive support and operations work while
keeping consequential actions bounded.

## Getting help today

Ask your **RCC approver**, who brings in the RCC team when needed. Do not send
credentials, private keys, restricted sample information, or other sensitive
project data in a message.

## Coding agent

> **Service status — available:** the RCC help assistant is open at
> <https://assistant.ikim.uk-essen.de/>. It answers from RCC documentation and
> never sees your project data unless you paste it; do not paste patient
> information.

The RCC coding agent is designed to explain RCC concepts, find documentation, interpret
common Slurm states/errors, diagnose supported environment/container problems,
explain transfer/storage guidance, prepare project requests, and escalate with
useful evidence.

It can also help convert sanitized shell scripts or command collections into a
dry-run-capable Snakemake or Nextflow workflow with explicit inputs, outputs,
resources, tests, and a pinned Apptainer runtime. Start with the
[safe conversion handoff](../paths/from-shell-scripts.md#7-ask-for-conversion-help-with-a-safe-handoff).
Scientific method, parameters, reference data, and interpretation remain the
project team's responsibility.

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
