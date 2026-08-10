#!/usr/bin/env bash
set -euo pipefail

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
target_dir=${XDG_CONFIG_HOME:-"${HOME}/.config"}/rcc
mode=dry-run
force=0
components=()

usage() {
  cat <<'EOF'
Usage: bash install.sh [--dry-run | --install] [--component NAME] [--target DIR] [--force]

Components: shell, prompt, conda, shiny, all
The default is --dry-run. The installer never edits shell startup files.
EOF
}

while (($#)); do
  case "$1" in
    --dry-run) mode=dry-run ;;
    --install) mode=install ;;
    --component)
      shift
      [[ $# -gt 0 ]] || { echo "--component needs a value" >&2; exit 2; }
      components+=("$1")
      ;;
    --target)
      shift
      [[ $# -gt 0 ]] || { echo "--target needs a value" >&2; exit 2; }
      target_dir=$1
      ;;
    --force) force=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if ((${#components[@]} == 0)); then
  components=(all)
fi

expanded=()
for component in "${components[@]}"; do
  case "$component" in
    all) expanded=(shell prompt conda shiny) ;;
    shell|prompt|conda|shiny) expanded+=("$component") ;;
    *) echo "Unknown component: $component" >&2; exit 2 ;;
  esac
done

copy_file() {
  local source=$1 destination=$2
  echo "  $source -> $destination"
  [[ $mode == install ]] || return 0
  install -d -m 0700 "$(dirname -- "$destination")"
  if [[ -e $destination && $force -ne 1 ]]; then
    echo "Refusing to replace $destination (use --force after reviewing it)." >&2
    exit 1
  fi
  install -m 0644 "$source" "$destination"
}

echo "RCC account setup: ${mode^^}"
echo "Target: $target_dir"
for component in "${expanded[@]}"; do
  case "$component" in
    shell) copy_file "$source_dir/shell/rcc-shell.sh" "$target_dir/rcc-shell.sh" ;;
    prompt) copy_file "$source_dir/prompt/rcc-prompt.sh" "$target_dir/rcc-prompt.sh" ;;
    conda)
      copy_file "$source_dir/conda/rcc-conda.sh" "$target_dir/rcc-conda.sh"
      copy_file "$source_dir/conda/environment.yml" "$target_dir/starters/conda/environment.yml"
      ;;
    shiny)
      copy_file "$source_dir/shiny/app.R" "$target_dir/starters/shiny/app.R"
      copy_file "$source_dir/shiny/environment.yml" "$target_dir/starters/shiny/environment.yml"
      copy_file "$source_dir/shiny/shiny.sbatch" "$target_dir/starters/shiny/shiny.sbatch"
      ;;
  esac
done

if [[ $mode == dry-run ]]; then
  echo
  echo "No files were changed. Re-run with --install when the plan looks right."
else
  echo
  echo "Installed selected files. Review them before enabling them."
fi

cat <<EOF

Optional activation lines (the installer does not add these):
  [ -r "$target_dir/rcc-shell.sh" ] && . "$target_dir/rcc-shell.sh"
  [ -r "$target_dir/rcc-conda.sh" ] && . "$target_dir/rcc-conda.sh"
  [ -r "$target_dir/rcc-prompt.sh" ] && . "$target_dir/rcc-prompt.sh"
EOF
