# RCC Onboarding Part 3 - Narration

## Slide 1: Performance and efficient I/O

Part Three explains performance engineering for biomedical research. The most important message is that faster hardware does not rescue a poorly structured workflow. A computation that should finish in hours can extend to weeks or months when it repeatedly scans network storage, opens millions of small files, requests the wrong number of threads, or runs out of memory and restarts. We will separate CPU, GPU, RAM, disk capacity, and input-output behavior. We will also explain streaming versus random access, large versus small files, compression, node-local scratch, and the tools used to find a bottleneck. The goal is not maximum speed at any cost. The goal is predictable, fair, and scientifically correct performance.

## Slide 2: 1. Performance is a systems property

Performance is not a single number. An analysis may be limited by CPU instructions, GPU kernels, memory capacity, memory bandwidth, network transfer, storage throughput, storage latency, or metadata operations. Improving a resource that is not limiting usually changes little. For example, adding CPU cores to a job that waits for thousands of small files can increase contention without shortening runtime. Start by describing the data path and measuring where elapsed time is spent. Then change one variable at a time. This approach is more reliable than guessing from the reputation of a tool or copying a resource request from another project.

## Slide 3: 2. The same analysis can take hours or months

Consider a workflow with five thousand samples. If a step spends one second on useful computation and twenty seconds opening, seeking, and closing small files on shared storage, the overhead dominates. Repeat that pattern across many rules and retries, and a nominally short analysis can occupy the system for weeks. Another common pattern is decompressing the same source repeatedly, copying entire directories for each rule, or requesting one core for software configured to use sixteen. Performance mistakes multiply by the number of samples, files, and workflow stages. Estimate scale before launch: number of jobs, files per job, bytes read and written, and expected runtime per unit.

## Slide 4: 3. CPU: cores, threads, and parallel efficiency

A CPU node contains cores that execute instruction streams. Some tools expose a threads option. Slurm must allocate at least that many CPUs per task, and the command must be told to use them. Parallel efficiency usually declines as thread count increases because threads coordinate, share memory bandwidth, and wait for input. Two independent samples may run faster as two smaller jobs than as one very wide job. Measure elapsed time and CPU utilization at several thread counts using representative data. Never start many background processes outside the allocation, and do not assume that a tool called multithreaded scales linearly.

## Slide 5: 4. GPU: powerful, specialized, and easy to underuse

GPUs contain many execution units optimized for highly parallel numerical work. They can accelerate deep learning, image analysis, molecular simulation, and selected sequence-analysis tools. A CPU program does not become GPU-enabled merely because a GPU is allocated. Request the correct GPU resource, use software built for the available driver and libraries, and monitor utilization with nvidia-smi. Low utilization may indicate tiny batches, CPU preprocessing, slow data loading, insufficient parallelism, or frequent host-to-device transfers. GPUs are scarce shared resources, so release them when the GPU portion is complete rather than reserving one during long CPU-only stages.

## Slide 6: 5. RAM: capacity is not the same as speed

RAM holds the active working set: data structures, indices, buffers, and program state. If a job exceeds its Slurm memory allocation, the job may be terminated. If the operating system begins swapping, performance can collapse because disk is far slower than RAM. Requesting far more memory than needed can delay scheduling and reduce capacity for everyone. Use Slurm accounting to inspect maximum resident memory after representative jobs. Some tools scale memory with threads or input size, so record the relationship. A memory leak shows steadily rising use; a normal workload often rises to a plateau.

## Slide 7: 6. Disk space and I/O are different questions

Disk space is capacity. Input-output performance describes how data moves. Four useful dimensions are throughput, latency, input-output operations per second, and metadata rate. Throughput matters for large sequential reads such as scanning a compressed FASTQ. Latency matters when a program waits for individual operations. IOPS matters for many small reads and writes. Metadata rate matters when listing directories, checking file existence, opening files, or creating thousands of paths. Network storage is designed for shared durable data, but it cannot provide local-disk behavior to every job simultaneously. Match the access pattern to the storage tier.

## Slide 8: 7. Streaming versus random I/O

