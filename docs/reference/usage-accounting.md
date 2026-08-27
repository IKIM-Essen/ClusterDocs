# RCC Usage reporting

RCC Usage is an **approximate, read-only capacity and storage-governance view**
for authorized RCC administrators/approvers. It is intended to make trends and
pressure visible early enough for a human conversation.

It is **not**:

- a billing system;
- a project entitlement system;
- an automatic punishment/quota engine; or
- proof that a particular user caused a storage or scheduler incident.

> **Availability:** the Usage view depends on the current RCC Admin deployment
> and collector activation. If the page is absent, do not infer usage from old
> screenshots or construct an unofficial replacement scan across project
> storage.

## What the Usage page shows

The intended fixed windows are:

- last 7 days;
- last 30 days;
- last 365 days.

Compute and storage are deliberately shown as related but different kinds of
resource pressure.

## Compute: capacity, use, and waiting demand

Compute reporting separates CPU and GPU capacity. The goal is to understand
whether capacity is being used, left idle, or has eligible work waiting for it.

A key distinction is **waiting demand**. Work that is eligible but waiting for a
resource should not be counted as ordinary idle capacity merely because it has
not started yet.

Usage is aggregated for cooperative planning rather than exposing a raw job
ledger as a public leaderboard.

## Storage: current size and growth

Storage reporting can show separate views for:

- homes/users;
- primary groups; and
- projects.

The selected time window provides a growth comparison in addition to current
size. Inode/file-count pressure can matter as much as bytes: millions of small
files may harm shared-storage performance even when the total number of bytes is
moderate.

## Metadata-pressure signals are approximate

RCC deliberately avoids solving a metadata problem by recursively scanning every
file on shared storage.

Instead, bounded sampling can identify large candidate areas and estimate when a
directory contains an unusually large number of entries. A value shown as
approximately a threshold can mean “at least this many”; it is a pressure signal,
not an exact forensic count.

The sampler should not retain ordinary user filenames merely to produce the
capacity dashboard.

## “Top consumer” does not mean “wrongdoer”

A project can be large for a valid scientific reason. A user can consume many
CPU/GPU hours because their approved research genuinely requires it.

Usage reporting is therefore a starting point for questions such as:

- Is this growth expected?
- Is an old intermediate tree safe to remove?
- Is a workflow creating too many tiny files?
- Is the group likely to need more storage in the next months?
- Is a workload waiting because the requested resource class is scarce?

Do not turn approximate usage ranking into an automatic misconduct or funding
decision.

## Capacity denominators can be imperfect

Several RCC namespaces may ultimately share a backend. If RCC cannot determine a
meaningful independent capacity denominator for one view, the UI should show a
share of tracked usage rather than inventing a misleading “free space” value.

For example, `/groups` and `/projects` should not be presented as two independent
physical pools merely because they are separate namespace roots.

## What users/project leads should take from Usage

If RCC contacts a group about usage, useful responses include:

- confirming whether the growth is expected;
- identifying retained data that can be archived or deleted according to the
  project retention plan;
- changing an inefficient workflow that creates excessive temporary files;
- planning storage funding/capacity before a hard ceiling is reached; and
- agreeing on a migration/archive schedule rather than performing emergency
  cleanup.

A usage discussion does not change the project's data-governance obligations:
files should not be deleted merely to improve a chart when the project requires
them to be retained.

## Privacy boundary

Usage reporting should aggregate enough information to support operations while
avoiding unnecessary disclosure of research contents. The dashboard does not
need filenames, patient information, or raw research records to show aggregate
bytes, inodes, capacity, or waiting demand.

## Relationship to RCC Analysis

RCC Analysis may use privacy-minimized historical utilization evidence to improve
future execution recommendations. That is a separate purpose from the RCC Admin
Usage dashboard, but both follow the same principle: **measure enough to improve
operations without turning raw research/job detail into a new authority source.**

See [RCC Analysis](../analysis/rcc-analysis.md) for the user-facing workflow
optimization model.
