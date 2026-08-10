#!/usr/bin/env bash
# Teaching wrapper: one active controller per analysis directory and one log per run.
set -Eeuo pipefail

: "${RCC_PROJECT_ROOT:?Set RCC_PROJECT_ROOT to an approved /projects or /groups path}"

case "$RCC_PROJECT_ROOT" in
    /projects/*|/groups/*) ;;
    *)
        echo "ERROR: RCC_PROJECT_ROOT must be below /projects or /groups" >&2
        exit 2
        ;;
esac

mkdir -p logs

# The lock is deliberately scoped to the current analysis directory, not the
# whole RCC project, so independent analyses may run concurrently.
exec 9> .rcc-nextflow-controller.lock
if ! flock -n 9; then
    cat >&2 <<'MSG'
ERROR: another Nextflow controller is active in this analysis directory.
Check tmux, pgrep, nextflow log, and squeue. Do not start a duplicate controller.
Use -resume only after the previous controller has stopped.
MSG
    exit 75
fi

stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="logs/nextflow-${stamp}.log"

printf 'RCC Nextflow log: %s\n' "$log" >&2
exec rcc-nextflow \
    --project-root "$RCC_PROJECT_ROOT" \
    -log "$log" \
    "$@"
