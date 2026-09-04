# Request and activate an RCC account

> **Current availability:** enrollment is an **invite-only pilot**, not general
> public signup. RCC Admin and My RCC must complete the deployment gates tracked
> in RCC PR #1672 and the directly stacked PR #1674 before the pilot expands.

## Before you begin

Ask the approver for your organizational **primary group** for a personal RCC
enrollment link. The signed link is valid for seven days and fixes both the
primary group and sponsor. Do not edit or forward it. If either value is wrong,
ask the sender for a new link.

Your primary group records where you belong. It is not a research project and
does not grant access to project data. Project membership is requested
separately after activation.

The short request asks for:

- your first and last name;
- institutional email address;
- organization or department;
- telephone or internal contact reference; and
- a short description of your intended RCC use.

You do **not** choose an RCC username, upload an SSH key, or request a project
in this form. RCC proposes a collision-checked username. Each person receives
one account; shared accounts and shared human credentials are not supported.

## Submit the request

1. Open the signed link supplied by the approver.
2. Confirm that the displayed primary group and sponsor are correct.
3. Enter the requested identity and contact information.
4. Submit once and retain the displayed request reference.

The request enters the authenticated RCC Admin queue. It is not approval and
does not create an LDAP account, project membership, home directory, or
credential.

Do not submit a second request. If the request has not been acknowledged within
two working days, contact the support route named on the receipt and include the
reference. Never include a password, activation code, recovery code, private SSH
key, or patient information.

## Approval and activation

The approver checks your identity, institutional email, affiliation, primary
group, sponsor, and intended use outside the form. Approval creates the RCC
identity in exactly one primary group and produces a single-use activation
slip.

The activation slip is handed to you through the approved direct channel. RCC
does not email activation secrets.

Use the slip at the RCC activation page to:

1. set your initial RCC password;
2. enroll the required authenticator;
3. save the recovery codes; and
4. complete the first login.

If the slip expires, ask the same approver for a replacement. Do not ask anyone
to send a replacement code through ordinary email or chat.

## After activation

Use **My RCC** for personal security settings, recovery factors, notification
preferences, and optional SSH public keys. Only add an SSH key if you need
terminal, VS Code, or command-line transfer access.

Project access remains a separate governed decision. Ask the project owner or
primary-group approver for membership in the appropriate project; do not change
your primary group merely to share research data.

Continue with [Expedition Light](index.md) when your account and approved RCC
connection configuration are available.

## If something goes wrong

Stop and contact the named RCC pilot support route when:

- the invitation shows the wrong sponsor or primary group;
- the form says enrollment is closed or the invitation is invalid;
- you may already have an RCC identity;
- approval or activation leaves you unsure what to do next;
- first login or authenticator enrollment fails; or
- an SSH host-identity warning appears.

A failed or delayed email never changes the authoritative state. RCC Admin is
the source of truth for the request and account; notification email is advisory
only.
