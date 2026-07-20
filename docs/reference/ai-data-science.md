# AI and data science on RCC

RCC supports reproducible data science, machine learning, and AI research when
the project governance covers the data and the computation runs through Slurm.
AI does not change the normal RCC rules for identity, storage, review, resource
requests, or biomedical-data protection.

> **Related learning:** Begin with [Class 7](../course/class-07-python-notebooks.md)
> for Python exploration, [Class 8](../course/class-08-r-analysis.md) for
> statistical analysis, and [Class 10](../course/class-10-notebook-to-service.md)
> before turning a model into a shared service.

## Choose the technique from the question

| Research goal | Useful starting techniques | Important check |
|---|---|---|
| Describe a cohort or dataset | summary statistics, visualization, stratification | missingness, selection effects, data quality |
| Estimate an association or effect | regression, survival analysis, causal designs where justified | assumptions, uncertainty, confounding |
| Predict a labeled outcome | regularized regression, trees, boosting, neural networks | leakage, calibration, external validity |
| Discover structure without labels | clustering, dimensionality reduction, representation learning | stability and biological interpretability |
| Work with images, sequences, or text | convolutional, transformer, embedding, or domain-specific models | provenance, bias, compute cost, data minimisation |
| Process data too large for one process | chunked/columnar tools or distributed dataframes | whether distribution is actually faster than local processing |

Start with the simplest method that can answer the question. A larger model is
not automatically more accurate, more reproducible, or more scientifically
useful.

## Reproducible model-development loop

1. Define the scientific question, outcome, and evaluation measure before
   fitting models.
2. Establish a simple baseline.
3. Separate training, validation, and test data without subject or temporal
   leakage.
4. Build preprocessing and feature engineering into the versioned pipeline.
5. Tune only on training and validation data.
6. Evaluate once on the held-out test set and report uncertainty, calibration,
   subgroup behavior, and known limitations.
7. Record code, environment, parameters, random seeds, data version, Slurm job
   IDs, logs, metrics, and model artifacts.
8. Review whether an independent dataset or prospective study is required.

For sensitive biomedical data, avoid copying identifying columns into feature
tables, logs, checkpoints, experiment trackers, prompts, or notebook output.

## Training and inference

Training is usually the expensive step. Run it as a bounded batch job with
checkpoints and explicit CPU, memory, GPU, and time requests. Inference may be a
batch workflow, an interactive research step, or a governed service; choose the
architecture from the expected users, latency, data sensitivity, and review
requirements.

A GPU request is justified only when the framework and workload use it. Measure
utilization and compare with a CPU baseline. Do not override
`CUDA_VISIBLE_DEVICES`, install host drivers, or request multiple GPUs before a
single-GPU run demonstrates a scaling need.

## Distributed data processing

Spark-style distributed dataframes and task graphs can help with datasets that
do not fit one process or with genuinely parallel transformations. They also add
serialization, scheduling, network, and debugging overhead.

Before distributing a workflow, try:

- selecting only required columns and rows;
- Parquet, Arrow, DuckDB, Polars, or chunked readers;
- vectorized operations instead of Python loops;
- one larger-memory Slurm job; and
- staging high-I/O data to job-local scratch.

If distribution is still justified, use an RCC-approved Slurm integration,
bound the number of workers, set memory and time limits, persist only deliberate
intermediates, and collect per-stage metrics. Do not create an unmanaged cluster
or open worker ports.

## Responsible use boundary

An AI result is a research output, not automatically a clinical decision.
Clinical use requires the applicable institutional, legal, quality-management,
medical-device, validation, and human-oversight processes. Generated labels,
embeddings, predictions, prompts, and model checkpoints may remain sensitive or
re-identifiable and must follow the same project governance as their source
data.
