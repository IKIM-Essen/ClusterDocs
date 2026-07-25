# Class 6: protected project websites — video narration

## Slide 1: Class 6: protected project websites

Welcome to Class 6: protected project websites. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning outcomes

By the end of this class, you should be able to: decide whether a project idea belongs on the governed vhost platform; distinguish a static information site from an active project application; explain what RCC provides and what the project application must provide; use the copyable example without creating local accounts or exposing storage paths; prepare a complete vhost request for project-lead and administrator review; recognize when computation belongs in Slurm rather than in a web request.

## Slide 3: What is in scope

Good candidates include: project documentation and study information; read-only dashboards and reports; search or query interfaces over an approved internal database; curated collections of reports, images or result files; small project tools used by an identified project group; bounded forms or upload workflows with a defined destination and owner. A vhost is particularly useful when medical professionals or biomedical researchers need a browser-based interface and should not be expected to install command-line tools.

## Slide 4: Standard architecture

Inside the hospital network, an active project application can use the low-friction RCC username/password or passkey flow. Outside the hospital, the gateway requires stronger authentication. Informational static sites may be available without login inside the hospital, but active applications always require an individual identity. The backend application is not directly reachable by ordinary users. This is important: the trusted identity information is meaningful only when it arrives through the RCC gateway.

## Slide 5: Division of responsibility

Junior developers are not expected to administer the authentication gateway, integrity checker or detection systems. They are expected to follow the application contract and keep their software maintainable.

## Slide 6: Safe data-access patterns

### Database-backed interface Prefer a dedicated application account with access to approved views or tables. A read-only dashboard should not receive write or administration privileges. ### Curated file collection Store a catalogue that maps an opaque identifier to an approved file. The browser supplies the identifier, not a filesystem path. The application checks project membership again before returning the file. ### Computational result portal The website may collect bounded parameters and display results, but substantial processing should be handled asynchronously through an approved workflow. Do not keep a browser request open while a large scientific analysis runs. ### Upload workflow Use a staging directory, server-generated.

## Slide 7: Request and approval workflow

A project lead describes the purpose, users, data type and required application pattern. RCC Admin selects the fixed security recipe that matches the function. A different administrator reviews the request and its data boundaries. An operator reviews the generated Git change. Deployment, local health checks and access tests run. The project owner periodically confirms that the site is still needed and maintained. Developers describe required functions, upstream service and data dependencies. They cannot disable authentication, integrity monitoring, logging, request limits or gateway-only access.

## Slide 8: Local copyable example

The example demonstrates: trusted identity handling; project-group checks; a read-only database query; curated downloads using opaque identifiers; safe failure for direct clients and invalid requests. Local demonstration mode accepts synthetic headers only from loopback. Production must use the governed RCC gateway and deployment workflow.

## Slide 9: Completion gate

You have completed this class when: all example unit tests pass; you can explain which of the four site patterns fits your project; the app refuses direct clients and missing project membership; no filesystem path is accepted from the URL; the request template names an owner, project, data classification, application pattern, data dependency and review date; you can identify any heavy computation that must move to Slurm.
