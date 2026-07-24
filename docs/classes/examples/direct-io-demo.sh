#!/usr/bin/env bash
#SBATCH --job-name=direct-io-demo
#SBATCH --partition=cpu_short
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x-%j.out

set -Eeuo pipefail
umask 007

usage() {
    echo "Usage: sbatch $0 INPUT.fastq.gz OUTPUT_DIR" >&2
    exit 2
}

[[ $# -eq 2 ]] || usage
readonly INPUT="$1"
readonly OUTPUT_DIR="$2"

[[ -r "${INPUT}" ]] || {
    echo "Input is not readable: ${INPUT}" >&2
    exit 1
}

mkdir -p -- "${OUTPUT_DIR}"
readonly TMP_OUTPUT="${OUTPUT_DIR}/.direct-summary.${SLURM_JOB_ID}.tmp"
readonly FINAL_OUTPUT="${OUTPUT_DIR}/direct-summary.tsv"

# This comparison deliberately reads the synthetic input from shared storage.
gzip -cd -- "${INPUT}" \
    | awk 'NR % 4 == 2 { bases += length($0); reads += 1 }
           END { print "reads\t" reads; print "bases\t" bases }' \
    > "${TMP_OUTPUT}"

test -s "${TMP_OUTPUT}"
grep -q $'^reads\t' "${TMP_OUTPUT}"
grep -q $'^bases\t' "${TMP_OUTPUT}"
mv -f -- "${TMP_OUTPUT}" "${FINAL_OUTPUT}"
sha256sum -- "${FINAL_OUTPUT}"
