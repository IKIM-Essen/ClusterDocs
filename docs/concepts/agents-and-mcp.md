# AI and coding agents without exposing project data

AI assistance is a major RCC capability, but using an agent should not require
sending the research dataset to the model.

The preferred RCC pattern is **data-blind by default**: an agent helps explain,
design, write, test, and debug the analysis using documentation, schemas, public
code, synthetic fixtures, and bounded diagnostics. RCC then executes the
resulting code or workflow against the real project data inside the governed
environment.

## The default agent workflow

```text
research question + non-sensitive context
                |
                v
agent helps design / write / test workflow
                |
                v
RCC checks identity + project + capability
                |
                v
RCC runs against real project data
                |
                v
permitted result / bounded diagnostic
```

The agent does not need the real rows, sequencing reads, microscopy images,
patient-derived records, or project filenames merely to be useful.

Useful context for an agent can include:

1. the scientific goal;
2. a public or synthetic example with the same structure;
3. a schema or data contract that contains no protected records;
4. the required workflow/software interface;
5. a sanitized error message or bounded diagnostic; and
6. limits that matter, such as a required method or reproducibility constraint.

## What agents are especially good for

Agents can help users and workflow developers with:

- understanding RCC documentation and error messages;
- turning an analysis idea into a script or workflow;
- creating synthetic tests before touching real data;
- reviewing Snakemake/Nextflow, Python, R, containers, and resource requests;
- converting repeated notebook work into a reproducible workflow;
- improving documentation, tests, and provenance capture;
- explaining why a job or workflow failed using bounded diagnostics; and
- preparing a change for human review before a large or consequential run.

This lets users benefit from strong coding/reasoning assistance without making
protected-data disclosure the price of using AI.

## The real data stays under RCC authority

RCC—not the agent—decides whether the requested action is allowed. The same
identity, project membership, delegated role, data policy, resource limits, and
execution controls apply whether the request came through a browser, CLI, API,
or MCP/agent interface.

An agent cannot:

- add itself or the user to another project;
- invent project membership or data approval;
- bypass resource/scheduler controls;
- convert natural-language intent into administrator authority;
- disclose project data merely because it would make debugging easier; or
- silently retry an unsafe alternative after a governed action is rejected.

## Separately approved RCC-local agent capabilities

Some RCC-local agent capabilities may be explicitly reviewed and authorized to
work near data that the user is already permitted to use. Those capabilities
remain constrained by the same project and purpose rules and should expose only
the minimum data required for the approved task.

This is an **explicit exception**, not the default assumption for coding agents.
For ordinary workflow development and user assistance, prefer the data-blind
pattern above.

## Off-site agents

Do not paste, upload, or otherwise disclose real or pseudonymised protected RCC
project data to an off-site coding agent. Use public code, documentation,
synthetic examples, and sanitized diagnostics instead.

Read [Before sharing data with a coding agent](../data/privacy-and-agents.md) for
the biomedical-data rule and practical alternatives.

## MCP and other interfaces

MCP is one interface through which an AI tool can call selected RCC capabilities.
The same capability may also be exposed through a web page, editor, command-line
tool, or API.

MCP does not decide project membership, data access, computing limits, approval,
or release status. RCC makes those decisions regardless of interface, and
important actions should retain provenance for the requesting principal,
capability, policy decision, and execution result.
