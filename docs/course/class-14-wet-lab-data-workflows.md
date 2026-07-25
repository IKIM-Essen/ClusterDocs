# Class 14: from instrument to analysis for wet-lab teams

This course is for laboratory assistants, technical staff, students, and
researchers who primarily operate instruments rather than Linux systems.

Typical participants use Windows or macOS and work with:

- Illumina sequencers;
- Oxford Nanopore sequencers;
- mass-spectrometry systems managed through Ardia;
- light or electron microscopes;
- in-vivo or intravital imaging systems; or
- image-analysis workstations.

You do not need to become a system administrator. You do need to understand
where instrument data are written, which copy is authoritative, how to transfer
data safely, and when RCC compute or storage is useful.

## Learning objectives

After this course, you should be able to:

- distinguish an instrument-control computer from storage and compute systems;
- choose among browser upload, SFTP, mounted storage, server-to-server transfer,
  and automated ingestion;
- estimate whether a dataset is difficult because of size, file count, or both;
- verify a transfer before deleting the source;
- explain why analysis should not run on an instrument-control computer;
- identify which data may be placed on RCC;
- place instrument data in an approved RCC project rather than a user's home
  directory;
- recognize and migrate documented legacy Windows and macOS storage paths; and
- prepare a clean handoff to bioinformatics or image-analysis staff.

## 1. Four different roles

### Instrument-control computer

This system operates the sequencer, mass spectrometer, or microscope. Its
priorities are stable acquisition, vendor support, enough local space for the
current run, and minimal software change.

Do not use it as a general-purpose analysis workstation unless the instrument
facility explicitly supports that use.

### Facility or acquisition storage

This is the first destination outside the instrument computer. It may be a
laboratory file server, vendor-managed repository, Ardia-managed system,
acquisition NAS, project share, or automated upload endpoint.

### RCC durable project storage

RCC project storage is for approved, governed research data without direct
identifiers and for durable analysis results. It is not a clinical archive, a
vendor operational database, or a place for primary identifying fields.

### RCC compute node

A compute node runs scheduled analysis. Active temporary and random I/O should
normally occur on node-local storage, with validated results returned to durable
project storage.

## 2. The instrument-data lifecycle

```text
plan experiment
    -> acquire data
    -> close and complete the run
    -> preserve the authoritative original
    -> transfer to an approved RCC project
    -> verify file count, size, and checksums
    -> register run and sample metadata
    -> analyse through Slurm or a supported service
    -> return validated results to the RCC project
    -> select and document the retained archive set
    -> transfer the approved archive set to Coscine
    -> verify archive acceptance
    -> remove temporary or superseded RCC copies according to policy
```

At every transition, somebody must know who owns the next step.

This is the target lifecycle for data using the planned RCC-to-Coscine archive
service. Coscine eligibility and the transfer route must still be confirmed for
the specific project before real data moves.

### The RCC landing point is a project, not a home directory

Instrument data must land in the approved RCC project area. A user's home
directory is for personal configuration, small source files, and individual
working material—not authoritative research data or shared instrument output.

This separation matters for governance and legal compliance:

- a project connects the data to an approved purpose, accountable owner, and
  project-specific governance;
- project membership provides a managed, attributable access boundary instead
  of making one person's account the de facto owner;
- team members can continue the work when a user changes role or leaves;
- retention, access review, archival, legal hold, and deletion decisions can be
  applied to the project record; and
- it reduces uncontrolled personal copies whose purpose, access, and deletion
  status cannot be demonstrated reliably.

It also matters operationally and for performance:

- home capacity and service behavior are intended for personal working files,
  not large or recurring instrument datasets;
- large transfers and many-small-file trees can consume home quota and create
  metadata load that affects unrelated interactive work;
- scheduled workflows need a stable team-owned input and output location; and
- temporary high-I/O analysis belongs on job-local storage, with validated
  results copied back to the project—not written intensively to either home or
  shared project storage.

Use this pattern:

```text
instrument or facility storage
    -> approved RCC project/incoming
    -> job-local analysis workspace
    -> approved RCC project/results
    -> verified Coscine archive set
```

Do not use:

```text
instrument -> /home/<user> -> analysis -> forgotten personal copy
```

Continue with [Class 15: manage the research data lifecycle](class-15-data-lifecycle.md)
for selection, retention, Coscine archival, and RCC cleanup.

## 3. Before starting a run

Record:

- project and responsible researcher;
- facility and instrument;
- run identifier;
- sample identifiers without direct patient identifiers;
- expected output size and file count;
- source directory and destination project;
- required analysis;
- retention requirements;
- person responsible for confirming the transfer.

Use a directory name such as:

```text
PROJECT_YYYY-MM-DD_INSTRUMENT_RUNID
```

Do not place patient names, birth dates, hospital numbers, or similar fields in
filenames.

## 4. Choosing a transfer method

| Situation | Preferred option |
|---|---|
| A few reports or spreadsheets | browser portal or mounted storage |
| Routine workstation transfer | SFTP or managed transfer |
| Large directory with many files | archive or manifest, then managed transfer |
| Recurring multi-terabyte output | automated facility ingestion |
| Data already on a facility server | server-to-server transfer |
| Editing one small file in place | legacy SSHFS may be acceptable |
| Compute-intensive analysis | transfer first, then use Slurm |

Mounted storage is convenient but is not the preferred path for instrument
datasets.

## 5. File count matters

