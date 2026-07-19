#!/usr/bin/env bash
#SBATCH --job-name=clusterdocs-gate
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --output=stdout.txt
#SBATCH --error=stderr.txt
set -euo pipefail
snakemake --cores 1 --snakefile Snakefile --printshellcmds
cat result.txt
