# rootless containers on cluster nodes

Due to the security implications and shortcommings of other container runtimes (namely docker) users of the managed cluster should move towards using apptainer for their workloads.
At some point the use of other runtimes is likely to be deprecated.

# Basic usage

Scenarios:
1. Run a workload that only needs to access files from the /homes directory
2. Workload needs to expose network ports
3. Workload nees to run commands as root inside the container
