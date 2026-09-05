# RCC Files: browser data entry and result retrieval

RCC Files is the project-facing browser and transfer surface. For many
researchers it should be the first and last stop of an RCC analysis:

```text
Files: upload / choose data
    -> RCC Analysis: Notebook or Workflow
    -> Files: inspect / download results
```

Files is deliberately narrower than “the server filesystem.” It exposes the
project-facing data RCC has admitted to the service; it is not a browser for
arbitrary paths on login, storage, or worker hosts.

## When to use Files

Use Files for ordinary project upload/download, browsing project data, choosing
inputs for RCC Analysis, retrieving results, and bounded approved handoffs.
For very large, automated, or specialized transfers, also read
[Storage and transfer](../reference/storage-transfer.md).

## Sign in with your RCC identity

The browser Files service uses the RCC sign-in boundary. Do not look for a
shared “project account” or separate Files password.

A browser-first RCC user does **not** need an SSH public key merely to use Files
or future browser Analysis capabilities. SSH keys remain optional credentials
for command-line/SFTP paths.

Web sign-in does not change project permissions. Files derives its project view
from current RCC entitlement data and the admitted Files policy.

## Which projects should appear?

For the ordinary Files service, a user should see **all current Files-enabled
Regular projects in which that RCC account is a member**, not only a primary
project or primary group.

The primary project may be used as a convenient landing directory, but it must
not hide the user's other eligible projects.

A project is intentionally absent from ordinary Files when, for example:

- it is not an RCC project object;
- Files publication is not enabled for it;
- the user is not currently a member;
- its admitted `/projects/<project>` directory does not exist; or
- it is a Controlled Data project that requires a different governed surface.

If an expected Regular project is missing, do not work around the problem by
using another user's account, loosening Unix permissions, or copying data into
an unrelated project. Fix the project membership/publication problem instead.

The durable location remains conceptually `/projects/<project>/`, but normal
browser users should not have to type that cluster path. Files and RCC Analysis
should present authorized projects directly.

## Browser transfer performance

The Files architecture is intended to avoid unnecessary copy hops, but good
throughput is a **runtime acceptance property**, not something documentation can
promise from source design alone.

Before broad browser-first rollout RCC should benchmark the deployed path with:

- a multi-GiB browser upload and checksum verification;
- a multi-GiB browser download and checksum verification;
- a representative many-small-file workload;
- at least two concurrent pilot users;
- sustained throughput, retries/errors, and relevant gateway/Files service
  resource use; and
- a same-user/same-project comparison against an accepted native transfer route
  such as SFTP.

A substantial unexplained browser penalty is an RCC defect to investigate. The
normal response should not be “use SSH instead.”

## Browser Files versus SFTP

### Browser — preferred for ordinary interactive use

Use the browser for ordinary upload/download and for the zero-SSH
`Files -> Analysis -> Files` journey.

### SFTP / public key — advanced or automated transfer

Use the approved SFTP/public-key route when scripting or automation is genuinely
more appropriate. This route needs a suitable public key and remains separate
from the browser-first identity path. An SFTP login is a transfer session, not a
general interactive shell.

## Which RCC surface should I use next?

| Goal | Better RCC surface |
|---|---|
| Upload/download or browse project files | **Files** |
| Explore data interactively | **RCC Analysis -> Notebook when released** |
| Run a repeatable/scalable analysis | **RCC Analysis -> Workflow when released** |
| Advanced development / command-line work | **SSH / local VS Code** |
| Direct scheduler work | **Slurm**, for users who need the advanced path |
| Publish/archive data | Separately approved publication/archive route |

The former “RCC Workbench” concept is now the underlying interactive session
machinery behind Analysis Notebook mode, not a separate primary step in the
normal researcher journey.

## From Files into Analysis

Future browser integration may carry selected project/data context from Files
into RCC Analysis. Such a deep link is navigation only: Analysis must re-check
current project and workflow authorization server-side.

For a user with exactly one eligible Analysis project, the product should use it
implicitly rather than require the user to type or select the only possible
project. With multiple projects, the user chooses from a server-generated list.
Navigation never grants new authority.

Results should return to the same project and be reachable again from Files.
RCC Analysis should not create a disconnected private result store.

## External access does not mean public access

A Files service reachable from outside a local network still requires an
approved RCC identity and project authorization. It is not a public file share.
Do not interpret “I can reach the Files page” as authorization to disclose
biomedical or confidential data to another person.

## Controlled Data projects

RCC defines a future **Controlled Data Project** type with a stronger
anti-exfiltration and governed-release boundary. The ordinary Files service and
ordinary Analysis Notebook session are not that boundary.

Controlled Data project creation/runtime admission is currently **not released**.
Until it is explicitly activated, follow the current Regular-project and
biomedical-data guidance rather than assuming browser convenience changes the
data-release rules.

Read [Regular and Controlled Data projects](project-types.md) for the distinction.

## Before every transfer

Check the correct RCC identity, project, source/destination, governance,
recipient authorization, data class, and released transfer route. For sharing
decisions, read [How to share data safely](../reference/data-sharing.md).
