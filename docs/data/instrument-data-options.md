# Choosing an instrument-data transfer path

Use this decision guide with
[Class 14: wet-lab instrument data](../course/class-14-wet-lab-data-workflows.md)
and the current [storage and transfer reference](../reference/storage-transfer.md).

## Start with six questions

1. Is the instrument still writing?
2. How many bytes and files are involved?
3. Is the source Windows, macOS, Linux, Ardia, or a vendor appliance?
4. Is the transfer one-time or recurring?
5. Does the data contain primary identifying fields?
6. Is RCC the approved destination?

RCC accepts only data covered by the applicable project approval and RCC data
policy. Primary identifying fields are not permitted.

## Browser or managed portal

Suitable for users who do not need command-line tools, modest file counts,
occasional transfer, and audited or resumable workflows where supported.

## SFTP

Suitable for Windows and macOS workstations and routine transfers. Use the
current RCC SFTP endpoint and current access instructions. Do not infer an
endpoint from the legacy pages.

## Server-to-server transfer

Suitable for facility file servers, large recurring datasets, and automation.
This avoids making a laptop an unnecessary intermediate copy.

## Automated instrument ingestion

Suitable for sequencers, recurring microscopy, mass-spectrometry exports,
long-running instruments, and high data volumes.

Automation must define:

- run-completion detection;
- retry and resume behavior;
- checksums;
- destination layout;
- permissions;
- monitoring;
- retention.

## Mounted storage

Suitable for opening a report, editing a small spreadsheet, or browsing a
selected project directory.

Not suitable for active acquisition, many-small-file datasets, multi-terabyte
copies, or computation.

## Avoid using a laptop as a router

Avoid:

```text
instrument -> laptop -> RCC
```

when this is possible:

```text
instrument or facility server -> RCC
```

The laptop path adds another copy, sleep and Wi-Fi failures, local capacity
limits, unclear deletion responsibility, and possible exposure of governed
data.

## Escalate to RCC operations when

- the dataset is expected to exceed 1 TB;
- the dataset contains more than 100,000 files;
- transfer is recurring;
- the source is a vendor appliance;
- data are exported from Ardia;
- the instrument writes continuously;
- destination permissions must be automated;
- the transfer crosses a security boundary;
- the correct data classification is uncertain.

Legacy workstation mounts are documented only for recognizing and migrating
existing setups:

- [Legacy Windows storage access](legacy-storage-windows.md)
- [Legacy macOS storage access](legacy-storage-macos.md)
