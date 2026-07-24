#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    echo "Usage: $0 OUTPUT.fastq.gz [READ_COUNT]" >&2
    exit 2
}

[[ $# -ge 1 && $# -le 2 ]] || usage
readonly OUTPUT="$1"
readonly READ_COUNT="${2:-100000}"

[[ "${READ_COUNT}" =~ ^[1-9][0-9]*$ ]] || {
    echo "READ_COUNT must be a positive integer" >&2
    exit 2
}

mkdir -p -- "$(dirname -- "${OUTPUT}")"

python3 - "${READ_COUNT}" <<'PY' | gzip -c > "${OUTPUT}.tmp"
import sys

n = int(sys.argv[1])
sequence = "ACGT" * 25
quality = "I" * len(sequence)
for i in range(n):
    print(f"@synthetic_{i}")
    print(sequence)
    print("+")
    print(quality)
PY

mv -f -- "${OUTPUT}.tmp" "${OUTPUT}"
gzip -t -- "${OUTPUT}"
sha256sum -- "${OUTPUT}"
