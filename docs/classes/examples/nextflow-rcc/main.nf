nextflow.enable.dsl=2

process SHARED_HELLO {
    label 'rcc_short'
    cpus 1
    memory 512.MB
    time 5.m

    output:
    path 'shared.txt'

    script:
    """
    printf 'shared job=%s node=%s\\n' "\$SLURM_JOB_ID" "\$SLURMD_NODENAME" > shared.txt
    """
}

process SCRATCH_HELLO {
    label 'rcc_short'
    label 'rcc_scratch'
    cpus 1
    memory 512.MB
    time 5.m

    output:
    path 'scratch.txt'

    script:
    """
    case "\$PWD" in
        /local/*) ;;
        *) echo 'task is not on RCC local scratch' >&2; exit 20 ;;
    esac
    printf 'scratch job=%s node=%s pwd=%s\\n' \
      "\$SLURM_JOB_ID" "\$SLURMD_NODENAME" "\$PWD" > scratch.txt
    """
}

workflow {
    SHARED_HELLO()
    SCRATCH_HELLO()
}
