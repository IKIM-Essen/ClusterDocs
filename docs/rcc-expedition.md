# RCC Expedition

!!! tip "Recommended onboarding for new RCC users"
    RCC Expedition is a self-contained interactive course for **Windows 11**
    and **current macOS**. It starts with workstation security and continues
    through SSH, Linux, Slurm, storage, data boundaries, and reproducible RCC
    workflows.

[**Download RCC Expedition v1.0.0**](assets/downloads/RCC-Expedition-USB-v1.0.0.zip)

SHA-256:

```text
680cc16b4d226de59e4dd7c6e0468ac3e9137b3bb7d438b94ad0c93152aa18c7
```

[Checksum file](assets/downloads/RCC-Expedition-USB-v1.0.0.sha256)

## Privacy: datensparsam by design

RCC Expedition runs locally on the user's computer.

It has:

- no learner account;
- no analytics;
- no telemetry;
- no central progress database;
- no supervisor dashboard; and
- no background course synchronization.

Course progress stays in local browser storage. Local workstation checks retain
only coarse states such as `PASS`, `WARN`, `FAIL`, or `UNKNOWN`.

The course does **not** collect passwords, MFA secrets, BitLocker/FileVault
recovery keys, SSH private-key contents, filenames, shell history, raw Wi-Fi
network names, or research data.

External documentation is contacted only when the user clicks an external
reference. RCC is contacted only when the user deliberately runs an RCC SSH
exercise.

## Supported workstation baseline

Use:

- a currently supported and patched **Windows 11** system; or
- a currently supported and patched **macOS** system.

Windows 10 is not treated as a suitable baseline for a newly configured RCC
research workstation because normal free Windows 10 security support ended in
October 2025.

### Windows 11

The course covers:

- Windows Update and application patching;
- Device Encryption / BitLocker;
- BitLocker recovery-key handling;
- Windows Security / Microsoft Defender;
- Windows Firewall and Secure Boot;
- screen locking and personal user accounts;
- backups plus an actual restore test;
- Windows OpenSSH Client; and
- RCC SSH-key setup.

### macOS

The course covers:

- macOS and application patching;
- FileVault;
- Gatekeeper;
- screen locking and personal user accounts;
- encrypted Time Machine backups plus an actual restore test; and
- RCC SSH-key setup.

## Research workstation and clinical-network boundary

A privately maintained or research workstation used for RCC should not be
turned into a clinical hospital endpoint.

Do **not** use hospital/clinical VPN as an RCC connectivity workaround, and do
not connect an unmanaged research laptop or desktop to clinical/internal
networks merely because those networks are available.

Network reachability itself can expose clinical resources and governed data to
browser sessions, mapped shares, caches, sync tools, temporary files, IDE
extensions, logs, and other background software.

Use an appropriately managed hospital endpoint for hospital-only clinical
resources.

For ordinary Internet access:

- use **eduroam** when eligible and available;
- where locally provided, **Stiftungsnetz** may be used as a
  semi-official/transitional Internet bootstrap route; or
- use another approved guest Internet path or a personal hotspot where
  appropriate.

Stiftungsnetz is mentioned only as a practical bootstrap option. This
documentation makes no undocumented claim about its network isolation.

## What the course teaches

The release contains platform-specific and common missions for:

1. workstation security and patching;
2. encryption and recovery planning;
3. backup and restore;
4. passwords and MFA;
5. safe network boundaries;
6. ClusterDocs as the RCC source of truth;
7. OpenSSH and RCC SSH keys;
8. Linux shell fundamentals;
9. submission hosts versus compute allocations;
10. first Slurm job and resource requests;
11. durable storage versus node-local scratch;
12. governed data and transfer boundaries;
13. explicit software environments;
14. Apptainer;
15. Snakemake and managed Nextflow, both ready now;
16. optional VS Code and Jupyter; and
17. an end-to-end synthetic RCC experiment.

Exercises use synthetic/non-sensitive material.

## Install

1. Download the ZIP.
2. Verify the SHA-256 checksum where practical.
3. Extract it to a local directory, or copy the extracted contents to a trusted
   USB key.
4. Open `START HERE.html`.
5. Follow the **Windows 11** or **macOS** path.
6. Continue in the local course.

## Relationship to ClusterDocs

**ClusterDocs remains the source of truth for mutable RCC technical facts.**

RCC Expedition links back to ClusterDocs for current:

- login/SSH configuration;
- Slurm resource policy;
- storage layout;
- transfer services;
- GPU instructions;
- containers;
- workflow execution; and
- Jupyter/remote-development instructions.
