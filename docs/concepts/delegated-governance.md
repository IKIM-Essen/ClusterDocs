# Delegated governance and project proxies

Institutional or project leads remain accountable, but they do not need to
perform every routine RCC action personally.

## Delegation is not administrator access

Selected proxies can receive named project capabilities such as:

- onboarding and offboarding members;
- membership approval;
- compute or storage requests;
- database or service requests;
- lifecycle notifications;
- archive preparation; and
- restore requests.

A proxy does not thereby receive general LDAP, Slurm, storage, or root
administration.

## Guarded route

```text
institutional lead
  -> delegates named capability
      -> proxy requests action
          -> RCC policy check
              -> constrained executor
```

Delegation should be scoped by project or organization and may include validity
periods, limits, and additional approvals.

## Guardian route

A Guardian or coding agent uses the **same** capability and authority model:

```text
lead or proxy
  -> Guardian interprets request
      -> same RCC capability
          -> same authorization
              -> same constrained executor
```

Automation does not create new authority.

Provenance should preserve accountable principal, proxy/requesting agent,
capability, policy decision, and execution result.
