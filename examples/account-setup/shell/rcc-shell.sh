# RCC interactive-shell helpers. Source this file only after reviewing it.
case $- in
  *i*) ;;
  *) return 0 2>/dev/null || exit 0 ;;
esac

# New files are private to the owner and readable by the project group.
umask 027

rcc-jobs() {
  squeue --me --format='%.18i %.12P %.24j %.8T %.10M %.4C %.10m %R'
}

rcc-job() {
  if [[ $# -ne 1 ]]; then
    echo "Usage: rcc-job JOB_ID" >&2
    return 2
  fi
  scontrol show job -- "$1"
}

rcc-resources() {
  sinfo --format='%18P %10a %12l %8D %14C %10G'
}
