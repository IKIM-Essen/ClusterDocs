# Novice review guide

## Rollout timing

Run this acceptance review against the newly published production site. It does
not block the initial switch because the exercise depends on that live user
journey, but it blocks declaring rollout complete. Roll back or publish a
corrected release if the reviewer finds a safety blocker or cannot complete a
required task without coaching.

## Who should review

A biomedical researcher who has not used RCC before and has not helped write
these materials. Use a test account and non-sensitive training data.

## Tasks

1. Start at the home page. Without coaching, choose the path for analysing
   data and explain what RCC is in your own words.
2. Watch Class 1 with captions on. Set up or inspect SSH, complete the bounded
   connection check, and open the approved target in VS Code.
3. Find where project data belongs and explain why a home directory is not the
   default project-data location.
4. Submit the smallest Slurm exercise, find its job ID and output, and explain
   why the command did not run directly on the submission host.
5. Find how to share data with someone in the same group, another RCC group,
   and someone outside RCC. Do not actually share sensitive data.
6. Choose a transfer route for a lab instrument and trace the intended data
   lifecycle through project storage to the planned Coscine archive flow.
7. Find help after an unexpected SSH identity warning without accepting the
   warning or deleting configuration files.

## What to record

For every hesitation, record the page, words or control that caused it, what
you expected, and what you tried next. Mark whether you were blocked, needed a
hint, or recovered alone. Screenshots must contain no usernames, keys, tokens,
patient-related names, or research data.

The review succeeds when the novice can complete the tasks safely, explain the
submission-host/compute-node and home/project-storage boundaries, and identify
the approved support route. Confusion is a documentation finding, not a test
failure by the reviewer.
