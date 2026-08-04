# Class 8: protected project websites — video narration

## Slide 1: Class 8: protected project websites

Welcome to Class 8: protected project websites. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

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

## Slide 7: Local copyable example

The example demonstrates: trusted identity handling; project-group checks; a read-only database query; curated downloads using opaque identifiers; safe failure for direct clients and invalid requests. Local demonstration mode accepts synthetic headers only from loopback. Production must use the governed RCC gateway and deployment workflow.
