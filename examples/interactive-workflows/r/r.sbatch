#!/usr/bin/env bash
#SBATCH --job-name=rcc-r
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:30:00
#SBATCH --output=r-%j.out

set -euo pipefail
source /etc/profile.d/conda.sh
scratch="/local/work/slurm-jobs/${USER}/slurm-job-${SLURM_JOB_ID}"
work="${scratch}/r"
mkdir -p "${work}"
cp analysis.R environment.yml "${work}/"
cd "${work}"

if ! conda env list | awk '{print $1}' | grep -qx rcc-r-example; then
    mamba env create -f environment.yml -n rcc-r-example
fi
conda run -n rcc-r-example Rscript analysis.R
mkdir -p "${SLURM_SUBMIT_DIR}/results"
rsync -a results/ "${SLURM_SUBMIT_DIR}/results/"
