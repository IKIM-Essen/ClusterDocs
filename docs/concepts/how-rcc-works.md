# Off-site coding agents must not receive RCC research data

A coding agent—an AI tool that writes, tests, and revises code—can save a great
deal of time. You can describe the table, plot, report, or workflow you want and
ask it to build reproducible code.

But RCC projects may contain patient-derived, genetic, confidential,
unpublished, or otherwise protected material. **You must not paste, upload, or
otherwise make real or pseudonymised RCC project data available to an off-site
coding agent.** Sending a prompt or file to such an agent is data processing and
disclosure outside the controlled RCC project environment.

Health and genetic data are specially protected. [Article 9 of the
GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/art_9/oj) starts from a
prohibition on processing these data unless a specific exception and safeguards
apply. German research provisions such as [section 27
BDSG](https://www.gesetze-im-internet.de/bdsg_2018/__27.html) impose necessity
and protective measures; they are not blanket permission to disclose research
data to another service. Medical confidentiality may impose additional duties
under [section 203
StGB](https://www.gesetze-im-internet.de/stgb/__203.html).

An agent being licensed, commercially available, institutionally provided, or
described as “approved” does **not** authorize it to receive RCC data. A user
cannot create the required legal basis, processor arrangement, safeguards, or
third-country transfer basis by opening an account or accepting a service's
terms. Any exceptional off-site processing arrangement must be established and
explicitly authorized by the responsible institution for that exact service
and purpose. Do not infer such authorization from this documentation.

There are two practical routes.

## Route A: use a coding agent inside RCC

Use an RCC-internal coding agent when it is available for your project. It works
inside the RCC environment under your normal project access. The real data stays
in RCC while the agent prepares code, requests bounded cluster computation, and
writes the permitted results back to the project.

```text
your request + real project data
              |
              v
     RCC-internal coding agent
              |
              v
       RCC workers -> project results
```

The agent does not become an administrator and does not gain access to another
project. You still review important actions, and substantial computation runs
through Slurm.

Read [how the RCC-internal coding-agent route works and what it can
do](agents-and-mcp.md).

## Route B: give an off-site coding agent synthetic data only

An off-site coding agent can still write useful code without seeing the real
dataset. Give it a small coding example in which every row and value is
invented, but the safe structure and the analysis task resemble the real
problem.

```text
real data stays in RCC
          |
          +--> invented coding example --> off-site coding agent
                                                |
                                                v
                                           general code
                                                |
                                                v
                              test and run inside RCC on real data
```

Bring the returned code into RCC, inspect it, test it on the invented example,
and then run it against the real input inside RCC. Real inputs, revealing error
messages, and real outputs do not go back to the off-site agent.

[Class 18 shows how to make the synthetic coding example and bring the code
back safely](../course/class-18-coding-agents.md). It includes a downloadable
example bundle and a prompt you can reuse. The documented manual method is
available now; **Make coding example** is the intended future shortcut.

## Which route should I choose?

| Situation | Route |
|---|---|
| The agent runs inside RCC and is available for this project | **A — work inside RCC** |
| The agent is a website, desktop service, or other system outside RCC | **B — synthetic data only** |
| You cannot tell where the agent processes or stores prompts and files | Do not attach the real data; use **B** |
| A useful synthetic example cannot be made without exposing protected detail | Use **A** or continue without an agent |

## What not to send outside RCC

Do not paste or upload real project files, real rows, identifiers, free text,
exact dates, revealing filenames, screenshots, real outputs, or unredacted error
messages to an off-site coding agent. Shuffling rows, hashing identifiers, or
changing names does not make the remaining data synthetic.

For the fuller data boundary, read [before sharing data with a coding
agent](../data/privacy-and-agents.md).

## The goal is still simple

Whichever route you use, ask for code that:

- accepts explicit input and output paths;
- does not modify its input;
- records its command, package versions, and logs;
- is tested on small invented data first; and
- uses RCC workers for substantial computation.

The result should be reviewable code and reproducible project output—not a
conversation that only the coding agent can reconstruct.

## Related guidance

- [RCC-internal coding agents and MCP](agents-and-mcp.md)
- [Class 18: off-site coding agents with synthetic data](../course/class-18-coding-agents.md)
- [Where you can work with RCC](workbench-interfaces.md)
- [Projects and supported actions](projects-and-capabilities.md)
- [RCC Expedition for new users](../rcc-expedition.md)
