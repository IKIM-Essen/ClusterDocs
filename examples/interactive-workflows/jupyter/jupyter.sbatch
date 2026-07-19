#!/usr/bin/env bash
#SBATCH --job-name=jupyter
#SBATCH --partition=interactive
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=jupyter-%j.out

set -euo pipefail
source /etc/profile.d/conda.sh
scratch="/local/work/slurm-jobs/${USER}/slurm-job-${SLURM_JOB_ID}"
mkdir -p "${scratch}/jupyter-runtime" "${scratch}/notebooks"
export JUPYTER_RUNTIME_DIR="${scratch}/jupyter-runtime"
export XDG_RUNTIME_DIR="${scratch}/xdg-runtime"
mkdir -p "${XDG_RUNTIME_DIR}"
chmod 700 "${JUPYTER_RUNTIME_DIR}" "${XDG_RUNTIME_DIR}"

if ! conda env list | awk '{print $1}' | grep -qx rcc-jupyter; then
    mamba env create -f "${SLURM_SUBMIT_DIR}/environment.yml" -n rcc-jupyter
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
echo "Tunnel: ssh -N -L 8888:127.0.0.1:${port} -J <RCC-SSH-ENTRY> ${USER}@${SLURMD_NODENAME:-$(hostname -s)}"
echo "Stop: scancel ${SLURM_JOB_ID}"

cd "${SLURM_SUBMIT_DIR}"
exec conda run --no-capture-output -n rcc-jupyter \
    jupyter lab --no-browser --ip=127.0.0.1 --port="${port}" \
    --ServerApp.port_retries=0