A 500 GB dataset in five files can be easier to move than a 50 GB dataset in
500,000 files. Record total bytes, file count, largest file, directory depth,
and whether files are still being written.

Microscopy and mass-spectrometry workflows often create preview images,
indexes, sidecars, databases, tiles, channels, or time-point files. Do not copy
a live acquisition directory unless the facility has a tested ingestion
process.

## 6. Illumina sequencing

An Illumina run may include run metadata, base calls, quality information,
logs, completion markers, sample sheets, and demultiplexed FASTQ files.

The facility must define whether the authoritative original is the complete run
directory, base calls, FASTQ files, or a combination. Do not delete a run
directory merely because FASTQ files exist.

Recommended handoff:

1. wait for acquisition and required conversion to complete;
2. freeze the source directory;
3. record size and file count;
4. transfer to durable storage;
5. verify checksums or a validated transfer report;
6. preserve sample sheets and run metadata;
7. notify the analysis owner.

Keep FASTQ files compressed when analysis tools support compressed input.

## 7. Oxford Nanopore sequencing

Oxford Nanopore runs may produce POD5 or FAST5 signal data, sequencing
summaries, run reports, base-called FASTQ, alignment output, and continuously
updated logs.

Decide before the run:

- where base calling occurs;
- whether raw signal must be retained;
- whether data are exported incrementally;
- how open files are handled;
- how complete and partial runs are distinguished.

For long-running acquisition, use a facility-approved incremental ingestion
process rather than repeated drag-and-drop copies.

## 8. Mass spectrometry and Ardia

Ardia is part of the instrument and data-management environment, not merely a
folder tree.

Before export, determine:

- whether analysis requires vendor-native raw data;
- whether Ardia remains the authoritative repository;
- whether the export is immutable;
- which processing method and software version created derived results;
- whether files must remain together.

Possible RCC handoffs include supported vendor-native exports, mzML or another
facility-approved open format, result tables, spectral libraries, QC reports,
and manifests.

Do not copy an internal Ardia database or application directory as if it were a
normal project folder. Use an Ardia-supported export or integration path.

Preserve instrument, acquisition method, processing method, software version,
database version, export time, operator, and checksum.

## 9. Microscopy and imaging

The Imaging Center Essen covers light and electron microscopy, in-vivo and
intravital imaging, and image analysis. Relevant instrument classes include:

- widefield and fluorescence microscopy;
- confocal and super-resolution microscopy;
- two-photon and light-sheet microscopy;
- IVIS and mouse ultrasound;
- TEM, SEM, and FIB-SEM;
- CLEM workflows;
- tiled, multichannel, time-series, and three-dimensional acquisition.

Microscopy size grows across multiple dimensions:

```text
subjects x positions x tiles x z-planes x channels x time points
```

Ask before acquisition:

- Which vendor-native format is authoritative?
- Is an open-format export required?
- Will calibration and metadata survive export?
- Is the dataset one container or many files?
- Does analysis need GPU, large RAM, or local NVMe?

Do not export every image to TIFF “just in case.” That can remove metadata,
multiply file count, and greatly increase storage.

## 10. When RCC is useful

RCC is appropriate for reproducible batch processing, many samples or images,
CPU parallelism, GPU acceleration, large memory, containers, automated quality
control, and durable project-level results.

RCC is not automatically appropriate for live instrument control, diagnostic
workflows, unsupported vendor databases, or data with primary identifying
fields.

## 11. A safe handoff package

```text
RUN/
├── README.txt
├── MANIFEST.tsv
├── CHECKSUMS.sha256
├── metadata/
├── raw-or-authoritative-export/
└── reports/
```

The manifest should record relative path, size, role, sample ID, format, and
creation time.

Generate checksums only after acquisition is complete:

```bash
find RUN -type f -print0 | sort -z | xargs -0 sha256sum -- > RUN/CHECKSUMS.sha256
```

## 12. Verification

Verify that:

- the destination exists;
- file count matches;
- total size is plausible;
- checksums match where practical;
- completion markers exist;
- key files open in the correct software;
- permissions allow the project team to read the data;
- source and destination are recorded.

Only then should deletion be considered under the facility retention policy.

## 13. Windows and macOS

Start with a browser portal, approved SFTP client, facility-managed ingestion,
or automated server-to-server transfer.

Historical ClusterDocs mounted selected RCC directories using SSHFS. These
paths remain documented so existing setups can be recognized and migrated:

- [Legacy Windows storage access](../data/legacy-storage-windows.md)
- [Legacy macOS storage access](../data/legacy-storage-macos.md)

Do not reuse their endpoint values unchanged. After migration to the approved
RCC alias, use SSHFS only for small files and occasional editing—not bulk
instrument transfer or computation.

## 14. Practical exercise

Using synthetic or non-sensitive data:

1. identify the instrument and output type;
2. estimate size and file count;
3. choose a transfer path;
4. create a run directory and manifest;
5. transfer to an approved test destination;
6. verify the copy;
7. classify raw, derived, temporary, and durable files;
8. describe the next analysis step.

## Take-home rule

> Protect acquisition first. Preserve an authoritative original. Use a transfer
> method suited to the data shape. Verify before deleting. Analyse through
> supported RCC services rather than on the instrument-control computer.

## Completion gate

Using synthetic or non-sensitive data, produce a handoff plan that identifies
the authoritative source, approved destination, transfer method, verification
evidence, retention owner, and next Slurm or service-based analysis step.
