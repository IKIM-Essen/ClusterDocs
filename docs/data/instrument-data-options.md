# Choosing an instrument-data transfer path

Use this decision guide with
[Class 16: wet-lab instrument data](../course/class-16-wet-lab-data-workflows.md)
and the current [storage and transfer reference](../reference/storage-transfer.md).

> **Service status:** project Samba shares are **ready now** for approved
> projects and registered devices. Ardia integration and RCC-to-Coscine
> transfer are **not yet released**.

## Start with six questions

1. Is the instrument still writing?
2. How many bytes and files are involved?
3. Is the source Windows, macOS, Linux, Ardia, or a vendor appliance?
4. Is the transfer one-time or recurring?
5. Does the data contain primary identifying fields?
6. Which approved RCC project is the destination?

RCC accepts only data covered by the applicable project approval and RCC data
policy. Primary identifying fields are not permitted.

The destination must be the named project area—not `/home/<user>` or another
personal directory. Project storage keeps ownership, membership, retention,
and eventual Coscine archiving connected to the project. Home storage is not a
governed instrument-data landing area and is not designed for large recurring
datasets or many-small-file ingestion.

The lifecycle continues after ingestion:

```text
instrument -> RCC project -> job-local analysis -> RCC project results
           -> future verified Coscine archive [not yet released]
           -> recorded RCC disposition
```

See [Class 17: research data lifecycle](../course/class-17-data-lifecycle.md)
and the [planned RCC project to Coscine flow](rcc-project-to-coscine.md).

## Lab network option

For a suitable registered instrument or acquisition workstation, ask whether
it can join the **Lab network**. The device then has no general direct Internet
route. It can retain direct access to explicitly approved server endpoints or
services needed for acquisition and transfer, plus limited outbound web access
through an explicit HTTP proxy for approved purposes such as updates.

This design reduces exposure without making the device trusted. Proxy access
does not allow unsolicited inbound Internet connections, and one approved
server path does not provide general RCC or hospital-network access. RCC must
review the device, owner, vendor support, licensing, update requirements,
credentials, server dependencies, and target project before connection.

Read [how RCC and the Lab network work together](../resources/how-it-all-works.md)
before requesting onboarding.

## Usual Lab-network path: the project's Samba share

For an ordinary file-producing instrument or Windows acquisition computer, the
usual approved destination is a **Samba share for the project**. Samba is the
technology behind a familiar Windows network folder. The operator completes a
run or supported export, copies it to that project folder, and verifies the
handoff. The data then belongs to the project team rather than to the operator's
personal account.

```text
registered instrument -> project Samba share -> RCC project/incoming
```

RCC supplies the exact share, server, credentials, and allowed device. Do not
guess those values, reuse another project's share, or use a personal home
directory. A Samba share is an ingestion path, not a place to run analysis over
the network. **Ardia integration is not yet released.** Its future route will
use the vendor-supported integration or export path agreed with RCC and the
facility.

## Browser or managed portal

Suitable for users who do not need command-line tools, modest file counts,
occasional transfer, and audited or resumable workflows where supported.

## SFTP

Suitable for Windows and macOS workstations and routine transfers. Use the
RCC SFTP address and access instructions you were given. Do not copy a server
address from the Windows or macOS pages for existing SSHFS setups.

## Server-to-server transfer

Suitable for facility file servers, large recurring datasets, and automation.
This avoids making a laptop an unnecessary intermediate copy.

## Automated instrument ingestion

Suitable for sequencers, recurring microscopy, mass-spectrometry exports,
long-running instruments, and high data volumes.

Where a direct RCC integration exists, use the dedicated campus **Lab VLAN**
and the managed ingestion endpoint configured for the instrument/project. The
Lab VLAN is an acquisition path; it does not make the instrument-control
computer a general compute node or unrestricted storage client.

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

If a workstation already has an SSHFS mount, use these pages to identify it.
Do not use them to create a new connection:

- [Recognize an existing Windows SSHFS setup](legacy-storage-windows.md)
- [Recognize an existing macOS SSHFS setup](legacy-storage-macos.md)
