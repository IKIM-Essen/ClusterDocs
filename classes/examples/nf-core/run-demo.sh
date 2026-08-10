#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 /projects/PROJECT /projects/PROJECT/training/nf-core-demo/run-NAME" >&2
    exit 2
fi

for command_name in rcc-nextflow apptainer sbatch; do
    if ! command -v "${command_name}" >/dev/null 2>&1; then
        echo "Required command not found: ${command_name}" >&2
        exit 1
    fi
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(readlink -f -- "$1")"
run_root="$2"

case "${project_root}" in
    /projects/* | /groups/*) ;;
    *)
        echo "Project root must be in an approved shared project path." >&2
        exit 2
        ;;
esac
case "${run_root}" in
    "${project_root}"/*) ;;
    *)
        echo "Run directory must be below the selected project root." >&2
        exit 2
        ;;
esac

mkdir -p \
    "${run_root}/cache/apptainer" \
    "${run_root}/cache/nextflow" \
    "${run_root}/results" \
    "${run_root}/work"

run_root="$(cd -- "${run_root}" && pwd)"
export NXF_HOME="${run_root}/cache/nextflow"
export NXF_APPTAINER_CACHEDIR="${run_root}/cache/apptainer"
export NXF_TEMP="${TMPDIR:-/local/tmp}/nextflow-${USER}"
mkdir -p "${NXF_TEMP}"

rcc-nextflow --project-root "${project_root}" \
    -log "${run_root}/nextflow.log" \
    run nf-core/demo \
    -r 1.2.0 \
    -profile test,apptainer \
    -c "${script_dir}/rcc-test.config" \
    -work-dir "${run_root}/work" \
    --outdir "${run_root}/results"
