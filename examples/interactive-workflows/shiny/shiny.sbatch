#!/usr/bin/env bash
#SBATCH --job-name=shiny
#SBATCH --partition=interactive
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=shiny-%j.out

set -euo pipefail
source /etc/profile.d/conda.sh
scratch="/local/work/slurm-jobs/${USER}/slurm-job-${SLURM_JOB_ID}"
mkdir -p "${scratch}/shiny-runtime"
export TMPDIR="${scratch}/shiny-runtime"

if ! conda env list | awk '{print $1}' | grep -qx rcc-shiny; then
    mamba env create -f "${SLURM_SUBMIT_DIR}/environment.yml" -n rcc-shiny
fi

port="$(python3 - <<'PY'
import socket
with socket.socket() as s:
    s.bind(("127.0.0.1", 0))
    print(s.getsockname()[1])
PY
)"

echo "Worker: ${SLURMD_NODENAME:-$(hostname -s)}"
echo "Port: ${port}"
echo "Tunnel: ssh -N -L 3838:127.0.0.1:${port} -J <RCC-SSH-ENTRY> ${USER}@${SLURMD_NODENAME:-$(hostname -s)}"
echo "Stop: scancel ${SLURM_JOB_ID}"

cd "${SLURM_SUBMIT_DIR}"
exec conda run --no-capture-output -n rcc-shiny \
    Rscript -e "shiny::runApp('app.R', host='127.0.0.1', port=${port}, launch.browser=FALSE)"
