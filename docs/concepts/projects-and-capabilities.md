# Projects and supported actions

## Your project keeps the work together

An RCC project connects the people, files, computing work, and results for one
approved purpose. It is more than a folder name.

When you use a browser, VS Code, SSH, a workflow, or a coding agent, the same
project decides which data you can use and where the results belong.

## Ask for the result you need

You can say:

```text
Run this workflow with 8 CPUs and 32 GB of memory.
Save the results and logs in my project.
```

You should not need to choose a physical worker or manually start cluster
services. RCC handles those infrastructure details.

Other supported requests may include creating a project database, transferring
approved data, or preparing an archive. Availability depends on the current RCC
service status.

## Finding an action does not grant access

A coding agent may know that RCC can run workflows or request services. That does
not mean it may do so for every project. RCC still checks your identity, project
membership, delegated approval, data rules, and the limits of the requested
action.

## Technical terms

| Term | Plain-language meaning |
|---|---|
| Interface | Where you ask: web page, editor, command line, API, or MCP |
| Tool | One callable operation |
| Capability | An RCC-supported action with permission checks and a recorded result |
| Managed service | A service RCC operates for an approved project |

Important actions should record who requested them, for which project, what RCC
allowed, and whether the action succeeded.
