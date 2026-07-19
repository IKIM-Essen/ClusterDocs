# Instructor and rollout checklist

## Before novice testing

- Replace all values in `config/public.yml`.
- Publish the host fingerprint through an independently trusted institutional channel.
- Test Class 1 on clean supported Windows and macOS systems.
- Verify the transfer portal with a normal user account and project membership.
- Run the Class 5 gates using a clean training account.
- Test the Class 6 example without access to RCC production services.
- Review wording with a medical professional who is not an experienced cluster user.
- Review Class 11 and the non-identifiable-data rule with the responsible institutional data-protection office.

## Security publication review

```bash
python3 tools/publication_lint.py
```

Manually verify that no screenshot, video frame, caption, downloadable slide or PDF discloses internal addresses, physical hostnames, node lists, credentials, patient data, terminal history or administrative interfaces.

## Load-safety review

- Every Slurm example is sequential and bounded.
- No example performs node-by-node execution.
- No connection test retries automatically.
- No tutorial performs broad filesystem traversal.
- No benchmark is run against shared storage without operator approval.

## Rollout

1. Deploy NG to a staging URL.
2. Test with novice biomedical users and technical users.
3. Freeze content and record checksums.
4. Publish the email and Mattermost notice shortly before rollout.
5. Promote the reviewed content into ClusterDocs proper.
6. Update the canonical URL at rollout.
7. Archive the NG repository after a defined observation period.
