# How RCC authentication fits together

RCC uses one human identity across several access methods. The credentials are
not interchangeable, and **an RCC account does not imply that every user needs
an SSH credential**.

The useful mental model is:

```text
RCC account
   |
   +--> web sign-in / SSO
   |      -> password and/or sign-in passkey
   |      -> Files
   |      -> My RCC
   |      -> RCC Analysis Notebook/Workflow when released
   |
   +--> account step-up / recovery
   |      -> portal passkey or YubiKey, authenticator code, recovery codes
   |
   +--> optional SSH / SFTP capability
          -> SSH public key registered to your RCC account
```

Never share any of these credentials with another person. Project access is
managed by membership, not by sharing an account.

## 1. Account activation creates the human RCC identity

The account-activation process establishes your RCC username and the initial
credentials required by the current enrollment flow. Follow the activation
instructions supplied by RCC rather than an old screenshot or a colleague's
saved procedure.

After activation, the same human identity is used by RCC web services, project
membership, Slurm attribution, Files, and optional SSH even though those
surfaces may use different authentication mechanisms.

A browser-first user may stop here: if their work is fully supported through
Files and RCC Analysis, there is no reason to create an SSH key merely because
the account exists.

## 2. Web sign-in is shared across RCC services

RCC web services use a common sign-in boundary where possible. A successful web
sign-in can establish your authenticated RCC identity for services such as
Files, account/project management, and other released RCC applications.

When RCC Analysis is released, Notebook and Workflow modes use this browser
identity plus server-side project authorization. They do not require a browser
user to possess a Slurm signing key or SSH private key.

This is **single sign-on**, not shared authorization. After sign-in, each service
still checks whether your identity may access the requested project or action.

Signing into one RCC website does not add you to a project or grant administrator
rights.

### Use the operating system's credential manager

For RCC web passwords, passkeys, and appropriate recovery material, use the
credential/password-manager facilities already provided by the supported
Windows or macOS environment, or another institutionally approved password
manager. On macOS this includes the system Passwords/Keychain facilities; on
Windows use the supported built-in password/passkey and Windows Hello/browser
facilities where the RCC sign-in flow offers them.

Do not write RCC passwords, recovery codes, or web credentials into source
files, notes stored with project data, shell scripts, Git repositories, or chat.
This recommendation is about **web/account credentials**. It is not a reason to
add a passphrase to the RCC SSH private key.

## 3. Sign-in passkeys belong to the RCC sign-in service

A passkey or hardware security key registered for **SSO sign-in** is intended to
sign you into RCC web services through the common sign-in portal.

Manage these credentials at the RCC sign-in portal's credential/settings page
when that option is available.

A sign-in passkey can therefore be present even if another RCC page says that no
**portal passkey** is registered. The two credentials may belong to different
relying-party stores and serve different purposes.

## 4. Portal passkeys / YubiKeys are for sensitive account actions

RCC account management may also keep a separate portal-local passkey or YubiKey
for step-up confirmation and recovery-related actions.

This credential is not necessarily the same WebAuthn credential used for SSO.
The account security page should label the two stores separately rather than
showing every credential as one generic “passkey.”

If you see both sections, read the labels before adding or deleting anything.
Removing a portal-local step-up credential should not be confused with removing
your SSO sign-in passkey, and vice versa.

## 5. Authenticator codes are a second factor

RCC may use an authenticator application code as an enrolled second factor.
Treat the seed/QR setup as secret. Do not photograph or distribute it to another
person.

If the current account-security page offers replacement, follow the guarded
replacement procedure rather than enrolling a second person's device on your
account.

## 6. Recovery codes are emergency credentials

Recovery codes are individual, single-use emergency credentials. Store them
away from the computer/session they protect, preferably in an approved password
manager or another secure location appropriate to your work environment.

Do not place recovery codes in:

- a project repository;
- a shared lab wiki;
- a shell-history command;
- a public or project-readable file; or
- a prompt to an external AI/coding service.

When a recovery code is used, it should no longer be considered available for a
future recovery.

## 7. SSH keys are an optional separate access mechanism

SSH does not normally reuse your browser passkey. It uses an SSH public/private
key pair registered to your RCC account.

Enroll an SSH key when you need the command-line path, VS Code Remote SSH, direct
Slurm use, SFTP/public-key automation, or another capability that explicitly
requires SSH.

Do **not** enroll an SSH key merely because you think every RCC account must have
one. Browser-first Files and future RCC Analysis users should be able to work
without SSH credentials.

Only the **public** key is registered with RCC. The private key remains on your
computer or compatible hardware authenticator. For the normal software-backed
RCC key, follow the RCC setup command, which intentionally creates it **without
a passphrase**. Protect the endpoint itself and do not copy the private key
between machines.

For a FIDO-backed SSH key, the authenticator protects the SSH private material;
this is still conceptually different from a browser/WebAuthn passkey even when
the same physical YubiKey is involved.

Follow [Class 1: safe access](../course/class-01-safe-access.md) and
[Access, SSH, and VS Code](access-ssh-vscode.md) when you actually need SSH.

## 8. One physical security key can contain different credentials

A YubiKey or similar authenticator can participate in several protocols. For
example, one device might hold:

- a WebAuthn credential for RCC SSO;
- a different WebAuthn credential for portal step-up/recovery; and
- an OpenSSH `*-sk` key used for SSH.

The physical device is the same; the credentials and relying parties are not.
Do not delete one entry merely because another entry on the same hardware works.

## 9. Sign-out and session expiry are normal security boundaries

Web sessions expire and sensitive actions may require a fresh step-up even when
you are still generally signed into RCC. An RCC Analysis Notebook reconnect may
similarly require fresh browser authentication while the underlying Slurm-backed
interactive session still exists.

This separation prevents an old browser tab from becoming indefinite authority.

## If you lose a credential

Use the documented RCC recovery route. Do not solve the problem by:

- borrowing another person's account;
- registering a shared lab credential;
- sending a private key or recovery code to support by ordinary email; or
- disabling host/authentication checks.

If the normal self-recovery methods are unavailable, follow the current
identity-verification and approver/support procedure.

## Quick reference

| Need | Credential / surface |
|---|---|
| Sign into RCC websites | RCC SSO password/passkey according to current policy; store it with the supported OS/password-manager facilities |
| Files / future Analysis Notebook / Workflow | web identity + project authorization; **no SSH key required** |
| Confirm a sensitive account action | step-up factor requested by the account portal |
| Emergency account recovery | recovery code or approved recovery procedure |
| SSH / VS Code Remote SSH / public-key SFTP | your registered SSH public key + local private key; normal RCC software key has **no passphrase** |
| Project access | **not a credential** — project membership / delegated role |
| Administrator capability | **not a credential** — separately authorized role/capability |

Authentication proves who you are. Authorization still decides what that
identity may do.
