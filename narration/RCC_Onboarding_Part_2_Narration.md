# RCC Onboarding Part 2 - Narration

## Slide 1: Reproducible scientific workflows

Part Two moves from access to reproducible analysis. Biomedical projects combine data, software, parameters, compute resources, and scientific interpretation. Reproducibility requires us to describe all of those layers. We will explain why environments exist, why Miniforge and Bioconda are useful, why Snakemake models dependencies, and how Slurm executes the expensive work. We will use two intentionally small examples: a statistical analysis of tabular data and a DNA sequence workflow using synthetic reads. The goal is not to teach every method. The goal is to establish a structure that remains understandable when a project grows.

## Slide 2: 1. A result is more than a script

A scientific result depends on more than the code file. It also depends on input data, software versions, parameters, reference data, the order of operations, and the compute environment. If any of those are implicit, a colleague may be unable to reproduce the result even when the script is available. A good workflow separates immutable source data from generated output, records software dependencies, and makes each transformation explicit. In regulated or clinically adjacent work, this structure also supports review and provenance. The cluster does not automatically make work reproducible; it only provides shared resources.

## Slide 3: 2. Project structure prevents accidental science

A project directory is a small information architecture. Raw data should be treated as read-only. Workflow files describe how outputs are created. Scripts contain substantial analysis code. Environment files declare software. Logs and benchmarks describe execution. Results are generated and can be recreated. This separation prevents common mistakes such as editing a raw file, overwriting a result by hand, or losing track of which parameters produced a figure. Use meaningful sample identifiers and a metadata table rather than encoding all information in filenames. Keep secrets and patient identifiers out of Git repositories and logs.

## Slide 4: 3. What is a software environment?

Scientific software has dependencies. One tool may need a specific Python version, another a compiled library, and a third a command-line executable. Installing everything globally creates conflicts and makes projects fragile. An environment is an isolated collection of compatible packages. Miniforge provides the conda and mamba tools without a large preselected package set. Mamba resolves and installs packages efficiently. Bioconda is a community channel containing many bioinformatics packages. An environment file records the package names and, where appropriate, versions. It is a recipe, not a substitute for validation. Part Four will explain why large active environments should not live on network storage.

## Slide 5: 4. Conda, Mamba, Bioconda, and channels

Conda is the environment and package model. Mamba is a compatible, faster resolver and installer. Miniforge is a compact distribution that provides these tools. Channels are package repositories, and Bioconda specializes in bioinformatics software. Channel order matters because packages from different repositories may be built against different libraries. Follow the RCC-supported configuration rather than copying arbitrary commands from an old tutorial. Keep the environment definition in the project, test it on synthetic data, and avoid continuously changing a shared environment underneath an active analysis. For production, a pinned container image is often more robust, as covered in Part Four.

## Slide 6: 5. Snakemake describes dependencies, not just command order

Snakemake is a workflow management system. Each rule declares input files, output files, software, resources, and a command or script. Snakemake builds a directed acyclic graph showing which outputs depend on which inputs. It runs only the steps needed to create the requested target. If an upstream input changes, the affected downstream steps can be recomputed. This is safer than a long shell script that assumes every previous command succeeded. The workflow graph also helps colleagues review the scientific logic. A dry run shows what would happen without executing commands.

## Slide 7: 6. Snakemake and Slurm have different jobs

Snakemake and Slurm solve different problems. Snakemake understands scientific dependencies and decides which rule is ready. The Slurm executor translates each ready rule into a cluster job with requested CPUs, memory, runtime, and other resources. The lightweight Snakemake controller can run in a tmux session on the submission host. The expensive commands run on compute nodes. This separation lets a workflow execute many independent samples in parallel without manually submitting hundreds of jobs. Resource values should be declared per rule and refined using measurements rather than copied blindly.

## Slide 8: 7. A minimal statistical workflow

A statistical workflow starts with input validation. Check column names, data types, missing values, group labels, and expected sample identifiers before calculating anything. The demonstration dataset contains synthetic measurements from two groups. One rule validates and cleans the table. Another calculates group counts, means, and variability. A third performs a Welch t test and records the effect estimate and uncertainty rather than reporting only a p value. A final rule creates a figure. The workflow is pedagogical; the correct statistical model for a real biomedical study depends on design, pairing, repeated measures, batch effects, confounders, and pre-specified hypotheses.

## Slide 9: 8. DNA workflows add domain-specific file types

DNA sequence analysis introduces file formats with different purposes. FASTQ stores reads and quality values and is normally kept compressed. A reference FASTA stores sequences. BAM or CRAM stores aligned reads in a binary, indexable format. VCF stores sequence variants and may use block compression with an index. Quality reports summarize technical characteristics but do not automatically establish biological validity. A typical small workflow validates read files, performs quality control, aligns or classifies reads, creates indexed outputs, and summarizes results. Real clinical or research pipelines require validated references, contamination controls, sample identity checks, and documented versions.

## Slide 10: 9. Dry runs, targets, logs, and benchmarks

Before a substantial run, request a specific target and perform a Snakemake dry run. Inspect the planned rules, inputs, and job count. Then execute through the RCC-supported Slurm profile. Each rule should have a useful log, and performance-sensitive rules should have a benchmark file. A completed workflow is not automatically a correct workflow. Review exit states, expected file counts, quality metrics, and biological plausibility. Avoid redirecting all commands into one giant log. Per-rule and per-sample logs make failures diagnosable and support audit trails.

## Slide 11: 10. Git records changes - not sensitive data

Git records changes to text files and supports review through branches and pull requests. Commit the Snakefile, scripts, environment definitions, configuration templates, and documentation. Do not commit raw sequencing data, patient identifiers, credentials, private keys, large binary outputs, or secrets. Use a gitignore file to exclude generated directories and local configuration. Small, descriptive commits make it possible to understand how a method evolved. Tag or record the exact workflow version used for an analysis. For collaborative projects, a pull request allows a colleague to review scientific logic and operational safety before changes reach the main branch.

## Slide 12: 11. Part Two completion checklist

You are ready for larger examples when the project has a clear directory structure and read-only source data; the software environment is declared; Snakemake can perform a dry run; the workflow submits rules through the approved Slurm profile; statistical inputs are validated; sequence files use appropriate compressed and indexed formats; logs and benchmarks are generated; and workflow changes are recorded in Git without sensitive data. The next lesson focuses on performance. It explains why an analysis with correct code can still take months when CPU, memory, and especially input-output behavior are structured poorly.

