# ClusterDocs NG development and promotion plan

## Repository recommendation

Develop the new curriculum in a separate `clusterdocs-ng` staging repository. Do not put public training material into the RCC infrastructure repository. The RCC repository remains authoritative for operational policy and tested examples; ClusterDocs NG imports reviewed, learner-safe copies with a source release reference.

After novice testing and rollout approval, merge the Markdown, exercises, tests and build workflow into the existing ClusterDocs repository. Publish large videos as institutional media or release assets. Archive the NG repository read-only after promotion.

## Pull request sequence

1. **Course shell and publication boundary**: eleven-class navigation, staging build, public-information linter and rollout page.
2. **Class 1**: Windows/macOS SSH and VS Code gates, one bounded credential test, web-transfer guidance.
3. **Classes 2-4**: reproducible workflows, performance/I/O and Apptainer.
4. **Class 5**: learner-safe Slurm Bash, Snakemake and Apptainer acceptance patterns.
5. **Class 6**: governed vhost workflow and protected application example.
6. **Classes 7-10**: Python, R, Jupyter, Shiny and notebook-to-service workflows.
7. **Class 11**: biomedical-data privacy, legal resources, controlled-enclave scenarios, and project-governance training.
8. **Media and accessibility**: remastered audio, captions, transcripts and media publication manifest.
9. **Rollout promotion**: replace staging values, run production validation, publish user messages, merge into ClusterDocs proper.

## Required acceptance tests

- One novice Windows user and one novice macOS user complete Class 1 without verbal assistance.
- Readiness scripts never print private-key material and make at most one live connection attempt.
- The three Slurm gates execute sequentially with fixed small limits.
- The vhost example rejects direct access, wrong project membership and arbitrary paths.
- Production publication fails if private IPs, physical hostnames, administrative control-plane details or unresolved placeholders appear.
- A medical professional reviews readability; an IT-affine user reviews the technical path.
- Videos and captions are reviewed for speech intelligibility and accidental terminal or infrastructure disclosure.
