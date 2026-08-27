# RCC Gitea: source control inside RCC

RCC Gitea is the RCC-managed source-control and software-artifact service. Use it
for project code, workflow source, reviewable infrastructure changes, and other
software assets that belong in version control.

> **Rollout status:** RCC already uses Gitea as infrastructure, while the newer
> RCC-authenticated general user access plane and its service-plane migration are
> still rollout-gated. This page documents the stable user contract; it does not
> claim that every access path described below is already enabled for every user.

## What belongs in Gitea

Good candidates include:

- analysis code;
- Nextflow/Snakemake workflow source;
- small configuration files without secrets;
- documentation;
- tests;
- reproducible environment/build definitions; and
- reviewed software packages or OCI artifacts when that project/service is
  explicitly enabled.

Do **not** use Git as a research-data store merely because a repository is
private.

Large datasets, patient-derived data, credentials, private keys, access tokens,
and generated result trees belong in their governed RCC data/service locations,
not in Git history.

## Browser sign-in

The intended browser access uses the normal RCC authentication boundary. That
means a user signs in as their RCC identity rather than maintaining a second
independent Gitea password identity for routine browser use.

Authentication answers **who are you?** Repository authorization is still
separate.

## Project membership is not repository permission

Being a member of an RCC project does not automatically make you a writer or
administrator of every repository with a similar name.

Gitea repository/organization ACLs remain explicit source-control permissions.
This is deliberate: filesystem/data authorization and source-code collaboration
are related but are not the same authority.

A useful mental model is:

```text
RCC identity
   |
   +--> project membership -> project data/services
   |
   +--> Gitea repository ACL -> source repository access
```

Neither branch silently widens the other.

## Git from the command line

For normal human Git CLI use, follow the **approved RCC SSH route** published by
RCC. The stable service identity should be used rather than a physical host name
or a transitional backend name.

Do not copy an operator bootstrap configuration that mentions an internal host
into long-lived user documentation or scripts.

Register only your own public SSH key with your account. Do not share one Git
identity across several researchers.

## Browser access is not an API credential

A browser SSO session is intended for interactive human use. Do not assume a
browser cookie can be reused as a machine API or OCI credential.

Automation should use a separately issued, least-privilege token or service
identity when the corresponding RCC capability is enabled. Tokens should be
scoped to the exact repository/package action required.

## OCI/package artifacts

Gitea can also serve as an RCC software artifact/catalog boundary. This is
useful for immutable, reviewed container/software artifacts used by RCC
services.

That does not mean compute nodes should receive broad registry credentials or
pull mutable images at runtime. RCC may instead promote exact digest-bound
artifacts and deploy them offline or through a reviewed service path.

For ordinary researchers, the key rule is simpler: refer to immutable versions
or digests when reproducibility matters.

## Keep secrets out of Git

Never commit:

- passwords;
- API tokens;
- private SSH keys;
- Slurm signing material;
- cloud/S3 credentials;
- recovery codes;
- vault plaintext; or
- patient/research data that is not explicitly approved for source control.

Deleting a secret in a later commit does not reliably remove it from Git
history. If a secret is committed, treat it as exposed and follow the relevant
rotation/recovery procedure.

## Gitea versus project data services

| Need | Better place |
|---|---|
| code, tests, workflow source, documentation | **Gitea** |
| durable research inputs/results | project storage |
| large versioned dataset content | managed DataLad when enabled |
| publication/archive custody | approved repository/Coscine path |
| secrets | RCC-approved secret/credential store, never Git |

## What ClusterDocs intentionally does not expose

This user guide does not document:

- the transitional physical Gitea host;
- Nomad placement internals;
- service UID/GID values;
- CAS secret-handoff transactions; or
- bootstrap single-writer recovery details.

Those are operator implementation details. Users should depend on stable RCC
service identities and the documented authentication/authorization contract.

For the wider developer journey, see the
[Software development path](../paths/software-development.md).
