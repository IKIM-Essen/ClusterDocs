# Class 14: from instrument to analysis for wet-lab teams — video narration

## Slide 1: Class 14: from instrument to analysis for wet-lab teams

Welcome to Class 14: from instrument to analysis for wet-lab teams. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning objectives

After this course, you should be able to: distinguish an instrument-control computer from storage and compute systems; explain how the Lab network limits Internet exposure while preserving approved server and proxy-based update access; choose among browser upload, SFTP, mounted storage, server-to-server transfer, and automated ingestion; estimate whether a dataset is difficult because of size, file count, or both; verify a transfer before deleting the source; explain why analysis should not run on an instrument-control computer; identify which data may be placed on RCC; place instrument data in an approved RCC project rather than a user's home directory; recognize and replace a saved Windows or macOS.

## Slide 3: Four different roles

### Instrument-control computer This system operates the sequencer, mass spectrometer, or microscope. Its priorities are stable acquisition, vendor support, enough local space for the current run, and minimal software change. Do not use it as a general-purpose analysis workstation unless the instrument facility explicitly supports that use. Where suitable, ask RCC whether the device can join the Lab network. Do not connect it yourself or guess network, server, or proxy settings. RCC must first review the owner, software and update requirements, required direct server endpoints, vendor remote-support needs, data flow, and destination project. The Lab network is not an Internet connection with extra firewall rules..

## Slide 4: The instrument-data lifecycle

At every transition, somebody must know who owns the next step. This is the target lifecycle for data using the planned RCC-to-Coscine archive service. Coscine eligibility and the transfer route must still be confirmed for the specific project before real data moves. ### The RCC landing point is a project, not a home directory Instrument data must land in the approved RCC project area. A user's home directory is for personal configuration, small source files, and individual working material—not authoritative research data or shared instrument output. This separation matters for governance and legal compliance: a project connects the data to an approved purpose, accountable owner.

## Slide 5: Before starting a run

Record: project and responsible researcher; facility and instrument; run identifier; sample identifiers without direct patient identifiers; expected output size and file count; source directory and destination project; required analysis; retention requirements; person responsible for confirming the transfer. Use a directory name such as: Do not place patient names, birth dates, hospital numbers, or similar fields in filenames.

## Slide 6: Choosing a transfer method

Mounted storage is convenient but is not the preferred path for instrument datasets.

## Slide 7: File count matters

A 500 GB dataset in five files can be easier to move than a 50 GB dataset in 500,000 files. Record total bytes, file count, largest file, directory depth, and whether files are still being written. Microscopy and mass-spectrometry workflows often create preview images, indexes, sidecars, databases, tiles, channels, or time-point files. Do not copy a live acquisition directory unless the facility has a tested ingestion process.

## Slide 8: When RCC is useful

RCC is appropriate for reproducible batch processing, many samples or images, CPU parallelism, GPU acceleration, large memory, containers, automated quality control, and durable project-level results. RCC is not automatically appropriate for live instrument control, diagnostic workflows, unsupported vendor databases, or data with primary identifying fields.

## Slide 9: A safe handoff package

The manifest should record relative path, size, role, sample ID, format, and creation time. Generate checksums only after acquisition is complete:

## Slide 10: Verification

Verify that: the destination exists; file count matches; total size is plausible; checksums match where practical; completion markers exist; key files open in the correct software; permissions allow the project team to read the data; source and destination are recorded. Only then should deletion be considered under the facility retention policy.
