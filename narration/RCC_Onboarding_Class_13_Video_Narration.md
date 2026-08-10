# Class 13: European and German data protection for biomedical research — video narration

## Slide 1: Class 13: European and German data protection for biomedical research

Welcome to Class 13: European and German data protection for biomedical research. This video introduces the core decisions and working patterns. Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material.

## Slide 2: Learning outcome

After this class, you should be able to distinguish direct identifiers from sensitive biomedical research data, understand why pseudonymised data remain personal data, and recognise when RCC is an appropriate controlled research environment. This class is practical RCC training. It does not replace the project's legal basis, ethics approval, consent documents, data-management plan, institutional policy, information-security review, or advice from the data-protection officer.

## Slide 3: The RCC rule in one sentence

RCC may process approved biomedical research data inside its controlled research enclave, but direct identifiers and re-identification keys must not be stored in RCC. Examples of direct identifiers that must not be uploaded include: names or initials; postal or email addresses; telephone or fax numbers; patient, case, insurance, personnel, or hospital record numbers; identifying free text, letters, referrals, consent forms, or screenshots; account credentials, access tokens, or authentication data; a lookup table that connects study codes to named individuals. The absence of these fields does not automatically make the remaining data anonymous. The research project must still have an appropriate legal basis and governance decision.

## Slide 4: Why biomedical data receive special protection

The EU General Data Protection Regulation treats genetic data, biometric data used for unique identification, and data concerning health as special categories of personal data. Their processing requires an applicable legal basis and safeguards appropriate to the risk. RCC contributes technical safeguards through controlled access, named user accounts, project-group permissions, auditability, restricted services, and a managed research-computing environment. Technical safeguards do not create the legal basis; they help implement an approved research project safely. Biomedical data can become identifying through context. Examples include: a very rare diagnosis in a small cohort; exact treatment or sampling dates linked to known clinical events; family relationships or pedigrees.

## Slide 5: A practical RCC decision model

### Suitable under the normal project workflow Examples include: synthetic teaching data; public reference genomes and public datasets used under their licence; non-human experimental data; aggregate statistics and approved derived results; approved individual-level biomedical research data without direct identifiers; approved genomic data; approved X-ray, CT, MRI, and other medical images after required metadata handling; pseudonymised research data when the project governance explicitly covers RCC and the re-identification key is held separately. ### Requires a project-level review before transfer Pause and confirm the approved workflow when the data include: a new data source not listed in the project documentation; detailed free text; a rare cohort or.

## Slide 6: Genomic research in RCC

Individual-level human genomic data can be scientifically valuable and computationally demanding. RCC can support such research when the project has established the permitted purpose and access model. Good practice includes: keep subject identity and the re-identification key in a separate approved system; use study codes rather than names or clinical identifiers; grant access only to named project members; document the source, purpose, permitted analyses, retention period, and deletion process; avoid unnecessary exports and local convenience copies; release results only through the project's approved disclosure process; consider relatives, rare variants, and external linkage when evaluating disclosure risk. The objective is controlled research use—not a claim that.

## Slide 7: X-ray, CT, MRI, and other medical images

Medical images can be used in RCC when covered by the project governance. The main practical checks are: remove or transform direct identifiers in DICOM headers as required by the approved export process; check for burned-in names, numbers, dates, or annotations; keep the linkage key outside RCC; preserve scientifically necessary image information; restrict access to the project group; do not place images or derived visualisations on public web pages without disclosure review. An image may contain anatomy that could contribute to indirect identification, especially in head imaging, but that does not make every image a direct identifier or make research processing impossible.

## Slide 8: Data minimisation without damaging the science

Use only the data needed for the approved purpose. In practice: select required columns instead of copying a complete clinical export; avoid detailed dates or locations when the analysis does not need them; transfer derived results rather than source data when this preserves the science; keep one authoritative project copy rather than personal duplicates; define retention and deletion; restrict access to named project members; avoid publishing small-cell or rare-combination outputs without review. Data minimisation often improves transfer speed, storage use, reproducibility, and analysis clarity as well as privacy.

## Slide 9: Legal and institutional resources

Use these official sources for orientation: EU General Data Protection Regulation (official EUR-Lex text) — especially Articles 4, 5, 9, 25, 32, 35, and 89. German Federal Data Protection Act, Section 22 — safeguards for special categories of personal data. German Health Data Use Act — use of health data for public-interest research and healthcare development. German Health Data Use Act, Section 7 — purpose limitation, confidentiality, and prohibition of re-identification for data made available under the Act. German Criminal Code, Section 203 — protection of private secrets and professional confidentiality. EDPB: anonymisation and pseudonymisation. Universitätsklinikum Essen data-protection information. These links support training. They do.

## Slide 10: Completion gate: explain the decision, do not scan the files

This class does not use an automated research-file scanner or a machine-generated legal decision. Completion is based on understanding and project governance. Before moving data into RCC, you should be able to answer: What is the approved research purpose? Which data categories are required for that purpose? Have direct identifiers and the re-identification key been excluded from RCC? Does the project documentation cover genomic data, images, pseudonymised records, or linkages being used? Who may access the data, and how will access be removed when no longer needed? Where will authoritative data, intermediate files, and final results be stored? What is the retention and deletion plan?.
