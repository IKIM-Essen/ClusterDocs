# Class 11: European and German data protection for biomedical research

## Learning outcome

After this class, you should be able to distinguish direct identifiers from sensitive biomedical research data, understand why pseudonymised data remain personal data, and recognise when RCC is an appropriate controlled research environment.

This class is practical RCC training. It does not replace the project's legal basis, ethics approval, consent documents, data-management plan, institutional policy, information-security review, or advice from the data-protection officer.

## The RCC rule in one sentence

**RCC may process approved biomedical research data inside its controlled research enclave, but direct identifiers and re-identification keys must not be stored in RCC.**

Examples of direct identifiers that must not be uploaded include:

- names or initials;
- postal or email addresses;
- telephone or fax numbers;
- patient, case, insurance, personnel, or hospital record numbers;
- identifying free text, letters, referrals, consent forms, or screenshots;
- account credentials, access tokens, or authentication data;
- a lookup table that connects study codes to named individuals.

The absence of these fields does not automatically make the remaining data anonymous. The research project must still have an appropriate legal basis and governance decision for processing biomedical data in RCC.

## Genomic and medical-imaging data are not automatically direct identifiers

Human genomic data and X-ray, CT, and MRI images are **not direct identifiers in the same sense as a name, address, telephone number, or hospital record number**. They may be processed for approved research in RCC because RCC is a restricted research enclave rather than a public-release platform.

They can nevertheless be:

- personal data or special-category health/genetic data;
- indirectly identifying in combination with other information;
- subject to consent, ethics, contractual, or project-specific restrictions;
- unsuitable for publication or transfer outside the approved project environment.

The correct conclusion is therefore not “genomes and images are prohibited.” It is:

> Genomes and medical images require appropriate project approval, data minimisation, named access groups, and controlled processing. Direct identifiers and the re-identification key stay outside RCC.

## Why biomedical data receive special protection

The EU General Data Protection Regulation treats genetic data, biometric data used for unique identification, and data concerning health as special categories of personal data. Their processing requires an applicable legal basis and safeguards appropriate to the risk.

RCC contributes technical safeguards through controlled access, named user accounts, project-group permissions, auditability, restricted services, and a managed research-computing environment. Technical safeguards do not create the legal basis; they help implement an approved research project safely.

Biomedical data can become identifying through context. Examples include:

- a very rare diagnosis in a small cohort;
- exact treatment or sampling dates linked to known clinical events;
- family relationships or pedigrees;
- combinations of age, location, diagnosis, and dates;
- DICOM metadata or burned-in annotations;
- free-text notes;
- external linkage with another dataset.

## Anonymous, pseudonymous, coded, and de-identified

These terms are often used inconsistently.

- **Anonymous / non-identifiable:** the person cannot reasonably be singled out using the data and reasonably available additional information in the relevant context.
- **Pseudonymous / coded:** direct identifiers are replaced, but a link can be restored or the person may still be singled out. This remains personal data.
- **De-identified:** useful descriptive language, but not a legal conclusion by itself. State what was removed, transformed, aggregated, or separated.
- **Controlled research data:** data that may still be personal or special-category data but are processed under an approved purpose and technical/organisational safeguards in a restricted environment.

The European Data Protection Board distinguishes pseudonymisation from anonymisation: pseudonymisation reduces linkability, while properly anonymised data are no longer attributable to an individual. [EDPB: anonymisation and pseudonymisation](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisationpseudonymisation_en)

## A practical RCC decision model

### Suitable under the normal project workflow

Examples include:

- synthetic teaching data;
- public reference genomes and public datasets used under their licence;
- non-human experimental data;
- aggregate statistics and approved derived results;
- approved individual-level biomedical research data without direct identifiers;
- approved genomic data;
- approved X-ray, CT, MRI, and other medical images after required metadata handling;
- pseudonymised research data when the project governance explicitly covers RCC and the re-identification key is held separately.

### Requires a project-level review before transfer

Pause and confirm the approved workflow when the data include:

- a new data source not listed in the project documentation;
- detailed free text;
- a rare cohort or a new linkage between datasets;
- exact dates or fine-grained locations not needed for the analysis;
- imaging exports whose metadata-handling process is unclear;
- human genomic data not covered by the existing project decision;
- an intended use that differs from the approved purpose;
- a plan to grant access to additional people or collaborators.

A review does not mean that the research is prohibited. It means the project must confirm that the purpose, people, data categories, and RCC environment are covered.

### Must not enter RCC

Do not upload:

- direct identifiers listed above;
- the re-identification or subject-code lookup key;
- unreviewed raw clinical documents or exports containing direct identifiers;
- credentials or secrets;
- data that the project approval assigns to a different environment;
- data obtained without a valid research, contractual, ethical, or institutional basis.

If prohibited data are discovered after upload, stop using the affected copy and contact the project lead and the appropriate data-protection or information-security channel. Do not reproduce the sensitive content in email, chat, screenshots, or tickets.

## Genomic research in RCC

Individual-level human genomic data can be scientifically valuable and computationally demanding. RCC can support such research when the project has established the permitted purpose and access model.

Good practice includes:

1. keep subject identity and the re-identification key in a separate approved system;
2. use study codes rather than names or clinical identifiers;
3. grant access only to named project members;
4. document the source, purpose, permitted analyses, retention period, and deletion process;
5. avoid unnecessary exports and local convenience copies;
6. release results only through the project's approved disclosure process;
7. consider relatives, rare variants, and external linkage when evaluating disclosure risk.

The objective is controlled research use—not a claim that a participant genome is anonymous and not a plan to publish the raw data.

## X-ray, CT, MRI, and other medical images

Medical images can be used in RCC when covered by the project governance. The main practical checks are:

