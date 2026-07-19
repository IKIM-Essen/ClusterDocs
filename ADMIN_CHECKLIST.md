# RCC onboarding publication checklist

Complete and test these items before publishing the curriculum.

## Identity and access

- [ ] Confirm the public RCC login gateway hostname.
- [ ] Confirm the Slurm submission-host hostname.
- [ ] Publish current ED25519 host-key fingerprints through an independently trusted channel.
- [ ] Confirm the approved SSH key type and whether a passphrase is mandatory.
- [ ] Confirm account-enrollment and public-key registration procedures.
- [ ] Confirm whether YubiKey or other MFA is required and update all screenshots and wording.
- [ ] Confirm the support email address and escalation process.

## Windows and macOS

- [ ] Complete Part 1 with a clean supported Windows installation.
- [ ] Complete Part 1 with a clean supported macOS installation.
- [ ] Verify OpenSSH, `ssh-agent`, key permissions, ProxyJump, VS Code, and Remote - SSH instructions.
- [ ] Verify the exact first-connection host-key prompts.

## Data transfer and protection

- [ ] Confirm the browser transfer service name, URL, sign-in method, collection/endpoint name, and destination convention.
- [ ] Confirm checksum commands and expected behavior.
- [ ] State which data classes may use the service and which require additional approval.
- [ ] Confirm the local policy that direct identifiers and re-identification keys remain outside RCC while approved biomedical research data may be processed in the controlled enclave.
- [ ] Review Class 11 wording, external legal links, and the data-protection contact before publication.
- [ ] Review the Class 11 scenarios for genomic, imaging, pseudonymised, and directly identifying data with the responsible institutional office.
- [ ] Publish project, home, archive, and scratch storage purposes and quotas.
- [ ] Confirm retention, deletion, backup, and recovery statements.

## Slurm

- [ ] Confirm cluster, account, partition, QOS, time, CPU, memory, and GPU request syntax.
- [ ] Confirm the first-job example runs on a compute node.
- [ ] Confirm `squeue`, `sacct`, `sstat`, and accounting fields available to users.
- [ ] Confirm local policy for login-host processes and tmux sessions.
- [ ] Confirm interactive allocation procedures and limits.

## Snakemake and environments

- [ ] Record supported Snakemake and executor/profile versions.
- [ ] Validate the dry-run and Slurm-execution commands.
- [ ] Confirm the supported Miniforge/Mamba installation or module.
- [ ] Confirm channel order, Bioconda policy, outbound-network policy, and package-cache location.
- [ ] Execute the statistical example in a clean test account.
- [ ] Execute the synthetic DNA example in a clean test account.
- [ ] Confirm logs, benchmarks, retries, and cancellation behavior.

## Performance and I/O

- [ ] Publish the node-local scratch path and capacity.
- [ ] Confirm how Snakemake should map `tmpdir` and whether a site profile provides it.
- [ ] Test the documented shadow/copy/staging pattern on the RCC filesystems.
- [ ] Confirm which shared filesystems are intended for streaming, project storage, archive, and temporary work.
- [ ] Publish practical file-count and directory-count guidance.
- [ ] Confirm availability of `time`, `sacct`, `sstat`, `pidstat`, `vmstat`, `iostat`, and `nvidia-smi`.
- [ ] Benchmark one representative FASTQ/BAM workload with shared versus local temporary I/O.

## Apptainer

- [ ] Record the supported Apptainer version.
- [ ] Publish approved image, cache, and temporary paths.
- [ ] Confirm allowed registries and image-signing or verification policy.
- [ ] Confirm bind-mount policy and automatic host binds.
- [ ] Confirm `--cleanenv`, containment, and writable-overlay policy.
- [ ] Test CPU and GPU images through Slurm.
- [ ] Confirm the local GPU request syntax and Apptainer `--nv` behavior.
- [ ] Validate the Snakemake Apptainer deployment command and image-prefix configuration.

## Editorial and accessibility

- [ ] Replace all administrator placeholders.
- [ ] Build MkDocs locally and run markdownlint.
- [ ] Check all internal and external links.
- [ ] Review terminology with a novice biomedical researcher.
- [ ] Review data-protection wording with the responsible institutional office.
- [ ] Review statistical and sequence-analysis disclaimers with domain experts.
- [ ] Check PDF and slide rendering on Windows and macOS.
- [ ] Review captions against the final narration.
- [ ] Publish an update date and tested-version matrix.
