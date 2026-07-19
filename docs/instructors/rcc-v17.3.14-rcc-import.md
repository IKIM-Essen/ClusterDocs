# RCC v17.3.14 documentation import

The v17.3.14 RCC release moves end-user courses, workflow examples, and
onboarding media out of the privileged infrastructure repository. ClusterDocs
is now the publication source for that material.

The four onboarding videos were relocated to the local `videos/` media staging
directory. The corresponding captions, narration, source, PDF, DOCX, and slide
artifacts are already present in the canonical ClusterDocs directories and
were checksum-compared before the RCC staging copy was removed. MP4 files stay
ignored by Git and follow the repository's institutional-media publication
policy.

The RCC repository remains authoritative for infrastructure contracts and
acceptance tests; this repository owns learner-facing wording and media.
