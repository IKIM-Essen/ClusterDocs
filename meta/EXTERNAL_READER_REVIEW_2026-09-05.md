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

## The remaining external-reader uncertainty

The largest presentation risk is **current state versus target state**.

ClusterDocs is appropriately honest about staged capabilities, but the browser-
first product story depends heavily on RCC Analysis, which is not yet released.
RCC-to-Coscine self-service, project vhosts, and selected vendor integrations are
also still staged. Repeated "not yet released" labels are truthful, but an
outside reader can finish with the question:

> How much of this compelling platform is actually available today?

This is not a reason to weaken the target-state story. It is a reason to add one
concise, authoritative distinction near the front door between the substantial
foundation available now and the next integrated browser capabilities.

## Recommended content correction

Add compact **RCC today** and **Coming next** sections to the home page using only
governed release facts. Do not create another large service-status matrix.

The current foundation should emphasize:

- Files as the current browser data path;
- current account/project self-service and approval functionality;
- RCC workers and Slurm as the current scientific-compute path;
- SSH/VS Code as the current advanced path;
- managed Nextflow-to-Slurm as ready now; and
- project Samba shares as ready now for approved registered devices.

The near-term integrated target should explicitly name:

- RCC Analysis Notebook and Workflow as not yet released;
- RCC-to-Coscine self-service as not yet released;
- protected project vhosts as not yet released; and
- selected vendor integrations such as Ardia as not yet released.

The detailed service pages remain the authority for per-capability status.

## External one-sentence summary

A technically informed outside reader is likely to describe RCC as:

> An institutional biomedical research platform that is turning traditional HPC
> into project-governed research computing spanning instruments, storage,
> notebooks, reproducible workflows, HPC/GPU, privacy-preserving AI assistance,
> and research-data lifecycle, with unusually strong attention to scientific I/O
> behavior as the real scaling constraint.

## Review conclusion

The product narrative is already strong enough that further simplification
should focus on **status clarity**, not removing advanced capability or technical
rationale. The next editorial change should make the current-versus-next boundary
visible in under one minute while preserving the task-first front door.
