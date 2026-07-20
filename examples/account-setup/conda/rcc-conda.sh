# Put Conda environments and package caches on node-local storage.
# Source this file after reviewing it; call rcc-conda-init before using Conda.
rcc-conda-init() {
  local conda_root="/local/conda/${USER}"
  if ! mkdir -p -- "$conda_root/envs" "$conda_root/pkgs"; then
    echo "Cannot create $conda_root; check the current RCC storage guidance." >&2
    return 1
  fi
  export CONDA_ENVS_PATH="$conda_root/envs"
  export CONDA_PKGS_DIRS="$conda_root/pkgs"
  echo "Conda environments: $CONDA_ENVS_PATH"
  echo "Conda package cache: $CONDA_PKGS_DIRS"
}
