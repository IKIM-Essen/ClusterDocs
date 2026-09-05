# ClusterDocs 3 adversarial expert review

Status: **required for the ClusterDocs 3 candidate.** The expert review recorded
on 9 August 2026 applied to the earlier product model and does not approve the
browser-first, optional-SSH, RCC Analysis, capability, or agent boundaries added
for ClusterDocs 3.

## Purpose

Treat the documentation and web shell as an operational product. Confirm that it
is technically correct, status-truthful, least-privilege, supportable, and safe
for a naive-user pilot and eventual broad exposure.

Record every finding with page/control, severity, exploit/failure mode,
reproduction steps where useful, and the required correction.

## Review in this order

1. **Product surfaces:** Home, Files, staged RCC Analysis, My RCC/Admin, Assistant,
   Documentation, sign-in/sign-out, project selection, and role-dependent UI.
2. **Zero-SSH journey:** verify an account with no SSH key can complete the
   intended browser path and never receives a hidden shell prerequisite.
3. **Authorization:** attempt cross-project navigation, stale deep links,
   guessed object/run IDs, role confusion, and agent/API calls outside the
   user's current project/capability.
4. **Execution:** verify Notebook and Workflow remain Slurm-governed, bounded,
   idempotent/reconciling on uncertain submission, and do not permit raw
   scheduler argument injection through the ordinary browser path.
5. **Agent boundary:** verify the normal external/general-purpose agent path can
   help from documentation/schemas/synthetic fixtures/bounded diagnostics
   without receiving real protected data, and that agent/MCP calls cannot create
   new authority.
6. **Data lifecycle:** instrument ingestion, project storage, S3/object storage
   where enabled, DataLad, sharing, scratch, retention, Coscine staging, and
   domain applications such as SeqLab.
7. **Advanced path:** SSH/ProxyJump, VS Code, direct Slurm, containers, Gitea,
   workflow engines, GPU selection, and efficient I/O remain technically
   accurate without leaking into the novice critical path.
8. **Web/ops shell:** service URLs and release states come from governed
   configuration; staged services fail closed; role-specific Admin/My RCC links
   are not misleading; decorative status UI does not masquerade as live health;
   external runtime assets are minimized; CSP/accessibility/mobile/keyboard and
   clean-client behavior are reviewed.
9. **Supportability:** diagnostics are reproducible without requesting secrets,
   unrestricted logs, patient data, or unnecessary filenames.

## Adversarial acceptance questions

- Can a user reach a service the page labels unreleased, or does the product
  merely document it?
- Can navigation or a deep link broaden project authority?
- Can My RCC/self-service be confused with administrator authority?
- Can an agent, MCP call, API, or natural-language request perform something the
  same user could not perform through another interface?
- Does the standard agent workflow expose real project data when a synthetic
  fixture or bounded diagnostic would suffice?
- Can a browser/network retry create a duplicate scientific run?
- Can ordinary Analysis users inject raw Slurm/workflow-engine parameters that
  bypass reviewed execution policy?
- Are CPU/RAM/GPU defaults bounded and are idle/repeated workloads steered toward
  more appropriate execution modes?
- Do instrument instructions avoid laptops/personal homes as the default landing
  zone and preserve project ownership/checksums/retry semantics?
- Is S3/object access separately entitled and project-scoped rather than implied
  by ordinary filesystem membership?
- Are archive/preservation claims explicit about current release state and
  verification rather than equating a copy with an archive?
- Are domain applications such as SeqLab described as governed consumers of RCC
  capabilities rather than hidden bypasses around project/storage/identity
  policy?
- Do advanced commands state where they run and avoid administrator privilege?
- Can support diagnose failures without asking users to paste keys, tokens,
  patient data, unrestricted logs, or complete datasets?

## Severity

- **Blocker:** unsafe or legally incorrect guidance; cross-project/role bypass;
  data-loss/disclosure risk; inaccessible critical service; wrong command;
  misleading release state; browser-first path secretly requiring SSH; or
  missing institutional decision required for exposure.
- **Major:** likely to block task completion, create duplicate/incorrect work,
  cause substantial support load, or teach a systematically wasteful pattern.
- **Minor:** local ambiguity, terminology, accessibility, or presentation issue
  with a safe workaround.

ClusterDocs 3 expert approval is recorded only after blocker/major findings are
resolved or explicitly accepted by the responsible owner. Media review remains
separate and does not become approved merely because the written product passes.
