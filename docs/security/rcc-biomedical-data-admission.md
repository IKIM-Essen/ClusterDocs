# RCC biomedical-data use: quick training guide

RCC is a controlled research-computing enclave. It may process approved biomedical research data, including genomic data and X-ray, CT, and MRI images. These data are not automatically direct identifiers, but they may remain personal or special-category data and must be handled under the project's approved purpose and safeguards.

## Do not place these in RCC

- names, initials, postal or email addresses, or telephone numbers;
- patient, case, insurance, personnel, or hospital record numbers;
- the subject-code lookup or re-identification key;
- unreviewed free text, clinical letters, referrals, or consent forms;
- passwords, private keys, access tokens, or other credentials;
- data assigned by the project approval to another environment.

## Data that may be used when the project governance covers RCC

- pseudonymised research records without the re-identification key;
- individual-level genomic or variant data;
- X-ray, CT, MRI, and other medical images after the approved metadata process;
- rare-disease and small-cohort data with appropriate access controls;
- linked biomedical datasets covered by the approved purpose;
- synthetic, public-reference, aggregate, and derived data.

## Before transfer

Confirm that:

1. RCC is named or covered as an approved processing environment;
2. the purpose and data categories match the project documentation;
3. direct identifiers and the linkage key remain outside RCC;
4. access is limited to named project members;
5. retention, deletion, and output disclosure are defined;
6. any new linkage, purpose, collaborator, or data source has been reviewed.

## Defacing

Defacing head CT or MRI can reduce facial-recognition risk, especially before wider sharing or when required by the project plan. It is not an automatic requirement for approved processing inside RCC. It may be expensive, may remove scientifically relevant anatomy, and does not replace metadata cleaning or access control.

## When uncertain

Ask the project lead or the Universitätsklinikum Essen data-protection office before changing the purpose, linking new data, including direct identifiers, or moving data to a different environment.

**Christian Hecke**  
Universitätsklinikum Essen (AöR), Datenschutz  
Hufelandstraße 55, D-45147 Essen  
Telephone: +49 201 / 723-6315  
Email: [datenschutz@uk-essen.de](mailto:datenschutz@uk-essen.de)  
Official information: <https://www.uk-essen.de/datenschutz>

Do not attach research data or include patient information in the initial enquiry.
