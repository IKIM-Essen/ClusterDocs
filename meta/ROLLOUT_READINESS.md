# ClusterDocs 3 production-candidate status

Review date: 5 September 2026

## Current decision

`clusterdocs-3` is the temporary future-release candidate. The branch materially
changes the product model: browser-first use, optional SSH, RCC Analysis
Notebook/Workflow, progressive disclosure of advanced HPC controls, a broader
RCC capability story, a stronger AI/agent boundary, corrected credential
policy, and an explicit **I/O-first** scheduler/storage/service-plane rationale.

The expert review recorded for the August candidate is superseded. Broad Stage-1
exposure is blocked until a fresh ClusterDocs 3 expert review and zero-SSH
naive-user browser acceptance are completed.

A very small controlled pilot is allowed before those reviews so the team can
prove the deployment works in principle and collect real browser evidence. The
pilot is not equivalent to broad production acceptance.

Production publication is **main-only**. Validation of `clusterdocs-3` is not
merge authorization and is not permission to publish directly from the
candidate branch. After acceptance closure, promoting the candidate into `main`
requires a separate explicit authorization.

## Why the platform looks different

The most important technical lesson behind RCC is that **I/O access pattern is a
first-order architecture constraint**. Small-file/metadata storms, repeated
scans, package trees, workflow temporary state, editor indexing, synchronized
reference access, and random temporary I/O can dominate both elapsed time and
shared-service pressure even when aggregate storage bandwidth is high.

That is why ClusterDocs now teaches local staging/scratch, deliberate workflow
I/O, immutable/cacheable artifacts, and low-I/O developer-tool settings. It is
also why “put everything on Ceph/Kubernetes/a single popular substrate” is not
treated as an automatic solution. Backend technology matters; workload shape
matters first.

## Stage 1 — written site

Stage 1 is the first production release and **does not wait for regenerated
videos**. It publishes the accepted written site from `main` while media player
links remain fail-closed.

Stage-1 blockers are:

1. complete the fresh adversarial review and resolve blocker/major findings;
2. run zero-SSH naive-user browser acceptance against the exact staged candidate;
3. run separate advanced-user acceptance, including the RCC-safe VS Code low-I/O profile;
4. review the I/O-first Slurm/service-plane/Kubernetes/Ceph explanation against the actual RCC implementation;
5. complete institutional/privacy/accessibility/operational checks;
6. verify all service links and release badges against the actual deployment;
7. verify role separation for self-service versus administrator actions;
8. verify the data-blind agent path and authority boundaries;
9. choose the final release version;
10. obtain explicit authorization to merge the accepted candidate into `main`;
11. rerun production gates on the exact resulting `main` commit; and
12. keep media `preview_links` disabled so generated pages contain no playable or broken unpublished video URL.

The existing generated Part-1 media predates the corrected SSH credential
policy, but this does not block Stage 1 because the player remains disabled. The
**written source/narration/caption text is current** and is the Stage-1 authority.

## Stage 2 — videos

After the written repository has settled, regenerate and review the videos on
the approved workstation. Stage 2 includes:

- corrected Part-1 media from the current source/narration;
- re-rendering any other video whose source changed materially;
- optional production of the prepared **3–4 minute “What changed from the old cluster?”** video for returning users;
- updated manifest hashes, sizes, durations, and caption timing;
- human video/caption review;
- media endpoint TLS/MIME/range/full-download verification; and
- changing the governed media state to `verified_live` before enabling links.

Once player links are enabled, media approval becomes a hard readiness gate.

## What ClusterDocs 3 must communicate

- New users can begin with a research task rather than learning cluster topology.
- Browser-first research is a legitimate complete path; an RCC account does not imply an SSH credential.
- Advanced users can immediately discover instrument ingestion, project S3/POSIX/DataLad, Notebook, Workflow, Slurm/GPU/HPC, self-governance/delegation, AI assistance, project services, Coscine status, and domain applications such as SeqLab.
- Agents can help explain, design, code, test, and debug without making protected project-data disclosure the default workflow.
- Windows/macOS password/passkey managers are recommended for web/account credentials; the normal RCC software-backed SSH key is generated without a passphrase.
- I/O patterns are treated as the primary performance/architecture concern; the low-I/O VS Code defaults are visible in first-use advanced guidance.
- Slurm owns scientific compute while the RCC service plane owns long-lived services; Kubernetes remains a possible future choice when a concrete workload justifies it, not a mandatory universal substrate.
- Every staged/future capability remains status-truthful and fail-closed.

## Manual review gate on the candidate

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --output site-review
python3 tools/rollout_readiness.py --manual-review
```

The manual-review command verifies that the active v3 documentation is coherent
enough to begin human review. It must not reuse the August expert receipt.

## Promotion gate

Only after Stage-1 candidate acceptance is complete and explicit merge
authorization is given:

1. merge the accepted `clusterdocs-3` candidate into `main` through the normal repository path;
2. record the exact resulting main commit;
3. verify no unreviewed changes entered with the promotion; and
4. run the production gates on that exact main commit.

No merge has been authorized by this plan.

## Production release gate on main

```bash
python3 tools/validate_repo.py
python3 tools/build_site.py --production --output site-production
python3 tools/rollout_readiness.py
```

For Stage 1, readiness must report that video links are fail-closed and video
human review is deferred. The manually dispatched production workflow itself
accepts only `refs/heads/main`. `assets/release.json` must record
`source_branch: main` and the exact source commit.

After verified main-based Stage-1 publication and rollback evidence,
`clusterdocs-ng` and `clusterdocs-3` can be retired through repository policy.
Stage-2 media work then branches normally from `main`.