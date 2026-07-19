# Class 3: performance and efficient I/O

## Learning objectives

You will distinguish CPU, GPU, memory, storage capacity, throughput, latency, IOPS and metadata operations, then select a resource request based on measurement rather than guesswork.

## The most important pattern

Keep durable input and final output on approved shared storage. Stage high-I/O temporary data to node-local storage inside the job, process it there, and copy only the required results back.

Poor I/O structure can turn work expected to take hours into work that takes weeks or months. Typical causes are:

- millions of tiny files;
- random reads against network storage;
- active Conda environments with many metadata operations;
- uncompressed intermediate text files;
- too many threads competing for the same storage path;
- requests for far more memory or CPU than the program can use.

## Good habits

- Keep sequence files compressed when tools can stream them.
- Avoid thousands of files in one directory; use a planned hierarchy or archive format.
- Measure with Slurm accounting and application benchmarks.
- Increase resources only when evidence shows the current resource is limiting performance.
- Never run synthetic load generators or broad benchmarks on shared services without approval.

## Security moment

Availability is part of security. Accidental denial of service can come from excessive job arrays, tight retry loops, recursive metadata scans, or filling shared storage. The training exercises therefore use bounded data and one job at a time.

## Completion gate

Explain which of CPU, RAM, GPU or I/O is the likely bottleneck for one representative workflow, and name the measurement that supports your conclusion.
