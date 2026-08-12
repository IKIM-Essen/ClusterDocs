# Before sharing data with a coding agent

Some RCC projects contain patient-derived or otherwise protected research data.
Removing names and phone numbers does not automatically make such data safe to
upload elsewhere.

## Off-site coding agents must not receive RCC research data

Do not paste, upload, or otherwise make real or pseudonymised RCC project data
available to an off-site coding agent. This is the RCC user rule for protected
biomedical data, not a preference or a warning that users may override.

Health and genetic data are special categories under [Article 9
GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/art_9/oj). German research law
does not give an individual user blanket permission to disclose them to a new
service. A service account, licence, or “approved” label is not the required
legal basis or processor arrangement. Any exceptional off-site processing must
be explicitly established and authorized by the responsible institution for
that exact service and purpose.

You can usually ask for help without sending the data. Describe the file type,
columns, error message, or intended analysis using a small synthetic example.

Shuffling rows, hashing an identifier, or replacing names is not enough. If
information can still be linked to a person using other information, it remains
personal data. Use values that are fully invented rather than transformed from
real people. The European Data Protection Board explains this distinction in
its [guidance on pseudonymisation](https://www.edpb.europa.eu/news/edpb-adopts-pseudonymisation-guidelines-and-paves-way-improve-cooperation_en).

## When a coding agent can work with the data

An approved RCC or locally operated coding agent can work near project data that
you are already allowed to use. The data remains subject to the same project,
purpose, access, and retention rules.

The preferred pattern is:

```text
you describe the result
        |
approved RCC computation runs near the data
        |
you receive the permitted plots, tables, code, and report
```

## When an off-site coding agent is useful

Off-site coding agents are useful for:

- public code and documentation;
- synthetic or teaching data;
- generic error messages with sensitive details removed; and
- other material explicitly approved for external processing.

If you are uncertain, do not attach the dataset. Use **Make coding example** for an
off-site coding agent or **Use inside RCC** for the real data. These should be the
normal choices; users should not need to complete a form for an ordinary
synthetic tabular fixture. Ask support only when neither route fits the task.

For a practical walkthrough, use [Class 18: coding agents without sharing real
data](../course/class-18-coding-agents.md).
