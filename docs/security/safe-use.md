# Safe everyday RCC practice

Security should support research rather than make ordinary work impossible. The following habits prevent most avoidable incidents without adding extra steps to every session.

## Accounts

- Use your own human account.
- Add colleagues to the project instead of sharing credentials.
- Lab instruments use individually registered machine accounts restricted to their spool location; people must not use those accounts.
- Never register one SSH key, passkey or TOTP seed for several human accounts.

## Credentials

- Use the built-in password/passkey manager provided by your supported Windows or macOS environment, or another institutionally approved password manager, for RCC web passwords, passkeys, recovery material, and other suitable secrets.
- Keep SSH private keys on the device where they were generated.
- RCC does **not** recommend adding a passphrase to the normal software-backed RCC SSH key; follow the current RCC key-generation command instead of generic SSH tutorials.
- Prefer a FIDO-backed SSH key where a compatible authenticator is available.
- Keep SSH agent forwarding disabled and do not copy long-lived private keys between computers.
- Never paste credentials or private data into issue trackers, chat, Git, notebooks or support screenshots.
- Report a lost device or unexpected session promptly.

## Endpoint trust

- A personally controlled endpoint is suitable for normal RCC SSH, VS Code and file-transfer workflows.
- A restricted institutionally managed endpoint must use the current RCC-approved connection method and may need support after local policy changes.
- An endpoint administered by an untrusted or actively hostile party is not suitable for sensitive RCC work, even when SSH encryption succeeds. Use an RCC-controlled workstation, virtual desktop, terminal or another trusted endpoint.
- Never approve an unexpected RCC server-identity warning. Stop and contact RCC support.

## Cluster availability

- Use Slurm for computation.
- Avoid job storms, arrays created by mistake, tight retries and repeated connection loops.
- Do not recursively scan shared storage merely to count files.
- Check available capacity before writing large outputs.
- Stop and ask when a tool unexpectedly creates extreme load.

## Web applications

- Do not implement a separate project password database.
- Do not expose a development server directly.
- Do not mount an entire project filesystem into a web application.
- Use the governed proxy, project authorization and curated data interfaces.

## Biomedical data

- RCC may process biomedical research data when the approved project purpose and safeguards cover RCC; the data do not have to be anonymous.
- Removing names is not enough when genomic, imaging, free-text, date, rare-disease, or linkage information can still identify a person.
- Keep direct identifying fields and re-identification keys outside RCC.
- Complete [Class 13](../course/class-13-biomedical-data-privacy.md); keep direct identifiers and re-identification keys outside RCC, and confirm that the project governance covers the biomedical data and intended use.
