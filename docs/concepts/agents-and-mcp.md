# RCC-internal coding agents: what they can and cannot do

An RCC-internal coding agent—an AI tool that writes, tests, and revises code
inside the controlled RCC environment—can help you turn a research
question into code, a scheduled calculation, plots, tables, and a report.

The coding agent is a helper inside the normal RCC rules. It is not a second user
with hidden administrator access.

## A useful request

Give the coding agent four things:

1. the project you are working in;
2. the input folder or files;
3. the result you want; and
4. any limits that matter, such as a deadline or required method.

Example:

```text
Work in project melanoma_score.
Read the files in incoming/run-17 without changing them.
Create a reproducible quality-control report in results/run-17.
Show me the plan before submitting a large job.
```

Good coding agents ask before making an important change, preserve the commands or
code they used, and tell you where the results and logs were written.

## Work near the data

For protected data, the safe pattern is to run approved computation inside RCC
and return only the permitted result. Do not solve the problem by uploading the
complete dataset to an external model.

```text
coding agent describes or prepares the analysis
                  |
                  v
RCC checks your project access
                  |
                  v
analysis runs inside RCC -> permitted result
```

An off-site coding agent remains useful for public code, documentation, and
synthetic examples. See [Before sharing data with an AI
coding agent](../data/privacy-and-agents.md).

## Normal limits still apply

The coding agent:

- sees only files and services available to your RCC identity;
- cannot add itself or you to another project;
- cannot bypass data approvals or storage rules;
- should use RCC workers for substantial computation; and
- should show failures rather than hiding them or repeatedly trying unsafe
  alternatives.

## Technical note: MCP and other interfaces

MCP is one way for an AI tool to call selected RCC actions. The same actions may
also be available through a web page, an editor, a command-line tool, or an API.

MCP does not decide project membership, data access, computing limits, or
approval. RCC makes those decisions regardless of which interface is used.
