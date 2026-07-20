# Lightweight RCC prompt: no Git scan, network request, or directory traversal.
case $- in
  *i*) ;;
  *) return 0 2>/dev/null || exit 0 ;;
esac

_rcc_prompt() {
  local job_marker=''
  if [[ -n ${SLURM_JOB_ID:-} ]]; then
    job_marker=" job:${SLURM_JOB_ID}"
  fi
  PS1="\[\033[38;5;31m\][RCC${job_marker}]\[\033[0m\] \u@\h:\w\$ "
}

PROMPT_COMMAND="_rcc_prompt${PROMPT_COMMAND:+;${PROMPT_COMMAND}}"
