# Planned PiKVM access through RCC Headscale

RCC is preparing **RCC Headscale** as its institutionally operated
coordination service for approved remote laboratory-device access.

> **Service status: not yet released.** Do not enroll a workstation or PiKVM
> device until RCC announces the service and supplies enrollment material
> through the approved institutional channel.

Headscale replaces the hosted Tailscale control plane for this workflow.
PiKVM devices and approved administrator computers still use a
Tailscale-compatible client. The client connects to RCC Headscale instead of
creating or joining a personal hosted Tailscale network. No personal Tailscale
SaaS account is part of the RCC design.

## What the service will provide

The service creates an encrypted device-to-device connection. It first attempts
a direct connection. When firewalls or NAT prevent direct communication, an
RCC-operated relay carries the already encrypted traffic.

The relay will not provide general RCC or Lab-network access. Reviewed policy
will permit named administrator devices to reach registered PiKVM controllers
only on the management services required for their approved purpose.

## Access after release

After RCC announces the service:

1. Ask RCC operations for access to the specific laboratory controller.
2. Install the supported Tailscale-compatible client when instructed.
3. Complete the one-time enrollment delivered through the approved
   institutional channel.
4. Open the stable PiKVM name supplied with the approval.
5. Remove the local enrollment material after the device has joined.

The Headscale endpoint is a machine-protocol service, not the PiKVM user
interface. RCC will publish the supported endpoint only when the service is
released.

## Safety rules

- Never copy enrollment keys into chat, email, Git, tickets, or shared notes.
- Do not reuse another person's enrolled workstation.
- Do not enroll personal or unapproved devices.
- Do not share PiKVM names or credentials outside the approved team.
- Keep PiKVM authentication enabled inside the tunnel.
- Report a lost computer or unexpected device immediately so RCC can remove
  its access.

Operational enrollment commands, device inventory, relay topology, addresses,
and recovery instructions remain in the private RCC infrastructure repository
and are not published in ClusterDocs.