- remove or transform direct identifiers in DICOM headers as required by the approved export process;
- check for burned-in names, numbers, dates, or annotations;
- keep the linkage key outside RCC;
- preserve scientifically necessary image information;
- restrict access to the project group;
- do not place images or derived visualisations on public web pages without disclosure review.

An image may contain anatomy that could contribute to indirect identification, especially in head imaging, but that does not make every image a direct identifier or make research processing impossible.

## Defacing: a possible safeguard, not a default requirement

Defacing modifies facial structures in head CT or MRI to reduce the chance of recognising or reconstructing a face. It can be appropriate when:

- a project intends to release or share images more broadly;
- the approved data-protection plan requires it;
- the destination environment has a stricter admission rule;
- facial anatomy is not needed for the scientific question;
- the method has been validated and quality-controlled for the modality.

Defacing is often **not necessary** merely to conduct approved analysis inside RCC. It can be expensive, can remove relevant anatomy, can fail on some scans, and does not remove DICOM metadata or burned-in annotations. The project should choose the least burdensome measure that achieves the approved protection goal.

Possible alternatives include:

- controlled access inside RCC without public release;
- validated metadata cleaning;
- using derived measures, segmentations, features, or cropped regions;
- limiting data access and retention;
- performing disclosure-oriented transformations only when exporting results.

## Free text, filenames, metadata, and notebook output

Direct identifiers are often introduced accidentally outside the main data table. Review:

- filenames and directory names;
- spreadsheet comments and hidden sheets;
- document properties;
- DICOM headers and overlays;
- notebook outputs and cached cells;
- plot labels and hover text;
- logs, command lines, and error messages;
- archive contents;
- clinical and laboratory free text.

Never use a real patient identifier as a file or directory name.

## Data minimisation without damaging the science

Use only the data needed for the approved purpose. In practice:

- select required columns instead of copying a complete clinical export;
- avoid detailed dates or locations when the analysis does not need them;
- transfer derived results rather than source data when this preserves the science;
- keep one authoritative project copy rather than personal duplicates;
- define retention and deletion;
- restrict access to named project members;
- avoid publishing small-cell or rare-combination outputs without review.

Data minimisation often improves transfer speed, storage use, reproducibility, and analysis clarity as well as privacy.

## Legal and institutional resources

Use these official sources for orientation:

- [EU General Data Protection Regulation (official EUR-Lex text)](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=EN) — especially Articles 4, 5, 9, 25, 32, 35, and 89.
- [German Federal Data Protection Act, Section 22](https://www.gesetze-im-internet.de/bdsg_2018/__22.html) — safeguards for special categories of personal data.
- [German Health Data Use Act](https://www.gesetze-im-internet.de/gdng/) — use of health data for public-interest research and healthcare development.
- [German Health Data Use Act, Section 7](https://www.gesetze-im-internet.de/gdng/__7.html) — purpose limitation, confidentiality, and prohibition of re-identification for data made available under the Act.
- [German Criminal Code, Section 203](https://www.gesetze-im-internet.de/stgb/__203.html) — protection of private secrets and professional confidentiality.
- [EDPB: anonymisation and pseudonymisation](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisationpseudonymisation_en).
- [Universitätsklinikum Essen data-protection information](https://www.uk-essen.de/datenschutz).

These links support training. They do not determine the legal basis for a specific project.

## Contact the Universitätsklinikum Essen data-protection office

Contact the office when a project is uncertain about its legal basis, a new data linkage or secondary use is proposed, direct identifiers appear necessary, a data-protection impact assessment may be required, or the existing approval does not clearly cover RCC.

**Christian Hecke**  
Universitätsklinikum Essen (AöR)  
Datenschutz  
Hufelandstraße 55  
D-45147 Essen  
Telephone: +49 201 / 723-6315  
Email: [datenschutz@uk-essen.de](mailto:datenschutz@uk-essen.de)

Do not attach research data or include patient information in an initial enquiry. Describe the purpose, data categories, scale, proposed users, and existing approvals without transmitting the sensitive content.

## Completion gate: explain the decision, do not scan the files

This class does not use an automated research-file scanner or a machine-generated legal decision. Completion is based on understanding and project governance.

Before moving data into RCC, you should be able to answer:

1. What is the approved research purpose?
2. Which data categories are required for that purpose?
3. Have direct identifiers and the re-identification key been excluded from RCC?
4. Does the project documentation cover genomic data, images, pseudonymised records, or linkages being used?
5. Who may access the data, and how will access be removed when no longer needed?
6. Where will authoritative data, intermediate files, and final results be stored?
7. What is the retention and deletion plan?
8. Which outputs require disclosure review before sharing or publication?
9. Who should be contacted if the actual data differ from the approved description?

### Scenario self-check

**Scenario A:** A pseudonymised MRI study has approved RCC processing, cleaned headers, no burned-in identifiers, and a linkage key stored in a separate clinical system.  
**Decision:** Suitable for RCC under the approved project workflow; defacing is not automatically required.

**Scenario B:** A whole-genome cohort is covered by the ethics and data-protection documentation, access is limited to named project members, and direct identifiers are held outside RCC.  
**Decision:** Suitable for controlled RCC research; raw data must not be publicly released merely because they are stored without names.

**Scenario C:** A spreadsheet contains names, hospital record numbers, and free-text notes.  
**Decision:** Do not upload. Create or request an approved research export first.

**Scenario D:** A project wants to combine an existing genomic cohort with a new registry that was not included in the original approval.  
**Decision:** Pause and obtain the appropriate project-level and institutional decision before linkage.

You complete this class when you can explain—in plain language—why the proposed RCC processing is permitted, which direct identifiers are excluded, what controls apply, and who owns the decision when circumstances change.