Streaming input-output reads or writes long contiguous sequences. This lets storage, operating-system caches, compression libraries, and network protocols work efficiently. Random input-output jumps among many positions or files and repeatedly pays seek, latency, and metadata costs. Indexed BAM and VCF access can be appropriate when querying a small genomic interval, but repeatedly issuing tiny queries across the entire genome can be slower than one sequential pass. Against network storage, avoid database-like random write patterns and large collections of temporary shards. Stage active files to node-local disk, process them there, and return only the required outputs.

## Slide 9: 8. Large files, small files, and crowded directories

A directory with hundreds of thousands of files can make listing, tab completion, backups, workflow discovery, and deletion painfully slow. Small files also waste storage blocks and require metadata operations. Many bioinformatics tools create temporary fragments, per-read outputs, or tiny environment files. Prefer a reasonable directory hierarchy, one result bundle per sample or batch, and archive cold collections when appropriate. Do not use tar archives as a substitute for formats that need random indexed access, but do use structured containers or archives for collections that are transferred and consumed together. Clean temporary files through workflow rules instead of leaving them indefinitely.

## Slide 10: 9. Leave files compressed when the toolchain supports it

Biomedical data is often compressible. FASTQ is commonly stored as gzip-compressed FASTQ. VCF can use block gzip with an index. BAM and CRAM are compressed binary alignment formats. Keeping files compressed reduces bytes transferred and stored, which often saves more time than decompression costs. Avoid repeatedly expanding a file to network storage merely because one command expects a path. Many tools read compressed input directly, and Unix pipes can stream decompressed data between compatible tools. Confirm that the chosen compression is splittable or indexable when parallel access is required. Keep the original compressed source and generate only formats needed for downstream analysis.

## Slide 11: 10. Use node-local scratch through Snakemake

Node-local scratch is temporary storage attached to the compute node. It provides lower latency and avoids making shared storage handle every temporary read and write. Snakemake can expose the job temporary directory through the standard tmpdir resource. Shadow rules can execute in an isolated directory, with modes that link or copy the required inputs. For tools that perform random access or create many temporary files, use an RCC-tested pattern: copy the required inputs to local scratch, run the command there, validate the output, and copy only final results back. Scratch is temporary, so the workflow must not treat it as durable storage.

## Slide 12: 11. Measure the bottleneck with the right tools

Use Slurm accounting first. S acct shows job state, elapsed time, allocated CPUs, and fields such as maximum resident memory. S stat reports live statistics for running jobs. Inside an allocation, time measures elapsed and CPU time, top or h top shows processes, and tools such as pidstat, vmstat, iostat, or dstat can reveal CPU wait, memory pressure, and storage activity when available. N v i d i a s m i reports GPU utilization and memory. Snakemake benchmark files connect measurements to specific rules. Interpret metrics together: low CPU plus high I/O wait suggests storage; full memory and rising swap suggests RAM; low GPU utilization with busy CPUs suggests preprocessing or data loading.

## Slide 13: 12. A bottleneck diagnosis matrix

A symptom is not a diagnosis. Low CPU efficiency may be caused by input-output wait, serial code, thread oversubscription, or frequent synchronization. A job killed for memory needs either a larger allocation or a method that reduces the working set. A GPU at ten percent utilization may be waiting on CPU preprocessing or tiny batches. A workflow that pauses while discovering files may have a metadata problem. Build a small representative benchmark, change one factor, and compare elapsed time and resource efficiency. Stop when performance is adequate and fair; optimization also has engineering cost and can introduce scientific errors.

## Slide 14: 13. Part Three operating rules

The operating rules are straightforward. Measure before scaling. Match Slurm requests to the software configuration. Keep source data compressed where possible. Prefer sequential streaming access. Avoid random temporary input-output on network storage. Stage active files to node-local scratch through a tested Snakemake pattern. Reduce small-file and directory counts. Preserve only necessary outputs and clean temporary files. Use Slurm accounting, Snakemake benchmarks, and operating-system tools to identify the actual bottleneck. Above all, perform a pilot at realistic scale. An inefficient workflow multiplied across thousands of samples can turn hours into months and degrade the shared service for colleagues.

