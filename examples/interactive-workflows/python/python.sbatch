#!/usr/bin/env bash
#SBATCH --job-name=rcc-python
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=python-%j.out

set -euo pipefail
source /etc/profile.d/conda.sh
scratch="/local/work/slurm-jobs/${USER}/slurm-job-${SLURM_JOB_ID}"
work="${scratch}/python"
mkdir -p "${work}"
cp analysis.py environment.yml "${work}/"
cd "${work}"

if ! conda env list | awk '{print $1}' | grep -qx rcc-python-example; then
    mamba env create -f environment.yml -n rcc-python-example
fi
conda run -n rcc-python-example python analysis.py
mkdir -p "${SLURM_SUBMIT_DIR}/results"
rsync -a results/ "${SLURM_SUBMIT_DIR}/results/"
