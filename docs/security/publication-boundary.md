# Public documentation security boundary

ClusterDocs is intentionally useful without becoming an infrastructure map.

## Allowed public information

- stable user-facing aliases;
- login and transfer workflows;
- user-visible storage conventions;
- Slurm resource-request examples;
- safe troubleshooting that concerns the user's own account or job;
- project-web-application development contracts;
- current trusted host fingerprints when approved for publication.

## Administrator-only information

Do not publish:

- internal or DMZ IP addresses;
- physical infrastructure hostnames;
- node lists, counts or host ranges;
- BMC, PiKVM, MAAS or power-control information;
- firewall rules, monitoring locations or detailed IDS signatures;
- LDAP bind identities, service credentials or secret locations;
- administrative SSH routes;
- detailed service topology or failover mapping;
- commands that scan hosts, networks or the full filesystem fleet.

## Denial-of-service-safe documentation

Examples must have explicit CPU, memory and time limits. Connection tests use one attempt. Training jobs run sequentially. Public troubleshooting never recommends host scans, infinite retries, full-fleet enumeration, uncontrolled benchmarks or broad recursive filesystem operations.

The publication linter enforces common cases, but human security review remains mandatory.
