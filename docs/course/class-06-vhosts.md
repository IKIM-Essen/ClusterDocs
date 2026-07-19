# Class 6: protected project websites

A **vhost**, or virtual host, is a named project website delivered through the RCC web gateway. It can be a simple information page or a small active application with a database-backed search, a curated file collection, a dashboard, a form, or a controlled upload area.

The vhost service is designed to make useful research web interfaces easier to deploy **without asking each project to build its own login system, internet-facing server, or security gateway**.

## Learning outcomes

By the end of this class, you should be able to:

- decide whether a project idea belongs on the governed vhost platform;
- distinguish a static information site from an active project application;
- explain what RCC provides and what the project application must provide;
- use the copyable example without creating local accounts or exposing storage paths;
- prepare a complete vhost request for project-lead and administrator review;
- recognize when computation belongs in Slurm rather than in a web request.

## What is in scope

Good candidates include:

- project documentation and study information;
- read-only dashboards and reports;
- search or query interfaces over an approved internal database;
- curated collections of reports, images or result files;
- small project tools used by an identified project group;
- bounded forms or upload workflows with a defined destination and owner.

A vhost is particularly useful when medical professionals or biomedical researchers need a browser-based interface and should not be expected to install command-line tools.

## What is not in scope

The platform is **not**:

- a general-purpose virtual machine or shell account;
- an unrestricted public web-hosting service;
- a raw browser for an entire project filesystem;
- a database-administration interface;
- a place to expose development servers directly;
- a replacement for Slurm, Snakemake or batch processing;
- a way to bypass project membership, data-protection review or application ownership.

A web request should return promptly. Expensive analyses, large conversions and long-running jobs should be submitted to Slurm and presented later through the web interface.

## Supported site patterns

### 1. Static information site

Use this for documentation, instructions, schedules and other reviewed read-only information.

- No application code runs.
- Hospital users may read approved non-sensitive information without signing in.
- External access receives the centrally defined stronger authentication policy.
- Active scripts, forms and arbitrary file browsing are not part of this profile.

### 2. Active read-only application

Use this for dashboards, database searches and curated downloads.

- Every user has an individual RCC identity.
- Hospital access uses a low-friction sign-in such as username/password or passkey.
- External access requires the stronger central authentication policy.
- The application receives only narrowly scoped, usually read-only data access.

### 3. Active application with controlled writes

Use this for bounded forms, annotations or other reviewed application changes.

- Writes are limited to named application data, not project-wide storage.
- The application records who changed what and when.
- Database permissions are limited to the exact tables or operations required.

### 4. Controlled upload application

Use this when a browser-based upload is more usable than SSH or SFTP.

- Uploads enter a dedicated staging area.
- File names, sizes, types and checksums are validated.
- Uploaded material is not automatically published or treated as trusted.
- A separate process promotes accepted data into its final project location.

## Standard architecture

```text
user browser
    ↓ HTTPS
RCC authentication and reverse proxy
    ↓ trusted identity over a restricted backend path
project application
    ↓ narrowly scoped database or curated file collection
```

Inside the hospital network, an active project application can use the low-friction RCC username/password or passkey flow. Outside the hospital, the gateway requires stronger authentication. Informational static sites may be available without login inside the hospital, but active applications always require an individual identity.

The backend application is not directly reachable by ordinary users. This is important: the trusted identity information is meaningful only when it arrives through the RCC gateway.

## Division of responsibility

| RCC platform provides | Project team provides |
|---|---|
| Central authentication and project-group authorization | A named project lead and technical contact |
| TLS, routing and gateway-only access | A clearly described user-facing purpose |
| Standard request limits and security headers | Application code and tests |
| Integrity monitoring, logging and detection recipes | A declared database or curated-file dependency |
| Deployment and operational health checks | Safe handling of research data and user input |
| Stronger authentication for external access | Maintenance, dependency updates and review responses |

Junior developers are not expected to administer the authentication gateway, integrity checker or detection systems. They are expected to follow the application contract and keep their software maintainable.

## Application contract

A governed active application must:

- have no local login form or separate password database;
- accept identity headers only from the trusted gateway;
- independently require the expected project group;
- reject unexpected host and forwarding information;
- use a dedicated, least-privilege database identity;
- expose curated records or opaque file identifiers, never arbitrary filesystem paths;
- keep deployed code and configuration read-only;
- keep runtime state, uploads and caches in separate writable locations;
- return safe error messages without stack traces, secrets or internal paths;
- log actions using the authenticated RCC username;
- avoid long-running computation in the web request.

## Safe data-access patterns

### Database-backed interface

Prefer a dedicated application account with access to approved views or tables. A read-only dashboard should not receive write or administration privileges.

### Curated file collection

Store a catalogue that maps an opaque identifier to an approved file. The browser supplies the identifier, not a filesystem path. The application checks project membership again before returning the file.

### Computational result portal

The website may collect bounded parameters and display results, but substantial processing should be handled asynchronously through an approved workflow. Do not keep a browser request open while a large scientific analysis runs.

### Upload workflow

Use a staging directory, server-generated names, limits, validation and a recorded promotion step. Do not mount an entire project directory writable into the application.

## Request and approval workflow

1. A project lead describes the purpose, users, data type and required application pattern.
2. RCC Admin selects the fixed security recipe that matches the function.
3. A different administrator reviews the request and its data boundaries.
4. An operator reviews the generated Git change.
5. Deployment, local health checks and access tests run.
6. The project owner periodically confirms that the site is still needed and maintained.

Developers describe required functions, upstream service and data dependencies. They cannot disable authentication, integrity monitoring, logging, request limits or gateway-only access.

## Local copyable example

```bash
cd exercises/vhost/protected-app
python3 -m unittest -v
python3 app.py
```

The example demonstrates:

- trusted identity handling;
- project-group checks;
- a read-only database query;
- curated downloads using opaque identifiers;
- safe failure for direct clients and invalid requests.

Local demonstration mode accepts synthetic headers only from loopback. Production must use the governed RCC gateway and deployment workflow.

## Common mistakes to avoid

- Building another username/password system inside the application.
- Sharing one project account among several people.
- Mounting or publishing the whole project filesystem.
- Passing a filename or directory path directly from the browser to the operating system.
- Running a development server as the production service.
- Giving a read-only interface a database-owner account.
- Performing large analyses synchronously in a web request.
- Returning stack traces or environment details to users.
- Leaving an application without an active owner or update plan.

## Completion gate

You have completed this class when:

- all example unit tests pass;
- you can explain which of the four site patterns fits your project;
- the app refuses direct clients and missing project membership;
- no filesystem path is accepted from the URL;
- the request template names an owner, project, data classification, application pattern, data dependency and review date;
- you can identify any heavy computation that must move to Slurm.
