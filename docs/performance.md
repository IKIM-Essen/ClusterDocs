# Resources and Performance -- The status, the DOs and DON'Ts

The performance of your computation depends primarily on:

 1. I/O (Input/Output)
 2. RAM
 3. Choice of technology stack
 4. Hardware

— in that order of importance.

## Cluster Overview

As of late 2024, the cluster offers:

- ~10,000 CPU cores
- ~100,000 GPU cores
- 35+ Terabytes of RAM
- 3+ Petabytes of storage

However, these impressive numbers are meaningless unless you optimize your computation with the appropriate tools and strategies. The machines are interconnected via 10 Gbit/sec Ethernet, while dedicated file servers utilize multiple 100 Gbit/sec connections. Data can move from file servers at ~1 GB/sec, making data transfer speed and local RAM availability critical.

## Key Factors in Optimizing Performance

### 1. Input/Output (I/O)

Your computation’s performance is far more dependent on I/O patterns than on raw hardware capabilities. Here are critical considerations:

- Local storage over remote access:
Always move your data to fast, local storage before starting computation. Running computations on remotely mounted data (e.g., directly from a file server) can be up to 100× slower than using local storage.
- Data transfer rates:
While nodes have 10 Gbit/sec Ethernet connections (~1 GB/sec), file servers must service hundreds of nodes. As such, they cannot guarantee high-performance, storage-agnostic I/O.
- Streaming computation:
Streaming data directly to a node and computing on-the-fly is an advanced approach that requires detailed knowledge of I/O bandwidth and the computational throughput of your device. Use this method only when confident in its feasibility.

### 2. RAM (Memory)

Efficient use of RAM is vital for performance. Key considerations include:

- Avoid paging and swapping:
When your computation exceeds available RAM, the system will “page” data to local disk storage, which can slow performance by up to 1,000×. Estimating your RAM requirements is critical.
- Divide data into subsets:
If your computation requires more RAM than available, consider splitting your dataset into manageable subsets to avoid paging.
- Node RAM capacities:
Nodes vary in RAM availability, with many offering 200 GB and fewer providing 1 TB. Overestimating your requirements and queuing for high-RAM nodes may increase wait times without guaranteeing success.

### 3. Technology Stack

When computations exceed a single CPU core’s capacity, ensure your software stack supports parallel processing technologies like OpenMP or MPI. Here’s how:

- Conda-installed software:
Most software distributed via Conda is pre-configured to leverage multi-core processing through OpenMP.
- Manually installed software:
If installing software manually, verify that multi-core or parallel processing support is enabled during installation.

### 4. Hardware Selection

Your choice of hardware should align with your software’s capabilities and your computational needs:

- CPU vs. GPU:
While GPUs can be significantly faster, their effectiveness depends on your software stack’s compatibility. Not all code is GPU-optimized.
- RAM requirements:
Select nodes based on your RAM needs:
- Overuse of high-RAM nodes (e.g., 1 TB) can lead to longer wait times.
- Understanding and optimizing your RAM usage often reduces bottlenecks.
- Divide datasets where possible to mitigate excessive RAM demands.

## Summary

To achieve optimal performance:

- Prioritize local storage for I/O-intensive tasks.
- Plan RAM usage to avoid paging.
- Ensure your software stack supports multi-core processing or GPU acceleration.
- Choose hardware configurations tailored to your workload’s requirements.

Understanding and managing these factors will help you maximize the efficiency of your computations on the cluster.

## Don't do this

- _Don't run_ computations that will access a lot of files in /projects or /groups (and of course /homes), at least don't act surprised if they are really slow and other users complain about the systems IO performance going down dramatically.

- _Don't run_ computations that require 10 MB (10 megabytes) of RAM blocking a 1 Terabyte (1000000 Megabytes) node
