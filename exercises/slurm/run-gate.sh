#!/usr/bin/env bash
set -euo pipefail
CASE="${1:-}"
ROOT=$(cd "$(dirname "$0")" && pwd)
case "$CASE" in
  bash) SRC="$ROOT/bash-hello" ;;
  snakemake) SRC="$ROOT/snakemake-native" ;;
  apptainer) SRC="$ROOT/apptainer-direct" ;;
  *) echo "Usage: $0 {bash|snakemake|apptainer}" >&2; exit 2 ;;
esac
command -v sbatch >/dev/null || { echo "sbatch is unavailable" >&2; exit 1; }
[[ -z "${SLURM_JOB_ID:-}" ]] || { echo "Run this gate from the RCC submission environment, not inside a job" >&2; exit 1; }
if command -v squeue >/dev/null 2>&1 && [[ $(squeue -h -u "$USER" -n clusterdocs-gate 2>/dev/null | wc -l) -gt 0 ]]; then
  echo "A clusterdocs gate is already active for this user; wait for it to finish" >&2
  exit 1
fi
WORK=$(mktemp -d "${TMPDIR:-/tmp}/clusterdocs-${CASE}.XXXXXX")
trap 'rm -rf "$WORK"' EXIT
cp -a "$SRC"/. "$WORK"/
cd "$WORK"
chmod +x job.sbatch
if command -v timeout >/dev/null 2>&1; then
  timeout 240 sbatch --wait --parsable job.sbatch >/dev/null
else
  sbatch --wait --parsable job.sbatch >/dev/null
fi
[[ ! -s stderr.txt ]] || { echo "Job wrote to stderr:" >&2; cat stderr.txt >&2; exit 1; }
case "$CASE" in
  bash)
    head -1 stdout.txt | grep -Fxq RCC_CLASS5_BASH_OK
    grep -Eq '^job_id=[0-9]+$' stdout.txt
    ;;
  snakemake)
    grep -Fxq RCC_CLASS5_SNAKEMAKE_OK result.txt
    ;;
  apptainer)
    grep -Fxq RCC_CLASS5_APPTAINER_OK stdout.txt
    ;;
esac
echo "PASS: $CASE Slurm gate"
