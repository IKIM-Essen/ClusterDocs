#!/usr/bin/env bash
#SBATCH --job-name=local-io-demo
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
readonly WORKDIR="${SLURM_TMPDIR:-/local/work/${USER}/slurm-job-${SLURM_JOB_ID}}"

cleanup() {
    local status=$?
    rm -rf -- "${WORKDIR}"
    exit "${status}"
}
trap cleanup EXIT INT TERM

[[ -r "${INPUT}" ]] || {
    echo "Input is not readable: ${INPUT}" >&2
    exit 1
}

mkdir -p -- "${WORKDIR}" "${OUTPUT_DIR}"
rsync -a --checksum -- "${INPUT}" "${WORKDIR}/sample.fastq.gz"

gzip -cd -- "${WORKDIR}/sample.fastq.gz" \
    | awk 'NR % 4 == 2 { bases += length($0); reads += 1 }
           END { print "reads\t" reads; print "bases\t" bases }' \
    > "${WORKDIR}/summary.tsv"

test -s "${WORKDIR}/summary.tsv"
grep -q $'^reads\t' "${WORKDIR}/summary.tsv"
grep -q $'^bases\t' "${WORKDIR}/summary.tsv"

readonly TMP_OUTPUT="${OUTPUT_DIR}/.summary.${SLURM_JOB_ID}.tmp"
readonly FINAL_OUTPUT="${OUTPUT_DIR}/summary.tsv"

rsync -a -- "${WORKDIR}/summary.tsv" "${TMP_OUTPUT}"
mv -f -- "${TMP_OUTPUT}" "${FINAL_OUTPUT}"
sha256sum -- "${FINAL_OUTPUT}"
