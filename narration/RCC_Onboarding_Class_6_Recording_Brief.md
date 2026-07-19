# Class 6 recording brief

## Purpose

Record an 8–10 minute introduction to the governed RCC vhost platform. The video should help a biomedical researcher decide whether a website is appropriate and help a junior developer understand the application contract before copying the example.

## Visual structure

1. **Definition:** browser → RCC gateway → project application → approved data.
2. **Four supported patterns:** static information, read-only application, controlled writes, controlled uploads.
3. **Out-of-scope panel:** no general VM, raw filesystem browser, database administration or long-running computation.
4. **Access model:** low-friction hospital sign-in; stronger external authentication.
5. **Responsibility split:** RCC platform versus project team.
6. **Safe patterns:** approved database views, opaque file identifiers, upload staging, scheduled computation.
7. **Governance:** project lead request, independent approval, reviewed deployment.
8. **Exercise:** local unit tests and request checklist.

## Tone

- Use plain language before introducing technical terminology.
- Explain the benefit of each security boundary rather than presenting it as a restriction.
- Emphasize that the platform reduces work for developers.
- Do not present the class as permission to expose arbitrary internal data.
- Do not show internal addresses, infrastructure hostnames, topology or administrative screens.

## Recording notes

- Aim for 125–135 words per minute.
- Pause briefly after each supported site pattern.
- Display code only when discussing the copyable example.
- Use a fictional project and synthetic data in screenshots.
- Leave production URLs out of the recording until rollout values are final.
- Record the final URL and rollout-specific introduction as a short replaceable segment.

## YouTube publication later

At rollout, prepare:

- a title without version-specific infrastructure terminology;
- the chapter list from the narration script;
- reviewed captions;
- a description linking to the canonical ClusterDocs page;
- a note that the website, not the video, contains the current instructions;
- comments moderated or disabled according to institutional policy.
