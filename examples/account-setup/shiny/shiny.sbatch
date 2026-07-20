#!/usr/bin/env bash
#SBATCH --job-name=rcc-shiny-starter
#SBATCH --partition=interactive
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=shiny-%j.out

set -euo pipefail
source /etc/profile.d/conda.sh

project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
scratch_dir="/local/work/slurm-jobs/${USER}/slurm-job-${SLURM_JOB_ID}"
mkdir -p -- "$scratch_dir"
export TMPDIR="$scratch_dir"

conda env update --name rcc-shiny-starter --file "$project_dir/environment.yml" --prune
port=$(python -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')

echo "Worker: $(hostname)"
echo "Port: $port"
echo "Create an SSH tunnel using the current RCC access guide."
echo "Stop: scancel ${SLURM_JOB_ID}"

cd -- "$project_dir"
conda run --name rcc-shiny-starter R -e \
  "shiny::runApp('.', host='127.0.0.1', port=${port}, launch.browser=FALSE)"
