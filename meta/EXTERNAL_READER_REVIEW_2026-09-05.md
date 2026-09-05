# External-reader review of ClusterDocs 3

Review date: 5 September 2026
Reviewed branch: `clusterdocs-3`
Reviewed candidate before this review wave: `52448d08dce613bbe498bf68642aab7c57fa3482`

## Executive assessment

An external reader is likely to leave with a strong and coherent impression:

> RCC is not primarily a cluster that researchers must learn to operate. It is a
> governed research-computing platform that connects data acquisition, project
> storage, analysis, reproducible workflows, collaboration, AI assistance,
> preservation, and domain-specific publication paths while retaining direct HPC
> controls for expert users.

This is a substantial improvement over an SSH-first or scheduler-first story.
The documentation now communicates an architectural point of view rather than a
collection of unrelated services.

## What an external reader takes home

### 1. The project is the center of RCC

The project is presented as the durable research boundary connecting people,
data, compute, services, workflows, results, provenance, and lifecycle. Moving
between Files, Analysis, agents, VS Code, SSH, or a domain application does not
create another authority boundary.

This makes governance look like part of the platform architecture rather than an
administrative add-on.

### 2. Ordinary researchers do not need to become HPC operators

The front door is task-first and browser-first. An RCC account does not imply an
SSH key. The intended ordinary path is project -> Files -> Notebook/Workflow ->
durable results. SSH, ProxyJump, VS Code, Slurm syntax, containers, and lower-
level diagnostics remain available when they are genuinely useful.

The resulting message is: advanced infrastructure remains present, but it is no
longer an entrance exam for doing science.

### 3. Advanced users have not been reduced to a simplified portal

The documentation retains Slurm, GPUs, SSH, VS Code, Conda/Mamba, Apptainer,
Snakemake, Nextflow, Gitea, local scratch, storage semantics, and lower-level
diagnostics. An experienced bioinformatician or research software engineer can
therefore see that browser-first does not mean beginner-only.

### 4. RCC spans the experimental lifecycle

The site connects sequencers, microscopes, mass spectrometers, acquisition
workstations, and facility servers to project-scoped ingestion, appropriate
storage, analysis, reproducible workflows, result/provenance handling, and
preservation or domain publication.

SeqLab is a useful exemplar: it shows how a domain application can connect
acquisition, analysis, review, metadata/provenance, and eventual submission to
an appropriate international archive without requiring the researcher to
assemble separate identity, scheduler, storage, and publication systems.

### 5. The AI model is unusually clear and conservative

The memorable architectural rule is **data-blind by default**. External/general-
purpose agents can work from documentation, public code, schemas, synthetic
fixtures, and bounded diagnostics. RCC executes against real governed data. An
agent does not receive a second identity or an authority bypass simply because
an action is requested through natural language, MCP, or an API.

This makes AI assistance look compatible with biomedical governance rather than
requiring disclosure of the dataset.

### 6. I/O behavior is a foundational engineering principle

The documentation now gives RCC a strong engineering thesis: scientific I/O
patterns often dominate the real scaling problem. Small-file metadata storms,
random access, repeated directory scans, Conda/package trees, workflow temporary
state, synchronized reference access, and editor/indexer activity can defeat
very large headline bandwidth numbers.

This makes node-local scratch, deliberate staging, immutable artifacts,
workflow-aware execution, low-I/O VS Code settings, POSIX versus S3 choices, and
backend-neutral storage semantics feel like one coherent architecture rather
than unrelated tuning advice.

### 7. Technology choices look intentional rather than fashionable

The Slurm/service-plane/Kubernetes/Ceph explanation is effective because it does
not claim that popular platforms are bad. It says that RCC uses the authority
and storage semantics that fit each workload, avoids two schedulers owning the
same scientific compute, and shapes pathological I/O before assuming another
backend will solve it.

## The external-reader uncertainty identified during review

The review originally identified **current state versus target state** as the
largest presentation risk. At that point RCC Analysis was not yet released,
while the browser-first story depended heavily on Analysis. A reader could
therefore ask how much of the complete platform was actually part of the coming
release.

The initial editorial recommendation was to add compact **RCC today** and
**Coming next** sections.

## Resolution after product decision

That editorial recommendation has been superseded by a stronger product/release
decision:

> **ClusterDocs 3 will not be released before the integrated browser product is
> ready.**

The release baseline is now explicitly:

1. RCC Home;
2. Files;
3. RCC Analysis — Notebook and Workflow;
4. My RCC; and
5. RCC Admin.

All five are one release bundle. RCC Analysis is no longer described as a
post-release capability that readers must mentally place under “coming next.”
The current candidate is simply not releasable until Analysis is ready and the
five-surface integration passes acceptance.

This resolves the external-reader ambiguity more cleanly than a current/future
marketing split: the public ClusterDocs 3 release should describe the integrated
browser baseline as the product users actually receive.

Separately governed capabilities can still remain staged after that boundary,
including RCC-to-Coscine self-service transfer, protected project vhosts, and
selected vendor integrations such as Ardia. Their individual status remains
explicit.

The two-stage media plan is unaffected: Stage 1 is the integrated RCC browser
product plus the written site with videos fail-closed; Stage 2 adds regenerated
and reviewed videos.

See `meta/RELEASE_BUNDLE_DECISION_2026-09-05.md` and
`tools/release_bundle_gate.py` for the governing decision and machine-enforced
release boundary.

## External one-sentence summary

A technically informed outside reader is likely to describe RCC as:

> An institutional biomedical research platform that is turning traditional HPC
> into project-governed research computing spanning instruments, storage,
> notebooks, reproducible workflows, HPC/GPU, privacy-preserving AI assistance,
> and research-data lifecycle, with unusually strong attention to scientific I/O
> behavior as the real scaling constraint.

## Review conclusion

The product narrative is strong enough that further simplification should focus
on preserving a coherent integrated release, not hiding advanced capability or
technical rationale. The five-surface browser bundle now provides that coherent
baseline while separately staged services keep explicit status labels.
