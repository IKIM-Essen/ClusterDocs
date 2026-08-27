# RCC Files: browse and transfer project data

RCC Files is the project-facing browser and transfer surface. Use it when the
main task is to move, upload, download, or inspect approved project files without
opening an interactive compute session.

Files is deliberately narrower than “the server filesystem.” It exposes the
project-facing data RCC has admitted to the service; it is not a browser for
arbitrary paths on login, storage, or worker hosts.

## When to use Files

Use Files for tasks such as:

- uploading an approved input into the correct project;
- downloading an approved result;
- browsing the project-facing file tree;
- creating a bounded handoff through the approved project surface; or
- using the supported SFTP/public-key route when a command-line transfer is more
  appropriate than a browser upload.

For very large, automated, or specialized transfers, check
[Storage and transfer](../reference/storage-transfer.md) before choosing a tool.

## Sign in with your RCC identity

The browser Files service uses the RCC sign-in boundary. Do not look for a
separate shared “project account” or a native Files password.

Use your individual RCC identity. Depending on the active authentication policy,
the sign-in flow may use your RCC password, passkey, or another enrolled factor.
A web sign-in does not change the project's filesystem permissions: the Files
service still resolves what your RCC account is allowed to see.

For the credential model, read
[How RCC authentication fits together](../reference/authentication-lifecycle.md).

## Files is project-scoped

Before transferring data, verify both:

1. the **project** you intend to work with; and
2. the **destination path** inside that project's admitted Files view.

If a project is missing, do not work around the problem by using another user's
account, loosening Unix permissions, or copying the data into an unrelated
project. Fix the project membership or service entitlement instead.

The usual durable research location remains conceptually:

```text
/projects/<project>/
```

The Files surface may expose only the portion of that project admitted for
transfer. Its absence from Files does not imply that all server paths should be
made visible.

## Browser Files versus SFTP

The browser and SFTP routes solve different interaction problems but should map
to the same project authorization model.

### Browser

Use the browser when you want an interactive upload/download experience and do
not need scripting.

### SFTP / public key

Use the approved SFTP/public-key route when a command-line or automated transfer
is more appropriate. Follow the current RCC connection instructions and use your
own SSH key; do not create shared credentials for a project.

An SFTP login is still a transfer session, not a general interactive shell.

## Files versus SSH, Workbench, and Analysis

| Goal | Better RCC surface |
|---|---|
| Upload/download or browse project files | **Files** |
| Edit code or work interactively | **SSH / VS Code now; Workbench when released** |
| Run substantial compute | **Slurm** |
| Run a repeatable governed workflow | **RCC Analysis when released** |
| Publish/archive data | Use the separately approved publication/archive route |

Moving data is not the same thing as computing on it, and neither action implies
permission to release it outside the project.

## External access does not mean public access

A Files service reachable from outside a local network still requires an
approved RCC identity and project authorization. It is not a public file share.
Additional authentication may be required for an external session.

Do not interpret “I can reach the Files page” as authorization to disclose
biomedical or confidential data to another person.

## Controlled Data projects

RCC defines a future **Controlled Data Project** type with a stronger
anti-exfiltration and governed-release boundary. The ordinary Files service is
not that boundary.

Controlled Data project creation/runtime admission is currently **not released**.
Until it is explicitly activated, follow the current Regular-project and
biomedical-data guidance rather than assuming Files can carry protected-data
release semantics.

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
