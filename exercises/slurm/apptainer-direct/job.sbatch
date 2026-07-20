#!/usr/bin/env bash
#SBATCH --job-name=clusterdocs-gate
#SBATCH --partition=cpu_short
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --output=stdout.txt
#SBATCH --error=stderr.txt
set -euo pipefail
: "${RCC_TRAINING_IMAGE:?Set RCC_TRAINING_IMAGE to the instructor-approved immutable SIF image}"
apptainer exec --cleanenv "$RCC_TRAINING_IMAGE" /bin/sh -c "printf 'RCC_CLASS5_APPTAINER_OK\\n'"
