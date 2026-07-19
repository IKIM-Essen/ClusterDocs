# Class 6 narration: protected project websites

**Target duration:** 8–10 minutes
**Audience:** biomedical researchers, medical professionals, project leads and junior research-software developers
**Recording style:** calm, practical and reassuring; approximately 125–135 spoken words per minute
**Status:** recording script for novice review before video production

## Pronunciation guide

- RCC: say each letter, “R C C”
- vhost: “vee-host”
- HTTPS: “H T T P S”
- Slurm: “slurm”
- SQLite: “S Q Lite”
- two-factor authentication: say the full phrase before using “two F A”

## YouTube-ready chapters

```text
00:00 What a protected project website is
00:48 Which projects fit the vhost platform
02:02 What is outside the scope
03:03 How access works inside and outside the hospital
04:08 What RCC provides
05:02 What the application team must provide
06:15 Safe database, file and upload patterns
07:42 Request, approval and deployment
08:38 The copyable example and completion gate
```

## Narration script

### 00:00 — What a protected project website is

Welcome to Class 6: protected project websites.

In this class, the word **vhost** means a named project website delivered through the RCC web platform. It may be a simple information page, or it may be a small active application—for example, a read-only database search, a dashboard, a curated file collection, a project form, or a controlled upload area.

The purpose of the platform is to make useful research web interfaces easier to provide without asking every project to build its own login system, internet-facing server, or security gateway.

This is especially important for medical professionals and biomedical researchers. A browser interface can be far easier to adopt than a command-line workflow, while still preserving individual access and project boundaries.

### 00:48 — Which projects fit the vhost platform

A good vhost has a clearly defined audience, owner and purpose.

Suitable examples include project documentation, study information, dashboards, report viewers, database query forms, approved collections of result files, and small tools used by a known project group.

There are four common patterns.

The first is a **static information site**. It contains reviewed, read-only information and runs no application code.

The second is an **active read-only application**. It may search a database or present a curated file collection, but it does not modify the underlying scientific records.

The third is an **active application with controlled writes**. It may save an annotation or a bounded form, but only through explicitly approved operations.

The fourth is a **controlled upload application**. It accepts files into a staging area, validates them, and records who submitted them before a separate process moves accepted data to its final location.

### 02:02 — What is outside the scope

The vhost platform is not a general-purpose virtual machine, a shell account, or unrestricted public web hosting.

It is not a raw browser for an entire project directory. It is not a database-administration tool. And it is not a replacement for Slurm or Snakemake.

A useful rule is this: the website should support interaction, navigation and presentation. Expensive analysis belongs in a scheduled workflow.

For example, a website may let a user select a sample and view a previously generated report. It may submit a carefully bounded request to an approved workflow. But it should not keep a browser connection open while a large scientific analysis consumes substantial CPU, memory or storage resources.

Separating interaction from computation improves reliability for the application and for the cluster as a whole.

### 03:03 — How access works inside and outside the hospital

RCC provides a central authentication and reverse-proxy layer in front of project applications.

Inside the hospital network, active project applications use a low-friction sign-in. Depending on the approved setup, the user can sign in with the normal RCC username and password or with a passkey.

From outside the hospital, the gateway requires stronger authentication, including two-factor authentication.

Read-only information sites may be available without a login inside the hospital when the content is approved for that audience. Active applications always require an individual identity because they display project information, accept input, or record user actions.

This distinction keeps simple information easy to reach while preserving attribution where actions matter.

Users should never share a project login. If a colleague needs access, the correct solution is to add that person to the project with their own account.

### 04:08 — What RCC provides

The RCC platform provides the common controls that would otherwise be difficult for every project to implement correctly.

It provides central authentication, project-group authorization, encrypted browser connections, routing, request limits, standard security headers, logging, integrity monitoring and operational health checks.

It also ensures that the application backend is reached through the governed gateway rather than directly by ordinary users.

This matters because the application receives trusted identity information from the gateway. A username presented by an arbitrary client must never be accepted as proof of identity.

The platform also applies a fixed security recipe for the type of site being deployed. Junior developers do not need to configure the authentication service, integrity checker or detection systems themselves.

### 05:02 — What the application team must provide

The project team still owns the scientific purpose and the application itself.

Every application needs a named project lead and a technical contact. It needs tests, a declared data source, and a maintenance plan.

The application must not create another local password database. It must accept identity information only through the trusted gateway and must check that the user belongs to the expected project group.

Database access must use a dedicated application identity with only the permissions needed for that interface. A read-only dashboard does not need permission to modify tables or administer the database.

Deployed code and configuration should be read-only. Runtime data, caches and uploads belong in separate writable locations.

Errors shown to users should be helpful but safe. They should include a request identifier, not a stack trace, secret, database error or internal filesystem path.

### 06:15 — Safe database, file and upload patterns

For a database interface, expose approved views or narrowly selected tables. Avoid connecting with a personal account or a database-owner credential.

For file access, use a curated catalogue. The browser asks for an opaque identifier, and the application maps that identifier to one approved file. The browser must not supply an operating-system path.

This prevents a small programming error from turning the website into a browser for unrelated project data.

For uploads, use a dedicated staging area. Generate the stored name on the server, enforce file-size and file-count limits, calculate a checksum, validate the content, and record the authenticated user.

An uploaded file is not automatically trusted and should not become public content merely because the transfer succeeded.

For computational portals, separate the web request from the scientific job. Validate the request, submit bounded work through the approved workflow, and let the user return later to view the result.

### 07:42 — Request, approval and deployment

The deployment process starts with a project lead describing the purpose, intended users, data classification and application pattern.

RCC Admin assigns the standard security recipe. A different administrator reviews the request and its data boundaries. An operator then reviews the generated Git change before deployment and health testing.

This separation keeps the process reviewable without forcing the developer to become a security-platform administrator.

It also creates useful bookkeeping: who owns the site, what it is allowed to access, when it must be reviewed, and how it can be retired safely.

A site that no longer has an active owner or maintenance plan should not remain deployed indefinitely.

### 08:38 — The copyable example and completion gate

The course includes a small protected application that junior developers can copy and adapt.

It demonstrates a read-only S Q Lite database, project-group authorization, curated file downloads, safe errors and local tests.

The tests prove that direct clients are rejected, the wrong project group is rejected, unexpected write methods are rejected, and browser-supplied filesystem paths are not accepted.

Your completion gate is not simply that the application starts.

You should be able to explain which site pattern fits your project, identify the project owner and data dependency, pass the example tests, and point out any substantial computation that must move to Slurm.

The central idea is straightforward: make the browser experience easy for users, keep identity and security controls consistent, and expose only the data and functions the application genuinely needs.

That produces a service which is easier to adopt, easier to maintain, and safer for the project and the wider RCC community.
