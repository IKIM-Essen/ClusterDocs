# Performance -- The DOs and DON'Ts

The performance of your computation in nearly all cases depends on:

- IO
- RAM
- choice of technology
- hardware

in that order.

As of late 2024 the cluster has approx. 10000 CPU cores, approx. 100000 GPU cores , over 35 Terabytes of RAM, over 3 Petabytes of storage etc. None of these numbers mean anything to your compute.

The fact that data can be moved from the file servers with approx. 1 gigabyte per second is important, as is the amount of available RAM on your computing device.

## IO

While performance measures and even top performer charts exist, your computation is far less impacted by the available hardware that e.g. by your choice of [IO pattern](./patterns.md). In short: make sure your data is moved onto local fast storage before you start computing.

Running a computation using remote date mounted off a file server will be up to 100 times slower than using a local storage device. Our nodes use 10 gigabit (10Gb) a second ethernet connections (allowing 1 Gigabyte (1GB) per second transfers). Howeverm there are hundreds of nodes, file servers cannot enable storage location agnostic IO, so copy your data in one stream to a local device before you start randomly accessing it aka computing on your data.

There is the notion of streaming your data to a node and computing on it _on the fly_, however this requires a precise understanding of the IO bandwidth and the throughput of your computational device.

## RAM or available memory

Our nodes come with a finite amount of [RAM](https://en.wikipedia.org/wiki/Random-access_memory). While computers have the ability to relocate data to hard local hard drives to free up space (see [Paging or Swapping](https://en.wikipedia.org/wiki/Memory_paging)), we note that Paging will make your computation up to 1,000 times slower. While there is no general strategy to avoid overtaxing the available RAM on a node and more RAM is always better, estimating the RAM requirements of any computational step is always a good idea. Typically software instructions mention RAM requirements and frequently simply dividing the data into subsets will solve slowdowns caused by paging.

## Technology stack

If your computation exceeds the capacity of a single [CPU](https://en.wikipedia.org/wiki/Central_processing_unit) core you need to make sure your software choice includes either [OpenMP](https://www.openmp.org) or [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) or uses another technology to [scale-out](https://portworx.com/blog/scale-up-vs-scale-out/).

Fortunately most software distributed via Conda already inludes the ability to use more than a single CPU core as it was built with OpenMP support. If you install software yourself (not using conda) make sure to enable multi-core usage.

## Hardware

The most important choices you face are:

### GPU or CPU

This comes down to what does your software stack support. Yes GPUs are faster, but not every bit of code works on GPUs.

### RAM how much RAM do I need

There are more nodes with approx. 200 gigabytes (200GB) of RAM and fewer nodes with 1,000 gigabytes (1TB) RAM.
If you always compute on 1TB nodes, you will spend more time waiting for nodes to become available and you might need more than 1TB moving you back to square one. A minimal understanding of your computations RAM requirements will help make good choices here. Frequently data sets can be subdivided and bottlenecks thus avoided.
