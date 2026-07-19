# RCC Onboarding Part 4 - Narration

## Slide 1: Containers with Apptainer

Part Four introduces containers using Apptainer. Containers package an application and its libraries into a portable image. On RCC, the operational reason is especially important: a large Conda environment contains thousands of small files. If those files are repeatedly opened from network storage by many jobs, metadata and random input-output can dominate runtime. A read-only Apptainer S I F image consolidates that software stack into one managed artifact and is suitable for shared high-performance computing. We will distinguish the image from project data, explain cache and temporary storage, cover bind mounts and GPU access, and show how Snakemake associates a container with a rule.

## Slide 2: 1. The problem: software can become an I/O workload

A Conda environment can contain tens of thousands of files: Python modules, shared libraries, metadata records, executables, and package caches. Starting a command may trigger many opens, stats, library searches, and imports before useful computation begins. On local solid-state storage this may be acceptable. On shared network storage, hundreds of simultaneous jobs can turn environment startup into a metadata bottleneck. The result may look like slow software even though the CPU is mostly waiting. Containers address this by packaging the software stack into a smaller number of image artifacts and by making the environment immutable and reproducible.

## Slide 3: 2. What a container is - and is not

A container image packages user-space software, libraries, and selected configuration. It does not include a separate hardware machine and normally shares the host Linux kernel. Apptainer is designed for multi-user high-performance computing and runs processes with the user identity rather than a privileged daemon model. The image is not the correct place for active project data, credentials, or patient information. Project inputs and outputs remain in approved storage and are made visible through explicit bind mounts. Containers improve reproducibility of software, but they do not validate algorithms, reference data, parameters, or scientific interpretation.

## Slide 4: 3. SIF: an immutable image artifact

Apptainer commonly uses the Singularity Image Format, or S I F. A SIF image can contain a compressed read-only filesystem plus metadata and signatures. Read-only images reduce accidental drift: a job cannot silently install a different library into the image. The same image can be used by many jobs. Record the image source, digest or checksum, creation recipe, and validation status. Do not rely only on a floating tag such as latest. A container is a versioned research dependency and should be managed with the same care as a reference genome or analysis script.

## Slide 5: 4. Image, cache, temporary space, and project data

Container workflows involve several storage locations. The SIF image is a durable, versioned software artifact. The Apptainer cache stores downloaded layers and should use an RCC-approved path; uncontrolled caches on a shared home directory can consume space and create metadata traffic. Temporary build or extraction space should use local scratch when possible. Project data remains in approved shared storage and is bound into the container. Distinguishing these locations prevents accidental data loss and avoids turning network storage into a scratch disk. The RCC should publish standard environment variables and paths for image stores, caches, and temporary directories.

## Slide 6: 5. Trust the image deliberately

Only run images from trusted sources or images built from reviewed definitions. Prefer immutable digests over floating tags. Calculate and record a checksum for a SIF image when it is transferred. Inspect image metadata and labels. Record the base image, installed package versions, build date, and definition file. Scan or review images according to institutional policy. Most importantly, validate the scientific behavior with synthetic and reference data. A correctly signed image can still contain an unsuitable algorithm, outdated database, or incorrect default parameter. Trust has both a software-supply-chain component and a scientific-validation component.

## Slide 7: 6. Run an image with explicit commands and a clean environment

Apptainer exec runs a command inside an image. Start with a harmless version check, then a small synthetic test. The clean environment option reduces accidental inheritance of host variables that could change behavior. The contain-all or site-recommended isolation options may be appropriate depending on policy. Record the full command in the workflow log. Avoid interactive changes inside writable sandboxes for production work because those changes are difficult to reproduce. If a command depends on locale, threads, temporary paths, or license variables, declare them explicitly and document why they are needed.

## Slide 8: 7. Bind mounts connect approved data to the container

A bind mount makes a host path visible at a chosen path inside the container. Bind source data read-only whenever possible. Bind a dedicated result directory read-write. Bind node-local scratch for temporary work. Avoid binding your entire home directory merely for convenience, because that makes hidden configuration and credentials visible and reduces reproducibility. Use stable internal paths such as slash data, slash results, and slash tmp so the command is independent of the host project layout. Verify ownership and permissions before starting thousands of jobs.

## Slide 9: 8. Containers do not remove I/O physics

A container does not make random network input-output fast. The executable may be packaged efficiently, but inputs, outputs, caches, and temporary files still follow the underlying storage behavior. Keep compressed inputs compressed when supported. Stage files that require random access or many temporary writes to node-local scratch. Avoid writing package caches or application caches into the project directory. Limit the number of tiny output files and organize directories. A container can even make performance worse if every job independently pulls an image from a registry. Pre-stage approved images and use a shared read-only image location or an RCC-supported cache strategy.

## Slide 10: 9. GPU access from Apptainer

For a GPU job, request the GPU through Slurm and run Apptainer with the N V option so the relevant NVIDIA devices and host driver libraries are available inside the container. The image should contain compatible user-space frameworks such as CUDA-enabled PyTorch or TensorFlow, but it should not attempt to replace the host kernel driver. Test compatibility on a small allocation and use nvidia-smi both on the host allocation and, where appropriate, inside the container. Record image digest, GPU type, driver, framework version, and command. GPU access does not change the need to optimize data loading and batch size.

## Slide 11: 10. Snakemake associates images with rules

Snakemake can associate a container image with a rule and execute the workflow using the Apptainer deployment method. This places the software dependency next to the declared inputs, outputs, threads, resources, log, and command. Use an RCC-supported Apptainer prefix or image store so jobs do not repeatedly download images. The rule should still use tmpdir or a shadow pattern when the tool needs local temporary work. Pin the image to an immutable digest or version and record it in reports. Test both the workflow logic and the image before scaling to production data.

## Slide 12: 11. Build once, test, publish, and reuse

A production image should be built from a version-controlled Apptainer definition file or an equivalent reviewed recipe. Build in an approved environment, because image construction may require privileges or a remote builder. Record base images and package versions. Run automated smoke tests, workflow tests with synthetic data, and scientific validation. Publish the image to an approved registry or image store, record the digest, and make it read-only. Rebuild through the recipe rather than modifying an existing image. Deprecate images that contain security problems or obsolete references, but preserve provenance for completed analyses.

## Slide 13: 12. Part Four operating rules

The container rules are these. Use trusted, immutable SIF images. Record source, digest, build recipe, and validation. Keep project data outside the image. Bind source data read-only, results deliberately, and temporary space to local scratch. Place caches and images in RCC-approved locations. Use clean environments and explicit commands. Request GPUs through Slurm and use the Apptainer GPU option only for compatible images. In Snakemake, pin the container per rule or workflow and avoid repeated pulls. Remember that containers improve software reproducibility and startup I/O, but good data input-output patterns, performance measurement, and scientific validation remain essential.

