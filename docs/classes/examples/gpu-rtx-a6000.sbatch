#!/usr/bin/env bash
#SBATCH --job-name=gpu-typed
#SBATCH --partition=gpu_nodes
#SBATCH --gpus-per-node=rtx_a6000:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:05:00
#SBATCH --output=logs/%x-%j.out

set -Eeuo pipefail
printf 'job=%s node=%s gpu_ids=%s\n' \
  "$SLURM_JOB_ID" "$SLURMD_NODENAME" "${SLURM_JOB_GPUS:-unknown}"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
