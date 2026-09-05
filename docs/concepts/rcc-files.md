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

Use Files for tasks such as:

- uploading an approved input into the correct project;
- choosing data that will be used by RCC Analysis;
- downloading an approved result;
- browsing the project-facing file tree; or
- creating a bounded handoff through the approved project surface.

For very large, automated, or specialized transfers, check
[Storage and transfer](../reference/storage-transfer.md) before choosing a tool.

## Sign in with your RCC identity

The browser Files service uses the RCC sign-in boundary. Do not look for a
separate shared “project account” or a native Files password.

A browser-first RCC user does **not** need an SSH public key merely to use Files
or future browser Analysis capabilities. SSH keys are optional credentials for
command-line/SFTP paths.

Use your individual RCC identity. Depending on the active authentication policy,
the sign-in flow may use your RCC password, passkey, or another enrolled factor.
A web sign-in does not change project permissions: the Files service resolves
what your RCC account is allowed to see.

For the credential model, read
[How RCC authentication fits together](../reference/authentication-lifecycle.md).

## Files is project-scoped

Before transferring data, verify both the project and the intended location
inside that project's admitted Files view.

If a project is missing, do not work around the problem by using another user's
account, loosening Unix permissions, or copying data into an unrelated project.
Fix the project membership or service entitlement instead.

The usual durable research location remains conceptually `/projects/<project>/`,
but normal browser users should not need to type that cluster path. Files and
RCC Analysis should present authorized projects directly.

## Browser Files versus SFTP

### Browser — preferred for ordinary interactive use

Use the browser for ordinary upload/download and for the zero-SSH
`Files -> Analysis -> Files` journey.

### SFTP / public key — advanced or automated transfer

Use the approved SFTP/public-key route when scripting or automation is genuinely
more appropriate. This route needs a suitable public key and remains separate
from the browser-first identity path.

An SFTP login is a transfer session, not a general interactive shell.

## Which RCC surface should I use next?

| Goal | Better RCC surface |
|---|---|
| Upload/download or browse project files | **Files** |
| Explore data interactively | **RCC Analysis -> Notebook when released** |
| Run a repeatable/scalable analysis | **RCC Analysis -> Workflow when released** |
| Advanced development / command-line work | **SSH / VS Code** |
| Direct scheduler work | **Slurm**, for users who need the advanced path |
| Publish/archive data | Separately approved publication/archive route |

The former “RCC Workbench” concept is now treated as the underlying interactive
session machinery behind Analysis Notebook mode, not a separate primary step in
the normal researcher journey.

## From Files into Analysis

The future browser integration may allow a researcher to select one or more
project objects in Files and continue into RCC Analysis with that project/data
context. Such a deep link is navigation only: Analysis must re-check project and
workflow authorization server-side.

Results should return to the same project and be reachable again from Files.
RCC Analysis should not create a disconnected private result store.

## External access does not mean public access

A Files service reachable from outside a local network still requires an
approved RCC identity and project authorization. It is not a public file share.
Additional authentication may be required for an external session.

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

Check:

- correct RCC identity;
- correct project;
- correct destination/source;
- whether the project's governance allows the transfer;
- whether the recipient is authorized; and
- whether the transfer route is released for this data class.

For sharing decisions, read [How to share data safely](../reference/data-sharing.md).
