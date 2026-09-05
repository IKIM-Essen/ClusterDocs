# ClusterDocs 3 novice browser acceptance

## Rollout timing

Run this acceptance review against the exact **staged production candidate before
broad exposure**. A very small controlled pilot may precede the review so the
team can prove the deployment works in principle, but post-rollout testing alone
is not sufficient for ClusterDocs 3.

A blocker or a task that requires facilitator shell intervention prevents broad
promotion until corrected and retested.

## Who should review

Use biomedical researchers or other scientific users who:

- have not helped design ClusterDocs 3;
- have little or no HPC background;
- do not have an SSH public key enrolled for the test account; and
- use only non-sensitive synthetic/training data during acceptance.

At least one reviewer should be able to complete the path without a facilitator
explaining RCC terminology first.

## Primary zero-SSH tasks

1. Start at RCC/ClusterDocs and, without coaching, explain what RCC can help the
   researcher accomplish.
2. Choose the browser path for a simple analysis without opening the SSH,
   VS Code, Slurm, or host-topology documentation.
3. Sign in and identify the correct project.
4. Open Files and upload or select a small synthetic input.
5. Open RCC Analysis Notebook without typing a hostname, project filesystem
   path, Slurm partition, worker name, tunnel command, or Jupyter token.
6. Produce a small result and save it durably to the project.
7. Identify when the same work should move from Notebook to Workflow.
8. Run or review a small supported Workflow using safe defaults when Workflow
   mode is part of the staged candidate.
9. Leave and return to the browser product without losing owned run/session
   state that the product promises to retain.
10. Open the result in Files and download it.
11. Find the account/project self-service route and explain that project actions
   remain role-authorized rather than making every user an RCC administrator.
12. Find the AI/agent guidance and explain how an agent can help develop or
   debug a workflow **without receiving the real research dataset**.
13. Find how an instrument such as a sequencer or microscope can feed a project,
   and identify that acquisition data should land in project storage rather than
   a personal laptop/home directory.
14. Find the lifecycle guidance and distinguish current project storage from
   governed archival/preservation such as the staged Coscine route.
15. Find the approved support route after an unexpected failure.

If RCC Analysis is absent from the staged candidate, the zero-SSH browser product
is not ready for broad promotion. Do not substitute SSH acceptance for this test.

## Separate advanced-user acceptance

Run an independent acceptance session for users who actually need SSH, VS Code,
direct Slurm, containers, workflow engines, GPUs, and lower-level storage tools.
A novice researcher does not have to pass that exam for the browser product to
be usable.

## What to record

For every hesitation, record:

- page/control and task;
- what the reviewer expected;
- what they tried next;
- whether they recovered alone, needed a hint, or were blocked; and
- whether the terminology or visual model caused the hesitation.

Screenshots and notes must contain no usernames, keys, tokens, patient-related
names, or real research data.

## Acceptance criteria

The primary review succeeds when a zero-SSH researcher can complete the
Files -> Analysis -> Files journey, understand project ownership and
Notebook-vs-Workflow, find help, and explain the data-blind agent boundary
without facilitator shell intervention.

Confusion is a product/documentation finding, not a failure by the reviewer.
